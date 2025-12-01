import uuid

from peewee import *
from playhouse.sqlite_ext import JSONField

db_proxy = DatabaseProxy()

class BaseModel(Model):
    class Meta:
        database = db_proxy

class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField()
    email_id = CharField()
    password = CharField()

    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)

class Income(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = CharField()
    income_type = CharField()
    amount = FloatField()
    description = CharField(null=True)
    created_at = DateTimeField()

    def save(self, *args, **kwargs):
        return super(Income, self).save(*args, **kwargs)

class Expenses(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = CharField()
    expense_type = CharField()
    amount = FloatField()
    description = CharField(null=True)
    created_at = DateTimeField()

    def save(self, *args, **kwargs):
        return super(Expenses, self).save(*args, **kwargs)

class Investments(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = CharField()
    investment_type = CharField()
    amount = FloatField()
    description = CharField(null=True)
    created_at = DateTimeField()

    def save(self, *args, **kwargs):
        return super(Investments, self).save(*args, **kwargs)

class Session(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = CharField()
    session_name = CharField(default="new-chat")

    def save(self, *args, **kwargs):
        return super(Session, self).save(*args, **kwargs)

class Chat(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    session_id = CharField(null=True)
    user_message = TextField(null=True)
    assistant_message = TextField(null=True)

    def save(self, *args, **kwargs):
        return super(Chat, self).save(*args, **kwargs)

def db_init():
    db = SqliteDatabase('finance-stock.db')
    db_proxy.initialize(db)
    db.connect()
    db.create_tables([User, Income, Expenses, Investments, Session, Chat])
    return db