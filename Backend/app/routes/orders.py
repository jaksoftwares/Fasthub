from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config import get_db
from app.schemas.order import Order, OrderCreate, OrderUpdate
from app.services.order import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = OrderService.create_order(db, order)
    if not db_order:
        raise HTTPException(status_code=400, detail="Failed to create order. Check customer ID and product availability.")
    return db_order

@router.get("/", response_model=List[Order])
def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    customer_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return OrderService.get_orders(db, skip=skip, limit=limit, customer_id=customer_id, status=status)

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = OrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=Order)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    order = OrderService.update_order(db, order_id, order_update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/{order_id}/cancel", response_model=Order)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = OrderService.cancel_order(db, order_id)
    if not order:
        raise HTTPException(status_code=400, detail="Order cannot be cancelled or not found")
    return order