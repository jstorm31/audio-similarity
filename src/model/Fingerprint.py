from mongoengine import *


class Fingerprint(Document):
    audiotrack = ReferenceField('Audiotrack', required=True)
    type = StringField(required=True)
    data = BinaryField()
    meta = {'allow_inheritance': True}
