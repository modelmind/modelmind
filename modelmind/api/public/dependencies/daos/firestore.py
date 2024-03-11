import logging
import sys

from google.cloud import firestore

from modelmind.config import settings


def initialize_firestore_client() -> firestore.AsyncClient:
    if "pytest" in sys.argv[0]:
        from mockfirestore import MockFirestore

        return MockFirestore()
    logging.info("Initializing Firestore client with database: %s", settings.firestore.database)
    return firestore.AsyncClient(database=settings.firestore.database)


firestore_client = initialize_firestore_client()


def get_firestore_client() -> firestore.AsyncClient:
    return firestore_client
