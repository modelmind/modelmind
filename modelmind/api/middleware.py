from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["modelmind.com", "localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_middlewares(app: FastAPI) -> None:
    setup_cors(app)
