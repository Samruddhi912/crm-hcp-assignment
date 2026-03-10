from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Added +pymysql explicitly and ensured the port is standard for XAMPP
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/crm_hcp_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True  # This helps reset "stale" connections
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()