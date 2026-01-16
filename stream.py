from random import random
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from config import Settings

settings = Settings()

app = FastAPI(title="stream ex")


async def stream_generator() -> AsyncGenerator:
    array_ex = ["some", "strings", "are", "longer than others", "."]
    for i in array_ex:
        yield i


async def slow_logic(gen: AsyncGenerator) -> AsyncGenerator:
    from time import sleep
    import asyncio

    async for i in gen:
        await asyncio.sleep(random() * 4)
        yield i + " "


@app.api_route("/stream", methods=["GET"])
async def stream_ex():
    gen = stream_generator()
    modded = slow_logic(gen)
    return StreamingResponse(modded)


@app.get("/")
def home():
    return JSONResponse("hello")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("stream:app", reload=True)
