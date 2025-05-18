"""SQLAlchemy ORM models."""

from datetime import date
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class HostTable(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rating = Column(Float, default=0.0)


class PropertyTable(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

    rooms = relationship("RoomTable", back_populates="property", cascade="all, delete-orphan")


class RoomTable(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    beds = Column(Integer, default=1)
    features = Column(String, nullable=True)
    price = Column(Float, default=0.0)

    property = relationship("PropertyTable", back_populates="rooms")


class BookingTable(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    guest_name = Column(String, nullable=False)
    language = Column(String, nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)

    room = relationship("RoomTable")
