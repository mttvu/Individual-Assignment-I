import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:root@localhost/deds_assignment1')

# get reviews from the database
reviews = None
connection = engine.raw_connection()
columns = []
cursor = connection.cursor()
# call stored procedure
cursor.callproc("GetAll")
for result in cursor.stored_results():
    # get columns 
    columns = [column[0] for column in result.description]
    print(columns)
    reviews = pd.DataFrame(result.fetchall())
    reviews.columns = columns

cursor.close()
connection.commit()
connection.close()

