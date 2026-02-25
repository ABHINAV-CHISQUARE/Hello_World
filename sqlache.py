import pandas as pd
from sqlalchemy import create_engine,text

db=create_engine("sqlite:///my_learning.db")

with db.begin() as con:
    con.execute(text("create table if not exists user (id integer,name text)"))
    con.execute(text("delete from users"))
    con.execute(text("insert into users(name,score) values('john',50),('emma',45)"))
df=pd.read_sql_table("users",db)
print(df)