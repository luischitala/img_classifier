from fastapi import FastAPI, UploadFile, File, HTTPException, status
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
# Models
from app.models import Client, Image
#Classifier
from tensorflow.keras.preprocessing.image import load_img

import numpy as np
from keras.models import load_model

# Tools
import shutil


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

"""
Endpoint para realizar la clasificación de imágenes
Recibe datos mediante form-data, el campo a enviar es "file"
Una vez realizda la clasificación, se guarda en un directorio interno
y escribe en una base de datos el resultado de la clasificación.
"""
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    try:
        contents = file.file.read()
        with open(file_location, 'wb') as f:
            f.write(contents)
        model = load_model('models/classifier.h5')
  
        image = load_img(file_location, target_size=(224, 224))
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
        moved_message = f"Image moved to /{result} folder"
        # Generate the new url once classifed
        file_location_category = f"files/{result}/{file.filename}"
        shutil.move(file_location, file_location_category)
        image = await Image.create(url=file_location, description=result, category=category, client_id=client.id)
    
    except Exception:
        data = {
            "status":status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "There was an error uploading the file", 
            "data":{}
        }
        raise HTTPException(status_code=500, detail=data)
    finally:
        file.file.close()
    
    data = {
        "classifier_result":result,
        "file_message":moved_message
    }

    return {"status":status.HTTP_200_OK,"message": f"Successfully uploaded {file.filename}", "data":data}


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)