from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
import uuid

router = APIRouter()


@router.get("/", response_model=list[schemas.DNSRecordPublic])
def read_dns_records(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve DNS records.
    """
    dns_records = crud.dns_record.get_multi(db, skip=skip, limit=limit)
    return dns_records


@router.post("/", response_model=schemas.DNSRecordPublic)
def create_dns_record(
    *,
    db: Session = Depends(deps.get_db),
    dns_record_in: schemas.DNSRecordCreate
):
    """
    Create new DNS record.
    """
    dns_record = crud.dns_record.create(db=db, obj_in=dns_record_in)
    return dns_record


@router.delete("/{record_id}", response_model=schemas.Message)
def delete_dns_record(
    *,
    db: Session = Depends(deps.get_db),
    record_id: uuid.UUID
):
    """
    Delete DNS record.
    """
    dns_record = crud.dns_record.get(db=db, id=record_id)
    if not dns_record:
        raise HTTPException(status_code=404, detail="DNS record not found")
    crud.dns_record.remove(db=db, id=record_id)
    return {"message": "DNS record deleted successfully"}
