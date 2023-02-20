"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
whiskey = User(first_name='Whiskey', last_name="Bandit", img_url="https://upload.wikimedia.org/wikipedia/commons/4/49/Jonathan_G_Meath_portrays_Santa_Claus.jpg")
bowser = User(first_name='Bowser', last_name="Bonger", img_url="https://upload.wikimedia.org/wikipedia/commons/4/49/Jonathan_G_Meath_portrays_Santa_Claus.jpg")
spike = User(first_name='Spike', last_name="Willow", img_url= None)

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()
