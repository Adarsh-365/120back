from pydantic import BaseModel

class Data(BaseModel):
    first_name: str
    middle_name: str
    sirname: str
    mob_no: str
    city : str