# init a base image (Alpine is small Linux distro)
FROM python:3.9


WORKDIR /code
# copy the contents into the working dir

COPY requirements.txt .

# run pip to install the dependencies of the flask app
RUN pip3 install -r requirements.txt


COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]