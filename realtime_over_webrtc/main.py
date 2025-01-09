from logging import getLogger
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import autogen
from autogen.agentchat.realtime_agent import RealtimeAgent

realtime_config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "tags": ["gpt-4o-mini-realtime"],
    },
)

realtime_llm_config = {
    "timeout": 600,
    "config_list": realtime_config_list,
    "temperature": 0.8,
}

app = FastAPI()


@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "WebRTC AG2 Server is running!"}


website_files_path = Path(__file__).parent / "website_files"

app.mount(
    "/static", StaticFiles(directory=website_files_path / "static"), name="static"
)

# Templates for HTML responses

templates = Jinja2Templates(directory=website_files_path / "templates")


@app.get("/start-chat/", response_class=HTMLResponse)
async def start_chat(request: Request):
    """Endpoint to return the HTML page for audio chat."""
    port = request.url.port
    return templates.TemplateResponse("chat.html", {"request": request, "port": port})


@app.websocket("/session")
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections providing audio stream and OpenAI."""
    await websocket.accept()

    logger = getLogger("uvicorn.error")

    realtime_agent = RealtimeAgent(
        name="Weather Bot",
        system_message="Hello there! I am an AI voice assistant powered by AG2 and the OpenAI Realtime API. You can ask me about weather or the temperature. Start by saying 'AG2 here, how can I help you'? Keep responses brief, two short sentences maximum.",
        llm_config=realtime_llm_config,
        websocket=websocket,
        logger=logger,
    )

    @realtime_agent.register_realtime_function(  # type: ignore [misc]
        name="get_weather", description="Get the current weather"
    )
    def get_weather(location: Annotated[str, "city"]) -> str:
        weather = (
            "The weather is cloudy."
            if location == "Seattle"
            else "The weather is sunny."
        )
        logger.info(f"<-- Calling get_weather function for {location}, Weather: {weather} -->")
        return weather

    @realtime_agent.register_realtime_function(  # type: ignore [misc]
        name="get_temperature", description="Get the current temperature"
    )
    def get_temperature(location: Annotated[str, "city"]) -> str:
        temperature = (
            "16 Degrees Fareinheit"
            if location == "Seattle"
            else "30 Degrees Celsius"
        )
        logger.info(f"<-- Calling get_temperature function for {location}, Temperature: {temperature} -->")
        return temperature
    
    await realtime_agent.run()