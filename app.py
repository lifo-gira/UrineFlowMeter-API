from typing import List
from bson import ObjectId
from fastapi import  FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import user_collection,patient_data_collection,therapist_collection
from models import FlowTestRecord, LoginRequest, User, PatientFlowData, Therapist

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
    # Determine which collection to use based on user type
    collection = user_collection if user.type == "patient" else therapist_collection

    # Retrieve user by email
    db_user = await collection.find_one({"email": user.email})
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check password
    if db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {
        "message": "Login successful",
        "username": db_user["username"],
        "type": db_user["type"]
    }


@app.post("/register/user")
async def register(user: User):
    # Only allow type "patient"
    if user.type != "patient":
        raise HTTPException(status_code=400, detail="Only patients can register via this endpoint")

    # Check if the email is already registered
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Store user data
    await user_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": user.password,  # NOTE: Insecure, consider hashing!
        "type": user.type
    })

    return {"message": "Patient registered successfully"}

@app.post("/register/therapist")
async def register_therapist(therapist: Therapist):
    # Check if the email is already registered
    existing_user = await therapist_collection.find_one({"email": therapist.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Insert the therapist data
    await therapist_collection.insert_one(therapist.dict())

    return {"message": "Therapist registered successfully"}

@app.post("/patient-data")
async def post_patient_data(patient_data: PatientFlowData):
    # Check if the email is already used in the collection
    existing_patient = await patient_data_collection.find_one({"email": patient_data.email})
    
    if existing_patient:
        raise HTTPException(status_code=400, detail="Email already registered with a patient")
    
    # Insert the patient data into the database
    result = await patient_data_collection.insert_one(patient_data.dict())
    
    return {"message": "Patient data successfully added"}


@app.get("/patients/{therapist_email}", response_model=List[PatientFlowData])
async def get_patients_by_therapist(therapist_email: str):
    # Query for patients by therapist_assigned (awaiting cursor)
    patients_cursor = patient_data_collection.find({"therapist_assigned": therapist_email})
    # Await the cursor and convert to a list
    patients_list = await patients_cursor.to_list(length=None)
    return patients_list

@app.get("/getTherapist/{email}", response_model=User)
async def get_therapist_by_email(email: str):
    therapist = await therapist_collection.find_one({"email": email, "type": "therapist"})
    
    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist not found")

    return User(**therapist)


@app.get("/getFullTherapist/{email}", response_model=Therapist)
async def get_full_therapist(email: str):
    therapist = await therapist_collection.find_one({"email": email, "type": "therapist"})

    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist not found")

    therapist.pop("_id", None)  # remove MongoDB's ObjectId if present
    return Therapist(**therapist)

@app.get("/patient-data", response_model=PatientFlowData)
async def get_patient_data(email: str):
    patient = await patient_data_collection.find_one({"email": email})
    if patient:
        return PatientFlowData(**patient)  # Return a single object, not a list
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
    
@app.post("/upload-exercise/")
async def upload_exercise(email: str, first_name: str, last_name: str, flowTestRecords: List[FlowTestRecord]):
    # Find the patient asynchronously
    patient = await patient_data_collection.find_one({"email": email, "first_name": first_name, "last_name": last_name})

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get existing exercise records
    existing_flowTestRecords_records = patient.get("flowTestRecords", [])

    for new_record in flowTestRecords:
        new_record_dict = new_record.dict()  # Convert Pydantic model to dict
        
        # Directly stack the new data without checking for matches
        existing_flowTestRecords_records.append(new_record_dict)

    # Update the database with the stacked records
    await patient_data_collection.update_one(
        {"email": email, "first_name": first_name, "last_name": last_name},
        {"$set": {"flowTestRecords": existing_flowTestRecords_records}}
    )

    return [
    {
        "message": "Record updated successfully"
    }
]
