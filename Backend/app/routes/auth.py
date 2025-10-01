
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config import get_db
from app.schemas.customer import CustomerCreate, Customer
from app.schemas.auth import Token
from app.services.customer import CustomerService
from app.utils.security import create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------------------------
# Get all customers (admin)
# ---------------------------
@router.get("/customers", response_model=List[Customer])
def get_all_customers(db: Session = Depends(get_db)):
    """
    Fetch all customers who have signed up, including their last order (as last login proxy), join date, etc.
    """
    customers = CustomerService.get_customers(db)
    return customers

# ---------------------------
# Register (Sign up)
# ---------------------------
@router.post("/register", response_model=Token)
def register(customer: CustomerCreate, db: Session = Depends(get_db)):
    existing_customer = CustomerService.get_customer_by_email(db, customer.email)
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    new_customer = CustomerService.create_customer(db, customer)

    # Issue JWT token immediately
    access_token = create_access_token(new_customer.email)
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------------------
# Login (Sign in)
# ---------------------------
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    customer = CustomerService.get_customer_by_email(db, form_data.username)
    if not customer:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not CustomerService.verify_password(form_data.password, customer.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(customer.email)
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------------------
# Refresh token (simple version)
# ---------------------------
@router.post("/refresh", response_model=Token)
def refresh_token(token: str, db: Session = Depends(get_db)):
    email = decode_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    customer = CustomerService.get_customer_by_email(db, email)
    if not customer:
        raise HTTPException(status_code=401, detail="Customer not found")

    new_token = create_access_token(email)
    return {"access_token": new_token, "token_type": "bearer"}


# ---------------------------
# Logout (stateless demo)
# ---------------------------
@router.post("/logout")
def logout():
    """
    Since JWT is stateless, logout is usually handled client-side
    by deleting the stored token. 
    If you want server-side logout, you’d need token blacklisting.
    """
    return {"message": "Logout successful. Please discard the token on the client."}
