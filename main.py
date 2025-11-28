import logging
import sys
# from backend.logging import setup_logging
from config import Settings
from fastapi import FastAPI, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
# https://fastapi.tiangolo.com/advanced/custom-response/
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime, timezone

settings = Settings()

def setup_logging():
    """
    Configures the root logger and specific framework loggers
    to output to stdout.
    """
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()  # Clear existing handlers from previous setups (e.g., reloads)
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.LOG_LEVEL)
    
    print(f"--- Global log level set to {settings.LOG_LEVEL} ---")
    pass

setup_logging()
logger = logging.getLogger(__name__)

def now():
    return datetime.now(timezone.utc).isoformat()

app = FastAPI(title="FastAPI example")

@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    logger.debug("--- received request for /---")
    return {
        "response": "server is running",
        "timestamp": now(),
    }

@app.api_route("/ping", methods=["GET", "HEAD", "OPTIONS"])
async def ping():
    start_time = datetime.now(timezone.utc)
    logger.debug("--- request received at /ping ---")
    return {
        "status": "healthy",
        "response": "pong",
        "timestamp": now(),
        "response_time_ms": (datetime.now(timezone.utc) - start_time).total_seconds() * 1000,
    }


@app.api_route("/health", methods=["GET", "OPTIONS"])
async def health_check():
    start_time = datetime.now(timezone.utc)
    logger.debug("--- request received at /health ---")
    return {
        "status": "healthy",
        "timestamp": now(),
        "response_time_ms": (datetime.now(timezone.utc) - start_time).total_seconds() * 1000,
    }

#TODO: properly render HTML
@app.api_route("/html", methods=["GET", "POST"])
async def html_response():
    html_to_send = html_wrapper("some data")
    return html_to_send

#TODO: properly return HTML
def html_wrapper(input:Optional[str]):
    html = f"""<!DOCTYPE html>
    <html>
    <head>
    <title>wrapped html response</title>
    </head>

    <body>
    <h1>hello world!</h1>
    <p>{input}</p>
    </body>

    </html>"""
    return html


class Context:
    def __init__(self):
        self.user = None
        self.timestamp = None
        self.request_id = None

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        # access_log=True,
        # log_config=None,
    )