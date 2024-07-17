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


class InsertCategory(BaseModel):
    ctg_name:str
    parent_category:Union[int,None] = None



class InsertCustomer(BaseModel):
    custom_name:str
    custom_address:str
    custom_custom_contact_info:str


class UpdateCustomer(BaseModel):
    custom_id:int
    custom_name:Union[str,None] = None
    custom_addres:Union[str,None] = None
    custom_custom_contact_info:Union[str,None] = None


class DeleteCustomer(BaseModel):
    custom_id:int


class InsertSupplier(BaseModel):
    supp_name:str
    supp_address:str
    supp_contact_info:str


class UpdateSupplier(BaseModel):
    supp_id:int
    supp_name:Union[str,None] = None
    supp_address:Union[str,None] = None
    supp_contact_info:Union[str,None] = None



class DeleteSupplier(BaseModel):
    supp_id:int
