from peewee import *
from config import DB_URL

db = SqliteDatabase(DB_URL)


class Person(Model):
    userid = CharField(unique=True)

    class Meta:
        database = db


class Ticker(Model):
    user = ForeignKeyField(Person, backref='tickers')
    name = CharField()

    class Meta:
        database = db


def initialize_db():
    db.connect()
    db.create_tables([Person, Ticker], safe=True)
    db.close()


def add_person(userid):
    try:
        Person.create(userid=userid)
    except IntegrityError:
        pass

def get_person(userid):
    try:
        person = Person.get(Person.userid == userid)
        return person
    except DoesNotExist:
        return None



def add_ticker(userid, name):
    if Ticker.select().where(Ticker.user == userid, Ticker.name == name).count() > 0:
        return
    try:
        print(userid)
        person = Person.get(Person.userid == userid)
        Ticker.create(user=person, name=name)
    except IntegrityError:
        pass


def get_tickers(userid):
    try:
        person = Person.get(Person.userid == userid)
        return [ticker.name for ticker in person.tickers]
    except DoesNotExist:
        return []

def remove_ticker(userid, name):
    try:
        person = Person.get(Person.userid == userid)
        ticker = Ticker.get(Ticker.user == person, Ticker.name == name)
        ticker.delete_instance()
    except DoesNotExist:
        pass