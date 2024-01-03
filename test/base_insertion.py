from sqlalchemy.sql import text

from .config import database_test_config


###
# Suport test for database insertions
###

engine = database_test_config.engine







def insert_into_users(input):
    ''' Insert into table users '''
    with engine.connect() as con:

        data = (
            {
                "id": input["id"],
                "first_name": input["first_name"],
                "last_name": input["last_name"],
                "email": input["email"],
                "password": input["password"],
            },
        )


        statement = text(
            """INSERT INTO users (id, first_name, last_name, email, password) VALUES (:id, :first_name, :last_name, :email, :password)"""
        )

        for line in data:
            con.execute(statement, **line)