from typing import List
from bson import ObjectId
from fastapi import  FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import user_collection,patient_data_collection
from models import LoginRequest, User, PatientFlowData

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Message": "use '/docs' endpoint to find all the api related docs "}

@app.post("/login")
async def login(user: LoginRequest):
    # Retrieve user from MongoDB using email
    db_user = await user_collection.find_one({"email": user.email})

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate password
    if db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {
        "message": "Login successful",
        "username": db_user["username"],
        "type": db_user["type"]  # Added type field
    }

@app.post("/register")
async def register(user: User):
    # Check if the email is already registered
    existing_user = await user_collection.find_one({"email": user.email})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Store user data in MongoDB with plain text password
    await user_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": user.password,  # Store plain text password
        "type": user.type  # Added type field
    })
    
    return {"message": "User registered successfully"}

@app.post("/patient-data")
async def post_patient_data(patient_data: PatientFlowData):
    # Check if the email is already used in the collection
    existing_patient = await patient_data_collection.find_one({"email": patient_data.email})
    
    if existing_patient:
        raise HTTPException(status_code=400, detail="Email already registered with a patient")
    
    # Insert the patient data into the database
    result = await patient_data_collection.insert_one(patient_data.dict())
    
    return {"message": "Patient data successfully added"}