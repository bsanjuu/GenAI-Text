import json
import boto3
import os
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3 = boto3.client('s3')

# Environment variables
FEEDBACK_BUCKET = os.environ.get('FEEDBACK_BUCKET', 'text-summarization-feedback')
TRIGGER_RETRAINING = os.environ.get('TRIGGER_RETRAINING', 'false').lower() == 'true'

def lambda_handler(event, context):
    """
    Collect and store user feedback on summaries
    This feedback will be used to improve model accuracy through continuous learning
    """
    logger.info(f"Received feedback event: {json.dumps(event)}")

    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))

        # Extract feedback data
        document_id = body.get('document_id')
        summary_id = body.get('summary_id')
        rating = body.get('rating')  # e.g., 1-5 scale
        feedback_text = body.get('feedback_text', '')  # Optional user comments
        original_summary = body.get('original_summary', '')
        user_edited_summary = body.get('user_edited_summary', '')  # If user provided improved summary

        # Validate required fields
        if not all([document_id, summary_id, rating]):
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Missing required fields: document_id, summary_id, and rating are required'
                })
            }

        # Create feedback record
        feedback = {
            'document_id': document_id,
            'summary_id': summary_id,
            'rating': rating,
            'feedback_text': feedback_text,
            'original_summary': original_summary,
            'user_edited_summary': user_edited_summary,
            'timestamp': datetime.utcnow().isoformat()
        }

        # Determine storage path based on positive/negative feedback
        feedback_type = 'positive' if int(rating) >= 3 else 'negative'
        feedback_key = f"{feedback_type}/{document_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"

        # Store feedback in S3
        s3.put_object(
            Bucket=FEEDBACK_BUCKET,
            Key=feedback_key,
            Body=json.dumps(feedback),
            ContentType='application/json'
        )

        logger.info(f"Feedback saved to s3://{FEEDBACK_BUCKET}/{feedback_key}")

        # Trigger model retraining if configured (could invoke another Lambda or step function)
        if TRIGGER_RETRAINING:
            logger.info("Triggering model retraining workflow")
            # Implementation would depend on your training pipeline
            # Example: invoke a Step Function or Lambda to coordinate training

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': 'Feedback collected successfully',
                'feedback_id': feedback_key
            })
        }

    except Exception as e:
        logger.error(f"Error collecting feedback: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': f'Error processing feedback: {str(e)}'
            })
        }
