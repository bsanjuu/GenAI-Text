import re
import string
from typing import List, Optional
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import logging

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextPreprocessor:
    """
    Text preprocessing utilities for summarization
    """

    def __init__(self, language: str = 'english'):
        self.language = language
        try:
            self.stop_words = set(stopwords.words(language))
        except OSError:
            logger.warning(f"Stopwords for language '{language}' not found, using English")
            self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove extra whitespace and normalize line breaks
        text = re.sub(r'\s+', ' ', text.strip())

        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\!\?\,\;\:\-\(\)]', '', text)

        # Fix common OCR errors
        text = self._fix_ocr_errors(text)

        return text

    def _fix_ocr_errors(self, text: str) -> str:
        """
        Fix common OCR errors

        Args:
            text: Text with potential OCR errors

        Returns:
            Text with OCR errors fixed
        """
        # Common OCR substitutions
        ocr_corrections = {
            r'\bl\b': 'I',  # lowercase l to uppercase I
            r'\b0\b': 'O',  # zero to letter O (context dependent)
            r'rn': 'm',     # rn to m
            r'vv': 'w',     # vv to w
        }

        for pattern, replacement in ocr_corrections.items():
            text = re.sub(pattern, replacement, text)

        return text

    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text

        Args:
            text: Input text

        Returns:
            List of sentences
        """
        if not text:
            return []

        # Clean text first
        cleaned_text = self.clean_text(text)

        # Extract sentences
        sentences = sent_tokenize(cleaned_text)

        # Filter out very short sentences (less than 3 words)
        filtered_sentences = [
            sent.strip() for sent in sentences
            if len(sent.split()) >= 3
        ]

        return filtered_sentences

    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract keywords from text

        Args:
            text: Input text
            max_keywords: Maximum number of keywords to return

        Returns:
            List of keywords
        """
        if not text:
            return []

        # Clean and tokenize
        cleaned_text = self.clean_text(text.lower())
        words = word_tokenize(cleaned_text)

        # Remove stopwords and punctuation
        keywords = [
            word for word in words
            if word.isalnum() and
               word not in self.stop_words and
               len(word) > 2
        ]

        # Count frequency
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Sort by frequency and return top keywords
        sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

        return [word for word, _ in sorted_keywords[:max_keywords]]

    def calculate_readability_score(self, text: str) -> float:
        """
        Calculate a simple readability score (Flesch Reading Ease approximation)

        Args:
            text: Input text

        Returns:
            Readability score (0-100, higher is easier to read)
        """
        if not text:
            return 0.0

        sentences = self.extract_sentences(text)
        if not sentences:
            return 0.0

        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum()]

        if not words:
            return 0.0

        # Count syllables (approximation)
        def count_syllables(word):
            vowels = "aeiouy"
            syllables = 0
            prev_was_vowel = False

            for char in word.lower():
                is_vowel = char in vowels
                if is_vowel and not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = is_vowel

            # Handle edge cases
            if word.endswith('e'):
                syllables -= 1
            if syllables == 0:
                syllables = 1

            return syllables

        total_syllables = sum(count_syllables(word) for word in words)
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = total_syllables / len(words)

        # Simplified Flesch Reading Ease formula
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)

        # Clamp to 0-100 range
        return max(0, min(100, score))

    def validate_text_length(self, text: str, max_length: int = 50000) -> bool:
        """
        Validate if text length is within acceptable limits

        Args:
            text: Input text
            max_length: Maximum allowed length

        Returns:
            True if text is valid length, False otherwise
        """
        return len(text) <= max_length

    def truncate_text(self, text: str, max_length: int = 50000) -> str:
        """
        Truncate text to maximum length while preserving sentence boundaries

        Args:
            text: Input text
            max_length: Maximum allowed length

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text

        sentences = self.extract_sentences(text)
        result = ""

        for sentence in sentences:
            if len(result) + len(sentence) + 1 <= max_length:
                result += sentence + " "
            else:
                break

        return result.strip()

# Create a default preprocessor instance
text_preprocessor = TextPreprocessor()