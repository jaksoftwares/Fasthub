from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.payment import Payment
from app.models.order import Order
from app.schemas.payment import PaymentCreate, PaymentUpdate
from app.services.mpesa import MpesaService
from app.services.order import OrderService

class PaymentService:
    @staticmethod
    def create_payment(db: Session, payment: PaymentCreate) -> Optional[Payment]:
        # Verify order exists
        order = OrderService.get_order(db, payment.order_id)
        if not order:
            return None
        
        db_payment = Payment(
            order_id=payment.order_id,
            method=payment.method,
            amount=payment.amount,
            phone_number=payment.phone_number
        )
        
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        return db_payment
    
    @staticmethod
    def get_payment(db: Session, payment_id: int) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.id == payment_id).first()
    
    @staticmethod
    def get_payment_by_order(db: Session, order_id: int) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.order_id == order_id).first()
    
    @staticmethod
    def get_payments(db: Session, skip: int = 0, limit: int = 100) -> List[Payment]:
        return db.query(Payment).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_payment(db: Session, payment_id: int, payment_update: PaymentUpdate) -> Optional[Payment]:
        db_payment = PaymentService.get_payment(db, payment_id)
        if not db_payment:
            return None
        
        update_data = payment_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_payment, field, value)
        
        db.commit()
        db.refresh(db_payment)
        
        # Update order status if payment is successful
        if db_payment.status == "success":
            from app.schemas.order import OrderUpdate
            OrderService.update_order(db, db_payment.order_id, OrderUpdate(status="paid"))
        
        return db_payment
    
    @staticmethod
    def initiate_mpesa_payment(db: Session, phone_number: str, amount: float, 
                              order_id: int, callback_url: str) -> dict:
        # Create payment record
        payment_data = PaymentCreate(
            order_id=order_id,
            method="M-Pesa",
            amount=amount,
            phone_number=phone_number
        )
        
        db_payment = PaymentService.create_payment(db, payment_data)
        if not db_payment:
            return {"success": False, "message": "Failed to create payment record"}
        
        # Initiate STK Push
        mpesa_result = MpesaService.initiate_stk_push(
            phone_number=phone_number,
            amount=amount,
            order_id=order_id,
            callback_url=callback_url
        )
        
        if mpesa_result["success"]:
            # Update payment with checkout request ID
            PaymentService.update_payment(
                db, 
                db_payment.id, 
                PaymentUpdate(status="pending", transaction_id=mpesa_result["checkout_request_id"])
            )
        
        return {
            **mpesa_result,
            "payment_id": db_payment.id
        }
    
    @staticmethod
    def process_mpesa_callback(db: Session, callback_data: dict) -> bool:
        checkout_request_id = callback_data.get("CheckoutRequestID")
        result_code = callback_data.get("ResultCode")
        
        # Find payment by transaction ID
        payment = db.query(Payment).filter(
            Payment.transaction_id == checkout_request_id
        ).first()
        
        if not payment:
            return False
        
        # Update payment status based on result code
        if result_code == 0:
            # Success
            PaymentService.update_payment(
                db, 
                payment.id, 
                PaymentUpdate(status="success", transaction_id=checkout_request_id)
            )
        else:
            # Failed
            PaymentService.update_payment(
                db, 
                payment.id, 
                PaymentUpdate(status="failed", transaction_id=checkout_request_id)
            )
        
        return True