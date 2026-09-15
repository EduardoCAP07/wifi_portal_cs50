# AI disclosure:

# I used ChatGPT as a learning assistant to understand FastAPI, Jinja2,
# request objects, debbuging, and general backend syntax

# Use case example: "What is the Request from FastAPI and when should I use it?"
# or
# "How do i render a template using Jinja2 and FastAPI?"

# most AI use cases were explanation questions for my doubts after reading the documentation on external libraries or python syntax

from fastapi import FastAPI, Request, Form, Query, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
import random

from datetime import datetime
import phonenumbers

# For password hashing
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError

# For Session
import itsdangerous
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

# For environment credentials
import os
from dotenv import load_dotenv

from email_validator import EmailNotValidError, validate_email

# Classes and functions used for sqlachemy
from app.models.lead import Lead
from app.models.user import User
from app.models.visit import Visit
from app.crud.lead import select_all_query, search_query, count_total_leads, get_lead_id
from app.crud.visits import lead_visits_query, count_total_visits, count_visits_today, count_visits_week
from app.crud.user import get_user_id_stmt, get_user_email_stmt, get_version_id_stmt
from app.db.database import async_session

SECRET_KEY = os.getenv("SECRET_KEY")

middleware =  [Middleware(SessionMiddleware,session_cookie="session_user", secret_key= SECRET_KEY, max_age = 3600, https_only=True)]

if SECRET_KEY is not None:
    app = FastAPI(middleware=middleware)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

password_hash = PasswordHash((Argon2Hasher(),))

load_dotenv()

def password_hashing (password):
    hash = password_hash.hash(password)

    return hash

async def get_user_by_email(email: str):
    async with async_session() as session:
        result = await session.execute(get_user_email_stmt(email))
        user = result.scalar_one_or_none()
    return user

async def get_user_by_id(id: int, version: int):
    async with async_session() as session:
        result = await session.execute(get_user_id_stmt(id, version))
        user = result.scalar_one_or_none()
    return user

async def get_version_by_id(id: int):
    async with async_session() as session:
        result = await session.execute(get_version_id_stmt(id))
        version = result.scalar_one_or_none()
    return version

# validating phone | Chat gpt helped me understand how type hints and type annotations work
def phone_validation (phone: str) -> str | None:

    try:
        parsed_number = phonenumbers.parse(phone, "BR")
        valid_number = phonenumbers.is_valid_number(parsed_number)

        if valid_number:
            # AI helped with syntax
            return phonenumbers.format_number(parsed_number,phonenumbers.PhoneNumberFormat.E164)

    except phonenumbers.NumberParseException:
        return None

# This function is going to actually get data from google auth2.0 in the future
# For the MVP it is just a random name generator + returns true for valid
def google_auth():
    #lists of fake names
    first_names = ["Eduardo", "David", "Mary", "Chad", "Taylor", "Monica", "Chandler", "Ross"]
    last_names = ["Silva", "Bing", "Geller", "Green", "Tribiani", "Buffet"]

    first_name  = random.choice(first_names)
    # AI helped with random.choice
    name = f"{first_name}" + " " + f"{random.choice(last_names)}"
    email = f"{first_name}" + "@gmail.com"
    valid = True
    return ({"name": name, "email": email, "valid": valid})

async def auth_user(request: Request):
    user_id = request.session.get("user_id")
    session_version = request.session.get("session_version")
    if user_id and session_version is not None:
        user = await get_user_by_id(user_id, session_version)
        if user:
            if user.is_active == True:
                return user_id
    request.session.clear()

async def update_session_version(id: int, session_version:int):
    async with async_session() as session:
        result = await session.execute(get_user_id_stmt(id, session_version))
        user = result.scalar_one_or_none()
        user.session_version += 1
        await session.commit()



async def create_lead (request: Request, *, google_data: dict, phone: str, user_id: int, ssid: str, mac: str, tos_accepted_at: datetime, visit_metadata: dict | None):
    name = google_data["name"]
    email = google_data["email"]
    async with async_session() as session:
        try:
            # AI helped with session.add and session.flush syntax
            lead = Lead(name = name, email = email, phone = phone, user_id = user_id)
            session.add(lead)

            await session.flush()

            first_visit = Visit(ssid = ssid, mac = mac, tos_accepted_at = tos_accepted_at, visit_metadata = visit_metadata, lead_id = lead.id)
            session.add(first_visit)
            await session.commit()
            return
        except IntegrityError:
            await session.rollback()
            request.session["lead_error"] = "Unable to login with these informations"
            return RedirectResponse(url="/", status_code=303)
        except SQLAlchemyError:
            await session.rollback()
            request.session["lead_error"] = "Unable to complete your request. Try again later"
            return RedirectResponse(url="/", status_code=303)



