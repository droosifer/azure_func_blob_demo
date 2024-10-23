import logging

import azure.functions as func
import azurefunctions.extensions.bindings.blob as blob

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.blob_trigger(
    arg_name="client", path="raw", connection="AzureWebJobsStorage"
)
def blob_trigger(client: blob.BlobClient):
    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Properties: {client.get_blob_properties()}\n"
        f"Blob content head: {client.download_blob().read(size=1)}"
    )