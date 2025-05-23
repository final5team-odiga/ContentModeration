import os
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.storage.blob import BlobServiceClient

load_dotenv(dotenv_path='D:\Microsoft AI School\Project 3\Content Safety\.env', override=True)

def analyze_text():
    # analyze text
    key = os.getenv("CONTENT_SAFETY_KEY")
    endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")
    # connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Create an Azure AI Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Create the BlobServiceClient object
    # blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Read user input
    userinput = ""    

    # Contruct request
    request = AnalyzeTextOptions(text=userinput)
    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    hate_result = next(item for item in response.categories_analysis if item.category == TextCategory.HATE)
    self_harm_result = next(item for item in response.categories_analysis if item.category == TextCategory.SELF_HARM)
    sexual_result = next(item for item in response.categories_analysis if item.category == TextCategory.SEXUAL)
    violence_result = next(item for item in response.categories_analysis if item.category == TextCategory.VIOLENCE)

    # Filter if result > 2 otherwise pass

    if hate_result:
        print(f"Hate severity: {hate_result.severity}")
    if self_harm_result:
        print(f"SelfHarm severity: {self_harm_result.severity}")
    if sexual_result:
        print(f"Sexual severity: {sexual_result.severity}")
    if violence_result:
        print(f"Violence severity: {violence_result.severity}")

if __name__ == "__main__":
    analyze_text()