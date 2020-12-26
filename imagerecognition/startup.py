import pandas as pd
import sqlalchemy as sqla
import settings

def populate_db():
    df = pd.read_csv( settings.FILEPATH + "resources/animals.csv") 
    dfdata = pd.read_csv( settings.FILEPATH + "resources/urls.csv") 
    SQLALCHEMY_DATABASE_URL = settings.DB_URL
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