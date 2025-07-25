#importa python
FROM python:3.9

#diretorio de trabalho
WORKDIR /ml


COPY ./requirements.txt /ml/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /ml/requirements.txt


COPY ./app /ml/app


EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000" , "--reload"]