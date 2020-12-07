import sqlalchemy as sqla
import pandas as pd
import uuid 
import settings

connectionstring = settings.DB_URL

def get_url(url):
    SQLALCHEMY_DATABASE_URL = connectionstring
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)
    connection = engine.connect()
    query = 'select * from urls where url = "' + url + '";'
    ResultProxy = connection.execute(query)
    Result = ResultProxy.fetchone()
    return Result

def create_url(animal, picture, plot):
    url = uuid.uuid4().hex[:10].upper()
    SQLALCHEMY_DATABASE_URL = connectionstring
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)
    connection = engine.connect()
    query = 'insert into imagerecog.urls (url, result, picturepath, plotdata) VALUES ("' + url + '", "' + animal + '", "' + picture + '", "' + plot + '");'
    connection.execute(query)
    return url
