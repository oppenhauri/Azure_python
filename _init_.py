import os
import urllib.request
from io import BytesIO
from PIL import Image
import azure.functions as func
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    image_url = req.params.get('url')
    if not image_url:
        return func.HttpResponse(
            "Please provide an image URL",
            status_code=400
        )
    
    # Download image
    image_data = urllib.request.urlopen(image_url).read()
    image = Image.open(BytesIO(image_data))
    
    # Process image
    # For example, convert an image to grayscale
    gray_image = image.convert('L')
    
    # Save images to Blob storage
    blob_service_client = BlobServiceClient.from_connection_string(os.environ['AzureWebJobsStorage'])
    container_client = blob_service_client.get_container_client("images")
    blob_client = container_client.get_blob_client("processed_image.jpg")
    
    with BytesIO() as output:
        gray_image.save(output, format="JPEG")
        output.seek(0)
        blob_client.upload_blob(output)
    
    return func.HttpResponse(
        "Processed image saved to Blob storage",
        status_code=200
    )
