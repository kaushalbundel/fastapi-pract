from pydantic import BaseModel


# Note: There will be two classes one for the read only use cases such get, and another for write use cases.

# Class for read only usecase
class Products(BaseModel):
        id: int
        name:  str
        description: str
        price: float
        quantity: int

# class for write use case like put, post etc.
class ProductsCreate(BaseModel):
        name: str
        description: str
        price: float
        quantity: int
    
    
