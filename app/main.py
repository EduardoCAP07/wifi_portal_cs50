# AI disclosure:

# I used ChatGPT as a learning assistant to understand FastAPI, Jinja2, 
# request objects, debbuging, and general backend syntax

# Use case example: "What is the Request from FastAPI and when should I use it?"
# or 
# "How do i render a template using Jinja2 and FastAPI?"

# most AI use cases were explanation questions for my doubts after reading the documentation on external libraries or python syntax

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import phonenumbers

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

            return parsed_number
        
        
    except phonenumbers.NumberParseException:
        return None

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
def home(request: Request, phone: str = Form(...)):
    client = {"name": "La Fleur", "subname": "Bistro Frances", "id": "lafleurbistro", "primary_color": "#512828", "secondary_color": "white", "text-color": "white"}
    logo_path = "/static/resources/images/" + client["id"] + ".png"
    parsed_phone = phone_validation(phone)

    if parsed_phone:

        # render sucess page if phone is valid
        return templates.TemplateResponse(
                    request=request,
                    name="login.html",
                    context= {"client_name": client["name"], "client_subname": client["subname"], "logo": logo_path, "primary_color": client["primary_color"], "secondary_color": client["secondary_color"], "text_color": client["text-color"], "error": None}
                    )
    else:

        # render error in login page if phone is invalid
        return templates.TemplateResponse(
                    request=request,
                    name="login.html",
                    context= {"client_name": client["name"], "client_subname": client["subname"], "logo": logo_path, "primary_color": client["primary_color"], "secondary_color": client["secondary_color"], "text_color": client["text-color"], "error": "Invalid phonenumber"}
                    )

    