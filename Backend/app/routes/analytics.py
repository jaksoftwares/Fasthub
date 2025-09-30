from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.config import get_db
from app.services.analytics import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/sales-trend")
def get_sales_trend(
    months: int = Query(12, ge=1, le=24, description="Number of months to include"),
    db: Session = Depends(get_db)
):
    return AnalyticsService.get_sales_trend(db, months)

@router.get("/categories")
def get_category_sales(db: Session = Depends(get_db)):
    return AnalyticsService.get_category_sales(db)

@router.get("/top-products")
def get_top_products(
    limit: int = Query(5, ge=1, le=20, description="Number of products to return"),
    db: Session = Depends(get_db)
):
    return AnalyticsService.get_top_products(db, limit)

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    return AnalyticsService.get_dashboard_stats(db)

@router.get("/customer-metrics")
def get_customer_metrics(db: Session = Depends(get_db)):
    return AnalyticsService.get_customer_metrics(db)

@router.get("/orders-trend")
def get_orders_trend(
    months: int = Query(12, ge=1, le=24, description="Number of months to include"),
    db: Session = Depends(get_db)
):
    return AnalyticsService.get_orders_trend(db, months)