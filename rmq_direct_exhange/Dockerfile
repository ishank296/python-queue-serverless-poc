FROM python:3
WORKDIR /app
COPY . .
RUN cat requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD ["consumer.py"]

