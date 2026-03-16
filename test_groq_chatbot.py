import asyncio
import os
from chatbot import GuardianBot
from models import Database

async def main():
    if not os.environ.get("GROQ_API_KEY"):
        print("Please set GROQ_API_KEY")
        return
        
    db = Database()
    bot = GuardianBot(db)
    user_id = "test_user"
    session_id = "test_session"
    
    # Send a Hindi query about getting a call from police regarding parcel
    message = "Mujhe abhi ek call aayi hai video call pe, ek police officer the, unhone bola ki mere naam pe drugs ka parcel hai aur mujhe arrest kiya jayega. Main kya karun?"
    
    print("User:", message)
    print("Generaring response...")
    
    response = await bot.process_message(user_id, session_id, message)
    
    print("\nBot Response:")
    print(response["response"])

if __name__ == "__main__":
    asyncio.run(main())
