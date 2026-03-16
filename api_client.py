"""
Guardian AI - API Client
Simple Python client to interact with the chatbot API
"""
import requests
from typing import Optional, List, Dict, Any


class GuardianAPI:
    """Python client for Guardian AI Chatbot API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
    
    def chat(self, user_id: str, session_id: str, message: str) -> Dict[str, Any]:
        """Send a message to the chatbot"""
        response = requests.post(
            f"{self.base_url}/api/v1/chat",
            headers=self.headers,
            json={"user_id": user_id, "session_id": session_id, "message": message}
        )
        response.raise_for_status()
        return response.json()
    
    def create_profile(self, user_id: str, industry: Optional[str] = None,
                       os_and_tools: Optional[List[str]] = None,
                       skill_level: str = "Beginner",
                       preferred_tone: str = "Simple") -> Dict[str, Any]:
        """Create or update user profile"""
        response = requests.post(
            f"{self.base_url}/api/v1/users/profile",
            headers=self.headers,
            json={
                "user_id": user_id,
                "industry": industry,
                "os_and_tools": os_and_tools or [],
                "skill_level": skill_level,
                "preferred_tone": preferred_tone
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile"""
        response = requests.get(
            f"{self.base_url}/api/v1/users/{user_id}/profile",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def submit_feedback(self, conversation_id: str, user_id: str,
                        feedback_type: str, comment: Optional[str] = None,
                        suggested_correction: Optional[str] = None) -> Dict[str, Any]:
        """Submit feedback on a response"""
        response = requests.post(
            f"{self.base_url}/api/v1/feedback",
            headers=self.headers,
            json={
                "conversation_id": conversation_id,
                "user_id": user_id,
                "feedback_type": feedback_type,
                "comment": comment,
                "suggested_correction": suggested_correction
            }
        )
        response.raise_for_status()
        return response.json()
    
    def report_threat(self, user_id: str, title: str, description: str,
                      attack_vector: Optional[str] = None,
                      targeted_system: Optional[str] = None,
                      severity: str = "Medium") -> Dict[str, Any]:
        """Report a new threat"""
        response = requests.post(
            f"{self.base_url}/api/v1/threats/report",
            headers=self.headers,
            json={
                "user_id": user_id,
                "title": title,
                "description": description,
                "attack_vector": attack_vector,
                "targeted_system": targeted_system,
                "severity": severity
            }
        )
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    # Initialize client
    api = GuardianAPI("http://localhost:8000")
    
    # Check health
    print("Health:", api.health_check())
    
    # Create profile
    profile = api.create_profile(
        user_id="user_123",
        industry="Finance",
        os_and_tools=["Windows 11", "AWS"],
        skill_level="Intermediate"
    )
    print("Profile created:", profile)
    
    # Chat
    response = api.chat(
        user_id="user_123",
        session_id="session_1",
        message="How do I protect against phishing attacks?"
    )
    print("Bot response:", response["response"][:200])
    
    # Submit feedback
    feedback = api.submit_feedback(
        conversation_id=response["conversation_id"],
        user_id="user_123",
        feedback_type="thumbs_up",
        comment="Very helpful!"
    )
    print("Feedback submitted:", feedback)
