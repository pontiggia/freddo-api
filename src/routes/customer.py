from typing import Dict
from fastapi import APIRouter, HTTPException
import requests
import os
from dotenv import load_dotenv
from starlette.status import HTTP_204_NO_CONTENT
from ..config.database import conn
from ..models.user import users
from ..schemas.user import Customer

customer = APIRouter()

load_dotenv()
TEST_API_TOKEN = os.environ.get("TEST_API_TOKEN")
mId = os.environ.get("MERCHANT_ID")
global filtered_data 
filtered_data = []

@customer.get("/", description="Get customer information")
def get_customer_data(): # get data from customer
    url = f"https://sandbox.dev.clover.com/v3/merchants/{mId}/customers?expand=emailAddresses%2CphoneNumbers"
    
    headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + TEST_API_TOKEN}
    
    try:
        response = requests.get(url, headers=headers)
        if response is None:
            raise HTTP_204_NO_CONTENT(status_code=204, detail="Customer data is empty")
        try:
            # Filter the data to only return the necessary fields
            customer_data = response.json()["elements"]
            for customer in customer_data:
                if customer["emailAddresses"]["elements"][0]["emailAddress"] is None or customer["phoneNumbers"]["elements"] is None:
                    continue
                filter_customer_data = {
                    "filter_id": customer["id"],
                    "filter_firstName": customer["firstName"],
                    "filter_lastName": customer["lastName"],
                    "filter_customer_since": customer_data[0]["customerSince"],
                    "filter_email": customer["emailAddresses"]["elements"][0]["emailAddress"],
                    "filter_phone": customer["phoneNumbers"]["elements"][0]["phoneNumber"]
                }
                filtered_data.append(filter_customer_data)
            return filtered_data
        except IndexError as e:
            return {"message": str(e)}
    except HTTPException as e:
        return {"error": str(e)}


@customer.post("/customer", description="Insert customer data into database")
def create_customer(): # Insert a new customer data into database
    # check if the customer exists in the database, if not, insert the data into the database
    for customer in filtered_data:
        if conn.execute(users.select().where(users.c.customerId == customer["filter_id"])).fetchone() is None:
            conn.execute(users.insert(), customer)
            print("Inserted customer data into database successfully")
        else:
            continue
        
        
        