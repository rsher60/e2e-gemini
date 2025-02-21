1) When you build the image, you need to build it with arguments for security


docker build --build-arg PROJECT_ID="copper-index-447603-b3" --build-arg BUCKET_NAME="ai-image-cloudfn" -t serverless-app .


docker run -p 8000:8000 \
-v /Users/riddhimansherlekar/.config/gcloud/application_default_credentials.json:/app/gcp_credentials.json \
-e GOOGLE_APPLICATION_CREDENTIALS=/app/gcp_credentials.json  serverless-app
