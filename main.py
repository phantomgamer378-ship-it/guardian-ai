"""
Guardian AI - FastAPI Application
Main API endpoints for the cybersecurity chatbot
"""
import os
from typing import Optional, List
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Database, get_db, UserProfile, Conversation, Feedback, ThreatReport, AbuseLog, KnowledgeBaseUpdate
from chatbot import GuardianBot, AbuseDetector

# Initialize FastAPI app
app = FastAPI(
    title="Guardian AI API",
    description="Cybersecurity Chatbot with Adaptive Learning",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = Database()


# ============ Pydantic Models ============

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    type: str


class UserProfileCreate(BaseModel):
    user_id: str
    industry: Optional[str] = None
    os_and_tools: Optional[List[str]] = None
    skill_level: str = "Beginner"
    preferred_tone: str = "Simple"


class UserProfileUpdate(BaseModel):
    industry: Optional[str] = None
    os_and_tools: Optional[List[str]] = None
    skill_level: Optional[str] = None
    preferred_tone: Optional[str] = None
    known_risks: Optional[List[str]] = None


class UserProfileResponse(BaseModel):
    user_id: str
    industry: Optional[str]
    os_and_tools: List[str]
    skill_level: str
    preferred_tone: str
    security_score: int
    corrections_given: int
    threats_reported: int
    last_session: Optional[str]


class FeedbackCreate(BaseModel):
    conversation_id: str
    user_id: str
    feedback_type: str = Field(..., pattern="^(thumbs_up|thumbs_down|correction)$")
    comment: Optional[str] = None
    suggested_correction: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: str
    feedback_type: str
    status: str


class ThreatReportCreate(BaseModel):
    user_id: str
    title: str
    description: str
    attack_vector: Optional[str] = None
    targeted_system: Optional[str] = None
    iocs: Optional[List[str]] = None
    observed_date: Optional[datetime] = None
    severity: str = "Medium"


class ThreatReportResponse(BaseModel):
    id: str
    status: str
    message: str


class AdminApproveRequest(BaseModel):
    item_id: str
    item_type: str = Field(..., pattern="^(correction|threat)$")
    action: str = Field(..., pattern="^(approve|reject)$")
    admin_notes: Optional[str] = None


# ============ Chat Endpoints ============

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db_session: Session = Depends(get_db)):
    """Send a message to the chatbot and get a response"""
    bot = GuardianBot(db_session)
    
    result = await bot.process_message(
        user_id=request.user_id,
        session_id=request.session_id,
        message=request.message
    )
    
    return ChatResponse(
        response=result["response"],
        conversation_id=result["conversation_id"],
        type=result["type"]
    )


# ============ User Profile Endpoints ============

@app.post("/api/v1/users/profile", response_model=UserProfileResponse)
def create_or_update_profile(profile: UserProfileCreate, db_session: Session = Depends(get_db)):
    """Create or update a user profile"""
    existing = db_session.query(UserProfile).filter(UserProfile.user_id == profile.user_id).first()
    
    if existing:
        # Update existing
        existing.industry = profile.industry or existing.industry
        existing.os_and_tools = profile.os_and_tools or existing.os_and_tools
        existing.skill_level = profile.skill_level
        existing.preferred_tone = profile.preferred_tone
        existing.last_session = datetime.utcnow()
    else:
        # Create new
        new_profile = UserProfile(
            user_id=profile.user_id,
            industry=profile.industry,
            os_and_tools=profile.os_and_tools or [],
            skill_level=profile.skill_level,
            preferred_tone=profile.preferred_tone,
            security_score=50
        )
        db_session.add(new_profile)
    
    db_session.commit()
    
    updated = db_session.query(UserProfile).filter(UserProfile.user_id == profile.user_id).first()
    
    return UserProfileResponse(
        user_id=updated.user_id,
        industry=updated.industry,
        os_and_tools=updated.os_and_tools or [],
        skill_level=updated.skill_level,
        preferred_tone=updated.preferred_tone,
        security_score=updated.security_score,
        corrections_given=updated.corrections_given,
        threats_reported=updated.threats_reported,
        last_session=updated.last_session.isoformat() if updated.last_session else None
    )


