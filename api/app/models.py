from tortoise.models import Model
from tortoise import fields


class Client(Model):
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Image(Model):
    client = fields.ForeignKeyField('models.Client', related_name='clients')
    url = fields.CharField(max_length=255)
    category = fields.IntField()
    description = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name

