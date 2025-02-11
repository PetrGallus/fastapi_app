import uuid
from typing import Any, List, Optional
from sqlmodel import Session, select

from app.models import Item, ItemCreate, DNSRecord, DNSRecordCreate, DNSRecordUpdate, User, UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


# DNS Record CRUD Operations

def create_dns_record(db: Session, dns_record: DNSRecordCreate) -> DNSRecord:
    """
    Create a new DNS record.
    """
    db_dns_record = DNSRecord(**dns_record.dict())
    db.add(db_dns_record)
    db.commit()
    db.refresh(db_dns_record)
    return db_dns_record


def get_dns_record(db: Session, id: uuid.UUID) -> Optional[DNSRecord]:
    """
    Get a DNS record by ID.
    """
    return db.get(DNSRecord, id)


def get_multi_dns_records(db: Session, skip: int = 0, limit: int = 100) -> List[DNSRecord]:
    """
    Get multiple DNS records with pagination.
    """
    statement = select(DNSRecord).offset(skip).limit(limit)
    return db.exec(statement).all()


def update_dns_record(
    db: Session, db_dns_record: DNSRecord, dns_record_in: DNSRecordUpdate
) -> DNSRecord:
    """
    Update a DNS record.
    """
    dns_record_data = dns_record_in.dict(exclude_unset=True)
    for key, value in dns_record_data.items():
        setattr(db_dns_record, key, value)
    db.add(db_dns_record)
    db.commit()
    db.refresh(db_dns_record)
    return db_dns_record


def delete_dns_record(db: Session, id: uuid.UUID) -> None:
    """
    Delete a DNS record by ID.
    """
    dns_record = get_dns_record(db=db, id=id)
    if dns_record:
        db.delete(dns_record)
        db.commit()


# User CRUD Operations

def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item(
        title=item_in.title,
        description=item_in.description,
        owner_id=owner_id
    )
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

