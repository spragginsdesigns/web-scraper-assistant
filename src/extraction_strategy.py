from typing import List, Dict, Optional, Any
from pydantic import BaseModel
import json
from enum import Enum

class InputFormat(str, Enum):
    MARKDOWN = "markdown"
    HTML = "html"
    FIT_MARKDOWN = "fit_markdown"
    RAW_HTML = "raw_html"

class ExtractionType(str, Enum):
    SCHEMA = "schema"
    BLOCK = "block"

class LLMExtractionStrategy:
    def __init__(
        self,
        provider: str,
        api_token: Optional[str] = None,
        schema: Optional[Dict] = None,
        extraction_type: str = ExtractionType.SCHEMA,
        instruction: str = "",
        chunk_token_threshold: int = 4000,
        overlap_rate: float = 0.1,
        apply_chunking: bool = True,
        input_format: str = InputFormat.MARKDOWN,
        extra_args: Optional[Dict[str, Any]] = None
    ):
        self.provider = provider
        self.api_token = api_token
        self.schema = schema
        self.extraction_type = extraction_type
        self.instruction = instruction
        self.chunk_token_threshold = chunk_token_threshold
        self.overlap_rate = overlap_rate
        self.apply_chunking = apply_chunking
        self.input_format = input_format
        self.extra_args = extra_args or {}

        # Usage tracking
        self.chunk_usages: List[Dict[str, int]] = []
        self.total_tokens: int = 0

    async def process_chunk(self, chunk: str) -> Dict:
        """Process a single chunk of content using the configured LLM."""
        # Implementation will vary based on provider
        raise NotImplementedError

    async def process_content(self, content: str) -> str:
        """Process the entire content, handling chunking if enabled."""
        if not self.apply_chunking:
            result = await self.process_chunk(content)
            return json.dumps(result)

        chunks = self._split_into_chunks(content)
        results = []

        for chunk in chunks:
            chunk_result = await self.process_chunk(chunk)
            results.append(chunk_result)

        return self._merge_results(results)

    def _split_into_chunks(self, content: str) -> List[str]:
        """Split content into chunks based on token threshold and overlap rate."""
        # Basic implementation - will need to be enhanced with proper token counting
        words = content.split()
        chunk_size = self.chunk_token_threshold
        overlap_size = int(chunk_size * self.overlap_rate)

        chunks = []
        start = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start = end - overlap_size

        return chunks

    def _merge_results(self, results: List[Dict]) -> str:
        """Merge results from multiple chunks into a single result."""
        if self.extraction_type == ExtractionType.SCHEMA:
            # For schema-based extraction, merge based on schema structure
            merged = {}
            for result in results:
                merged.update(result)
            return json.dumps(merged)
        else:
            # For block extraction, concatenate results
            return json.dumps(results)

    def show_usage(self) -> None:
        """Display token usage statistics."""
        print(f"Total tokens used: {self.total_tokens}")
        print(f"Number of chunks processed: {len(self.chunk_usages)}")
        for i, usage in enumerate(self.chunk_usages):
            print(f"Chunk {i + 1} usage: {usage}")