async def create_visit(request: Request, ssid: str, mac: str, tos_accepted_at: datetime, visit_metadata, lead_id: int):
    async with async_session() as session:
        try:
            # AI helped with session.add syntax
            visit= Visit(ssid = ssid, mac = mac, tos_accepted_at = tos_accepted_at, visit_metadata = visit_metadata, lead_id = lead_id)
            session.add(visit)
            await session.commit()
        #AI helped with exception
        except IntegrityError:
            await session.rollback()
            request.session["lead_error"] = "Unable to login with these informations"
            return RedirectResponse(url="/", status_code=303)

        except SQLAlchemyError:
            await session.rollback()
            request.session["lead_error"] = "Unable to complete your request. Try again later"
            return RedirectResponse(url="/", status_code=303)

async def lead_exists(request: Request, phone: str, user_id: int):
    async with async_session() as session:
        try:
            result = await session.execute(get_lead_id(phone, user_id))
            lead_id = result.scalar_one_or_none()

        except IntegrityError:
            await session.rollback()
            request.session["lead_error"] = "Unable to login with these informations"
            return RedirectResponse(url="/", status_code=303)

        except SQLAlchemyError:
            await session.rollback()
            request.session["lead_error"] = "Unable to complete your request. Try again later"
            return RedirectResponse(url="/", status_code=303)

    return lead_id

# Function that selects all leads
async def select_all(user_id):
    async with async_session() as session:
        result = await session.execute(select_all_query(user_id))
        leads = result.mappings().all()
        return leads

# Function that gets all the simple metrics for the dashboard
async def select_total(user_id: int):
    async with async_session() as session:
        result  = await session.execute(count_total_leads(user_id))
        clients = result.scalar_one()

        result = await session.execute(count_total_visits(user_id))
        visits = result.scalar_one()

        result = await session.execute(count_visits_today(user_id))
        today = result.scalar_one()

        result = await session.execute(count_visits_week(user_id))
        week = result.scalar_one()

        total = {"clients": clients, "visits": visits, "today": today, "week": week}
        return total


# Function that gets leads based on the user search
async def search(search_term, user_id):
    async with async_session() as session:
        result = await session.execute(search_query(search_term, user_id))
        leads = result.mappings().all()
        return leads

# Function that gets all visits from a specifc lead
async def lead_visits(lead_id, user_id):
    async with async_session() as session:
        result = await session.execute(lead_visits_query(lead_id, user_id))
        visits = result.mappings().all()
        return visits

# Adapted from https://pypi.org/project/email-validator/
def check_and_normalize_email(email: str) -> dict:
    try:

        email_info = validate_email(email, check_deliverability=False)

        email_normalized = email_info.normalized

        return {"email": email_normalized, "error": None}

    except EmailNotValidError as e:

        return {"email": None, "error": str(e)}

# response_class tip from FastAPI documentation
# and modification of the FastAPI example for Jinja2 templates
# https://fastapi.tiangolo.com/advanced/templates/#using-jinja2templates
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    client = {"id": 1, "name": "La Fleur", "subname": "Bistro Frances", "image_id": "lafleurbistro", "primary_color": "#512828", "secondary_color": "white", "text-color": "white"}
    logo_path = "/static/resources/images/" + client["image_id"] + ".png"
    error = request.session.pop("lead_error", None)
    # render login page
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context= {"client_name": client["name"], "client_subname": client["subname"], "logo": logo_path, "primary_color": client["primary_color"], "secondary_color": client["secondary_color"], "text_color": client["text-color"], "error": error}
    )

# ChatGPT helped me get the syntax for Form function from Jinja2
@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, phone: str = Form(...)):
    client = {"id": 1, "name": "La Fleur", "subname": "Bistro Frances", "image_id": "lafleurbistro", "primary_color": "#512828", "secondary_color": "white", "text-color": "white"}
    logo_path = "/static/resources/images/" + client["image_id"] + ".png"
    parsed_phone = phone_validation(phone)
    google_auth_response = google_auth()
    user_id = client["id"]

    if (parsed_phone and google_auth_response["valid"]):



        # Check if lead exists
        lead_id = await lead_exists(request, parsed_phone, user_id)

        # AI made this snippet
        # Check if it returned an error
        if isinstance(lead_id, RedirectResponse):
            return lead_id

        # Fake ssid and mac
        ssid = "La Fleur - WiFi"
        mac = "AA:BB:CC:DD:EE:FF"

        tos_accepted_at = datetime.now()

        # Checks if the
        # AI helped with the use of error_reponse to catch the errors from the helpers
        if lead_id:
            error_reponse = await create_visit(request,ssid, mac, tos_accepted_at, None, lead_id)
        else:
            error_reponse = await create_lead(
                request,
                google_data = google_auth_response,
                phone=parsed_phone,
                user_id=user_id,
                ssid=ssid,
                mac=mac,
                tos_accepted_at=tos_accepted_at,
                visit_metadata={"extra_info": "First Access"}
                )
        if error_reponse is not None:
            return error_reponse

        # Render sucess page if phone is valid
        return templates.TemplateResponse(
                    request=request,
                    name="success.html",
                    context= {"client_name": client["name"], "client_subname": client["subname"], "logo": logo_path, "primary_color": client["primary_color"], "secondary_color": client["secondary_color"], "text_color": client["text-color"], "error": None}
                    )
    else:

        # render error in login page if phone is invalid
        return templates.TemplateResponse(
                    request=request,
                    name="login.html",
                    context= {"client_name": client["name"], "client_subname": client["subname"], "logo": logo_path, "primary_color": client["primary_color"], "secondary_color": client["secondary_color"], "text_color": client["text-color"], "error": "Invalid phonenumber"}
                    )

