from mongoengine import *

class Fingerprint(ABC, Document):
    audiotrack = ReferenceField('Audiotrack', required=True)
    type = StringField(required=True)
    data = BinaryField()
    meta = { 'allow_inheritance': True }
