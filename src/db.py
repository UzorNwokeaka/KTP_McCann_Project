import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local_backpack.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class JobSubmission(Base):
    __tablename__ = "job_submissions"

    id = Column(Integer, primary_key=True, index=True)
    job_reference = Column(String(100), nullable=False)
    asset_id = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    job_type = Column(String(100), nullable=False)

    arrival_time = Column(String(20), nullable=False)
    departure_time = Column(String(20), nullable=False)
    hours_on_site = Column(Float, nullable=False)
    number_of_operatives = Column(Integer, nullable=False)

    vehicle_type = Column(String(100), nullable=False)
    tool_type = Column(String(100), nullable=False)
    tool_hours = Column(Float, nullable=False)

    lamp_qty = Column(Integer, nullable=False)
    cable_qty = Column(Integer, nullable=False)
    fuse_qty = Column(Integer, nullable=False)

    work_completed = Column(Text, nullable=False)

    labour_cost = Column(Float, nullable=False)
    vehicle_cost = Column(Float, nullable=False)
    tool_cost = Column(Float, nullable=False)
    material_cost = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)

    qs_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_reference = Column(String(100), nullable=False)
    action_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_job_submission(job_data: dict):
    session = SessionLocal()

    try:
        job = JobSubmission(**job_data)
        session.add(job)

        audit = AuditLog(
            job_reference=job_data["job_reference"],
            action_type="JOB_SUBMITTED",
            description=f"Job {job_data['job_reference']} submitted with total estimated cost £{job_data['total_cost']:.2f}",
        )
        session.add(audit)

        session.commit()
        return job.id

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()
