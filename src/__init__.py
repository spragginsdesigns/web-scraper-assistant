"""
Firecrawl CLI - A command line interface for the Firecrawl API
"""

from .extraction_strategy import LLMExtractionStrategy, InputFormat, ExtractionType
from .providers import OpenAIExtractionStrategy, DeepSeekExtractionStrategy

__all__ = [
    'LLMExtractionStrategy',
    'OpenAIExtractionStrategy',
    'DeepSeekExtractionStrategy',
    'InputFormat',
    'ExtractionType'
]

__version__ = "0.1.0"