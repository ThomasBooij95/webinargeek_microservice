# Use the official image as a parent image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install project dependencies using Poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Install the dependencies using pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code into the container
COPY . ./app/

CMD ["uvicorn","app.app.main:app","--port", "80","--host","0.0.0.0" ,"--log-level", "debug"]