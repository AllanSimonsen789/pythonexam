import sqlalchemy as sqla
import pandas as pd
import uuid 
import settings

connectionstring = settings.DB_URL

def get_url_data(url):
    SQLALCHEMY_DATABASE_URL = connectionstring
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)
    connection = engine.connect()
    query = 'select * from urls where url = "' + url + '";'
    ResultProxy = connection.execute(query)
    Result = ResultProxy.fetchone()
    return Result

def create_url(picture, resultvgg, plotvgg, resultmanual, plotmanual):
    url = uuid.uuid4().hex[:10].upper()
    SQLALCHEMY_DATABASE_URL = connectionstring
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)
    connection = engine.connect()
    query = 'insert into imagerecog.urls (url, picturepath, resultmanual, plotdatamanual, resultvgg, plotdatavgg) VALUES("' + url + '", "' + picture + '", "' + resultmanual + '", "' + plotmanual + '", "' + resultvgg + '", "' + plotvgg + '");'
    connection.execute(query)
    return url
