from fastapi import Depends, FastAPI, UploadFile, File, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from database.conection import connect_to_database
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
# Models
from app.models import Client, Image
from typing import Union
#Classifier
from tensorflow.keras.preprocessing.image import load_img

import numpy as np
from keras.models import load_model

# Tools
import shutil

# Mocks
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


# Login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

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

def fake_hash_password(password: str):
    return "fakehashed" + password

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# 1. Define an API object
app = FastAPI()
# Security
client_pydantic = pydantic_model_creator(Client)

image_pydantic = pydantic_model_creator(Image)

# 2. Define data type
class Msg(BaseModel):
    msg: str


# 3. Map HTTP method and path to python function
@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to the API home page!"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    try:
        contents = file.file.read()
        with open(file_location, 'wb') as f:
            f.write(contents)
        model = load_model('model_saved.h5')
  
        image = load_img(file_location, target_size=(224, 224))
        #image = load_img('v_data/test/planes/5.jpg', target_size=(224, 224))
        img = np.array(image)
        img = img / 255.0
        img = img.reshape(1,224,224,3)
        label = model.predict(img)
        # Improve classifier results
        if label > 0.5:
            result = "plane"
            category = 1
        else:
            result = "car"
            category = 2
        client = await client_pydantic.from_queryset_single(Client.get(id=1))
        print(client)
        # Add log
        print(f"You Submitted a {result} photo")
        moved_message = f"Once classifed the photo will be moved to the /{result} folder"
        # Generate the new url once classifed
        file_location_category = f"files/{result}/{file.filename}"
        shutil.move(file_location, file_location_category)
        image = await Image.create(url=file_location, description=result, category=category, client_id=client.id)
    
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"upload_message": f"Successfully uploaded {file.filename}", "classifier_result": result, "file_message": moved_message}

# !uvicorn main:app --reload

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)