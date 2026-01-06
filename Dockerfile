FROM python:3.13.11-slim

WORKDIR /var/task

RUN pip install awslambdaric

COPY main.py .

ENTRYPOINT ["python", "-m", "awslambdaric"]
CMD ["main.lambda_handler"]