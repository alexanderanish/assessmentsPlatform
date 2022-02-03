# build python image
FROM python:3.9

# create working dir in docker
WORKDIR /code

# copy requirements 
COPY ./requirements.txt /code/requirements.txt

# install packages
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy backend code
COPY ./app /code/app

COPY ./main.py /code/main.py

# run server
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]
