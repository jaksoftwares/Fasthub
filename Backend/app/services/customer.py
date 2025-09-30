from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List, Optional
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CustomerService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_customer(db: Session, customer: CustomerCreate) -> Customer:
        hashed_password = CustomerService.hash_password(customer.password)
        db_customer = Customer(
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            password=hashed_password
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    
    @staticmethod
    def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.id == customer_id).first()
    
    @staticmethod
    def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.email == email).first()
    
    @staticmethod
    def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
        return db.query(Customer).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_customer(db: Session, customer_id: int, customer_update: CustomerUpdate) -> Optional[Customer]:
        db_customer = CustomerService.get_customer(db, customer_id)
        if not db_customer:
            return None
        
        update_data = customer_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = CustomerService.hash_password(update_data["password"])
        
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        
        db.commit()
        db.refresh(db_customer)
        return db_customer
    
    @staticmethod
    def delete_customer(db: Session, customer_id: int) -> bool:
        db_customer = CustomerService.get_customer(db, customer_id)
        if not db_customer:
            return False
        
        db.delete(db_customer)
        db.commit()
        return True