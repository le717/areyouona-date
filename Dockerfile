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
RUN pip3 install --upgrade pip
RUN python3 ./get_requirements.py
RUN pip3 install --no-cache-dir -r requirements.txt
RUN rm ./requirements.txt

# Start the gunicorn service to run the app
RUN chmod +x ./run-gunicorn.sh
ENTRYPOINT ["sh", "./run-gunicorn.sh" ]
