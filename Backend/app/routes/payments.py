from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.config import get_db
from app.schemas.payment import Payment, PaymentCreate, PaymentUpdate, MpesaSTKRequest, MpesaCallback
from app.services.payment import PaymentService

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=Payment)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = PaymentService.create_payment(db, payment)
    if not db_payment:
        raise HTTPException(status_code=400, detail="Failed to create payment. Check order ID.")
    return db_payment

@router.get("/", response_model=List[Payment])
def get_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return PaymentService.get_payments(db, skip=skip, limit=limit)

@router.get("/{payment_id}", response_model=Payment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = PaymentService.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/order/{order_id}", response_model=Payment)
def get_payment_by_order(order_id: int, db: Session = Depends(get_db)):
    payment = PaymentService.get_payment_by_order(db, order_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found for this order")
    return payment

@router.put("/{payment_id}", response_model=Payment)
def update_payment(payment_id: int, payment_update: PaymentUpdate, db: Session = Depends(get_db)):
    payment = PaymentService.update_payment(db, payment_id, payment_update)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.post("/mpesa/stk-push")
def initiate_mpesa_payment(request: MpesaSTKRequest, db: Session = Depends(get_db)):
    callback_url = "https://your-domain.com/payments/mpesa/callback"  # This should be configurable
    
    result = PaymentService.initiate_mpesa_payment(
        db=db,
        phone_number=request.phone_number,
        amount=request.amount,
        order_id=request.order_id,
        callback_url=callback_url
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.post("/mpesa/callback")
def mpesa_callback(callback_data: MpesaCallback, db: Session = Depends(get_db)):
    success = PaymentService.process_mpesa_callback(db, callback_data.model_dump())
    if not success:
        raise HTTPException(status_code=400, detail="Failed to process callback")
    
    return {"message": "Callback processed successfully"}