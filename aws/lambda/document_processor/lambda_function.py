import json
import boto3
import os
import logging
from urllib.parse import unquote_plus

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')

# Environment variables
SUMMARIZATION_FUNCTION = os.environ.get('SUMMARIZATION_FUNCTION', 'text-summarization-tool-summarization')
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'text-summarization-output')

def extract_text_from_document(bucket, key):
    """
    Extract text content from uploaded document
    Currently supports plain text files
    Could be extended to support PDF, DOCX, etc.
    """
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        text_content = response['Body'].read().decode('utf-8')
        logger.info(f"Successfully extracted text from {key}")
        return text_content
    except Exception as e:
        logger.error(f"Error extracting text from {key}: {str(e)}")
        raise e

def lambda_handler(event, context):
    """
    Process documents uploaded to S3
    1. Extract text from document
    2. Invoke summarization Lambda asynchronously
    """
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        # Get the S3 bucket and object key from the event
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])

            # Extract text from document
            text_content = extract_text_from_document(bucket, key)

            # Prepare payload for summarization Lambda
            payload = {
                'text': text_content,
                'document_id': key,
                'source_bucket': bucket
            }

            # Invoke summarization Lambda
            logger.info(f"Invoking summarization Lambda for document {key}")
            lambda_client.invoke(
                FunctionName=SUMMARIZATION_FUNCTION,
                InvocationType='Event',  # asynchronous
                Payload=json.dumps(payload)
            )

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': f'Document processing initiated for {key}',
                    'document_id': key
                })
            }

    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error processing document: {str(e)}'
            })
        }
