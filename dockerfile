FROM python:3
WORKDIR /app
COPY api.py .
COPY bd.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8689
CMD ["python","api.py"]
