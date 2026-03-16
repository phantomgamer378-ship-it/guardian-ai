"""
Example usage of the Guardian AI API
Run this to test the API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    resp = requests.get(f"{BASE_URL}/health")
    print(f"Health: {resp.json()}")


def test_create_profile():
    """Test creating a user profile"""
    data = {
        "user_id": "user123",
        "industry": "Healthcare",
        "os_and_tools": ["Windows 11", "AWS", "Office 365"],
        "skill_level": "Intermediate",
        "preferred_tone": "Technical"
    }
    resp = requests.post(f"{BASE_URL}/api/v1/users/profile", json=data)
    print(f"Create Profile: {json.dumps(resp.json(), indent=2)}")
    return data["user_id"]


def test_chat(user_id: str, session_id: str, message: str):
    """Test chat endpoint"""
    data = {
        "user_id": user_id,
        "session_id": session_id,
        "message": message
    }
    resp = requests.post(f"{BASE_URL}/api/v1/chat", json=data)
    result = resp.json()
    print(f"\nUser: {message}")
    print(f"Bot: {result['response'][:200]}...")
    return result.get("conversation_id")


def test_feedback(conversation_id: str, user_id: str, feedback_type: str, comment: str = None):
    """Test feedback submission"""
    data = {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "feedback_type": feedback_type,
        "comment": comment
    }
    resp = requests.post(f"{BASE_URL}/api/v1/feedback", json=data)
    print(f"Feedback submitted: {resp.json()}")


def test_threat_report(user_id: str):
    """Test threat report submission"""
    data = {
        "user_id": user_id,
        "title": "Suspicious GitHub OAuth App",
        "description": "Users are receiving fake GitHub OAuth app requests that steal repository access tokens.",
        "attack_vector": "OAuth consent phishing",
        "targeted_system": "GitHub",
        "severity": "High"
    }
    resp = requests.post(f"{BASE_URL}/api/v1/threats/report", json=data)
    print(f"Threat Report: {json.dumps(resp.json(), indent=2)}")


def test_admin_stats():
    """Test admin dashboard stats"""
    resp = requests.get(f"{BASE_URL}/api/v1/admin/stats")
    print(f"Admin Stats: {json.dumps(resp.json(), indent=2)}")


def run_demo():
    """Run a complete demo of the API"""
    print("=" * 60)
    print("Guardian AI API Demo")
    print("=" * 60)
    
    # Test health
    test_health()
    print()
    
    # Create profile
    user_id = test_create_profile()
    session_id = "session_001"
    print()
    
    # Test chat conversations
    print("-" * 60)
    print("CHAT DEMO")
    print("-" * 60)
    
    # Onboarding
    conv1 = test_chat(user_id, session_id, "Hi, I'm new here. What industry are you in?")
    
    # Security question
    conv2 = test_chat(user_id, session_id, "I got a suspicious email asking for my password. What should I do?")
    
    # Correction
    conv3 = test_chat(user_id, session_id, "That's not quite right for my environment. We use a different email gateway.")
    
    # Submit feedback
    if conv2:
        test_feedback(conv2, user_id, "thumbs_up", "Very helpful!")
    
    print()
    print("-" * 60)
    print("THREAT REPORT DEMO")
    print("-" * 60)
    test_threat_report(user_id)
    
    print()
    print("-" * 60)
    print("ADMIN DASHBOARD DEMO")
    print("-" * 60)
    test_admin_stats()
    
    print()
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
