FROM python:3
ENV TZ="Brazil/East"
WORKDIR /usr/src/Monitor_Preco_Buscape
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]