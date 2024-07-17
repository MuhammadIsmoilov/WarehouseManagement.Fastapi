from fastapi import FastAPI,HTTPException
from src.models import (RoleDelete, RoleInsert, RoleUpdate, UserUpdate, UsersRegistration,UserDelete,InvoiceInsert,InvoiceDelete, InvoiceUpdate)
from lib.connection import connection
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.post('/user/reg/')
def user_registration(data: UsersRegistration):
    try:
        with connection() as cur:
            text_res = "Initial Value"
            cur.execute('CALL users.user_insert(%s, %s, %s, %s, %s, %s, %s)', 
                        (data.fullname, data.gender, data.user_address, 
                         data.user_phone_number, data.user_password, data.role_id, text_res))
            
            result = cur.fetchone()[0]
        
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.put('/update/user/')
def update_user(data: UserUpdate):
    try:
        with connection() as cur:
            text_res = "Initial Value"
            cur.execute('call users.update_user(%s, %s, %s, %s, %s, %s, %s, %s)', (data.user_id,data.fullname, data.gender,data.user_address, 
                         data.user_phone_number, data.user_password, data.role_id, text_res,))
        return 'User updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.delete('/delete/user/')
def delete_user(data: UserDelete):
    try:
        with connection() as cur:
            cur.execute('call users.delete_user(%s)', (data.user_id,))
        return 'User deleted successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



    
@app.post('/insert/role/')
def role_insert(data:RoleInsert):
    try:
        with connection() as cur:
            cur.execute('call users.role_insert(%s)', (data.role_name,))
            return 'Role added seccessfuly'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put('/update/role/')
def update_role(data: RoleUpdate):
    try:
        with connection() as cur:
            cur.execute('call users.update_user(%s,%s)', (data.role_id, data.role_name))
        return 'User updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



@app.delete('/delete/role/')
def delete_role(data: RoleDelete):
    try:
        with connection() as cur:
            cur.execute('call users.delete_user(%s)', (data.role_id,))
        return 'Role deleted successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    




@app.post('/add/invoice/')
def insert_invoice(data: InvoiceInsert):
    try:
        with connection() as cur:

            cur.execute('CALL sales.invoice_insert(%s, %s, %s, %s, %s, %s,)', 
                       (data.customer_id,
                        data.product_id,
                        data.invoice_quontity, 
                        data.invoice_unit_price,
                        data.invoice_date, 
                        data.invoice_total_amount, ))
            
            
        
        return {"message": 'Invoice added successfuly'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.put('/update/invoice/')
def update_invoice(data: InvoiceUpdate):
    try:
        with connection() as cur:
         cur.execute('CALL sales.update_invoice(%s, %s, %s, %s, %s, %s, %s,)', 
                       (data.invoice_id,
                        data.customer_id,
                        data.product_id,
                        data.invoice_quontity, 
                        data.invoice_unit_price,
                        data.invoice_date, 
                        data.invoice_total_amount, ))
        return 'Invoice updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.delete('/delete/invoice/')
def delete_invoice(data: InvoiceDelete):
    try:
        with connection() as cur:
            cur.execute('call sales.delete_invoice(%s)', (data.user_id,))
        return 'Invoice deleted successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))