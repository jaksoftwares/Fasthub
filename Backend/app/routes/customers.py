from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from app.config import get_db
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate
from app.services.customer import CustomerService
from app.utils.security import decode_access_token

router = APIRouter(prefix="/customers", tags=["customers"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = decode_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    customer = CustomerService.get_customer_by_email(db, email)
    if not customer:
        raise HTTPException(status_code=401, detail="Customer not found")
    return customer

@router.post("/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    existing_customer = CustomerService.get_customer_by_email(db, customer.email)
    if existing_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return CustomerService.create_customer(db, customer)

@router.get("/", response_model=List[Customer])
def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return CustomerService.get_customers(db, skip=skip, limit=limit)

@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerService.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer_update: CustomerUpdate, db: Session = Depends(get_db)):
    customer = CustomerService.update_customer(db, customer_id, customer_update)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    success = CustomerService.delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@router.get("/me", response_model=Customer)
def read_current_customer(current_customer: Customer = Depends(get_current_customer)):
    return current_customer
