from fastapi import FastAPI,HTTPException
from src.models import InsertCategory
app = FastAPI()
from lib.connection import connection


@app.post('/insert/category')   
def InsertCategory(data:InsertCategory):
    try:
        with connection() as cur:
            cur.execute('call catalogs.category_insert(%s,%s)',(data.ctg_name,data.parent_category,))
            return 'Ok'
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))