"""
Database models for Guardian AI Chatbot
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())


class UserProfile(Base):
    """User Security Profile - persistent across sessions"""
    __tablename__ = "user_profiles"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, unique=True, index=True, nullable=False)
    industry = Column(String, nullable=True)
    os_and_tools = Column(JSON, default=list)
    skill_level = Column(String, default="Beginner")  # Beginner, Intermediate, Expert
    preferred_tone = Column(String, default="Simple")  # Technical, Simple
    security_score = Column(Integer, default=50)
    corrections_given = Column(Integer, default=0)
    threats_reported = Column(Integer, default=0)
    known_risks = Column(JSON, default=list)
    past_incidents = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_session = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")


class Conversation(Base):
    """Chat conversations stored for context"""
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("user_profiles.user_id"), nullable=False)
    session_id = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    message_type = Column(String, default="user")  # user, system, assistant
    timestamp = Column(DateTime, default=datetime.utcnow)
    context_data = Column(JSON, default=dict)  # Store user context at time of message
    
    # Relationships
    user = relationship("UserProfile", back_populates="conversations")
    feedback = relationship("Feedback", back_populates="conversation", uselist=False)


class Feedback(Base):
    """User feedback on bot responses"""
    __tablename__ = "feedback"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    user_id = Column(String, ForeignKey("user_profiles.user_id"), nullable=False)
    feedback_type = Column(String, nullable=False)  # thumbs_up, thumbs_down, correction
    comment = Column(Text, nullable=True)
    original_response = Column(Text, nullable=False)
    suggested_correction = Column(Text, nullable=True)
    is_addressed = Column(Boolean, default=False)
    admin_reviewed = Column(Boolean, default=False)
    admin_action = Column(String, nullable=True)  # approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="feedback")
    user = relationship("UserProfile", back_populates="feedbacks")


class ThreatReport(Base):
    """New threat reports from users"""
    __tablename__ = "threat_reports"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("user_profiles.user_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    attack_vector = Column(String, nullable=True)
    targeted_system = Column(String, nullable=True)
    iocs = Column(JSON, default=list)  # Indicators of Compromise
    observed_date = Column(DateTime, nullable=True)
    severity = Column(String, default="Medium")  # Low, Medium, High, Critical
    status = Column(String, default="pending")  # pending, verified, rejected
    admin_notes = Column(Text, nullable=True)
    similar_reports_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)


class AbuseLog(Base):
    """Log of abuse attempts for security monitoring"""
    __tablename__ = "abuse_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=True)
    session_id = Column(String, nullable=True)
    input_text = Column(Text, nullable=False)
    abuse_type = Column(String, nullable=False)  # jailbreak, harmful_request, manipulation
    confidence_score = Column(Float, nullable=False)
    action_taken = Column(String, default="blocked")  # blocked, logged, flagged
    timestamp = Column(DateTime, default=datetime.utcnow)


class KnowledgeBaseUpdate(Base):
    """Approved updates to knowledge base from user corrections"""
    __tablename__ = "kb_updates"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    source_type = Column(String, nullable=False)  # user_correction, threat_report
    source_id = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    old_content = Column(Text, nullable=True)
    new_content = Column(Text, nullable=False)
    approved_by = Column(String, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Database connection setup
class Database:
    def __init__(self, database_url: str = "sqlite:///./guardianai.db"):
        self.engine = create_engine(database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {})
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self):
        return self.SessionLocal()


def get_db():
    """Dependency for FastAPI to get database session"""
    db = Database().get_session()
    try:
        yield db
    finally:
        db.close()
