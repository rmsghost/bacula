FROM python:3
WORKDIR /app
COPY api.py .
COPY bd.py .
COPY traccing.py .
COPY bd-pkm-definition.sql .
COPY pokemonsimple.csv .
COPY requirements.txt .
COPY templates/ ./templates
RUN ls
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8689
CMD ["python","api.py"]
