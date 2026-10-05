import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, String, Text, JSON, DateTime, ForeignKey, Numeric, Integer, Float, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

def now():return datetime.now(timezone.utc)
class Base(DeclarativeBase):pass
class ExtractionRun(Base):
    __tablename__='extraction_runs'
    id:Mapped[str]=mapped_column(String(36),primary_key=True)
    source_sha256:Mapped[str]=mapped_column(String(64),index=True)
    status:Mapped[str]=mapped_column(String(20))
    filename:Mapped[str]=mapped_column(String(200))
    source_path:Mapped[str]=mapped_column(Text)
    created:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    completed:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    result:Mapped[dict|None]=mapped_column(JSON,nullable=True)
    provenance:Mapped[dict|None]=mapped_column(JSON,nullable=True)
    raw_response:Mapped[dict|None]=mapped_column(JSON,nullable=True)
    error:Mapped[str|None]=mapped_column(Text,nullable=True)
class Review(Base):
    __tablename__='review_revisions'
    id:Mapped[str]=mapped_column(String(36),primary_key=True)
    run_id:Mapped[str]=mapped_column(ForeignKey('extraction_runs.id'),index=True)
    reviewer:Mapped[str]=mapped_column(String(200))
    result:Mapped[dict]=mapped_column(JSON)
    created:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Listing(Base):
    __tablename__='listings'
    id:Mapped[str]=mapped_column(String(36),primary_key=True)
    review_id:Mapped[str]=mapped_column(ForeignKey('review_revisions.id'))
    title:Mapped[str]=mapped_column(String(160))
    price:Mapped[float]=mapped_column(Numeric(14,2))
    latitude:Mapped[float]=mapped_column(Float)
    longitude:Mapped[float]=mapped_column(Float)
    status:Mapped[str]=mapped_column(String(20),default='Active')
    data:Mapped[dict]=mapped_column(JSON)
class Evaluation(Base):
    __tablename__='evaluations'
    id:Mapped[str]=mapped_column(String(36),primary_key=True)
    run_id:Mapped[str]=mapped_column(ForeignKey('extraction_runs.id'),index=True)
    test_set_hash:Mapped[str]=mapped_column(String(64))
    key_hash:Mapped[str]=mapped_column(String(64))
    metrics:Mapped[dict]=mapped_column(JSON)
    created:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
_engine=None
Session=None
def initialize():
    global _engine,Session
    url=os.environ.get('DATABASE_URL')
    if not url:raise RuntimeError('DATABASE_URL is required; no implicit in-memory database')
    _engine=create_engine(url,pool_pre_ping=True)
    Session=sessionmaker(_engine,expire_on_commit=False)
    # Development bootstrap only; use schema.sql / versioned migrations in production.
    if os.getenv('DB_AUTO_CREATE')=='1':Base.metadata.create_all(_engine)
    return _engine
