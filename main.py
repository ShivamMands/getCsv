from fastapi.responses import StreamingResponse
import io
from typing import Union
from fastapi import Body,Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import pandas as pd
import uvicorn ##ASGI       For Asynchronous Server Gateway Interface
from fastapi import FastAPI, Request
import csv
from flask import Flask, render_template, Response

# app = FastAPI()
#
#
# fake_users_db = {
#     "idgdev1": {
#         "username": "idgdev1",
#         "full_name": "Akanksh Belchada",
#         "email": "akanksh@t.digital",
#         "hashed_password": "fakehashedinsideidgsecret10!",
#         "disabled": False,
#     },
#     "idgdev2": {
#         "username": "idgdev2",
#         "full_name": "Allama Hossain",
#         "email": "allama@t.digital",
#         "hashed_password": "fakehashedinsideidgsecret11!",
#         "disabled": True,
#     },
# }
#
app = FastAPI()
# # app = FastAPI(
# #     title="idg-data-receiver",
# #     version=0.1,
# #     root_path="/dev/"
# # )
#
# def fake_hash_password(password: str):
#     return "fakehashed" + password
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
#
# class User(BaseModel):
#     username: str
#     email: Union[str, None] = None
#     full_name: Union[str, None] = None
#     disabled: Union[bool, None] = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

@app.get('/')
def home(request: Request):
    # return {"This is the idg-data-server @ Thanawalla Digital"}
  return {"message": "Hello World", "root_path": request.scope.get("root_path")}

# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}


# @app.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
#
# # @app.post("/accept-idg-payload")
# # async def get_body(request: Request):
# #     return await request.json()
t_host = "ec2-44-206-117-24.compute-1.amazonaws.com"  # either "localhost", a domain name, or an IP address.
t_port = "5432"  # default postgres port
t_dbname = "d5knigjrb5pdph"
t_user = "euxqqreycxujvt"
t_pw = "6fb679bd22aec45667687c79a3e4ed958c81cf584b489302a1bb38a9fe397469"



@app.get("/get_csv")
async def get_csv():
    s = 'SELECT * FROM "leads"'
    try:
        db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
        db_cursor = db_conn.cursor()
        db_cursor.execute(s)
        column_names = [desc[0] for desc in db_cursor.description]
        leadlist = db_cursor.fetchall()
        ourData = []
        for x in leadlist:
            listing = [x[0], x[1], x[2]]
            ourData.append(listing)

        with open('crypto.csv', "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(column_names)
            writer.writerows(ourData)

        with open("crypto.csv") as fp:
            newCsv = fp.read()

        return Response(
            newCsv,
            mimetype="text/csv",
            headers={"Content-disposition":
                         "attachment; filename=leads.csv"})
    except Exception as e:
        print(e)


import psycopg2

if __name__ == '__main__':
    print("Here")
    uvicorn.run(app, host='127.0.0.1', port=8000)

 
