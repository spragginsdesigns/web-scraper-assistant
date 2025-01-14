from openai import OpenAI
from typing import Dict, Optional
import json
import asyncio
from ..extraction_strategy import LLMExtractionStrategy

class OpenAIExtractionStrategy(LLMExtractionStrategy):
    def __init__(self, api_token: str, **kwargs):
        super().__init__(provider="openai", api_token=api_token, **kwargs)
        # Configure OpenAI client
        self.client = OpenAI(api_key=api_token, timeout=30.0)  # Add timeout

    async def process_chunk(self, chunk: str) -> Dict:
        """Process a chunk using OpenAI's API."""
        try:
            print(f"Processing chunk with OpenAI (length: {len(chunk)} chars)")  # Debug log

            # Construct the prompt
            system_prompt = "You are a helpful assistant that extracts structured information from text."
            if self.schema:
                system_prompt += f"\nPlease extract information according to this JSON schema: {json.dumps(self.schema)}"

            user_prompt = f"{self.instruction}\n\nContent:\n{chunk}"

            print("Making API call to OpenAI...")  # Debug log

            # Make API call using the configured client
            try:
                response = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        model=self.extra_args.get("model", "gpt-3.5-turbo"),
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=self.extra_args.get("temperature", 0.0),
                        max_tokens=self.extra_args.get("max_tokens", 3000)
                    ),
                    timeout=60.0  # Set a timeout of 60 seconds
                )
            except asyncio.TimeoutError:
                print("OpenAI API call timed out after 60 seconds")  # Debug log
                return {"error": "API call timed out"}
            except Exception as api_error:
                print(f"OpenAI API call failed: {str(api_error)}")  # Debug log
                return {"error": f"API call failed: {str(api_error)}"}

            print("Successfully received response from OpenAI")  # Debug log

            # Track usage
            usage = response.usage.to_dict()
            self.chunk_usages.append(usage)
            self.total_tokens += usage.get("total_tokens", 0)

            # Parse and return the result
            result = response.choices[0].message.content
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON response: {result}")  # Debug log
                # If the model didn't return valid JSON, wrap it in a basic structure
                return {"extracted_text": result}

        except Exception as e:
            # Handle errors gracefully
            error_msg = f"Error processing chunk with OpenAI: {str(e)}"
            print(f"Error: {error_msg}")  # Debug log
            return {"error": error_msg}