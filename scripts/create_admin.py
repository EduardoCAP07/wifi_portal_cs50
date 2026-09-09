from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from email_validator import EmailNotValidError, validate_email
from app.db.database import async_session, engine
from app.models.user import User
from app.models.lead import Lead
from app.models.visit import Visit
from datetime import datetime
import phonenumbers
import asyncio
import getpass

password_hash = PasswordHash((Argon2Hasher(),))


def password_hashing (password):
    hash = password_hash.hash(password)

    #temporary printing
    return hash

def check_and_normalize_email(email: str) -> dict:
    try:

        email_info = validate_email(email, check_deliverability=True)

        email_normalized = email_info.normalized

        return {"email": email_normalized, "error": None}

    except EmailNotValidError as e:

        return {"email": None, "error": str(e)}

def phone_validation (phone: str) -> str | None:

    try:
        parsed_number = phonenumbers.parse(phone, "BR")
        valid_number = phonenumbers.is_valid_number(parsed_number)

        if valid_number:
            # AI helped with syntax
            return phonenumbers.format_number(parsed_number,phonenumbers.PhoneNumberFormat.E164)

    except phonenumbers.NumberParseException:
        print("Invalid Phonenumber")
        return None

async def create_user():
    try:
        while True:
            email = str(input("Email: "))
            email_data = check_and_normalize_email(email)
            if email_data["error"]:
                print(email_data["error"])
            phone = str(input("Phone: "))
            valid_phone = phone_validation(phone)
            tos_accepted_at = datetime.now()
            password = str(getpass.getpass("Password: "))
            confirmation = str(getpass.getpass("Confirmation: "))
            if (len(password) >= 15 and password.isspace() == False):
                if (password == confirmation):
                    if email_data["email"]:
                        if valid_phone:
                            hash = password_hashing(password)
                            async with async_session() as session:
                                user = User(email = email_data["email"], password = hash, phone = valid_phone, tos_accepted_at = tos_accepted_at, is_active = True, user_metadata = {"creation": "script"})
                                session.add(user)
                                await session.commit()
                            break
                        else:
                            print("Invalid Phone")
                    else:
                        print("Email is not valid")
                else:
                    print("Password and confirmation must be the same")
            else:
                print("15 characters minimum")

    except Exception as e:
        if e:
            print(str(e))
        else:
            print("Invalid Credentials")


    finally:
        await engine.dispose()

async def main():
    await create_user()


if __name__ == "__main__":
    asyncio.run(main())
