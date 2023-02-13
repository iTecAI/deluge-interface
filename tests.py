from deluge_interface import Deluge
from dotenv import load_dotenv
import os

load_dotenv()

deluge = Deluge(os.getenv("HOST"), os.getenv("PASSWORD"))
print(deluge.session_id)
print(deluge.methods)