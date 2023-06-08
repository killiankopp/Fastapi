FROM python:3.8

EXPOSE 81

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt && rm requirements.txt

COPY src .

CMD ["uvicorn", "main:api", "--port", "81"]