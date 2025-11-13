from pydantic import BaseModel,Field,ConfigDict


class StudentValidation(BaseModel):
    id: int = Field(..., description="Student ID") 
    name: str = Field(..., min_length=4, max_length=30, pattern="^[A-Za-z]+$")
    dept: str = Field(..., min_length=3, max_length=30, pattern="^[A-Za-z]+$")
    fees: float = Field(..., gt=20, lt=500)
    
    
class StudentResponse(StudentValidation):
   
    model_config = ConfigDict(from_attributes=True)

class Location(BaseModel):
    location1: str = Field(..., min_length=4, max_length=30, pattern="^[A-Za-z]+$")
    details: StudentValidation
    location2: str = Field(..., min_length=4, max_length=30, pattern="^[A-Za-z]+$")

class StudentUpdate(StudentValidation):
    pass