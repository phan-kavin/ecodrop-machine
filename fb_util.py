import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pathlib import Path

db = None
users_coll = None

class User:
	def __init__(self, campus_id, f_name, l_name, points):
		self.campus_id = campus_id
		self.f_name = f_name
		self.l_name = l_name
		self.points = points
	
	@staticmethod
	def from_dict(src):
		return User(
			src["campus_id"], src["f_name"], src["l_name"], src["points"]
		)
	
	def to_dict(self):
		return {
			"campus_id": self.campus_id, "f_name": self.f_name, "l_name": self.l_name, "points": self.points
		}

	def __repr__(self):
		return(
			"User(campus_id={}, f_name={}, l_name={}, points={})".format(
				self.campus_id, self.f_name, self.l_name, self.points
			)
		)

def init():
	global db, users_coll

	base_path = Path(__file__).parent
	key_path = (base_path / "./security/ecodrop-key.json").resolve()

	# use a service account
	cred = credentials.Certificate(str(key_path))
	firebase_admin.initialize_app(cred)

	db = firestore.client()
	users_coll = db.collection("users")

# TODO add try-catch
def get_user(iso):
	user_doc_ref = users_coll.document(iso)
	user_doc = user_doc_ref.get()
	user_obj = User.from_dict(user_doc.to_dict())

	return user_obj

def add_points_iso(iso, user, points):
	user_dict = user.to_dict()
	user_doc_ref = users_coll.document(iso)

	user_dict["points"] += points
	user_doc_ref.set(user_dict)