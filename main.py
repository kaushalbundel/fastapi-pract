from fastapi import FastAPI, HTTPException
from models import Products
app = FastAPI()

# this is a simple way. The actual way is to store this information in database
products = [
Products(id=1, name="Mobile Phone", description="An expensive mobile phone", price= 15999.0, quantity=10), 
Products(id=2, name="Laptop", description="Gaming Laptop", price= 50000.0, quantity=10), 
Products(id=3, name="Vaccum Cleaner", description="Eureka Forbs", price= 12999.0, quantity=1), 
Products(id=4, name="Refrigerator", description="Double Door", price= 20999.0, quantity=20), 
]

@app.get("/products")
def get_all_products():
    '''
    Get all products in the database
    '''
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    '''
   Get a single product by sending an product id 
    '''
    # return [product for product in products if product.id == id ]
    # This method will work but if has a limitation
    # It returns an list object but by definition it should recieve an single product information. It also sends just an empty list when an out of bound id is mentioned
    for product in products:
        if product.id == id:
            return product

    raise HTTPException(404, f"The product with id: {id} not found")


@app.post("/product")
def add_product(product: Products):
    '''
    Add a single product
    '''
    # return products.append(product) 
    # the above line will just append the product in the product list, what is wanted is also to give an indication that the product has been uploaded
    for items in products:
        if items.id == product.id:
            raise HTTPException(400, f"The id: {product.id} is already present.")
    products.append(product)
    return product

# updating a product on the basis of an id

@app.put("/product/{id}")
def update_product_by_id(id: int, product: Products):
    '''
    Updates the entire product information on the basis of an id
    '''
    for id_counter, existing_product in enumerate(products):
        if existing_product.id == id:
            products[id_counter] = product

            # There are two sources of truth here, one is the url and the other is the product that we are updating
            # Out of these two which id do we take as a final source of truth
            # Assumption: Taking url id as the single source of truth
            product.id = id
            return product
    raise HTTPException(404, f"The id: {id} does not exists, or the id does not match.")

    # The above code is giving me unexpected error
    # When I add a product that does not have the same id as the id in the url then also the update operation is being performed

