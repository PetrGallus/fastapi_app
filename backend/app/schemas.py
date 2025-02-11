from pydantic import BaseModel, Field
import uuid


# Base Schema for DNS Record
class DNSRecordBase(BaseModel):
    name: str = Field(..., description="DNS record name")
    record_type: str = Field(..., description="DNS record type (e.g., A, CNAME, MX)")
    value: str = Field(..., description="DNS record value")


# Schema for Creating a DNS Record (Request Body)
class DNSRecordCreate(DNSRecordBase):
    pass


# Schema for Publicly Exposing a DNS Record (Response Model)
class DNSRecordPublic(DNSRecordBase):
    id: uuid.UUID = Field(..., description="Unique ID for the DNS record")

    class Config:
        orm_mode = True


# Schema for Deletion Response
class Message(BaseModel):
    message: str