@app.get("/api/v1/users/{user_id}/profile", response_model=UserProfileResponse)
def get_profile(user_id: str, db_session: Session = Depends(get_db)):
    """Get a user's profile"""
    profile = db_session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    return UserProfileResponse(
        user_id=profile.user_id,
        industry=profile.industry,
        os_and_tools=profile.os_and_tools or [],
        skill_level=profile.skill_level,
        preferred_tone=profile.preferred_tone,
        security_score=profile.security_score,
        corrections_given=profile.corrections_given,
        threats_reported=profile.threats_reported,
        last_session=profile.last_session.isoformat() if profile.last_session else None
    )


@app.patch("/api/v1/users/{user_id}/profile")
def update_profile(user_id: str, update: UserProfileUpdate, db_session: Session = Depends(get_db)):
    """Partial update of user profile"""
    profile = db_session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    if update.industry is not None:
        profile.industry = update.industry
    if update.os_and_tools is not None:
        profile.os_and_tools = update.os_and_tools
    if update.skill_level is not None:
        profile.skill_level = update.skill_level
    if update.preferred_tone is not None:
        profile.preferred_tone = update.preferred_tone
    if update.known_risks is not None:
        profile.known_risks = update.known_risks
    
    profile.last_session = datetime.utcnow()
    db_session.commit()
    
    return {"status": "updated", "user_id": user_id}


# ============ Feedback Endpoints ============

