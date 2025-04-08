import asyncio
import httpx
import json

async def test_webhook():
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "https://17c9-66-55-65-195.ngrok-free.app/webhook/payment",
                json=
                {
  "eventType": "subscription.recurring.payment.failed",
  "product": {
    "id": "4b8ec623-d0d0-4ce2-90bf-e442f4095153",
    "title": "Subscription 1243547918"
  },
  "contractId": "f2bda49a-2076-4dd7-acee-0cc74a699816",
   "parentContractId": "f2bda49a-2076-4dd7-acee-0cc74a699816",
  "buyer": {
    "email": "lol"
  }, 
  "amount": 50.0,
  "currency": "RUB",
  "timestamp": "2025-03-20T02:01:46.119475Z",
  "status": "subscription-active",
  "errorMessage": ""
},
                headers={
                    "Authorization": "test_signature"
                }
            )
            print(f"Status code: {response.status_code}")
            print(f"Response text: {response.text}")
            
            try:
                json_response = response.json()
                print(f"JSON response: {json_response}")
            except json.JSONDecodeError:
                print("Response is not JSON format")
                
        except httpx.RequestError as e:
            print(f"Error making request: {e}")

if __name__ == "__main__":
    asyncio.run(test_webhook())
