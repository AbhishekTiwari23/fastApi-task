from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Text, func
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, max_length=50, nullable=False)
    last_name = Column(String, max_length=50, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False, max_length=100)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    join_date = Column(default=datetime.now().date())
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    gender = Column(String, nullable=False)
    expected_calories = Column(Integer)

    items = relationship("Item", back_populates="owner")
    settings = relationship("UserSettings", back_populates="user")

    @property
    def is_calories_less(self):
        total_calories = sum(item.calories for item in self.items)
        return total_calories < self.expected_calories


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.now().date())
    time = Column(Time, default=datetime.now().time())
    name = Column(Text, nullable=False, max_length=100)
    quantity = Column(Integer, default=1)
    calories = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class UserSettings(Base):
    __tablename__ = "user_settings"

    user = relationship("User", back_populates="settings")
    id = Column(Integer, primary_key=True, index=True,)
    user_id = Column(Integer, ForeignKey("users.id"))
    expected_calories = Column(Integer, nullable=False, default=func.case(
        [
            (func.lower(User.gender) == 'male', 2500),
            (func.lower(User.gender) == 'female', 2000),
        ],
        else_=2250
    ))


