## My connection string


import logging
import requests
import azure.functions as func
from azure.storage.blob import BlobClient
import os
from dotenv import load_dotenv


# Load the .env file
load_dotenv()
my_con_string = os.getenv("AZURE_CONNECTION_STRING")


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python timer trigger function processed a request.")

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,el;q=0.8,fr;q=0.7",
        "Connection": "keep-alive",
        "Dnt": "1",
        "Host": "ponip.fina.hr",
        "Referer": "https://ponip.fina.hr/ocevidnik-web/",
        "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }

    url = "https://ponip.fina.hr/ocevidnik-web/preuzmi/csv"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # You can replace the connection string and container name with your values
        blob_conn_str = my_con_string
        container_name = "csv-storing"
        blob_name = "ponip_ocevidnik.csv"

        blob_client = BlobClient.from_connection_string(
            blob_conn_str, container_name, blob_name
        )
        blob_client.upload_blob(response.content, overwrite=True)

        logging.info("CSV file uploaded to Azure Blob Storage successfully!")
        return func.HttpResponse(
            "CSV file uploaded to Azure Blob Storage successfully!", status_code=200
        )
    else:
        logging.error("Failed to download the CSV.")
        return func.HttpResponse("Failed to download the CSV.", status_code=500)
