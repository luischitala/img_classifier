# Retrieve a basic python image
FROM python:3.9

# Select the workdir
WORKDIR /code

# Copy the requirements file

COPY /deployment/api/requirements.txt /code/requirements.txt

# Install the requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the required directories to compose and run the app 
COPY /* /code/
COPY /database /code/database
COPY /app /code/app
COPY /files /code/files
COPY /models /code/models


# Run the application 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]