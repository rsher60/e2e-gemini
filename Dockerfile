FROM python:3.10-slim

ENV PORT 8000
EXPOSE ${PORT}

WORKDIR /app

# Declare build arguments (only for local teting)
#ARG PROJECT_ID 
#ARG BUCKET_NAME

# Set environment variables using the build arguments (only for local testing)
#ENV PROJECT_ID=${PROJECT_ID}
#ENV BUCKET_NAME=${BUCKET_NAME}


COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000


# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]