
from mongoengine import *


class Audiotrack(Document):
    filename = StringField(required=True)
    duration = FloatField(required=True)
