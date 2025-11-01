from fastapi import FastAPI, HTTPException, Depends
from models import Products
from database import SessionLocal, engine
import database_model
from sqlalchemy.orm import Session

app = FastAPI()

# creating a table
database_model.BASE.metadata.create_all(bind = engine )

# this is a simple way. The actual way is to store this information in database
products = [
Products(id=1, name="Mobile Phone", description="An expensive mobile phone", price= 15999.0, quantity=10), 
Products(id=2, name="Laptop", description="Gaming Laptop", price= 50000.0, quantity=10), 
Products(id=3, name="Vaccum Cleaner", description="Eureka Forbs", price= 12999.0, quantity=1), 
Products(id=4, name="Refrigerator", description="Double Door", price= 20999.0, quantity=20), 
]


# populating the product values as defined here in the database
# in actual situation this process is redundant as the records will be added in the sql directly or through some other route
def init_db():
    '''
   Check if the table is empty and adds the products in the product list.  
    '''
    # starting the session
    db = SessionLocal()

    is_table_empty = True if db.query(database_model.Products) == 0 else False

    # we need to map the product(pydantic)-database with the product that is related to sqlalchemy, since we are trying to link the products data above to populate the database table
    if is_table_empty:
        for product in products:
            db.add(instance=database_model.Products(**product.model_dump())) 
    
    # commiting manually
    db.commit()

init_db()

# Creating dependency injection for the database

# creating the dependency
# why yield is used and not anything else because yield creates a generator that wraps the code where this dependency will be executed
'''
A summary as to how this is used:

Here's the exact flow:

A request comes in for your endpoint.

FastAPI sees Depends(get_db) and calls the get_db function.

get_db runs up to the yield line. It creates the db session.

yield db pauses the get_db function and "injects" the db session into your endpoint.

Your endpoint code (e.g., db.query(...)) runs and finishes.

FastAPI resumes the get_db function after the yield.

The finally block is executed, guaranteeing that db.close() is called.
'''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# showing all products
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    '''
    Get all products in the database
    '''
    db_products = db.query(database_model.Products).all()
    return db_products


# showing specific product using an id
@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    '''
   Get a single product by sending an product id 
    '''
    # return [product for product in products if product.id == id ]
    # This method will work but if has a limitation
    # It returns an list object but by definition it should recieve an single product information. It also sends just an empty list when an out of bound id is mentioned
    # for product in products:
    #     if product.id == id:
    #         return product
    db_product = db.query(database_model.Products).filter(database_model.Products.id == id).first() 

    if db_product:
        return db_product

    raise HTTPException(404, f"The product with id: {id} not found")

# appending a product
@app.post("/product")
def add_product(product: Products, db: Session = Depends(get_db)):
    '''
    Add a single product
    '''
    # return products.append(product) 
    # the above line will just append the product in the product list, what is wanted is also to give an indication that the product has been uploaded
    # for items in products:
    #     if items.id == product.id:
    #         raise HTTPException(400, f"The id: {product.id} is already present.")
    # products.append(product)
    try: 
        db.add(database_model.Products(**product.model_dump()))
        db.commit()
        return product
    except:
        HTTPException(404, "The product is not inserted")

# updating a product on the basis of an id
@app.put("/product/{id}")
def update_product_by_id(id: int, product: Products, db: Session = Depends(get_db)):
    '''
    Updates the entire product information on the basis of an id
    '''
    # for id_counter, existing_product in enumerate(products):
    #     if existing_product.id == id:
    #         products[id_counter] = product

    #         # There are two sources of truth here, one is the url and the other is the product that we are updating
    #         # Out of these two which id do we take as a final source of truth
    #         # Assumption: Taking url id as the single source of truth
    #         product.id = id
    #         return product

    db_product = db.query(database_model.Products).filter(database_model.Products.id == id).first()
    if db_product:
        db_product.description = product.description
        db_product.name =  product.name
        db_product.price = product.price
        db_product.quantity = product.quantity

        db.commit()
        return f"The product is updated."

    raise HTTPException(404, f"The id: {id} does not exists, or the id does not match.")


# Delete request
@app.delete("/product/{id}")
def delete_product_by_id(id: int):
    '''
    deletes product on the basis of the id provided
    '''
    for index, existing_product in enumerate(products):
        if existing_product.id == id:
            products.pop(index)
            return f"The product item {products[index]} is successfully removed"
    
    # In case product is not found
    raise HTTPException(404, f"No product with product id {id} found.")


