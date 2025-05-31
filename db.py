from motor import motor_asyncio

# MongoDB setup
client = motor_asyncio.AsyncIOMotorClient("mongodb+srv://lifogira:lifogira@cluster0.5b1k67b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database = client.Main
user_collection = database.User 
therapist_collection = database.Therapist
patient_data_collection = database.PatientData 