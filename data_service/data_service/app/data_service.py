import os
import hashlib
import json
from datetime import datetime
from typing import List, Optional
import time

# --- FastAPI and Pydantic Imports ---
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field

# --- Database (SQLAlchemy) Imports ---
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base

# --- Cryptography Imports ---
from cryptography.fernet import Fernet

# --- Blockchain (Web3.py) Imports ---
from web3 import Web3

# ==============================================================================
# 1. CONFIGURATION & INITIALIZATION
# ==============================================================================

# --- Database Setup (PostgreSQL) ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("FATAL: DATABASE_URL environment variable not set.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Smart Tourist DBMS v4.0 (Production - Web3)",
    description="Manages a relational PostgreSQL database with data classification.",
    version="4.0.0"
)

# --- Encryption Setup ---
KEY_FILE = "secret.key"
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
with open(KEY_FILE, "rb") as key_file:
    SECRET_KEY = key_file.read()
cipher_suite = Fernet(SECRET_KEY)

# --- Blockchain Connection (THE DEFINITIVE WEB3.PY FIX) ---
# Connect directly to the Ganache instance running on the host machine
GANACHE_URL = "http://host.docker.internal:8545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Wait for the connection to be established
retries = 10
# CRITICAL FIX: The method name is 'isConnected' (camelCase) in web3.py v5
while not w3.isConnected() and retries > 0:
    print("Waiting for connection to Ganache...")
    time.sleep(2)
    retries -= 1
# CRITICAL FIX: Use the correct method name here as well
if not w3.isConnected():
    raise ConnectionError("FATAL: Could not connect to Ganache RPC.")
print("Successfully connected to Ganache.")

# Get contract address and account from environment
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
if not CONTRACT_ADDRESS:
    raise RuntimeError("FATAL: CONTRACT_ADDRESS environment variable not set.")
# In Ganache, the first account is typically the default deployer/user
deployer_account = w3.eth.accounts[0]

# Load the contract ABI from the mounted volume
ABI_PATH = "/app/blockchain/build/contracts/TouristRegistry.json"
if not os.path.exists(ABI_PATH):
    raise FileNotFoundError(f"ABI file not found at {ABI_PATH}.")
with open(ABI_PATH) as f:
    contract_abi = json.load(f)["abi"]

# Create the contract instance
registry_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)


# ==============================================================================
# 2. DATABASE MODELS (Unchanged)
# ==============================================================================
class TouristDB(Base):
    __tablename__ = "tourists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="Active")
    registration_date = Column(DateTime, default=datetime.utcnow)
    encrypted_passport = Column(Text, nullable=False)
    itineraries = relationship("ItineraryDB", back_populates="tourist", cascade="all, delete-orphan")
    emergency_contacts = relationship("EmergencyContactDB", back_populates="tourist", cascade="all, delete-orphan")
    blockchain_log = relationship("BlockchainLogDB", back_populates="tourist", uselist=False, cascade="all, delete-orphan")

class ItineraryDB(Base):
    __tablename__ = "itineraries"
    id = Column(Integer, primary_key=True, index=True)
    day_number = Column(Integer, nullable=False)
    encrypted_plan = Column(Text, nullable=False)
    tourist_id = Column(Integer, ForeignKey("tourists.id"))
    tourist = relationship("TouristDB", back_populates="itineraries")

class EmergencyContactDB(Base):
    __tablename__ = "emergency_contacts"
    id = Column(Integer, primary_key=True, index=True)
    encrypted_name = Column(Text, nullable=False)
    encrypted_phone = Column(Text, nullable=False)
    encrypted_relation = Column(Text, nullable=False)
    tourist_id = Column(Integer, ForeignKey("tourists.id"))
    tourist = relationship("TouristDB", back_populates="emergency_contacts")

