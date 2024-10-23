import logging
import io
import azure.functions as func
import azurefunctions.extensions.bindings.blob as blob

from resources.predict import predict_image

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.blob_trigger(
    arg_name="client", path="raw", connection="AzureWebJobsStorage"
)
def blob_trigger(client: blob.BlobClient):
    blob_metadata = client.get_blob_properties()
    blob_content = client.download_blob().read()
    logging.info(
        f"Python blob trigger function processed blob {blob_metadata} \n"
        # f"Properties: {blob_content}\n"
    )

    blob_prediction = predict_image(io.BytesIO(blob_content))

    logging.info(
        f"Blob prediction results {blob_prediction}"
    )

