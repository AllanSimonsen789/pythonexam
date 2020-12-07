import sqlalchemy as sqla
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.cm as cm 
import numpy as np
import settings

connectionstring = settings.DB_URL

def populate_db():
    df = pd.read_csv("/home/jovyan/my_notebooks/imagerecognition/resources/animals.csv") 
    dfdata = pd.read_csv("/home/jovyan/my_notebooks/imagerecognition/resources/urls.csv") 
    SQLALCHEMY_DATABASE_URL = connectionstring
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)
    df.to_sql(
        "animals",
        engine,
        if_exists="replace",
        dtype={col_name: sqla.types.NVARCHAR(length=255) for col_name in df})
    dfdata.to_sql(
        "urls",
        engine,
        if_exists="replace",
        dtype={col_name: sqla.types.NVARCHAR(length=255) for col_name in df})

def get_animal(name):
    SQLALCHEMY_DATABASE_URL = connectionstring
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)
    connection = engine.connect()
    query = 'select * from animals where AnimalName = "' + name + '";'
    ResultProxy = connection.execute(query)
    Result = ResultProxy.fetchone()
    return Result[2]