from fastapi import FastAPI,HTTPException
from src.models import InsertCategory,InsertCustomer,InsertSupplier,UpdateSupplier,UpdateCustomer,DeleteCustomer,DeleteSupplier
app = FastAPI()
from lib.connection import connection


@app.post('/insert/category')   
def insert_category(data:InsertCategory):
    try:
        with connection() as cur:
            cur.execute('call catalogs.category_insert(%s,%s)',(data.ctg_name,data.parent_category,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.post('/insert/customer')   
def insert_customer(data:InsertCustomer):
    try:
        with connection() as cur:
            cur.execute('call customer.customer_insert(%s,%s,%s)',(data.custom_name,data.custom_address,data.custom_custom_contact_info,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))    


@app.put('/update/customer')   
def update_customer(data:UpdateCustomer):
    try:
        with connection() as cur:
            cur.execute('call customer.update_customer(%s,%s,%s,%s)',(data.custom_id,data.custom_name,data.custom_addres,data.custom_custom_contact_info,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))  


@app.delete('/delete/categoty')
def delete_customer(data:DeleteCustomer ): 
    try:
        with connection() as cur:
            cur.execute("Call customer.delete_customer (%s)",(data.custom_id,)) 
            return "OK"
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))      



@app.post('/insert/supplier')   
def insert_supplier(data:InsertSupplier):
    try:
        with connection() as cur:
            cur.execute('call provider.supplier_insert(%s,%s,%s)',(data.supp_name,data.supp_address,data.supp_contact_info,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))    
        


@app.put('/update/supplier')   
def update_supplier(data:UpdateSupplier):
    try:
        with connection() as cur:
            cur.execute('call provider.update_supplier(%s,%s,%s,%s)',(data .supp_id,data.supp_name,data.supp_address,data.supp_contact_info,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))  


@app.delete('/delete/supplier')
def delete_supplier(data:DeleteSupplier ): 
    try:
        with connection() as cur:
            cur.execute("Call provider.delete_supplier (%s)",(data.supp_id,)) 
            return "OK"
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))  













@app.get('/categories/all')
def get_all_categories():
    result = None 
    with connection() as cur:
        cur.execute('SELECT catalogs.get_all_categories()')
        result = cur.fetchone()[0]

    return result