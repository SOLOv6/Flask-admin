# Base Image
FROM  python:3.9

# Move to flask-admin directory
WORKDIR /flask-admin

# Copy dependency packages
COPY ./requirements.txt /flask-admin/requirements.txt

# Install dependency packages
RUN pip install -r requirements.txt
RUN pip install gunicorn==20.1.0

# Copy all files
COPY . /flask-admin

# Open 8080 port
EXPOSE 8080