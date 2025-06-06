import boto3
from botocore.exceptions import ClientError
from typing import Dict, List, Optional, Any
import json
import logging
from app.config.aws_config import aws_config

logger = logging.getLogger(__name__)

class TextractHelper:
    """
    Helper class for AWS Textract operations
    """

    @staticmethod
    def extract_text_from_document(document_bytes: bytes) -> str:
        """
        Extract text from a document using AWS Textract

        Args:
            document_bytes: Document content as bytes

        Returns:
            Extracted text
        """
        try:
            client = aws_config.textract_client
            if not client:
                raise Exception("Textract client not available")

            response = client.detect_document_text(
                Document={'Bytes': document_bytes}
            )

            # Extract text from response
            extracted_text = ""
            for block in response.get('Blocks', []):
                if block['BlockType'] == 'LINE':
                    extracted_text += block['Text'] + '\n'

            return extracted_text.strip()

        except Exception as e:
            logger.error(f"Textract text extraction failed: {str(e)}")
            return ""

    @staticmethod
    def extract_text_with_confidence(document_bytes: bytes, min_confidence: float = 80.0) -> Dict[str, Any]:
        """
        Extract text with confidence scores

        Args:
            document_bytes: Document content as bytes
            min_confidence: Minimum confidence threshold

        Returns:
            Dictionary with text and confidence information
        """
        try:
            client = aws_config.textract_client
            if not client:
                raise Exception("Textract client not available")

            response = client.detect_document_text(
                Document={'Bytes': document_bytes}
            )

            lines = []
            total_confidence = 0
            valid_blocks = 0

            for block in response.get('Blocks', []):
                if block['BlockType'] == 'LINE':
                    confidence = block.get('Confidence', 0)
                    if confidence >= min_confidence:
                        lines.append({
                            'text': block['Text'],
                            'confidence': confidence
                        })
                        total_confidence += confidence
                        valid_blocks += 1

            avg_confidence = total_confidence / valid_blocks if valid_blocks > 0 else 0
            extracted_text = '\n'.join([line['text'] for line in lines])

            return {
                'text': extracted_text,
                'average_confidence': avg_confidence,
                'total_lines': len(lines),
                'lines_with_confidence': lines
            }

        except Exception as e:
            logger.error(f"Textract text extraction with confidence failed: {str(e)}")
            return {
                'text': '',
                'average_confidence': 0,
                'total_lines': 0,
                'lines_with_confidence': []
            }

class ComprehendHelper:
    """
    Helper class for AWS Comprehend operations
    """

    @staticmethod
    def detect_language(text: str) -> Dict[str, Any]:
        """
        Detect the language of the text

        Args:
            text: Input text

        Returns:
            Language detection results
        """
        try:
            client = aws_config.comprehend_client
            if not client:
                raise Exception("Comprehend client not available")

            response = client.detect_dominant_language(Text=text[:5000])  # Limit to 5000 chars

            languages = response.get('Languages', [])
            if languages:
                primary_language = languages[0]
                return {
                    'language_code': primary_language['LanguageCode'],
                    'score': primary_language['Score'],
                    'all_languages': languages
                }

            return {'language_code': 'en', 'score': 0.0, 'all_languages': []}

        except Exception as e:
            logger.error(f"Language detection failed: {str(e)}")
            return {'language_code': 'en', 'score': 0.0, 'all_languages': []}

    @staticmethod
    def extract_key_phrases(text: str, language_code: str = 'en') -> List[Dict[str, Any]]:
        """
        Extract key phrases from text

        Args:
            text: Input text
            language_code: Language code

        Returns:
            List of key phrases with scores
        """
        try:
            client = aws_config.comprehend_client
            if not client:
                raise Exception("Comprehend client not available")

            response = client.detect_key_phrases(
                Text=text[:5000],  # Limit to 5000 chars
                LanguageCode=language_code
            )

            return response.get('KeyPhrases', [])

        except Exception as e:
            logger.error(f"Key phrase extraction failed: {str(e)}")
            return []

    @staticmethod
    def analyze_sentiment(text: str, language_code: str = 'en') -> Dict[str, Any]:
        """
        Analyze sentiment of the text

        Args:
            text: Input text
            language_code: Language code

        Returns:
            Sentiment analysis results
        """
        try:
            client = aws_config.comprehend_client
            if not client:
                raise Exception("Comprehend client not available")

            response = client.detect_sentiment(
                Text=text[:5000],  # Limit to 5000 chars
                LanguageCode=language_code
            )

            return {
                'sentiment': response.get('Sentiment', 'NEUTRAL'),
                'sentiment_score': response.get('SentimentScore', {}),
                'mixed_score': response.get('SentimentScore', {}).get('Mixed', 0),
                'positive_score': response.get('SentimentScore', {}).get('Positive', 0),
                'negative_score': response.get('SentimentScore', {}).get('Negative', 0),
                'neutral_score': response.get('SentimentScore', {}).get('Neutral', 0)
            }

        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            return {
                'sentiment': 'NEUTRAL',
                'sentiment_score': {},
                'mixed_score': 0,
                'positive_score': 0,
                'negative_score': 0,
                'neutral_score': 1
            }

    @staticmethod
    def detect_entities(text: str, language_code: str = 'en') -> List[Dict[str, Any]]:
        """
        Detect named entities in text

        Args:
            text: Input text
            language_code: Language code

        Returns:
            List of detected entities
        """
        try:
            client = aws_config.comprehend_client
            if not client:
                raise Exception("Comprehend client not available")

            response = client.detect_entities(
                Text=text[:5000],  # Limit to 5000 chars
                LanguageCode=language_code
            )

            return response.get('Entities', [])

        except Exception as e:
            logger.error(f"Entity detection failed: {str(e)}")
            return []

