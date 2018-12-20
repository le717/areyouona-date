FROM python:alpine3.6

# Set any env values we need
EXPOSE 5000

# Copy the app files into the container
COPY . ./

# Install all required modules
RUN pip3 install --upgrade pip
RUN python3 ./get_requirements.py
RUN pip3 install --no-cache-dir -r requirements.txt
RUN rm ./requirements.txt

# Start the gunicorn service to run the app
COPY run-gunicorn.sh /run-gunicorn.sh
RUN chmod +x /run-gunicorn.sh
ENTRYPOINT ["sh", "/run-gunicorn.sh" ]
