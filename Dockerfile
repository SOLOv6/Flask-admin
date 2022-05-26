# Base Image
FROM  python:3.9

# Move to flask-admin directory
WORKDIR /flask-admin

# Copy dependency packages
COPY ./requirements.txt requirements.txt

# Install dependency packages
RUN pip install -r requirements.txt
RUN pip install gunicorn==20.1.0

# Copy all files
COPY . .

# Open 8080 port
EXPOSE 8080

# Execute gunicorn
CMD gunicorn --bind :8080 --workers 2 --threads 8 'project:create_app()'