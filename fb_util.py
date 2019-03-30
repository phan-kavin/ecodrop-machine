import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pathlib import Path

db = None

def init():
	global db

	base_path = Path(__file__).parent
	key_path = (base_path / "./security/ecodrop-key.json").resolve()

	# use a service account
	cred = credentials.Certificate(str(key_path))
	firebase_admin.initialize_app(cred)

	db = firestore.client()