from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cấu hình kết nối PostgreSQL
user = "postgres"
password = "1"
host = "localhost"
port = "5432"
database = "postgres"
connection_str = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# Tạo engine
engine = create_engine(connection_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Hàm lấy session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hàm khởi tạo database
def init_db():
    from src.model.user import User
    from src.model.rider import Rider
    from src.model.booking import Booking
    from src.model.history import History

    Base.metadata.create_all(bind=engine)
