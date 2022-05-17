from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv

load_dotenv()
mysql_user = os.environ.get("MYSQL_USER")
mysql_password = os.environ.get("MYSQL_PASSWORD")

# connect to mysql database using sqlalchemy and pymysql
engine = create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@localhost:3306/freddo_test')

meta = MetaData()
conn = engine.connect()