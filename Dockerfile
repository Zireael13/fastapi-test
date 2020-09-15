FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# set path to our python api file
ENV MODULE_NAME="server.main"

# copy contents of project into docker
COPY ./ /app

# install poetry
RUN pip install poetry

# disable virtualenv for poetry
RUN poetry config virtualenvs.create false

# install dependencies
RUN poetry install