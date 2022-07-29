from fastapi.responses import StreamingResponse
import io
from typing import Union
from fastapi import Body,Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import pandas as pd
import uvicorn ##ASGI       For Asynchronous Server Gateway Interface
from fastapi import FastAPI, Request

app = FastAPI()


fake_users_db = {
    "idgdev1": {
        "username": "idgdev1",
        "full_name": "Akanksh Belchada",
        "email": "akanksh@t.digital",
        "hashed_password": "fakehashedinsideidgsecret10!",
        "disabled": False,
    },
    "idgdev2": {
        "username": "idgdev2",
        "full_name": "Allama Hossain",
        "email": "allama@t.digital",
        "hashed_password": "fakehashedinsideidgsecret11!",
        "disabled": True,
    },
}

app = FastAPI()
# app = FastAPI(
#     title="idg-data-receiver",
#     version=0.1,
#     root_path="/dev/"
# )

def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get('/')
def home(request: Request):
    # return {"This is the idg-data-server @ Thanawalla Digital"}
  return {"message": "Hello World", "root_path": request.scope.get("root_path")}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# @app.post("/accept-idg-payload")
# async def get_body(request: Request):
#     return await request.json()


@app.get("/get_csv")
async def get_csv(current_user: User = Depends(get_current_active_user)):
    
       conn = psycopg2.connect(database="d2r45oj3jf7gs7",
                           host="ec2-44-205-97-79.compute-1.amazonaws.com",
                           user="ucrol25emqd2ch",
                           password="p31d791a3fe8bcb5b5102d7b8b43f08ca70ee2cc9d7943c23b4db6b110324346e",
                           port="5432")
       
       cursor = conn.cursor()
       s="SELECT * FROM pgadmin.\"Prospect\" where ZIP_CD='75080' "  #LIMIT 1000 #Million records

       try:
          cursor.execute(s)
       except (Exception, psycopg2.DatabaseError) as error:
          print("Error: %s" % error)
          cursor.close()
       tupples = cursor.fetchall()

       print("tupples: ",tupples)
      
      # We just need to turn it into a pandas dataframe
       df = pd.DataFrame(tupples)
    
       stream = io.StringIO()
    
       df.to_csv(stream, index = False)
    
       response = StreamingResponse(iter([stream.getvalue()]),
                            media_type="text/csv"
       )
    
       response.headers["Content-Disposition"] = "attachment; filename=export.csv"

       return response


import psycopg2

if __name__ == '__main__':
    print("Here")
    uvicorn.run(app, host='127.0.0.1', port=8000)

 
