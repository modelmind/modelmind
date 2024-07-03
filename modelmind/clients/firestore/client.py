import sys
from typing import Optional

from google.cloud import firestore

from modelmind.config import settings
from modelmind.logger import log


def initialize_firestore_client(database: Optional[str] = None) -> firestore.AsyncClient:
    if "pytest" in sys.argv[0]:
        from mockfirestore import MockFirestore

        return MockFirestore()

    selected_database = database or settings.firestore.database
    log.info("Initializing Firestore client with database: %s" % selected_database)
    return firestore.AsyncClient(database=selected_database)
