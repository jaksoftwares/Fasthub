from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.services.customer import CustomerService
from app.utils.security import create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    @staticmethod
    def authenticate_customer(db: Session, email: str, password: str):
        customer = CustomerService.get_customer_by_email(db, email)
        if not customer or not CustomerService.verify_password(password, customer.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return customer

    @staticmethod
    def login(db: Session, form_data: OAuth2PasswordRequestForm):
        customer = AuthService.authenticate_customer(db, form_data.username, form_data.password)
        token = create_access_token(subject=customer.email)
        return {"access_token": token, "token_type": "bearer"}
