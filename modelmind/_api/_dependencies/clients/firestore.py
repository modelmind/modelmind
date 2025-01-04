from fastapi import Request
from google.cloud import firestore


def get_firestore_client(request: Request) -> firestore.AsyncClient:
    return request.app.state.firestore
