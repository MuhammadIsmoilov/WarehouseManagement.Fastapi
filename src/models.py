from pydantic import BaseModel,Field
from typing import Union,Optional



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