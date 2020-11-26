FROM python:3.8
WORKDIR /app
COPY main.py /app
RUN pip install flask
RUN pip install prometheus_client
RUN pip install boto3
EXPOSE 6000
CMD ["python", "/app/main.py"]