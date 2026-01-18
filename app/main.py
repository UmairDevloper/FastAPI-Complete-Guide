from fastapi import FastAPI, HTTPException, Query, Path, Depends, Request
from service.product import get_all_products, add_product_to_store, remove_products, change_product
from schema.products import Product, ProductUpdate
from uuid import uuid4, UUID
from datetime import datetime
import os
from fastapi.responses import JSONResponse
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()

#------------------------------------------------
# Routing                                       |
#------------------------------------------------
# # Static Route
@app.get("/", response_model=dict)
def root(dep=Depends(get_all_products)):
    DATA_PATH = os.getenv("BASE_URL")
    return  JSONResponse(
        status_code=200,
        content={
            "message":"Welcome to FastAPI.",
            # "dependency": dep,
            "data": DATA_PATH
        }
    )


# #   Dynamic Route
# @app.get("/products/{id}")
# def get_product(id:int):
#     products = ["Laptop", "Monitor", "Headphone", "Speaker"]
#     return products[id]


#-----------------
# Getting By id  |
#-----------------

@app.get("/products/{id}", response_model=dict)
def get_product_by_id(id: str):
    products = get_all_products()
    for product in products:
        if product["id"] == id:
            return product
    raise HTTPException(
                status_code=404,
                detail="Record not found."
            )


#---------------------
# Validation         |
#---------------------

# Create product Route
@app.post("/product", status_code=201)
def create_product(product: Product):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat() + "Z"

    try:
        add_product_to_store(product_dict)
    except ValueError as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
        )

    return product_dict


# Delete Product Route
@app.delete("/products/{product_id}")
def delete_product(product_id: UUID = Path(..., description="ID required as UUID")):
    try:
        res = remove_products(product_id)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# Update Product Route
@app.patch("/products/{product_id}")
def update_product(product_id: UUID = Path(..., description="Product ID UUID"), payload: ProductUpdate = ...):
    try:
        update_product = change_product(str(product_id), payload.model_dump( exclude_unset=True))
        return update_product
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )




#--------------------
# Middleware        |
#-------------------

@app.middleware("http")
async def lifecycle(request:Request, call_next):
    print("Before Request.")
    response = await call_next(request)
    print("After Request.")
    return response


