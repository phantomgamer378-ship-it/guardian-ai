"""
Indian Cybersecurity Knowledge Base
Additional context for Guardian AI
"""

INDIAN_CYBERSECURITY_DATA = {
    "emergency_contacts": {
        "cyber_crime_helpline": "1930",
        "cert_in": "https://cert-in.org.in",
        "cyber_crime_portal": "https://cybercrime.gov.in",
        "national_cyber_security_coordinator": "https://ncsc.gov.in"
    },
    
    "common_threats": {
        "upi_scams": {
            "description": "Fraudulent UPI requests, QR code scams, fake payment links",
            "prevention": [
                "Never scan unknown QR codes",
                "Verify UPI handles before sending money",
                "Use UPI apps with transaction limits",
                "Enable transaction notifications"
            ]
        },
        "aadhaar_fraud": {
            "description": "Unauthorized use of Aadhaar data for identity theft",
            "prevention": [
                "Never share Aadhaar OTP",
                "Use masked Aadhaar when possible",
                "Lock biometric data in mAadhaar app",
                "Regularly check Aadhaar authentication history"
            ]
        },
        "digital_payment_fraud": {
            "description": "Credit/debit card fraud, net banking scams",
            "prevention": [
                "Use virtual cards for online payments",
                "Enable 3D secure authentication",
                "Never share CVV or OTP",
                "Use different cards for online/offline"
            ]
        },
        "job_scams": {
            "description": "Fake job offers demanding payment for training/verification",
            "prevention": [
                "Never pay for job offers",
                "Verify company details on official portals",
                "Be cautious of work-from-home offers",
                "Check company registration details"
            ]
        }
    },
    
    "legal_framework": {
        "it_act_2000": "Primary legislation for cybersecurity in India",
        "it_rules_2021": "Latest amendments covering data protection, intermediary guidelines",
        "data_protection_bill": "Personal Data Protection Bill (pending implementation)",
        "rbi_guidelines": "Reserve Bank of India cybersecurity guidelines for banks"
    },
    
    "best_practices": {
        "mobile_security": [
            "Enable device encryption",
            "Use official app stores only",
            "Regular security updates",
            "App permission review",
            "Antivirus/anti-malware protection"
        ],
        "banking_security": [
            "Enable SMS/email alerts",
            "Use transaction limits",
            "Regular password changes",
            "Avoid public WiFi for banking",
            "Check bank statements regularly"
        ],
        "social_media_security": [
            "Privacy settings review",
            "Two-factor authentication",
            "Avoid sharing personal details",
            "Be cautious with friend requests",
            "Report fake profiles"
        ]
    },
    
    "reporting_procedures": {
        "financial_fraud": [
            "Contact bank immediately",
            "File complaint at cybercrime.gov.in",
            "Call 1930 helpline",
            "Document all communications",
            "File FIR with local police"
        ],
        "identity_theft": [
            "Lock Aadhaar biometrics",
            "Report to CERT-In",
            "File cybercrime complaint",
            "Inform credit bureaus",
            "Monitor credit reports"
        ],
        "social_media_hacking": [
            "Change all passwords",
            "Enable 2FA on all accounts",
            "Report to platform",
            "Inform contacts about compromise",
            "File cybercrime report if needed"
        ]
    },
    
    "indian_specific_tools": {
        "m_ahaar": "Official Aadhaar app with security features",
        "digi_locker": "Government digital wallet with security",
        "csc_vle": "Common Service Centers for digital literacy",
        "cyber_swachhta": "National cybersecurity awareness program"
    }
}

def get_indian_context(topic: str) -> dict:
    """Get India-specific cybersecurity context for a topic"""
    topic_lower = topic.lower()
    
    context_mapping = {
        "upi": INDIAN_CYBERSECURITY_DATA["common_threats"]["upi_scams"],
        "aadhaar": INDIAN_CYBERSECURITY_DATA["common_threats"]["aadhaar_fraud"],
        "banking": {
            "threats": INDIAN_CYBERSECURITY_DATA["common_threats"]["digital_payment_fraud"],
            "guidelines": INDIAN_CYBERSECURITY_DATA["legal_framework"]["rbi_guidelines"],
            "practices": INDIAN_CYBERSECURITY_DATA["best_practices"]["banking_security"]
        },
        "mobile": INDIAN_CYBERSECURITY_DATA["best_practices"]["mobile_security"],
        "social_media": INDIAN_CYBERSECURITY_DATA["best_practices"]["social_media_security"],
        "emergency": INDIAN_CYBERSECURITY_DATA["emergency_contacts"],
        "legal": INDIAN_CYBERSECURITY_DATA["legal_framework"]
    }
    
    for key, value in context_mapping.items():
        if key in topic_lower:
            return value
    
    return {"general": "Use CERT-In and cybercrime.gov.in for Indian-specific guidance"}

def format_indian_response(topic: str, base_response: str) -> str:
    """Format response with Indian context"""
    context = get_indian_context(topic)
    
    if topic.lower() in ["upi", "payment", "scam"]:
        indian_tips = "\n\n🇮🇳 **Indian-Specific Protection:**\n"
        indian_tips += "\n".join([f"• {tip}" for tip in context["prevention"]])
        return base_response + indian_tips
    
    elif topic.lower() in ["banking", "finance"]:
        contact_info = "\n\n🇮🇳 **Indian Emergency Contacts:**\n"
        contact_info += f"• Cyber Crime Helpline: 1930\n"
        contact_info += f"• Report Portal: cybercrime.gov.in\n"
        contact_info += f"• CERT-In: cert-in.org.in"
        return base_response + contact_info
    
    return base_response
