import requests
import base64
from datetime import datetime
from typing import Optional, Dict, Any
from app.config import settings

class MpesaService:
    @staticmethod
    def get_access_token() -> Optional[str]:
        """Get OAuth access token from Safaricom API"""
        if not settings.MPESA_CONSUMER_KEY or not settings.MPESA_CONSUMER_SECRET:
            return None
        
        api_url = f"{settings.MPESA_SANDBOX_URL}/oauth/v1/generate?grant_type=client_credentials"
        
        # Create credentials
        credentials = f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                return response.json().get("access_token")
        except Exception as e:
            print(f"Error getting access token: {e}")
        
        return None
    
    @staticmethod
    def generate_password() -> str:
        """Generate password for STK Push"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
        encoded_string = base64.b64encode(data_to_encode.encode()).decode()
        return encoded_string
    
    @staticmethod
    def initiate_stk_push(phone_number: str, amount: float, order_id: int, 
                         callback_url: str) -> Dict[str, Any]:
        """Initiate STK Push for M-Pesa payment"""
        access_token = MpesaService.get_access_token()
        if not access_token:
            return {"success": False, "message": "Failed to get access token"}
        
        api_url = f"{settings.MPESA_SANDBOX_URL}/mpesa/stkpush/v1/processrequest"
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = MpesaService.generate_password()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": f"Order{order_id}",
            "TransactionDesc": f"Payment for Order {order_id}"
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            result = response.json()
            
            if response.status_code == 200 and result.get("ResponseCode") == "0":
                return {
                    "success": True,
                    "checkout_request_id": result.get("CheckoutRequestID"),
                    "merchant_request_id": result.get("MerchantRequestID"),
                    "customer_message": result.get("CustomerMessage")
                }
            else:
                return {
                    "success": False,
                    "message": result.get("errorMessage", "STK Push failed")
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error initiating STK Push: {str(e)}"
            }
    
    @staticmethod
    def query_transaction_status(checkout_request_id: str) -> Dict[str, Any]:
        """Query transaction status"""
        access_token = MpesaService.get_access_token()
        if not access_token:
            return {"success": False, "message": "Failed to get access token"}
        
        api_url = f"{settings.MPESA_SANDBOX_URL}/mpesa/stkpushquery/v1/query"
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = MpesaService.generate_password()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers)
            result = response.json()
            
            return {
                "success": response.status_code == 200,
                "data": result
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error querying transaction: {str(e)}"
            }