# AI disclosure:

# I used ChatGPT as a learning assistant to understand FastAPI, Jinja2, 
# request objects, debbuging, and general backend syntax

# Use case example: "What is the Request from FastAPI and when should I use it?"
# or 
# "How do i render a template using Jinja2 and FastAPI?"

# most AI use cases were explanation questions for my doubts after reading the documentation on external libraries or python syntax

from fastapi import FastAPI, Request, Form, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
import random

from datetime import datetime
import phonenumbers

# classes used for sqlachemy
from app.models.lead import Lead
from app.models.user import User
from app.models.visit import Visit
from app.crud.lead import select_all_query, search_query, get_lead_id
from app.crud.visits import lead_visits_query
from app.db.database import async_session

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# response_class tip from FastAPI documentation
# and modification of the FastAPI example for Jinja2 templates

# https://fastapi.tiangolo.com/advanced/templates/#using-jinja2templates
# validating phone | Chat gpt helped me understand how type hints and type annotations work
def phone_validation (phone: str) -> str | None:


    try:
        parsed_number = phonenumbers.parse(phone, "BR")
        valid_number = phonenumbers.is_valid_number(parsed_number)

        if valid_number:

            print("numero valido")

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

#TODO: Function that stores leads in the database
async def create_lead (google_data: dict, phone: str, user_id: int, ssid: str, mac: str, tos_accepted_at: datetime, visit_metadata: dict | None):
    name = google_data["name"]
    email = google_data["email"]
    async with async_session() as session:
        # AI helped with session.add and session.flush syntax
        lead = Lead(name = name, email = email, phone = phone, user_id = user_id)
        session.add(lead)

        await session.flush()

        first_visit = Visit(ssid = ssid, mac = mac, tos_accepted_at = tos_accepted_at, visit_metadata = visit_metadata, lead_id = lead.id)
        session.add(first_visit)
        await session.commit()
    return
async def create_visit(ssid: str, mac: str, tos_accepted_at: datetime, visit_metadata, lead_id):
    async with async_session() as session:
        # AI helped with session.add syntax
        visit= Visit(ssid = ssid, mac = mac, tos_accepted_at = tos_accepted_at, visit_metadata = visit_metadata, lead_id = lead_id)
        session.add(visit)
        await session.commit()


async def lead_exists(phone: str, user_id: int):
    async with async_session() as session:
        result = await session.execute(get_lead_id(phone, user_id))
        lead_id = result.scalar_one_or_none()
    return lead_id

# Function that selects all leads

async def select_all():
    async with async_session() as session:
        result = await session.execute(select_all_query)
        leads = result.mappings().all()
        return leads


async def search(search_term):
    async with async_session() as session:
        result = await session.execute(search_query(search_term))
        leads = result.mappings().all()
        return leads


async def lead_visits(lead_id):
    async with async_session() as session:
        result = await session.execute(lead_visits_query(lead_id))
        print(result.keys())
        visits = result.mappings().all()
        return visits


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    client = {"name": "La Fleur", "subname": "Bistro Frances", "id": "lafleurbistro", "primary_color": "#512828", "secondary_color": "white", "text-color": "white"}
    logo_path = "/static/resources/images/" + client["id"] + ".png"
    
    # render login page
    return templates.TemplateResponse(
        request=request,
        name="login.html", 
        context= {"client_name": client["name"], "client_subname": client["subname"], "logo": logo_path, "primary_color": client["primary_color"], "secondary_color": client["secondary_color"], "text_color": client["text-color"], "error": None}
    )

# ChatGPT helped me get the syntax for Form function from Jinja2
@app.post("/login", response_class=HTMLResponse)
async def home(request: Request, phone: str = Form(...)):
    client = {"name": "La Fleur", "subname": "Bistro Frances", "id": "lafleurbistro", "primary_color": "#512828", "secondary_color": "white", "text-color": "white"}
    logo_path = "/static/resources/images/" + client["id"] + ".png"
    parsed_phone = phone_validation(phone)

    if (parsed_phone and google_auth_response["valid"]):

        #TODO: Change hardcoded user_id when login is implemented
        # Stores leads in database
        user_id = 1

        lead_id = await lead_exists(parsed_phone, user_id)

        # Fake ssid and mac
        ssid = "La Fleur - WiFi"
        mac = "AA:BB:CC:DD:EE:FF"
        tos_accepted_at = datetime.now()
        if lead_id:
            await create_visit(ssid, mac, tos_accepted_at, None, lead_id)
        else:
            await create_lead(google_auth_response, parsed_phone, user_id, ssid, mac, tos_accepted_at, {"extra_info": "First Access"})

        # render sucess page if phone is valid
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
    
@app.get("/dashboard", response_class=HTMLResponse)
async def home(request: Request):
    google_auth_response = google_auth()
    client = {"name": "La Fleur", "subname": "Bistro Frances", "id": "lafleurbistro", "primary_color": "#512828", "secondary_color": "white", "text-color": "white"}
    logo_path = "/static/resources/images/" + client["id"] + ".png"
    # created with sqlalchemy's syntax help from AI
    # gets all the leads from database
    leads = await select_all()


    # render login page
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html", 
        context= {"client_name": client["name"], "client_subname": client["subname"], "logo": logo_path, "primary_color": client["primary_color"], "secondary_color": client["secondary_color"], "text_color": client["text-color"], "error": None, "leads": leads}
    )

# AI helped debbug
@app.get("/api/leads")
async def search_fetch(search_term: str | None = Query(default=None, alias="search")) -> list[dict]:
    # normalizing
    json_leads = []
    if not search_term or search_term.isspace():
        leads = await select_all()
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

    leads = await search(search_term)

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
async def history_fetch(lead_id: int | None = Query(default=None, alias="lead_id")) -> list[dict]:
    json_visits = []

    #TODO: Validates if user has autorization to search for that specific lead


    if not lead_id:
        json_visits.append({"error": "Invalid id"})
        return json_visits



    # Gets all visits from database
    visits = await lead_visits(lead_id)


    if visits:
        for visit in visits:
            visit_dict = dict(visit)
            visit_dict["created_at"] = jsonable_encoder(visit_dict["created_at"])
            json_visits.append(visit_dict)
        return json_visits

    json_visits.append({"error": "Invalid id"})
    return json_visits


    # end of normalizing