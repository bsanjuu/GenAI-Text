import json
import boto3
import os
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import numpy as np

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3 = boto3.client('s3')

# Environment variables
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'text-summarization-output')
MODEL_PATH = os.environ.get('MODEL_PATH', '/tmp/model')
DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL', 'facebook/bart-large-cnn')
MAX_LENGTH = int(os.environ.get('MAX_LENGTH', '150'))
MIN_LENGTH = int(os.environ.get('MIN_LENGTH', '40'))

# Create /tmp/model directory if it doesn't exist
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

# Initialize the model and tokenizer
tokenizer = None
model = None
summarizer = None

def load_model():
    global tokenizer, model, summarizer

    try:
        logger.info(f"Loading model {DEFAULT_MODEL}")
        # Load model and tokenizer from Hugging Face
        tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL, cache_dir=MODEL_PATH)
        model = AutoModelForSeq2SeqLM.from_pretrained(DEFAULT_MODEL, cache_dir=MODEL_PATH)

        # Initialize the summarization pipeline
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
        logger.info("Model loaded successfully")

    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise e

def generate_summary(text, max_length=MAX_LENGTH, min_length=MIN_LENGTH):
    """
    Generate a summary of the input text using the transformer model
    """
    # Ensure the model is loaded
    if summarizer is None:
        load_model()

    try:
        # Split long text into chunks if needed (transformer models have input limits)
        if len(text) > 10000:
            logger.info("Text is too long, truncating...")
            text = text[:10000]  # Simple truncation; could implement smarter chunking

        # Generate summary
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)

        return summary[0]['summary_text']

    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise e

def save_summary(document_id, original_text, summary, source_bucket):
    """
    Save the summary to S3
    """
    try:
        # Create a result object with original text and summary
        result = {
            'document_id': document_id,
            'source_bucket': source_bucket,
            'original_text': original_text,
            'summary': summary,
            'timestamp': str(s3.head_object(Bucket=source_bucket, Key=document_id)['LastModified'])
        }

        # Save to S3
        output_key = f"summaries/{document_id.split('/')[-1]}.json"
        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=json.dumps(result),
            ContentType='application/json'
        )

        logger.info(f"Summary saved to s3://{OUTPUT_BUCKET}/{output_key}")
        return output_key

    except Exception as e:
        logger.error(f"Error saving summary: {str(e)}")
        raise e

def lambda_handler(event, context):
    """
    Process text and generate a summary
    """
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        # Extract text and document info from the event
        text = event.get('text')
        document_id = event.get('document_id')
        source_bucket = event.get('source_bucket')

        if not text or not document_id:
            raise ValueError("Missing required parameters: text and document_id")

        # Generate summary
        summary = generate_summary(text)

        # Save summary to S3
        output_key = save_summary(document_id, text, summary, source_bucket)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Summary generated successfully',
                'document_id': document_id,
                'output_key': output_key
            })
        }

    except Exception as e:
        logger.error(f"Error in summarization lambda: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error generating summary: {str(e)}'
            })
        }
