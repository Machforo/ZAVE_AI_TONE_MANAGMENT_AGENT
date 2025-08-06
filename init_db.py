from sqlalchemy import create_engine
from app.models.user import Base as UserBase
from app.models.conversation import Base as ConvBase
from app.models.message import Base as MsgBase
from app.models.memory import Base as MemBase

DATABASE_URL = "sqlite:///tone_ai.db"

def init_db():
    engine = create_engine(DATABASE_URL)
    UserBase.metadata.create_all(engine)
    ConvBase.metadata.create_all(engine)
    MsgBase.metadata.create_all(engine)
    MemBase.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
