# AI disclosure:

# I used ChatGPT as a learning assistant to understand FastAPI, Jinja2, 
# request objects, debbuging, and general backend syntax

# Use case example: "What is the Request from FastAPI and when should I use it?"
# or 
# "How do i render a template using Jinja2 and FastAPI?"

# most AI use cases were explanation questions for my doubts after reading the documentation on external libraries or python syntax

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# response_class tip from FastAPI documentation
# and modification of the FastAPI example for Jinja2 templates
# https://fastapi.tiangolo.com/advanced/templates/#using-jinja2templates

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    client = {"name": "La Fleur", "subname": "Bistro Frances", "id": "lafleurbistro", "primary_color": "#512828", "secondary_color": "white", "text-color": "white"}
    logo_path = "/static/resources/images/" + client["id"] + ".png"

    return templates.TemplateResponse(
        request=request,
        name="login.html", 
        context= {"client_name": client["name"], "client_subname": client["subname"], "logo": logo_path, "primary_color": client["primary_color"], "secondary_color": client["secondary_color"], "text-color": client["text-color"]   }
    )
