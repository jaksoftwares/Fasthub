# FastAPI E-commerce Backend

## Overview

This is a complete FastAPI backend for a single-store e-commerce application with comprehensive support for product management, customer handling, order processing, payment integration (including M-Pesa), repair services, and analytics dashboards. The application follows a modular architecture with clear separation of concerns between models, schemas, routes, and business logic services.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Database Layer
- **ORM**: SQLAlchemy with declarative base for object-relational mapping
- **Database**: SQLite for development/testing (easily configurable for other databases)
- **Session Management**: Dependency injection pattern for database sessions
- **Models**: Six core entities - Product, Customer, Order, Payment, RepairRequest, and Settings

### API Layer
- **Framework**: FastAPI with automatic OpenAPI documentation
- **Routing**: Modular router system organized by domain (products, customers, orders, etc.)
- **Validation**: Pydantic schemas for request/response validation and serialization
- **Error Handling**: HTTP exception handling with appropriate status codes
- **CORS**: Configured for cross-origin requests

### Business Logic Layer
- **Service Pattern**: Domain-specific service classes encapsulating business logic
- **Password Security**: bcrypt hashing for customer authentication
- **Stock Management**: Automatic inventory updates during order processing
- **Customer Analytics**: Automatic tracking of customer spending and order history

### Payment Integration
- **M-Pesa Integration**: STK Push implementation for mobile payments
- **Multiple Payment Methods**: Support for M-Pesa, card payments, and cash on delivery
- **Transaction Tracking**: Complete payment lifecycle management with status updates
- **Security**: OAuth token management and secure credential handling

### Data Models Architecture
- **Product Management**: Comprehensive product catalog with technical specifications, inventory tracking, and categorization
- **Customer Management**: User accounts with password hashing, spending analytics, and order history
- **Order Processing**: JSON-based product storage, status tracking, and shipping address management
- **Repair Services**: Independent repair request system with status tracking and technician notes
- **Configuration**: Centralized settings management for store, payment, shipping, and notification preferences

### External Service Integration
- **Environment Configuration**: dotenv for secure credential management
- **API Communication**: HTTP client integration for external payment gateways
- **Analytics**: Built-in reporting system for sales trends, customer metrics, and product performance

## External Dependencies

### Core Framework Dependencies
- **FastAPI**: Modern Python web framework with automatic API documentation
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Pydantic**: Data validation and serialization using Python type hints
- **passlib[bcrypt]**: Password hashing library with bcrypt support

### Database
- **SQLite**: Lightweight database for development (configured for easy PostgreSQL migration)

### Payment Services
- **Safaricom M-Pesa API**: Mobile payment integration for Kenyan market
  - OAuth authentication endpoint
  - STK Push API for payment initiation
  - Callback handling for transaction status updates

### Development Tools
- **python-dotenv**: Environment variable management
- **uvicorn**: ASGI server for running the FastAPI application

### Security
- **bcrypt**: Password hashing algorithm
- **Base64 encoding**: For M-Pesa API authentication
- **Environment variables**: Secure storage of API keys and secrets

The application is designed to be easily deployable on cloud platforms with minimal configuration changes, particularly for scaling from SQLite to PostgreSQL in production environments.