class BlockchainLogDB(Base):
    __tablename__ = "blockchain_logs"
    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String, unique=True, nullable=False)
    data_hash = Column(String, unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tourist_id = Column(Integer, ForeignKey("tourists.id"))
    tourist = relationship("TouristDB", back_populates="blockchain_log")

Base.metadata.create_all(bind=engine)

# ==============================================================================
# 3. API MODELS (Unchanged)
# ==============================================================================
class ItineraryItemCreate(BaseModel):
    day_number: int = Field(..., example=1)
    plan: str = Field(..., example="Visit Museum of History")

class EmergencyContactCreate(BaseModel):
    name: str = Field(..., example="Jane Doe")
    phone: str = Field(..., example="555-1234")
    relation: str = Field(..., example="Spouse")

class TouristCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    passport_number: str = Field(..., example="A12345678")
    itinerary: List[ItineraryItemCreate]
    emergency_contacts: List[EmergencyContactCreate]

class ItineraryItemResponse(ItineraryItemCreate):
    id: int
    class Config: orm_mode = True

class EmergencyContactResponse(EmergencyContactCreate):
    id: int
    class Config: orm_mode = True

class BlockchainLogResponse(BaseModel):
    tx_hash: str
    data_hash: str
    timestamp: datetime
    class Config: orm_mode = True

class TouristResponse(BaseModel):
    id: int; name: str; status: str; registration_date: datetime; passport_number: str
    itinerary: List[ItineraryItemResponse]
    emergency_contacts: List[EmergencyContactResponse]
    blockchain_log: BlockchainLogResponse
    class Config: orm_mode = True

# ==============================================================================
# 4. HELPER FUNCTIONS (Blockchain function updated)
# ==============================================================================
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def encrypt_data(data: str) -> str: return cipher_suite.encrypt(data.encode()).decode()
def decrypt_data(data: str) -> str: return cipher_suite.decrypt(data.encode()).decode()

def anchor_data_on_blockchain(data_payload: dict) -> (str, str):
    data_string = json.dumps(data_payload, sort_keys=True)
    data_hash_hex = hashlib.sha256(data_string.encode()).hexdigest()
    data_hash_bytes = bytes.fromhex(data_hash_hex)
    try:
        tx_hash = registry_contract.functions.registerHash(data_hash_bytes).transact({'from': deployer_account})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 0:
            raise Exception("Transaction failed on-chain")
        return tx_hash.hex(), data_hash_hex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blockchain transaction failed: {e}")

# ==============================================================================
# 5. API ENDPOINTS (Unchanged)
# ==============================================================================
@app.post("/tourists/", response_model=TouristResponse, status_code=201)
def register_tourist(tourist_data: TouristCreate, db: Session = Depends(get_db)):
    anchor_payload = {"name": tourist_data.name, "passport": tourist_data.passport_number, "timestamp": datetime.utcnow().isoformat()}
    tx_hash, data_hash = anchor_data_on_blockchain(anchor_payload)
    db_tourist = TouristDB(name=tourist_data.name, encrypted_passport=encrypt_data(tourist_data.passport_number))
    db_tourist.itineraries = [ItineraryDB(day_number=i.day_number, encrypted_plan=encrypt_data(i.plan)) for i in tourist_data.itinerary]
    db_tourist.emergency_contacts = [EmergencyContactDB(encrypted_name=encrypt_data(c.name), encrypted_phone=encrypt_data(c.phone), encrypted_relation=encrypt_data(c.relation)) for c in tourist_data.emergency_contacts]
    db_tourist.blockchain_log = BlockchainLogDB(tx_hash=tx_hash, data_hash=data_hash)
    db.add(db_tourist)
    db.commit()
    db.refresh(db_tourist)
    return TouristResponse(
        id=db_tourist.id, name=db_tourist.name, status=db_tourist.status, registration_date=db_tourist.registration_date,
        passport_number=decrypt_data(db_tourist.encrypted_passport),
        itinerary=[ItineraryItemResponse(id=i.id, day_number=i.day_number, plan=decrypt_data(i.encrypted_plan)) for i in db_tourist.itineraries],
        emergency_contacts=[EmergencyContactResponse(id=c.id, name=decrypt_data(c.encrypted_name), phone=decrypt_data(c.encrypted_phone), relation=decrypt_data(c.encrypted_relation)) for c in db_tourist.emergency_contacts],
        blockchain_log=db_tourist.blockchain_log
    )

@app.get("/tourists/{tourist_id}", response_model=TouristResponse)
def get_tourist_details(tourist_id: int, db: Session = Depends(get_db)):
    db_tourist = db.query(TouristDB).filter(TouristDB.id == tourist_id).first()
    if db_tourist is None:
        raise HTTPException(status_code=404, detail="Tourist not found")
    return TouristResponse(
        id=db_tourist.id, name=db_tourist.name, status=db_tourist.status, registration_date=db_tourist.registration_date,
        passport_number=decrypt_data(db_tourist.encrypted_passport),
        itinerary=[ItineraryItemResponse(id=i.id, day_number=i.day_number, plan=decrypt_data(i.encrypted_plan)) for i in db_tourist.itineraries],
        emergency_contacts=[EmergencyContactResponse(id=c.id, name=decrypt_data(c.encrypted_name), phone=decrypt_data(c.encrypted_phone), relation=decrypt_data(c.encrypted_relation)) for c in db_tourist.emergency_contacts],
        blockchain_log=db_tourist.blockchain_log
    )

