import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import uuid
from typing import List, Dict, Any
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

logger = logging.getLogger(__name__)

class SummarizationService:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
    def generate_summary(self, text: str, summary_type: str, summary_length: str) -> Dict[str, Any]:
        """
        Generate a summary of the given text
        
        Args:
            text: The text to summarize
            summary_type: The type of summarization to perform (extractive, abstractive, bullet)
            summary_length: The length of the summary (short, medium, long)
            
        Returns:
            A dictionary containing the summary and related information
        """
        if not text.strip():
            return {
                "summary": "",
                "original_length": 0,
                "summary_length": 0,
                "compression_ratio": 0,
                "summary_type": summary_type
            }
        
        # Define length ratios based on summary_length
        length_ratios = {
            "short": 0.1,
            "medium": 0.3,
            "long": 0.5
        }
        
        ratio = length_ratios.get(summary_length, 0.3)
        
        if summary_type == "extractive":
            summary = self._generate_extractive_summary(text, ratio)
        elif summary_type == "abstractive":
            # In a real implementation, this would use a transformer model
            # For now, we'll use a simplified approach
            summary = self._generate_mock_abstractive_summary(text, ratio)
        elif summary_type == "bullet":
            summary = self._generate_bullet_summary(text, ratio)
        else:
            summary = self._generate_extractive_summary(text, ratio)
        
        return {
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
            "compression_ratio": 1 - (len(summary) / len(text)) if len(text) > 0 else 0,
            "summary_type": summary_type
        }
    
    def _generate_extractive_summary(self, text: str, ratio: float) -> str:
        """
        Generate an extractive summary using TextRank algorithm
        
        Args:
            text: The text to summarize
            ratio: The ratio of sentences to include in the summary
            
        Returns:
            The extractive summary
        """
        sentences = sent_tokenize(text)
        
        if not sentences:
            return ""
        
        # If there are very few sentences, return them all
        if len(sentences) <= 3:
            return " ".join(sentences)
        
        # Build similarity matrix
        similarity_matrix = self._build_similarity_matrix(sentences)
        
        # Rank sentences using PageRank algorithm
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph)
        
        # Sort sentences by score and select top sentences
        ranked_sentences = sorted([(scores[i], s) for i, s in enumerate(sentences)], reverse=True)
        
        # Calculate number of sentences to include
        num_sentences = max(1, int(len(sentences) * ratio))
        
        # Get the top sentences
        top_sentences = [s for _, s in ranked_sentences[:num_sentences]]
        
        # Reorder sentences based on their original position
        ordered_sentences = []
        for sentence in sentences:
            if sentence in top_sentences:
                ordered_sentences.append(sentence)
        
        return " ".join(ordered_sentences)
    
    def _generate_mock_abstractive_summary(self, text: str, ratio: float) -> str:
        """
        Generate a mock abstractive summary
        In a real implementation, this would use a transformer model
        
        Args:
            text: The text to summarize
            ratio: The ratio of the original text to include in the summary
            
        Returns:
            The abstractive summary
        """
        sentences = sent_tokenize(text)
        
        if not sentences:
            return ""
        
        # For mock implementation, we'll just take the first sentence and add a generic phrase
        first_sentence = sentences[0].strip()
        return f"This text discusses {first_sentence.lower()}. The main points include key concepts and their implications for the subject matter."
    
    def _generate_bullet_summary(self, text: str, ratio: float) -> str:
        """
        Generate a bullet-point summary
        
        Args:
            text: The text to summarize
            ratio: The ratio of sentences to include in the summary
            
        Returns:
            The bullet-point summary
        """
        sentences = sent_tokenize(text)
        
        if not sentences:
            return ""
        
        # Calculate number of sentences to include
        num_sentences = max(1, int(len(sentences) * ratio))
        
        # Get the top sentences using TextRank
        similarity_matrix = self._build_similarity_matrix(sentences)
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph)
        
        ranked_sentences = sorted([(scores[i], i, s) for i, s in enumerate(sentences)], reverse=True)
        top_sentences = [(i, s) for _, i, s in ranked_sentences[:num_sentences]]
        
        # Sort by original position
        top_sentences.sort(key=lambda x: x[0])
        
        # Format as bullet points
        bullet_points = [f"• {s.strip()}" for _, s in top_sentences]
        
        return "\n".join(bullet_points)
    
    def _build_similarity_matrix(self, sentences: List[str]) -> np.ndarray:
        """
        Build a similarity matrix for the given sentences
        
        Args:
            sentences: List of sentences
            
        Returns:
            Similarity matrix as a numpy array
        """
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
        
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i == j:
                    continue
                
                similarity_matrix[i][j] = self._sentence_similarity(sentences[i], sentences[j])
                
        return similarity_matrix
    
    def _sentence_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate the cosine similarity between two sentences
        
        Args:
            sent1: First sentence
            sent2: Second sentence
            
        Returns:
            Cosine similarity between the sentences
        """
        # Convert sentences to lowercase and tokenize
        words1 = [word.lower() for word in nltk.word_tokenize(sent1) if word.isalnum()]
        words2 = [word.lower() for word in nltk.word_tokenize(sent2) if word.isalnum()]
        
        # Remove stop words
        words1 = [word for word in words1 if word not in self.stop_words]
        words2 = [word for word in words2 if word not in self.stop_words]
        
        # If either sentence has no words, return 0
        if not words1 or not words2:
            return 0.0
        
        # Create a set of all unique words
        all_words = list(set(words1 + words2))
        
        # Create word vectors
        vector1 = [1 if word in words1 else 0 for word in all_words]
        vector2 = [1 if word in words2 else 0 for word in all_words]
        
        # Calculate cosine similarity
        return 1 - cosine_distance(vector1, vector2)

# Create a singleton instance
summarization_service = SummarizationService()
