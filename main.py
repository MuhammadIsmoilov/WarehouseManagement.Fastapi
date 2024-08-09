from fastapi import FastAPI,HTTPException
from src.models import (InsertNomenclature, InvoicePropertyInsert, InvoicePropertyUpdate, PurchasePropertyInsert,
                        PurchasePropertyUpdate,RolesPermissionInsert, RolesPermissionUpdate,UpdateNomenclature,
                        ProductInsert,ProductUpdate,InsertCategory,UpdateCategory,InsertCustomer,InsertSupplier,
                        UpdateSupplier,UpdateCustomer,UserUpdate, UsersRegistration,InvoiceInsert, InvoiceUpdate,
                        PurchaseInsert, PurchaseUpdate,RoleInsert, RoleUpdate,Incoming_and_outgoingInsert,UpdateIncoming_and_outgoing,
                        Tags)
from lib.connection import connection
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from docx import Document 
import json


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.post('/user/registration/', tags=[Tags.user])
def user_registration(data: UsersRegistration):
    try:
        with connection() as cur:
            text_res = "Initial Value"
            cur.execute('CALL users.user_insert(%s, %s, %s, %s, %s, %s, %s)', 
                        (data.fullname, data.gender, data.user_address, 
                         data.user_phone_number, data.user_password,data.role_id, text_res))
            
            result = cur.fetchone()[0]
        
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    

@app.put('/user/',tags=[Tags.user])
def update_user(data: UserUpdate):
    try:
        with connection() as cur:
            text_res = "Initial Value"
            cur.execute('call users.update_user(%s, %s, %s, %s, %s, %s, %s,)', (data.user_id,data.fullname, data.gender,data.user_address, 
                         data.user_phone_number, data.user_password,data.role_id, text_res,))
        return 'User updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    



    
@app.post('/role/', tags=[Tags.user])
def role_insert(data:RoleInsert):
    try:
        with connection() as cur:
            cur.execute('call users.role_insert(%s)', (data.role_name,))
            return 'Role added seccessfuly'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put('/role/', tags=[Tags.user])
def update_role(data: RoleUpdate):
    try:
        with connection() as cur:
            cur.execute('call users.update_role(%s,%s)', (data.role_id, data.role_name))
        return 'Role updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
   



@app.post('/role-permission/',tags=[Tags.user])
def roles_permission_insert(data:RolesPermissionInsert):
    try:
        with connection() as cur:
            cur.execute('call users.roles_permission_insert(%s,%s)', (data.role_id,data.permission_id,))
            return 'Role permission added seccessfuly'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put('/role-permission/', tags=[Tags.user])
def update_roles_permission(data: RolesPermissionUpdate):
    try:
        with connection() as cur:
            cur.execute('call users.update_roles_permission(%s,%s,%s)', (data.roles_permission_id,data.role_id, data.permission_id,))
        return 'Role permission updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    




