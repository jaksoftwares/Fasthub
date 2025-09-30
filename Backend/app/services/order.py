from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.order import Order
from app.models.customer import Customer
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.customer import CustomerService
from app.services.product import ProductService

class OrderService:
    @staticmethod
    def create_order(db: Session, order: OrderCreate) -> Optional[Order]:
        # Verify customer exists
        customer = CustomerService.get_customer(db, order.customer_id)
        if not customer:
            return None
        
        # Verify products exist and have sufficient stock
        total_calculated = 0
        for item in order.products:
            product = ProductService.get_product(db, item.id)
            if product is None or product.stock < item.quantity:
                return None
            total_calculated += item.price * item.quantity
        
        # Create order
        db_order = Order(
            customer_id=order.customer_id,
            products=[item.model_dump() for item in order.products],
            total=order.total,
            payment_method=order.payment_method,
            shipping_address=order.shipping_address
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # Update product stock
        for item in order.products:
            ProductService.update_stock(db, item.id, -item.quantity)
        
        # Update customer stats
        setattr(customer, 'total_orders', customer.total_orders + 1)
        setattr(customer, 'total_spent', customer.total_spent + order.total)
        setattr(customer, 'last_order', datetime.utcnow())
        db.commit()
        
        return db_order
    
    @staticmethod
    def get_order(db: Session, order_id: int) -> Optional[Order]:
        return db.query(Order).filter(Order.id == order_id).first()
    
    @staticmethod
    def get_orders(db: Session, skip: int = 0, limit: int = 100, 
                  customer_id: Optional[int] = None, status: Optional[str] = None) -> List[Order]:
        query = db.query(Order)
        
        if customer_id:
            query = query.filter(Order.customer_id == customer_id)
        if status:
            query = query.filter(Order.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_order(db: Session, order_id: int, order_update: OrderUpdate) -> Optional[Order]:
        db_order = OrderService.get_order(db, order_id)
        if not db_order:
            return None
        
        update_data = order_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        
        db.commit()
        db.refresh(db_order)
        return db_order
    
    @staticmethod
    def cancel_order(db: Session, order_id: int) -> Optional[Order]:
        db_order = OrderService.get_order(db, order_id)
        if not db_order or db_order.status in ["shipped", "completed", "cancelled"]:
            return None
        
        # Restore product stock
        for item in db_order.products:
            ProductService.update_stock(db, item["id"], item["quantity"])
        
        # Update customer stats
        customer = CustomerService.get_customer(db, db_order.customer_id)
        if customer:
            setattr(customer, 'total_orders', customer.total_orders - 1)
            setattr(customer, 'total_spent', customer.total_spent - db_order.total)
        
        setattr(db_order, 'status', "cancelled")
        db.commit()
        db.refresh(db_order)
        return db_order