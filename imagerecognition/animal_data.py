import sqlalchemy as sqla
import settings

connectionstring = settings.DB_URL

def get_Animal_funfact(animal):
    SQLALCHEMY_DATABASE_URL = connectionstring
    engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL)
    connection = engine.connect()
    query = 'select * from animals where AnimalName = "' + animal + '";'
    ResultProxy = connection.execute(query)
    Result = ResultProxy.fetchone()
    return Result[2]