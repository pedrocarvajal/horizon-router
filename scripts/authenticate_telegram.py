import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram configuration from environment
TELEGRAM_API_ID = os.environ.get("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH")
TELEGRAM_SESSION_NAME = os.environ.get("TELEGRAM_SESSION_NAME", "telegram_session")

async def authenticate():
    if not TELEGRAM_API_ID or not TELEGRAM_API_HASH:
        print("Error: TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in environment variables")
        return
    
    client = TelegramClient(TELEGRAM_SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    
    await client.connect()
    
    if not await client.is_user_authorized():
        print("Not authorized, starting authentication...")
        phone = input("Enter your phone number (with country code): ")
        await client.send_code_request(phone)
        
        try:
            code = input("Enter the code you received: ")
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input("Two-step verification is enabled. Enter your password: ")
            await client.sign_in(password=password)
    else:
        print("Already authorized")
    
    me = await client.get_me()
    print(f"Logged in as: {me.first_name} {me.last_name or ''} (@{me.username or 'No username'})")
    print(f"Phone: {me.phone}")
    
    try:
        message = await client.send_message("me", "Connection successfully")
        print(f"Test message sent to saved messages (Message ID: {message.id})")
    except Exception as e:
        print(f"Error sending message to saved messages: {e}")
        import traceback
        traceback.print_exc()
    
    await client.disconnect()

if __name__ == "__main__":
    print("Setting up Telegram session...")
    session_file = f"{TELEGRAM_SESSION_NAME}.session"
    if os.path.exists(session_file):
        print(f"Existing session found: {session_file}")
    else:
        print("You will be asked for your phone number and SMS code")
    asyncio.run(authenticate())