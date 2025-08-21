from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine & session setup
DATABASE_URL = "mysql+pymysql://root:your_password@localhost/team_agents"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ Run table creation when executed directly
if __name__ == "__main__":
    from apps.server import models  # make sure this imports your models
    Base.metadata.create_all(bind=engine)
