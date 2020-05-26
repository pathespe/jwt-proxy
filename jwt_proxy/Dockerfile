FROM python:3.8
COPY . /jwt_proxy
WORKDIR /jwt_proxy
RUN pip install -r ./jwt_proxy/requirements.txt
CMD ["python", "./jwt_proxy/app.py"]