FROM python:3.9-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY environments/requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]