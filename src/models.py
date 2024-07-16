from pydantic import BaseModel,Field
from typing import Union,Optional



class InsertCategory(BaseModel):
    ctg_name:str
    parent_category:Union[int,None] = None