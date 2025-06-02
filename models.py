from pydantic import BaseModel, EmailStr
from typing import Literal, Optional, List, Dict

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    type: Literal["patient", "therapist"]

    class Config:
        schema_extra = {
            "example": {
                "type": "patient",
                "email": "APM@gmail.com",
                "password": "21345"
            }
        }
    

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    type: Literal["patient","therapist"]

    class Config:
        schema_extra = {
            "example": {
                "username": "APM",
                "email": "APM@gmail.com",
                "password": "21345",
                "type": "patient"
            }
        }

class Therapist(BaseModel):
    username: str
    email: EmailStr
    password: str
    type: Literal["therapist"]
    first_name: str
    last_name: str
    dob: Optional[str] = None
    blood_grp: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "therapist123",
                "email": "therapist@example.com",
                "password": "securepassword123",
                "type": "therapist",
                "first_name": "Jane",
                "last_name": "Doe",
                "dob": "1985-03-25",
                "blood_grp": "A+",
                "height": 165,
                "weight": 60,
                "gender": "female",
                "phone_number": "9876543210"
            }
        }

class FlowTestRecord(BaseModel):
    device_name: str
    date: str
    maximum_flow_rate: float  # Max flow rate (replaces peak_flow_rate)
    average_flow_rate: float  # Average flow rate
    voided_volume: float      # Total urine volume voided in ml
    flow_time: float          # Duration of flow in seconds
    voiding_time: float       # Time taken to start voiding
    peak_flow_rate: float     # Time of peak flow
    flow_pattern: str         # e.g., normal, obstructed, intermittent
    raw_values: List[float]   # Live graph data - volume or rate vs time

class PatientFlowData(BaseModel):
    user_id: str
    therapist_assigned: str
    username: Optional[str] = None
    first_name: str
    last_name: str
    email: EmailStr
    dob: Optional[str] = None
    blood_grp: Optional[str] = None
    flag: int
    height: Optional[int] = None
    weight: Optional[int] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    flowTestRecords: Optional[List[FlowTestRecord]] = None

    class Config:
        schema_extra = {
            "example": {
                "user_id": "12345",
                "therapist_assigned": "therapist@gmail.com",
                "username": "APM",
                "first_name": "Anirudh",
                "last_name": "Menon",
                "email": "APM@gmail.com",
                "dob": "22-08-2024",
                "blood_grp": "O+",
                "phone_number": "28917221",
                "height": 176,
                "weight": 70,
                "gender": "male",
                "flag": 1,
                "flowTestRecords": [
                    {
                        "device_name": "UrineFlowMeter",
                        "date": "2025-05-22",
                        "maximum_flow_rate": 310.5,
                        "average_flow_rate": 16.8,
                        "voided_volume": 11.4,
                        "flow_time": 27.2,
                        "voiding_time": 11.4,
                        "peak_flow_rate": 27.2,
                        "flow_pattern": "normal",
                        "raw_values": [0, 15, 32, 55, 74, 88, 102, 110, 120, 125, 130, 131, 131, 131],
                    }
                ]
            }
        }