import json
from weather.db import DB

db = DB('db.json')

db.add_user(15435233424345, 'John', 'Doe', 'johndoe')
