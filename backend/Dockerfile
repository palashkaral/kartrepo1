ROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r backend_requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "backend_app:superkart_api"]