class S3Helper:
    """
    Helper class for S3 operations
    """

    @staticmethod
    def generate_presigned_url(
            key: str,
            expiration: int = 3600,
            operation: str = 'get_object'
    ) -> Optional[str]:
        """
        Generate a presigned URL for S3 object

        Args:
            key: S3 object key
            expiration: URL expiration time in seconds
            operation: S3 operation (get_object, put_object, etc.)

        Returns:
            Presigned URL or None if failed
        """
        try:
            client = aws_config.s3_client
            bucket = aws_config.s3_bucket

            if not client or not bucket:
                raise Exception("S3 client or bucket not configured")

            response = client.generate_presigned_url(
                operation,
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=expiration
            )

            return response

        except Exception as e:
            logger.error(f"Failed to generate presigned URL: {str(e)}")
            return None

    @staticmethod
    def list_objects(prefix: str = '', max_keys: int = 1000) -> List[Dict[str, Any]]:
        """
        List objects in S3 bucket

        Args:
            prefix: Object key prefix to filter
            max_keys: Maximum number of keys to return

        Returns:
            List of object information
        """
        try:
            client = aws_config.s3_client
            bucket = aws_config.s3_bucket

            if not client or not bucket:
                raise Exception("S3 client or bucket not configured")

            response = client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix,
                MaxKeys=max_keys
            )

            return response.get('Contents', [])

        except Exception as e:
            logger.error(f"Failed to list S3 objects: {str(e)}")
            return []

    @staticmethod
    def get_object_metadata(key: str) -> Dict[str, Any]:
        """
        Get S3 object metadata

        Args:
            key: S3 object key

        Returns:
            Object metadata
        """
        try:
            client = aws_config.s3_client
            bucket = aws_config.s3_bucket

            if not client or not bucket:
                raise Exception("S3 client or bucket not configured")

            response = client.head_object(Bucket=bucket, Key=key)

            return {
                'content_length': response.get('ContentLength', 0),
                'content_type': response.get('ContentType', ''),
                'last_modified': response.get('LastModified'),
                'etag': response.get('ETag', ''),
                'metadata': response.get('Metadata', {})
            }

        except Exception as e:
            logger.error(f"Failed to get S3 object metadata: {str(e)}")
            return {}

class DocumentProcessor:
    """
    Document processing using AWS services
    """

    @staticmethod
    def process_document(
            document_bytes: bytes,
            filename: str,
            extract_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Process a document using AWS services

        Args:
            document_bytes: Document content as bytes
            filename: Original filename
            extract_metadata: Whether to extract metadata

        Returns:
            Processing results
        """
        results = {
            'text': '',
            'language': 'en',
            'confidence': 0,
            'key_phrases': [],
            'sentiment': {},
            'entities': []
        }

        try:
            # Extract text using Textract
            if filename.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
                textract_result = TextractHelper.extract_text_with_confidence(document_bytes)
                results['text'] = textract_result['text']
                results['confidence'] = textract_result['average_confidence']
            else:
                # For text files, decode directly
                try:
                    results['text'] = document_bytes.decode('utf-8')
                    results['confidence'] = 100.0
                except UnicodeDecodeError:
                    results['text'] = document_bytes.decode('utf-8', errors='ignore')
                    results['confidence'] = 80.0

            if extract_metadata and results['text']:
                # Detect language
                lang_result = ComprehendHelper.detect_language(results['text'])
                results['language'] = lang_result['language_code']

                # Extract key phrases
                results['key_phrases'] = ComprehendHelper.extract_key_phrases(
                    results['text'], results['language']
                )

                # Analyze sentiment
                results['sentiment'] = ComprehendHelper.analyze_sentiment(
                    results['text'], results['language']
                )

                # Detect entities
                results['entities'] = ComprehendHelper.detect_entities(
                    results['text'], results['language']
                )

        except Exception as e:
            logger.error(f"Document processing failed: {str(e)}")

        return results