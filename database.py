# database.py
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime

# Database URL - Render provides DATABASE_URL for PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # For PostgreSQL on Render
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
else:
    # Fallback to SQLite for local development
    DATABASE_URL = "sqlite:///./sahayak.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------- Models ----------
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    account_type = Column(String(50), default="teacher")
    
    # Relationships
    settings = relationship("UserSettings", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("UserProfile", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    lesson_plans = relationship("LessonPlan", back_populates="user", cascade="all, delete-orphan")

class UserSettings(Base):
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    settings_type = Column(String(50), default="general")
    settings_data = Column(JSON, default={})
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="settings")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    profile_type = Column(String(50), default="personal")
    profile_data = Column(JSON, default={})
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="profile")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(100), ForeignKey("conversations.conversation_id", ondelete="CASCADE"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    role = Column(String(20), nullable=False)  # user or assistant
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="chat")  # chat, lesson_plan, etc.
    extra_data = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    user = relationship("User")

class LessonPlan(Base):
    __tablename__ = "lesson_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    conversation_id = Column(String(100), ForeignKey("conversations.conversation_id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255))
    topic = Column(String(255))
    grade = Column(String(50))
    content = Column(Text)
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="lesson_plans")

class GeneratedFile(Base):
    __tablename__ = "generated_files"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, docx, pptx, etc.
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    extra_data = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

class StudentRecord(Base):
    __tablename__ = "student_records"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    name = Column(String(255), nullable=False)
    class_name = Column(String(100), nullable=False)
    grade = Column(String(50), nullable=False)
    email = Column(String(255), nullable=True)
    parent_contact = Column(String(255), nullable=True)
    progress = Column(Float, default=0.0)
    attendance = Column(Float, default=100.0)
    status = Column(String(50), default="average")
    created_at = Column(DateTime(timezone=True), default=func.now())
    last_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class ProgressHistory(Base):
    __tablename__ = "progress_history"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(String(100), unique=True, index=True, nullable=False)
    student_id = Column(String(100), ForeignKey("student_records.student_id", ondelete="CASCADE"), index=True, nullable=False)
    assignment_name = Column(String(255), nullable=False)
    assignment_type = Column(String(100), nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    date_completed = Column(DateTime(timezone=True), nullable=False)
    notes = Column(Text, nullable=True)
    recorded_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationship
    student = relationship("StudentRecord")

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

# Test database connection
def test_connection():
    try:
        with engine.connect() as connection:
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False