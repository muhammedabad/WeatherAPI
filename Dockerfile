FROM python:3.11-slim

# Setup environment
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

# Copy the application
COPY . /code

# Install python packages as needed
RUN pip install -r requirements.txt

# Run the application
CMD ["sh", "/code/runserver.sh"]
