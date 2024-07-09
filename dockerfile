FROM python:3
WORKDIR /app
COPY /src/api.py .
COPY /src/bd.py .
COPY /src/traccing.py .
COPY /src/bd-pkm-definition.sql .
COPY /src/pokemonsimple.csv .
COPY /src/requirements.txt .
RUN ls
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8689
CMD ["python","api.py"]
