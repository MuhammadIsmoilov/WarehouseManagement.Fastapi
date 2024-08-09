from pydantic import BaseModel
from typing import Union 
from datetime import datetime
from enum import Enum



class Tags(Enum):
    login = 'Login'
    user = 'User'
    sales = 'Sales'
    purchase = 'Buying'
    catalog = 'Catalogs'
    customer = 'Customer'
    provider = 'Supplier'
    inventory = 'Inventory'


class UsersRegistration(BaseModel):
    fullname: str
    gender: str
    user_address: str
    user_phone_number: str
    user_password: str
    role_id:int




class UserUpdate(BaseModel):
    user_id:int
    fullname: str
    gender: str
    user_address: str
    user_phone_number: str
    user_password: str
    role_id:int




class RoleInsert(BaseModel):
    role_name: str



class RoleUpdate(BaseModel):
    role_id:int
    role_name: str


class RolesPermissionInsert(BaseModel):
    role_id:int
    permission_id:int



class RolesPermissionUpdate(BaseModel):
    roles_permission_id:int
    role_id:int
    permission_id:int


class InvoiceInsert(BaseModel):
    customer_id: Union[int,None] = None
    invoice_quantity: Union[int,None] = None
    invoice_unit_price: Union[int,None] = None
    invoice_date: Union[datetime,None] = None


class InvoiceUpdate(BaseModel):
    invoice_id:Union[int,None] = None
    customer_id:Union[int,None] = None
    invoice_quantity:Union[int,None] = None
    invoice_unit_price:Union[int,None] = None
    invoice_date:Union[datetime,None] = None


class InvoicePropertyInsert(BaseModel):
    prod_id:int
    invoice_id:int



class InvoicePropertyUpdate(BaseModel):
    property_id:int
    prod_id:int
    invoice_id:int



class PurchaseInsert(BaseModel):        
    sup_id:int                      
    purch_date:datetime      
    purch_quantity:int   
    purch_unit_price:int
    user_id:int

class PurchaseUpdate(BaseModel):
    purch_id:int         
    sup_id:int                                            
    purch_date:datetime      
    purch_quantity:int   
    purch_unit_price:int
    user_id:int

        




class PurchasePropertyInsert(BaseModel):        
    prod_id:int
    purchase_id:int

class PurchasePropertyUpdate(BaseModel):
    property_id:int
    prod_id:int
    purchase_id:int



class InsertCategory(BaseModel):
    ctg_name:str
    parent_category_id:Union[int,None] = None

class UpdateCategory(BaseModel):
    ctg_id:int
    ctg_name:str
    parent_category_id:Union[int,None] = None





class InsertNomenclature(BaseModel):
    nom_name:str
    nom_description:str

class UpdateNomenclature(BaseModel):
    nom_id:int
    nom_name:str
    nom_description:str




class InsertCustomer(BaseModel):
    custom_name:str
    custom_address:str
    custom_custom_contact_info:str


class UpdateCustomer(BaseModel):
    custom_id:int
    custom_name:Union[str,None] = None
    custom_addres:Union[str,None] = None
    custom_custom_contact_info:Union[str,None] = None





class InsertSupplier(BaseModel):
    supp_name:str
    supp_address:str
    supp_contact_info:str


class UpdateSupplier(BaseModel):
    supp_id:int
    supp_name:Union[str,None] = None
    supp_address:Union[str,None] = None
    supp_contact_info:Union[str,None] = None







class ProductInsert(BaseModel):
    nom_id:int
    category_id:int
    prod_price:int
    prod_quontity:int
    articul:Union[str,None] = None
    barcode:Union[str,None] = None
    prod_attribute:Union[dict,None] = None


class ProductUpdate(BaseModel):
    prod_id:int
    nom_id:int
    category_id:int
    prod_price:int
    prod_quontity:int
    articul:Union[str,None] = None
    barcode:Union[str,None] = None
    prod_attribute:Union[dict,None] = None


class Incoming_and_outgoingInsert(BaseModel):
    product_id:int
    quantity:int
    date_of_incoming_and_outgoing:datetime
    incoming_and_outgoing_type:bool
    is_active:bool



class UpdateIncoming_and_outgoing(BaseModel):
    income_id:int
    product_id:int
    quantity:int
    date_of_incoming_and_outgoing:datetime
    incoming_and_outgoing_type:bool
    is_active:bool


