FROM python:3.9

WORKDIR /code

COPY ./requirements0722.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

EXPOSE 8080

CMD ["uvicorn", "fast:app", "--host", "0.0.0.0", "--port", "8080"]