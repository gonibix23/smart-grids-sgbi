FROM python:3.9-slim
WORKDIR /app
COPY api.py /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

# Ejecución
CMD ["python", "api.py"]