from flask import Flask
from app.db.base import Base
from app.db.session import engine
from app.routes.user_routes import user_bp
from app.routes.chats import chat_bp
from app.routes.memory import memory_bp

def create_app():
    app = Flask(__name__)
    Base.metadata.create_all(bind=engine)
    app.register_blueprint(user_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(memory_bp)
    return app
