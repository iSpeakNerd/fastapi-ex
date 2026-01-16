from random import random
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from config import Settings

settings = Settings()

app = FastAPI(title="stream ex")

# Once a generator, always a generator until final usage
# pattern is
# async def api_response():
#   step1 = source_generator()
#   step2 = logic(step1)
#   .....
#   final_step = last_logic(penultimate_step)
#   return StreamingResponse(final_step)


async def stream_generator() -> AsyncGenerator:
    array_ex = ["some", "strings", "are", "longer than others", "."]
    for i in array_ex:
        yield i


async def slow_logic(gen: AsyncGenerator) -> AsyncGenerator:
    from time import sleep

    # display each chunk as we go instead of waiting for whole return
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
