from pydantic import BaseModel
from typing import Union 
from datetime import datetime


class UsersRegistration(BaseModel):
    fullname: str
    gender: str
    user_address: str
    user_phone_number: str
    user_password: str
    role_id: Union[int, None] = None

class UserDelete(BaseModel):
    user_id:int

class UserUpdate(BaseModel):
        user_id:int
        fullname: str
        gender: str
        user_address: str
        user_phone_number: str
        user_password: str
        role_id: int



class RoleInsert(BaseModel):
    role_name: str


class RoleDelete(BaseModel):
    role_id:int

class RoleUpdate(BaseModel):
    role_id:int
    role_name: str
      

class InvoiceInsert(BaseModel):
    customer_id:int
    product_id:int
    invoice_quontity:int
    invoice_unit_price:int
    invoice_date:datetime
    invoice_total_amount:int

class InvoiceDelete(BaseModel):
    invoice_id:int

class InvoiceUpdate(BaseModel):
    invoice_id:int
    customer_id:int
    product_id:int
    invoice_quontity:int
    invoice_unit_price:int
    invoice_date:datetime
    invoice_total_amount:int

