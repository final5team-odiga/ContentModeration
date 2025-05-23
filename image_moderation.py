import os
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData, ImageCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.storage.blob import BlobServiceClient

load_dotenv(dotenv_path='D:\Microsoft AI School\Project 3\Content Safety\.env', override=True)

def analyze_image():
    key = os.getenv("CONTENT_SAFETY_KEY")
    endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")
    # connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    image_path = os.path.join("D:\Microsoft AI School\Project 3\Content Safety\sample_image", "eduardo-juhyun-kim-Xyhn1VUlOOg-unsplash.jpg")

    # Create an Azure AI Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Create the BlobServiceClient object
    # blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Build request
    with open(image_path, "rb") as file:
        request = AnalyzeImageOptions(image=ImageData(content=file.read()))

    # Analyze image
    try:
        response = client.analyze_image(request)
    except HttpResponseError as e:
        print("Analyze image failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    hate_result = next(item for item in response.categories_analysis if item.category == ImageCategory.HATE)
    self_harm_result = next(item for item in response.categories_analysis if item.category == ImageCategory.SELF_HARM)
    sexual_result = next(item for item in response.categories_analysis if item.category == ImageCategory.SEXUAL)
    violence_result = next(item for item in response.categories_analysis if item.category == ImageCategory.VIOLENCE)

    if hate_result:
        print(f"Hate severity: {hate_result.severity}")
    if self_harm_result:
        print(f"SelfHarm severity: {self_harm_result.severity}")
    if sexual_result:
        print(f"Sexual severity: {sexual_result.severity}")
    if violence_result:
        print(f"Violence severity: {violence_result.severity}")

if __name__ == "__main__":
    analyze_image()