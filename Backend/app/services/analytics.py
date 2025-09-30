from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.models.order import Order
from app.models.payment import Payment
from app.models.product import Product
from app.models.customer import Customer

class AnalyticsService:
    @staticmethod
    def get_sales_trend(db: Session, months: int = 12) -> List[Dict[str, Any]]:
        """Get monthly sales trend for the last N months"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        results = db.query(
            extract('year', Payment.created_at).label('year'),
            extract('month', Payment.created_at).label('month'),
            func.sum(Payment.amount).label('total_sales'),
            func.count(Payment.id).label('order_count')
        ).filter(
            Payment.status == 'success',
            Payment.created_at >= start_date
        ).group_by(
            extract('year', Payment.created_at),
            extract('month', Payment.created_at)
        ).order_by(
            extract('year', Payment.created_at),
            extract('month', Payment.created_at)
        ).all()
        
        return [
            {
                "year": int(row.year),
                "month": int(row.month),
                "total_sales": float(row.total_sales or 0),
                "order_count": row.order_count
            }
            for row in results
        ]
    
    @staticmethod
    def get_category_sales(db: Session) -> List[Dict[str, Any]]:
        """Get sales by product category"""
        # This is a simplified version - in practice, you'd need to parse the JSON products field
        results = db.query(
            Product.category,
            func.count(Product.id).label('product_count')
        ).group_by(Product.category).all()
        
        # For demonstration, return mock data since we need to parse order products
        categories = [
            {"category": "Electronics", "sales": 25000, "count": 150},
            {"category": "Computers", "sales": 45000, "count": 89},
            {"category": "Phones", "sales": 32000, "count": 203},
            {"category": "Accessories", "sales": 8000, "count": 95}
        ]
        
        return categories
    
    @staticmethod
    def get_top_products(db: Session, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top selling products"""
        # This would require parsing the JSON products field in orders
        # For now, return mock data
        products = db.query(Product).limit(limit).all()
        
        return [
            {
                "id": product.id,
                "name": product.name,
                "units_sold": 50 + (product.id * 10),  # Mock data
                "revenue": product.price * (50 + (product.id * 10))
            }
            for product in products
        ]
    
    @staticmethod
    def get_dashboard_stats(db: Session) -> Dict[str, Any]:
        """Get KPI statistics for dashboard"""
        # Total revenue from successful payments
        total_revenue = db.query(func.sum(Payment.amount)).filter(
            Payment.status == 'success'
        ).scalar() or 0
        
        # Total orders
        total_orders = db.query(func.count(Order.id)).scalar() or 0
        
        # Total customers
        total_customers = db.query(func.count(Customer.id)).scalar() or 0
        
        # Total products
        total_products = db.query(func.count(Product.id)).scalar() or 0
        
        # Recent orders (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_orders = db.query(func.count(Order.id)).filter(
            Order.date >= thirty_days_ago
        ).scalar() or 0
        
        return {
            "total_revenue": float(total_revenue),
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_products": total_products,
            "recent_orders": recent_orders
        }
    
    @staticmethod
    def get_customer_metrics(db: Session) -> Dict[str, Any]:
        """Get customer satisfaction and delivery metrics"""
        # Mock data for demonstration
        return {
            "avg_rating": 4.3,
            "satisfaction_rate": 87.5,
            "avg_delivery_time": 2.8  # days
        }
    
    @staticmethod
    def get_orders_trend(db: Session, months: int = 12) -> List[Dict[str, Any]]:
        """Get order count trend by month"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        results = db.query(
            extract('year', Order.date).label('year'),
            extract('month', Order.date).label('month'),
            func.count(Order.id).label('order_count')
        ).filter(
            Order.date >= start_date
        ).group_by(
            extract('year', Order.date),
            extract('month', Order.date)
        ).order_by(
            extract('year', Order.date),
            extract('month', Order.date)
        ).all()
        
        return [
            {
                "year": int(row.year),
                "month": int(row.month),
                "order_count": row.order_count
            }
            for row in results
        ]