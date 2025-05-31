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
    type: Literal["patient", "therapist"]

    class Config:
        schema_extra = {
            "example": {
                "username": "APM",
                "email": "APM@gmail.com",
                "password": "21345",
                "type": "patient"
            }
        }

class FlowTestRecord(BaseModel):
    device_name: str
    date_of_test: str
    total_voided_volume_ml: float  # Total urine volume voided in ml
    peak_flow_rate_ml_s: float  # Peak urine flow rate in ml/sec
    average_flow_rate_ml_s: float  # Average flow rate in ml/sec
    voiding_time_sec: float  # Total time taken to void in seconds
    flow_pattern: str  # Pattern type e.g. normal, intermittent, obstructed
    raw_values: List[float]  # Live graph data - weight or volume vs time

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
                        "total_voided_volume_ml": 310.5,
                        "peak_flow_rate_ml_s": 16.8,
                        "average_flow_rate_ml_s": 11.4,
                        "voiding_time_sec": 27.2,
                        "flow_pattern": "normal",
                        "raw_values": [0, 15, 32, 55, 74, 88, 102, 110, 120, 125, 130, 131, 131, 131],
                        "notes": "Flow rate and pattern within normal range."
                    }
                ]
            }
        }