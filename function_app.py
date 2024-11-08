import logging
import io
import azure.functions as func
import azurefunctions.extensions.bindings.blob as blob

from resources.predict import predict_image

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.blob_trigger(
    arg_name="client", path="raw", connection="AzureWebJobsStorage"
)
@app.cosmos_db_output(arg_name="documents", 
                      database_name="image_prediction",
                      collection_name="mace",
                      create_if_not_exists=True,
                      connection_string_setting="CosmosDBConnectionString")
def predict(client: blob.BlobClient, documents: func.Out[func.Document]):
    blob_metadata = client.get_blob_properties()
    blob_content = client.download_blob().read()
    logging.info(
        f"Python blob trigger function processed blob {blob_metadata} \n"
        # f"Properties: {blob_content}\n"
    )

    blob_prediction = predict_image(io.BytesIO(blob_content))

    blob_id = str(client._blobName).split('.')[0]

    cosmos_doc_dict = {
        'id' :  blob_id,
        'url' : client.url,
        'prediction_results' : blob_prediction
    }

    documents.set(func.Document.from_dict(cosmos_doc_dict))

    logging.info(
        f"Blob prediction results {blob_prediction}"
    )

