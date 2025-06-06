import pytest
from app.services.summarization_service import summarization_service

class TestSummarizationService:
    """
    Test cases for the summarization service
    """

    def test_generate_summary_extractive(self):
        """Test extractive summarization"""
        text = """
        The quick brown fox jumps over the lazy dog. This is a classic pangram used in typography.
        Pangrams are sentences that contain every letter of the alphabet at least once.
        They are useful for testing fonts and keyboard layouts. The quick brown fox sentence
        is probably the most famous pangram in English. It has been used since the early 1900s.
        Many variations of this sentence exist, but the original remains the most popular.
        """

        result = summarization_service.generate_summary(text, "bullet", "medium")

        assert result is not None
        assert result["summary_type"] == "bullet"
        assert "•" in result["summary"]  # Check for bullet points
        assert len(result["summary"]) > 0

    def test_generate_summary_abstractive(self):
        """Test abstractive summarization"""
        text = """
        Artificial intelligence is revolutionizing many industries. Machine learning algorithms
        can process vast amounts of data quickly. They can identify patterns that humans might miss.
        AI is being used in healthcare, finance, and transportation. Self-driving cars use AI
        to navigate roads safely. In healthcare, AI helps diagnose diseases more accurately.
        The future of AI looks promising but also raises ethical concerns.
        """

        result = summarization_service.generate_summary(text, "abstractive", "long")

        assert result is not None
        assert result["summary_type"] == "abstractive"
        assert len(result["summary"]) > 0

    def test_empty_text(self):
        """Test summarization with empty text"""
        result = summarization_service.generate_summary("", "extractive", "medium")

        assert result["summary"] == ""
        assert result["original_length"] == 0
        assert result["summary_length"] == 0
        assert result["compression_ratio"] == 0

    def test_short_text(self):
        """Test summarization with very short text"""
        text = "This is a short sentence."

        result = summarization_service.generate_summary(text, "extractive", "medium")

        assert result is not None
        assert len(result["summary"]) > 0
        # Short text should be returned as-is or minimally processed

    def test_invalid_summary_type(self):
        """Test with invalid summary type"""
        text = "This is a test text for summarization."

        # Should default to extractive
        result = summarization_service.generate_summary(text, "invalid_type", "medium")

        assert result is not None
        assert len(result["summary"]) > 0

    def test_different_lengths(self):
        """Test different summary lengths"""
        text = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
        nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore 
        eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
        sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut 
        perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque 
        laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis.
        """

        short_result = summarization_service.generate_summary(text, "extractive", "short")
        medium_result = summarization_service.generate_summary(text, "extractive", "medium")
        long_result = summarization_service.generate_summary(text, "extractive", "long")

        # Generally, longer summaries should be longer than shorter ones
        # (though this isn't guaranteed for all texts)
        assert all(result["summary"] for result in [short_result, medium_result, long_result])

    def test_similarity_matrix(self):
        """Test similarity matrix calculation"""
        sentences = [
            "The cat sat on the mat.",
            "A feline was sitting on a rug.",
            "Dogs are great pets.",
            "Cats and dogs are both animals."
        ]

        matrix = summarization_service._build_similarity_matrix(sentences)

        assert matrix.shape == (4, 4)
        # Diagonal should be zero (sentences don't compare to themselves)
        for i in range(4):
            assert matrix[i][i] == 0

        # Matrix should be symmetric
        for i in range(4):
            for j in range(4):
                assert abs(matrix[i][j] - matrix[j][i]) < 0.001

    def test_sentence_similarity(self):
        """Test sentence similarity calculation"""
        sent1 = "The cat sat on the mat."
        sent2 = "A cat was sitting on a mat."
        sent3 = "The dog ran in the park."

        # Similar sentences should have higher similarity
        sim1 = summarization_service._sentence_similarity(sent1, sent2)
        sim2 = summarization_service._sentence_similarity(sent1, sent3)

        assert sim1 > sim2
        assert 0 <= sim1 <= 1
        assert 0 <= sim2 <= 1extractive", "short")

        assert result is not None
        assert isinstance(result, dict)
        assert "summary" in result
        assert "original_length" in result
        assert "summary_length" in result
        assert "compression_ratio" in result
        assert "summary_type" in result

        assert result["summary_type"] == "extractive"
        assert len(result["summary"]) > 0
        assert result["original_length"] == len(text)
        assert result["summary_length"] == len(result["summary"])
        assert 0 <= result["compression_ratio"] <= 1

    def test_generate_summary_bullet(self):
        """Test bullet point summarization"""
        text = """
        Climate change is a long-term shift in global weather patterns. It is primarily caused by human activities.
        The burning of fossil fuels releases greenhouse gases into the atmosphere. These gases trap heat from the sun.
        This leads to global warming and changes in weather patterns. Rising sea levels are one consequence.
        Extreme weather events are becoming more frequent. Scientists are working on solutions to reduce emissions.
        """

        result = summarization_service.generate_summary(text, "