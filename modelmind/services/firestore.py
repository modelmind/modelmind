import sys

from google.cloud import firestore

# Project ID is determined by the GCLOUD_PROJECT environment variable
if "pytest" in sys.argv[0]:
    # testing db
    from mockfirestore import MockFirestore

    firestore_client = MockFirestore()
else:
    # not a testing db
    firestore_client = firestore.Client()  # pragma: no cover
