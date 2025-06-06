from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class SummarizationRequest(BaseModel):
    """
    Request model for text summarization
    """
    text: str = Field(..., description="The text to summarize")
    summary_type: Literal["extractive", "abstractive", "bullet"] = Field(
        "extractive", 
        description="Type of summarization to perform"
    )
    summary_length: Literal["short", "medium", "long"] = Field(
        "medium", 
        description="Length of the summary"
    )

class SummarizationResponse(BaseModel):
    """
    Response model for text summarization
    """
    summary: str = Field(..., description="The generated summary")
    original_length: int = Field(..., description="Length of the original text in characters")
    summary_length: int = Field(..., description="Length of the summary in characters")
    compression_ratio: float = Field(..., description="Compression ratio (1 - summary_length/original_length)")
    summary_type: str = Field(..., description="Type of summarization performed")
