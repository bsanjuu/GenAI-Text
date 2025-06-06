import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional, Dict, Any
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

class AWSConfig:
    """
    AWS configuration and client management
    """

    def __init__(self):
        self.region = settings.aws_region
        self.access_key_id = settings.aws_access_key_id
        self.secret_access_key = settings.aws_secret_access_key
        self.s3_bucket = settings.s3_bucket_name

        # Initialize clients
        self._s3_client = None
        self._dynamodb_client = None
        self._textract_client = None
        self._comprehend_client = None

    def _get_aws_session(self) -> boto3.Session:
        """
        Create AWS session with credentials

        Returns:
            Boto3 session
        """
        if self.access_key_id and self.secret_access_key:
            return boto3.Session(
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.region
            )
        else:
            # Use default credentials (IAM role, environment variables, etc.)
            return boto3.Session(region_name=self.region)

    @property
    def s3_client(self):
        """
        Get S3 client

        Returns:
            Boto3 S3 client
        """
        if not self._s3_client:
            try:
                session = self._get_aws_session()
                self._s3_client = session.client('s3')
                logger.info("S3 client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize S3 client: {str(e)}")
                self._s3_client = None

        return self._s3_client

    @property
    def dynamodb_client(self):
        """
        Get DynamoDB client

        Returns:
            Boto3 DynamoDB client
        """
        if not self._dynamodb_client:
            try:
                session = self._get_aws_session()
                self._dynamodb_client = session.client('dynamodb')
                logger.info("DynamoDB client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize DynamoDB client: {str(e)}")
                self._dynamodb_client = None

        return self._dynamodb_client

    @property
    def textract_client(self):
        """
        Get Textract client for document text extraction

        Returns:
            Boto3 Textract client
        """
        if not self._textract_client:
            try:
                session = self._get_aws_session()
                self._textract_client = session.client('textract')
                logger.info("Textract client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Textract client: {str(e)}")
                self._textract_client = None

        return self._textract_client

    @property
    def comprehend_client(self):
        """
        Get Comprehend client for text analysis

        Returns:
            Boto3 Comprehend client
        """
        if not self._comprehend_client:
            try:
                session = self._get_aws_session()
                self._comprehend_client = session.client('comprehend')
                logger.info("Comprehend client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Comprehend client: {str(e)}")
                self._comprehend_client = None

        return self._comprehend_client

    def test_connection(self) -> Dict[str, bool]:
        """
        Test AWS service connections

        Returns:
            Dictionary of service connection statuses
        """
        results = {
            's3': False,
            'dynamodb': False,
            'textract': False,
            'comprehend': False
        }

        # Test S3 connection
        try:
            if self.s3_client:
                self.s3_client.list_buckets()
                results['s3'] = True
                logger.info("S3 connection test passed")
        except Exception as e:
            logger.warning(f"S3 connection test failed: {str(e)}")

        # Test DynamoDB connection
        try:
            if self.dynamodb_client:
                self.dynamodb_client.list_tables()
                results['dynamodb'] = True
                logger.info("DynamoDB connection test passed")
        except Exception as e:
            logger.warning(f"DynamoDB connection test failed: {str(e)}")

        # Test Textract connection
        try:
            if self.textract_client:
                # Just check if we can make a basic call
                self.textract_client.detect_document_text(
                    Document={
                        'Bytes': b'test'
                    }
                )
        except ClientError as e:
            if e.response['Error']['Code'] in ['InvalidParameterException', 'InvalidDocumentException']:
                # These errors mean the service is reachable
                results['textract'] = True
                logger.info("Textract connection test passed")
        except Exception as e:
            logger.warning(f"Textract connection test failed: {str(e)}")

        # Test Comprehend connection
        try:
            if self.comprehend_client:
                # Test with minimal text
                self.comprehend_client.detect_sentiment(
                    Text='test',
                    LanguageCode='en'
                )
                results['comprehend'] = True
                logger.info("Comprehend connection test passed")
        except Exception as e:
            logger.warning(f"Comprehend connection test failed: {str(e)}")

        return results

    def upload_to_s3(self, file_content: bytes, key: str, content_type: str = None) -> bool:
        """
        Upload file to S3 bucket

        Args:
            file_content: File content as bytes
            key: S3 object key
            content_type: Content type of the file

        Returns:
            True if upload successful, False otherwise
        """
        if not self.s3_client or not self.s3_bucket:
            logger.error("S3 client or bucket not configured")
            return False

        try:
            upload_args = {'Bucket': self.s3_bucket, 'Key': key, 'Body': file_content}

            if content_type:
                upload_args['ContentType'] = content_type

            self.s3_client.put_object(**upload_args)
            logger.info(f"File uploaded to S3: {key}")
            return True

        except Exception as e:
            logger.error(f"Failed to upload to S3: {str(e)}")
            return False

    def download_from_s3(self, key: str) -> Optional[bytes]:
        """
        Download file from S3 bucket

        Args:
            key: S3 object key

        Returns:
            File content as bytes, or None if failed
        """
        if not self.s3_client or not self.s3_bucket:
            logger.error("S3 client or bucket not configured")
            return None

        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=key)
            return response['Body'].read()

        except Exception as e:
            logger.error(f"Failed to download from S3: {str(e)}")
            return None

    def delete_from_s3(self, key: str) -> bool:
        """
        Delete file from S3 bucket

        Args:
            key: S3 object key

        Returns:
            True if deletion successful, False otherwise
        """
        if not self.s3_client or not self.s3_bucket:
            logger.error("S3 client or bucket not configured")
            return False

        try:
            self.s3_client.delete_object(Bucket=self.s3_bucket, Key=key)
            logger.info(f"File deleted from S3: {key}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete from S3: {str(e)}")
            return False

# Create AWS config instance
aws_config = AWSConfig()