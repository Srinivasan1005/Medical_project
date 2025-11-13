from fastapi import FastAPI,Form,Depends,HTTPException
from schemas import StudentValidation,Location,StudentResponse,StudentUpdate
from pydantic import EmailStr
from database import engine,Base,Sesssionlocal
import models
from models import Students
from sqlalchemy.orm import Session
from typing import Annotated,List
from auth import hash_password,verify_password

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

#dependence
def get_db():
    db=Sesssionlocal()
    try:
        yield db     
    finally:
        db.close()
        
db_dependence= Annotated[Session,Depends(get_db)]

        
@app.get('/')
def Home():
    return {
        "Welcome to home page (FAST_API project)"
    }
    
@app.post('/get')
def forcheck(valid: Location):
    return {
        "Json":"format",
        "location1":valid.location1,
        "id":valid.details.id,
        "name":valid.details.name,
        "dept":valid.details.dept,
        "fees":valid.details.fees,
        "loaction2":valid.location2,
    }
    
@app.post('/form')
def formdetails(uname:str=Form(..., 
                min_length=3,max_length=20,
                pattern="^[a-zA-Z]+$",
                description="Username must contain only letters"),
                email: EmailStr=Form(...,)):
    return {
        "json":"format",
        "uname":uname,
        "email":email,
    }


# database posting details   
@app.post('/db_send', response_model=List[StudentResponse])
def databasesend(stu: StudentValidation, db: db_dependence):
    try:
        db_req=models.Students(id=stu.id,name=stu.name,dept=stu.dept,fees=stu.fees)
        db.add(db_req)
        db.commit()
        db.refresh(db_req)
        return db_req
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=f"Error{e}")
    
    
# 🟡 READ (Get All)
@app.get("/students/", response_model=List[StudentResponse])
def read_students(db: db_dependence):
    students = db.query(models.Students).all()
    return students


# 🟣 READ only on data (Get by ID)
@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: db_dependence):
    student=db.query(models.Students).filter(models.Students.id==student_id).first()
    if not student:
        raise HTTPException(status_code=404,detail="Student not found")
    return student


# 🟠 UPDATE
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, stu: StudentUpdate, db: db_dependence):
    student=db.query(models.Students).filter(models.Students.id==student_id).first()
    if not student:
        raise HTTPException(status_code=404,detail="Student not found")
    student.name=stu.name
    student.dept=stu.dept
    student.fees=stu.fees
    db.commit()
    db.refresh(student)
    return student

# 🔴 DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: db_dependence):
    student = db.query(models.Students).filter(models.Students.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found ❌")
    db.delete(student)
    db.commit()
    return {"message": f"Student {student.name} deleted successfully ✅"}
        

@app.get("/hash_test/{password}")
def hash_tester(password: str):
    hashed = hash_password(password)
    return {
        "original": password,
        "hashed": hashed,
        "verify": verify_password(password, hashed)
    }