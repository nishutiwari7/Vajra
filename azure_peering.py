import requests
import razorpay
from config import RAZORPAY_API_KEY, RAZORPAY_API_SECRET, RAZORPAY_PAYMENT_LINKS

class AzurePeering:
    def __init__(self):
        self.client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))
        self.azure_api_url = "https://management.azure.com/"  # Base Azure API URL

    def create_peering(self, subscription_id, resource_group, virtual_network_name, peering_name, remote_vnet_id):
        """
        Creates a VNet peering in Azure.
        """
        endpoint = f"{self.azure_api_url}subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Network/virtualNetworks/{virtual_network_name}/virtualNetworkPeerings/{peering_name}?api-version=2022-01-01"
        
        headers = {
            "Authorization": "Bearer <YOUR_AZURE_ACCESS_TOKEN>",
            "Content-Type": "application/json"
        }
        
        payload = {
            "properties": {
                "remoteVirtualNetwork": {"id": remote_vnet_id},
                "allowVirtualNetworkAccess": True,
                "allowForwardedTraffic": True,
                "allowGatewayTransit": False
            }
        }
        
        response = requests.put(endpoint, headers=headers, json=payload)
        if response.status_code == 200 or response.status_code == 201:
            print(f"Peering '{peering_name}' created successfully.")
            return response.json()
        else:
            raise Exception(f"Failed to create peering: {response.text}")

    def initiate_payment(self, amount, currency):
        """
        Initiates Razorpay payment for the Azure peering service.
        """
        try:
            order_data = {
                "amount": amount * 100,  # Razorpay expects the amount in the smallest currency unit
                "currency": currency,
                "payment_capture": 1
            }
            order = self.client.order.create(order_data)
            print(f"Payment initiated for {currency}. Visit: {RAZORPAY_PAYMENT_LINKS[currency]}")
            return order
        except Exception as e:
            raise Exception(f"Failed to initiate payment: {str(e)}")
