# Create our image based on Python 3.8
FROM python:3.8

# Expose ports
EXPOSE 5000

# Tell Python to not generate .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Turn off buffering
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libsndfile1 ffmpeg

# Install requirements using pip
ADD ./server/requirements.txt .
RUN python -m pip install -r requirements.txt

# Set working directory and addour Flask API files
WORKDIR /app
ENV DATA_PATH /app_data/
ADD ./server /app
ADD .env /app
ADD ./data /app_data

CMD python app.py