@app.post('/invoice/', tags=[Tags.sales])
def insert_invoice(data: InvoiceInsert):
    try:
        with connection() as conn:
            with conn as cur:
                cur.execute(
                    'CALL sales.invoice_insert(%s, %s, %s, %s)', 
                    (data.customer_id, data.invoice_quantity, data.invoice_unit_price, data.invoice_date))
        return {"message": 'Invoice added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.put('/invoice/', tags=[Tags.sales])
def update_invoice(data: InvoiceUpdate):
    try:
        with connection() as cur:
         cur.execute('CALL sales.update_invoice(%s, %s, %s, %s, %s, %s)', 
                       (data.invoice_id,
                        data.customer_id,
                        data.invoice_quantity, 
                        data.invoice_unit_price,
                        data.invoice_date,))
        return 'Invoice updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.post('/invoice-property/', tags=[Tags.sales])
def insert_invoice_property(data: InvoicePropertyInsert):
    try:
        with connection() as conn:
            with conn as cur:
                cur.execute(
                    'CALL sales.invoice_property_insert(%s, %s)', 
                    (data.prod_id, data.invoice_id,))
        return {"message": 'Invoice property added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.put('/invoice-property/', tags=[Tags.sales])
def update_invoice_property(data: InvoicePropertyUpdate):
    try:
        with connection() as cur:
         cur.execute('CALL sales.update_invoice_property(%s, %s, %s)', 
                       (data.property_id,
                        data.prod_id,
                        data.invoice_id,))
        return 'Invoice property updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get('/invoice/of/product/', tags=[Tags.sales])
def get_invoice_details_of_product():
    result = None
    with connection() as cur:
        cur.callproc('sales.get_invoice_details_of_product')
        result = cur.fetchall()
        
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="No data found")

        row = result[0][0]

        invoice = row[0]

        doc = Document("files/Накладная продажи.docx")
        data_mapping = {
            "{invoice_id}": str(invoice['invoice_id']),
            "{invoice_date}": str(invoice['invoice_date']),
            "{custom_name}": str(invoice['custom_name']),
            "{custom_address}": str(invoice['custom_address']),
            "{custom_contact_info}": str(invoice['custom_contact_info']),
            "{invoice_quantity}": str(invoice['invoice_quantity']),
            "{invoice_unit_price}": str(invoice['invoice_unit_price']),
            "{articul}": str(invoice['articul']),
            "{barcode}": str(invoice['barcode']),
            "{ctg_name}": str(invoice['ctg_name']),
            "{invoice_total_amount}": str(invoice['invoice_total_amount'])
        }

        column_to_property = {
            0: "nom_name",
            1: "invoice_quantity",
            2: "invoice_unit_price",
            3: "articul",
            4: "barcode",
            5: "invoice_total_amount"
        }

        tbl = doc.add_table(0, 6)

        for r in row:
            t_row = tbl.add_row()
            for y in range(0, 6):
                t_row.cells[y].add_paragraph(str(r[column_to_property[y]]))

        # Replace placeholders in DOCX
        for paragraph in doc.paragraphs:
            for marker, value in data_mapping.items():
                if marker in paragraph.text:
                    paragraph.text = paragraph.text.replace(marker, value)

        filename_docx = f"{invoice['invoice_id']}.docx"
        doc.save(filename_docx)
        doc = Document(filename_docx)

        return FileResponse(filename_docx, media_type='application/pdf', filename=filename_docx)

        




@app.post('/purchase/', tags=[Tags.purchase])
def insert_purchase(data: PurchaseInsert):
    try:
        with connection() as cur:
           cur.execute('CALL buying.purchase_insert(%s, %s, %s, %s, %s, %s)', 
                            (data.sup_id,
                             data.purch_date, 
                             data.purch_quantity,
                             data.purch_unit_price,
                             data.user_id,))
        return {"message": 'Purchase added successfuly'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.put('/purchase/', tags=[Tags.purchase])
def update_purchase(data: PurchaseUpdate):
    try:
        with connection() as cur:
         cur.execute('CALL buying.update_purchase(%s, %s, %s, %s, %s, %s, %s)', 
                       (data.purch_id,
                        data.sup_id,
                        data.purch_date, 
                        data.purch_quantity,
                        data.purch_unit_price,
                        data.user_id,))
        return 'Purchase updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@app.post('/purchase-property/', tags=[Tags.purchase])
def insert_purchase_property(data: PurchasePropertyInsert):
    try:
        with connection() as cur:
           cur.execute('CALL buying.purchase_property_insert(%s, %s)', 
                            (data.prod_id,
                             data.purchase_id,))
        return {"message": 'Purchase property added successfuly'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.put('/purchase-property/', tags=[Tags.purchase])
def update_purchase_property(data: PurchasePropertyUpdate):
    try:
        with connection() as cur:
         cur.execute('CALL buying.update_purchase_property(%s, %s, %s)', 
                       (data.property_id,
                        data.prod_id,
                        data.purchase_id,))
        return 'Purchase property updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get('/purchase-invoice/of/product/', tags=[Tags.purchase])
def get_purchase_details_of_product():
    result = None
    with connection() as cur:
        cur.callproc('buying.get_purchase_details_of_product')
        result = cur.fetchall()
        
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="No data found")

        row = result[0][0]
        purchase = row[0]
        
        doc = Document("files/Накладная покупки.docx")
        data_mapping = {
            "{purchase_id}":str(purchase['purchase_id']),
            "{purchase_date}": str(purchase['purchase_date']),
            "{supp_name}": str(purchase['supp_name']),
            "{supp_address}": str(purchase['supp_address']),
            "{supp_contact_info}": str(purchase['supp_contact_info']),
            "{nom_name}": str(purchase['nom_name']),
            "{purchase_quantity}": str(purchase['purchase_quantity']),
            "{purchase_unit_price}": str(purchase['purchase_unit_price']),
            "{articul}": str(purchase['articul']),
            "{barcode}": str(purchase['barcode']),
            "{ctg_name}": str(purchase['ctg_name']),
            "{purchase_total_amount}": str(purchase['purchase_total_amount']),
            "{fullname}":str(purchase['fullname'])
        }

        column_to_property = {
            0: "nom_name",
            1: "purchase_quantity",
            2: "purchase_unit_price",
            3: "articul",
            4: "barcode",
            5: "purchase_total_amount"
            
        }

        tbl = doc.add_table(0, 6)

        for r in row:
            t_row = tbl.add_row()
            for y in range(0, 6):
                t_row.cells[y].add_paragraph(str(r[column_to_property[y]]))
                
        # Replace placeholders in DOCX
        for paragraph in doc.paragraphs:
            for marker, value in data_mapping.items():
                if marker in paragraph.text:
                    paragraph.text = paragraph.text.replace(marker, value)

        filename_docx = f"{purchase['purchase_id']}.docx"
        doc.save(filename_docx)
        doc = Document(filename_docx)

        return FileResponse(filename_docx, media_type='application/pdf', filename=filename_docx)

    




@app.post('/customer/', tags=[Tags.customer])   
def insert_customer(data:InsertCustomer):
    try:
        with connection() as cur:
            cur.execute('call customer.customer_insert(%s,%s,%s)',(data.custom_name,data.custom_address,data.custom_custom_contact_info,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))    



@app.put('/customer/', tags=[Tags.customer])   
def update_customer(data:UpdateCustomer):
    try:
        with connection() as cur:
            cur.execute('call customer.update_customer(%s,%s,%s,%s)',(data.custom_id,data.custom_name,data.custom_addres,data.custom_custom_contact_info,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))  

    



@app.post('/supplier/', tags=[Tags.provider])   
def insert_supplier(data:InsertSupplier):
    try:
        with connection() as cur:
            cur.execute('call provider.supplier_insert(%s,%s,%s)',(data.supp_name,data.supp_address,data.supp_contact_info,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))    
        


@app.put('/supplier/', tags=[Tags.provider])   
def update_supplier(data:UpdateSupplier):
    try:
        with connection() as cur:
            cur.execute('call provider.update_supplier(%s,%s,%s,%s)',(data .supp_id,data.supp_name,data.supp_address,data.supp_contact_info,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))  




@app.post('/category/',tags=[Tags.catalog])
def category_insert(data: InsertCategory):
    try:
        with connection() as cur:
            cur.execute('call catalogs.category_insert(%s,%s)', (data.ctg_name, data.parent_category_id))
            return 'Category added successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.put('/category/', tags=[Tags.catalog])
def update_category(data: UpdateCategory):
    try:
        with connection() as cur:
            cur.execute('call catalogs.update_category(%s,%s, %s)', (data.ctg_id,data.ctg_name, data.parent_category_id,))
        return 'Category updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get('/categories/all', tags=[Tags.catalog])
def get_all_categories():
    result = None 
    with connection() as cur:
        cur.execute('SELECT catalogs.get_all_categories()')
        result = cur.fetchone()[0]

    return result


@app.post('/nomenclature/', tags=[Tags.catalog])
def nomenclature_insert(data: InsertNomenclature):
    try:
        with connection() as cur:
            cur.execute('call catalogs.nomenclature_insert(%s,%s)', (data.nom_name, data.nom_description))
            return 'Nomenclature added successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.put('/nomenclature/', tags=[Tags.catalog])
def update_nomenclature(data: UpdateNomenclature):
    try:
        with connection() as cur:
            cur.execute('call catalogs.update_nomenclature(%s,%s, %s)', (data.nom_id,data.nom_name, data.nom_description,))
        return 'Nomenclature updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@app.post('/product/', tags=[Tags.catalog])
def product_insert(data: ProductInsert):
    try:
        with connection() as cur:
            cur.execute('CALL catalogs.product_insert(%s,%s,%s,%s,%s,%s,%s)', 
                        (data.nom_id, data.category_id, data.prod_price, 
                         data.prod_quontity, data.articul, data.barcode, 
                         json.dumps(data.prod_attribute)))  
            return 'Product added successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


@app.put('/product/', tags=[Tags.catalog])
def update_product(data: ProductUpdate):
    try:
        with connection() as cur:
            cur.execute('call catalogs.update_product(%s,%s,%s,%s,%s,%s,%s,%s)',
                         (data.prod_id,data.nom_id, data.category_id,data.prod_price,
                          data.prod_quontity,data.articul,data.barcode,
                          json.dumps(data.prod_attribute)))
        return 'Product updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get('/all/about/product/', tags=[Tags.catalog])
def get_product_with_details():
    result = None
    with connection() as cur:
        cur.callproc('catalogs.get_products_with_all_details')
        result = cur.fetchone()[0]
    return result




@app.post('/income-outgoing/', tags=[Tags.inventory])
def insert_income_and_outgoing(data: Incoming_and_outgoingInsert):
    try:
        with connection() as cur:
           cur.execute('CALL inventory.incoming_and_outgoing_insert(%s, %s, %s, %s, %s)', 
                           (data.product_id,
                            data.quantity,
                            data.date_of_incoming_and_outgoing,
                            data.incoming_and_outgoing_type,
                            data.is_active,))
        return {"message": 'Income and outgoing added successfuly'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.put('/income-outgoing/', tags=[Tags.inventory])
def update_income_and_outgoing(data: UpdateIncoming_and_outgoing):
    try:
        with connection() as cur:
         cur.execute('CALL inventory.update_incoming_and_outgoing(%s, %s, %s, %s, %s, %s, %s)', 
                           (data.income_id,
                            data.product_id,
                            data.quantity,
                            data.date_of_incoming_and_outgoing,
                            data.incoming_and_outgoing_type,
                            data.is_active,))
        return 'Income and outgoing updated successfully'
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))