@app.get("/admin/login", response_class=HTMLResponse)
def admin_login(request: Request):
    error = request.session.pop("login_error", None)
    return templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context= {"primary_color": "#512828", "secondary_color": "white", "text_color": "white", "error": error}
    )

@app.post("/admin/login", response_class=HTMLResponse)
async def admin_login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    # AI helped with best validation flow
    normalized_email = check_and_normalize_email(email)
    if normalized_email["email"]:
        try:
            user = await get_user_by_email(normalized_email["email"])
            if user and password_hash.verify(password, user.password):
                if user.is_active == True:
                    session_version = await get_version_by_id(user.id)
                    if session_version is not None:
                        request.session.clear()
                        request.session["user_id"] = user.id
                        request.session["session_version"] = session_version
                        # AI helped with status_code=303 to use method get
                        return RedirectResponse(url="/dashboard", status_code=303)
        except Exception:
            request.session["login_error"] = "Invalid credentials"
            return RedirectResponse(url="/admin/login", status_code=303)
    request.session["login_error"] = "Invalid credentials"
    return RedirectResponse(url="/admin/login", status_code=303)



# PROTECTED ROUTES/ENDPOINTS

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: int = Depends(auth_user)):
    if not user_id:
        #AI helped with status_code
        request.session["login_error"] = "Invalid credentials"
        return RedirectResponse(url="/admin/login", status_code=303)
    client = {"name": "La Fleur", "subname": "Bistro Frances", "id": "lafleurbistro", "primary_color": "#512828", "secondary_color": "white", "text-color": "white"}
    logo_path = "/static/resources/images/" + client["id"] + ".png"
    # created with sqlalchemy's syntax help from AI
    # gets all the leads from database
    leads = await select_all(user_id)
    total = await select_total(user_id)


    # render login page
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context= {"client_name": client["name"], "client_subname": client["subname"], "logo": logo_path, "primary_color": client["primary_color"], "secondary_color": client["secondary_color"], "text_color": client["text-color"], "error": None, "leads": leads, "total": total}
    )

@app.post("/admin/logout", response_class=HTMLResponse)
async def admin_logout(request: Request, user_id: int = Depends(auth_user)):
    if not user_id:
        #AI helped with status_code
        request.session["login_error"] = "Invalid credentials"
        return RedirectResponse(url="/admin/login", status_code=303)
    session_version = request.session.get("session_version")
    await update_session_version(user_id, session_version)
    request.session.clear()

    return RedirectResponse(url="/admin/login", status_code=303)


@app.get("/api/leads")
async def search_fetch(search_term: str | None = Query(default=None, alias="search"), user_id: int = Depends(auth_user)) -> list[dict]:
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    # normalizing
    json_leads = []
    if not search_term or search_term.isspace():
        leads = await select_all(user_id)
        for lead in leads:
            lead_dict = dict(lead)
            #lead_dict["created_at"] = jsonable_encoder(lead_dict["created_at"])
            json_leads.append(lead_dict)
        return json_leads

    # trimmer for external spaces and collapse for internal whitespaces with AI help
    search_term = " ".join(search_term.split())

    error_len = []
    # check lenght
    if len(search_term) > 100:
        error_len.append({"error": "over_max_length"})
        return error_len

    # Normalizign search term for ("%%") LIKE sqlalchemy query
    search_term = "%" + search_term + "%"

    leads = await search(search_term, user_id)

    no_result = []

    if leads:
        for lead in leads:
            lead_dict = dict(lead)
            #if lead_dict["created_at"]:
                #lead_dict["created_at"] = jsonable_encoder(lead_dict["created_at"])
            json_leads.append(lead_dict)
        return json_leads

    no_result.append({"error": "no_result"})
    return no_result

    # end of normalizing


@app.get("/api/history")
async def history_fetch(lead_id: int | None = Query(default=None, alias="lead_id"), user_id: int = Depends(auth_user)) -> list[dict]:
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    json_visits = []

    if not lead_id:
        json_visits.append({"error": "Invalid id"})
        return json_visits

    # Gets all visits from database
    visits = await lead_visits(lead_id, user_id)

    if visits:
        for visit in visits:
            visit_dict = dict(visit)
            visit_dict["created_at"] = jsonable_encoder(visit_dict["created_at"])
            json_visits.append(visit_dict)
        return json_visits

    json_visits.append({"error": "Invalid id"})
    return json_visits


    # end of normalizing
