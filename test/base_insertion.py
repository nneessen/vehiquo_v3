
from .config import database_test_config


###
# Suport test for database insertions
###

engine = database_test_config.engine


def insert_into_users(input):
    ''' Insert input into users table '''
    
    with engine.connect() as con:
        
        statement = """INSERT INTO users (first_name, last_name, email, username, password, phone_number)
                       VALUES ('{first_name:s}', '{last_name:s}', '{email:s}', '{username:s}', '{password:s}', '{phone_number:s}')"""
        
        for line in input:
            con.execute(statement.format(**line))