FROM python:3.8

# Set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/

# Install required packages
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

# Start Flask app along with .env settings
EXPOSE 5000
ENTRYPOINT ./bootstrap.sh