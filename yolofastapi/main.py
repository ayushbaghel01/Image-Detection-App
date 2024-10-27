from uvicorn import Server, Config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import os

from routers import yolo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"],
)

app.include_router(yolo.router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to port 80 if not set
    config = Config(app, host="127.0.0.1", port=port, lifespan="on")
    server = Server(config)
    server.run()
