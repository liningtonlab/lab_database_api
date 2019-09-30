from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from api.common.sql_models import (Base, Diver, DiveSite, Extract, Fraction,
                                   FractionScreenPlate, Isolate, IsolateStock,
                                   Library, Media, MediaRecipe, Permit, Sample,
                                   SampleType, ScreenPlate)


class User(Base):
    # User class for SQL
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    login = Column(String(125), nullable=False, unique=True)
    name = Column(String(256), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    # 0 = SUPERUSER; 1 = ADMIN; 2 = GUEST
    level = Column(Integer, nullable=False, default=2)
    tokens = relationship("UserToken", backref="user")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserToken(Base):
    # Store JWT tokens for authentication
    __tablename__ = "user_token"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    token = Column(String(4056))