@app.post("/api/v1/feedback", response_model=FeedbackResponse)
def submit_feedback(feedback: FeedbackCreate, db_session: Session = Depends(get_db)):
    """Submit feedback on a bot response"""
    # Get the conversation
    conv = db_session.query(Conversation).filter(Conversation.id == feedback.conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Create feedback record
    new_feedback = Feedback(
        conversation_id=feedback.conversation_id,
        user_id=feedback.user_id,
        feedback_type=feedback.feedback_type,
        comment=feedback.comment,
        original_response=conv.response,
        suggested_correction=feedback.suggested_correction
    )
    db_session.add(new_feedback)
    
    # Update user corrections count if it's a correction
    if feedback.feedback_type == "correction":
        user = db_session.query(UserProfile).filter(UserProfile.user_id == feedback.user_id).first()
        if user:
            user.corrections_given += 1
            user.security_score = min(100, user.security_score + 5)  # Reward for corrections
    
    db_session.commit()
    
    return FeedbackResponse(
        id=new_feedback.id,
        feedback_type=feedback.feedback_type,
        status="submitted"
    )


# ============ Threat Report Endpoints ============

@app.post("/api/v1/threats/report", response_model=ThreatReportResponse)
def report_threat(report: ThreatReportCreate, db_session: Session = Depends(get_db)):
    """Report a new threat"""
    new_report = ThreatReport(
        user_id=report.user_id,
        title=report.title,
        description=report.description,
        attack_vector=report.attack_vector,
        targeted_system=report.targeted_system,
        iocs=report.iocs or [],
        observed_date=report.observed_date,
        severity=report.severity,
        status="pending"
    )
    db_session.add(new_report)
    
    # Update user's threat reported count
    user = db_session.query(UserProfile).filter(UserProfile.user_id == report.user_id).first()
    if user:
        user.threats_reported += 1
        user.security_score = min(100, user.security_score + 10)  # Reward for reporting
    
    db_session.commit()
    
    return ThreatReportResponse(
        id=new_report.id,
        status="pending",
        message="Thank you for reporting this threat. Our security team will review it."
    )


@app.get("/api/v1/threats/my-reports")
def get_my_threats(user_id: str = Query(...), db_session: Session = Depends(get_db)):
    """Get all threat reports by a specific user"""
    reports = db_session.query(ThreatReport).filter(ThreatReport.user_id == user_id).all()
    return [
        {
            "id": r.id,
            "title": r.title,
            "status": r.status,
            "severity": r.severity,
            "created_at": r.created_at.isoformat()
        }
        for r in reports
    ]


# ============ Admin Dashboard Endpoints ============

@app.get("/api/v1/admin/corrections")
def get_pending_corrections(status: str = "pending", db_session: Session = Depends(get_db)):
    """Get pending user corrections for admin review"""
    corrections = db_session.query(Feedback).filter(
        Feedback.feedback_type == "correction",
        Feedback.admin_reviewed == (status != "pending")
    ).all()
    
    return [
        {
            "id": c.id,
            "user_id": c.user_id,
            "original_response": c.original_response,
            "suggested_correction": c.suggested_correction,
            "comment": c.comment,
            "created_at": c.created_at.isoformat(),
            "admin_reviewed": c.admin_reviewed,
            "admin_action": c.admin_action
        }
        for c in corrections
    ]


@app.get("/api/v1/admin/threats")
def get_pending_threats(status: str = "pending", db_session: Session = Depends(get_db)):
    """Get pending threat reports for admin review"""
    threats = db_session.query(ThreatReport).filter(
        ThreatReport.status == status if status else True
    ).all()
    
    return [
        {
            "id": t.id,
            "user_id": t.user_id,
            "title": t.title,
            "description": t.description,
            "attack_vector": t.attack_vector,
            "severity": t.severity,
            "status": t.status,
            "similar_reports_count": t.similar_reports_count,
            "created_at": t.created_at.isoformat()
        }
        for t in threats
    ]


@app.post("/api/v1/admin/approve")
def approve_item(request: AdminApproveRequest, db_session: Session = Depends(get_db)):
    """Approve or reject a correction or threat report"""
    
    if request.item_type == "correction":
        item = db_session.query(Feedback).filter(Feedback.id == request.item_id).first()
    else:
        item = db_session.query(ThreatReport).filter(ThreatReport.id == request.item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if request.item_type == "correction":
        item.admin_reviewed = True
        item.admin_action = request.action
        item.is_addressed = (request.action == "approve")
        
        if request.action == "approve":
            # Add to knowledge base updates
            kb_update = KnowledgeBaseUpdate(
                source_type="user_correction",
                source_id=item.id,
                topic="User Correction",
                old_content=item.original_response,
                new_content=item.suggested_correction or item.comment,
                approved_by="admin"  # In production, use actual admin ID
            )
            db_session.add(kb_update)
    else:
        item.status = "verified" if request.action == "approve" else "rejected"
        item.admin_notes = request.admin_notes
        
        if request.action == "approve":
            item.verified_at = datetime.utcnow()
            # Add to knowledge base
            kb_update = KnowledgeBaseUpdate(
                source_type="threat_report",
                source_id=item.id,
                topic=item.title,
                new_content=item.description,
                approved_by="admin"
            )
            db_session.add(kb_update)
    
    db_session.commit()
    
    return {
        "status": "success",
        "item_id": request.item_id,
        "action": request.action,
        "item_type": request.item_type
    }


@app.get("/api/v1/admin/abuse-logs")
def get_abuse_logs(limit: int = 50, db_session: Session = Depends(get_db)):
    """Get abuse attempt logs"""
    logs = db_session.query(AbuseLog).order_by(AbuseLog.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "abuse_type": log.abuse_type,
            "confidence_score": log.confidence_score,
            "action_taken": log.action_taken,
            "timestamp": log.timestamp.isoformat()
        }
        for log in logs
    ]


@app.get("/api/v1/admin/stats")
def get_admin_stats(db_session: Session = Depends(get_db)):
    """Get dashboard statistics"""
    pending_corrections = db_session.query(Feedback).filter(
        Feedback.feedback_type == "correction",
        Feedback.admin_reviewed == False
    ).count()
    
    pending_threats = db_session.query(ThreatReport).filter(
        ThreatReport.status == "pending"
    ).count()
    
    total_users = db_session.query(UserProfile).count()
    total_conversations = db_session.query(Conversation).count()
    
    recent_abuse = db_session.query(AbuseLog).filter(
        AbuseLog.timestamp > datetime.utcnow().replace(hour=datetime.utcnow().hour - 24)
    ).count()
    
    return {
        "pending_corrections": pending_corrections,
        "pending_threats": pending_threats,
        "total_users": total_users,
        "total_conversations": total_conversations,
        "abuse_attempts_24h": recent_abuse
    }


# ============ Health Check ============

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Guardian AI", "version": "2.0.0"}


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Guardian AI API",
        "docs": "/docs",
        "version": "2.0.0"
    }
