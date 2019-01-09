FROM python:alpine3.7

# Set any env values we need
EXPOSE 5000
ENV PYTHONPATH=/app

# Copy the app files into the container
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN mkdir -p ./data

# Install all required modules
RUN apk update && apk add curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3
RUN poetry install

# Start the gunicorn service to run the app
RUN chmod +x ./run-gunicorn.sh
ENTRYPOINT ["sh", "./run-gunicorn.sh" ]
