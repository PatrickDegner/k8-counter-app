from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

BACKEND_URL = "http://backend-service:80/"  

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        response = requests.get(BACKEND_URL)
        response.raise_for_status()
        data = response.json()

        backend_hostname = data.get("Hostname", "Unknown Backend Hostname")
        hit_counter = data.get("Counter", 0)
        frontend_hostname = os.environ.get('HOSTNAME', 'Unknown Frontend Hostname') 

        return templates.TemplateResponse("index.html", {
            "request": request, 
            "hit_counter": hit_counter, 
            "backend_hostname": backend_hostname,
            "frontend_hostname": frontend_hostname
        })

    except requests.exceptions.RequestException as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)