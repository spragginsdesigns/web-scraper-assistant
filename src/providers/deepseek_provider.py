from openai import OpenAI
from typing import Dict, Optional
import json
import asyncio
import time
import aiohttp
from .openai_provider import OpenAIExtractionStrategy

class DeepSeekExtractionStrategy(OpenAIExtractionStrategy):
    """DeepSeek-specific implementation of LLM extraction strategy."""

    DEEPSEEK_BASE_URL = "https://api.deepseek.ai/v1"  # Updated to the correct endpoint

    def __init__(self, api_token: str, **kwargs):
        print("Initializing DeepSeek extraction strategy...")  # Debug log
        # Remove provider from kwargs if it exists
        kwargs.pop('provider', None)

        # Set DeepSeek-specific defaults
        kwargs.setdefault('extra_args', {})
        kwargs['extra_args'].setdefault('model', 'deepseek-chat')
        print(f"Using model: {kwargs['extra_args']['model']}")  # Debug log

        # Initialize the parent class with explicit provider
        super().__init__(api_token=api_token, **kwargs)

        # Configure OpenAI client with DeepSeek settings
        print(f"Configuring DeepSeek client with base URL: {self.DEEPSEEK_BASE_URL}")  # Debug log
        try:
            self.client = OpenAI(
                api_key=api_token,
                base_url=self.DEEPSEEK_BASE_URL,
                timeout=30.0  # Set client timeout
            )
            print("DeepSeek client configured successfully")
        except Exception as e:
            print(f"Error configuring DeepSeek client: {str(e)}")
            raise

    async def test_connection(self):
        """Test the connection to DeepSeek API."""
        try:
            print("\nTesting connection to DeepSeek API...")
            timeout = aiohttp.ClientTimeout(total=10)  # 10 second timeout
            async with aiohttp.ClientSession(timeout=timeout) as session:
                headers = {
                    "Authorization": f"Bearer {self.client.api_key}",
                    "Content-Type": "application/json"
                }
                # Test with a simple chat completion request instead of models endpoint
                payload = {
                    "model": self.extra_args.get("model", "deepseek-chat"),
                    "messages": [{"role": "user", "content": "test"}],
                    "max_tokens": 1
                }
                async with session.post(
                    f"{self.DEEPSEEK_BASE_URL}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        print("Successfully connected to DeepSeek API")
                        return True
                    else:
                        text = await response.text()
                        print(f"Failed to connect to DeepSeek API. Status: {response.status}")
                        print(f"Response: {text}")
                        return False
        except asyncio.TimeoutError:
            print("Connection test timed out after 10 seconds")
            return False
        except Exception as e:
            print(f"Error testing connection: {str(e)}")
            return False

    async def process_chunk(self, chunk: str) -> Dict:
        """Process a chunk using DeepSeek's API."""
        start_time = time.time()
        try:
            # Test connection first
            if not await self.test_connection():
                return {"error": "Failed to connect to DeepSeek API"}

            print(f"\nProcessing chunk with DeepSeek (length: {len(chunk)} chars)")  # Debug log
            print(f"API Key (first 8 chars): {self.client.api_key[:8]}...")  # Show part of API key for verification

            # Construct the prompt
            print("Building prompts...")  # Debug log
            system_prompt = "You are a helpful assistant that extracts structured information from text."
            if self.schema:
                print(f"Using schema: {json.dumps(self.schema)}")  # Debug log
                system_prompt += f"\nPlease extract information according to this JSON schema: {json.dumps(self.schema)}"

            user_prompt = f"{self.instruction}\n\nContent:\n{chunk}"
            print(f"Instruction: {self.instruction}")  # Debug log

            # Make API call using the configured client
            print("\nPreparing API call to DeepSeek...")  # Debug log
            print(f"Request details:\n- Model: {self.extra_args.get('model', 'deepseek-chat')}\n- Max tokens: {self.extra_args.get('max_tokens', 3000)}")

            try:
                print("Starting API call...")
                call_start_time = time.time()

                # Create the request payload
                payload = {
                    "model": self.extra_args.get("model", "deepseek-chat"),
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": self.extra_args.get("temperature", 0.0),
                    "max_tokens": self.extra_args.get("max_tokens", 3000)
                }

                # Make the API call using aiohttp for better control
                timeout = aiohttp.ClientTimeout(total=60)  # 60 second timeout for processing
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    headers = {
                        "Authorization": f"Bearer {self.client.api_key}",
                        "Content-Type": "application/json"
                    }
                    async with session.post(
                        f"{self.DEEPSEEK_BASE_URL}/chat/completions",
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            print(f"DeepSeek API returned status {response.status}: {error_text}")
                            return {"error": f"API returned status {response.status}: {error_text}"}

                        response_data = await response.json()

                call_duration = time.time() - call_start_time
                print(f"API call completed in {call_duration:.2f} seconds")
                print("Successfully received response from DeepSeek")

                # Track usage
                if "usage" in response_data:
                    usage = response_data["usage"]
                    self.chunk_usages.append(usage)
                    self.total_tokens += usage.get("total_tokens", 0)
                    print(f"Tokens used in this chunk: {usage.get('total_tokens', 0)}")

                # Parse and return the result
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    result = response_data["choices"][0]["message"]["content"]
                    print("\nAttempting to parse response as JSON...")
                    try:
                        parsed_result = json.loads(result)
                        print("Successfully parsed JSON response")
                        return parsed_result
                    except json.JSONDecodeError:
                        print(f"Failed to parse JSON response. Raw response: {result[:200]}...")
                        return {"extracted_text": result}
                else:
                    return {"error": "No content in response"}

            except asyncio.TimeoutError:
                print(f"DeepSeek API call timed out after {time.time() - call_start_time:.2f} seconds")
                return {"error": "API call timed out"}
            except Exception as api_error:
                print(f"DeepSeek API call failed after {time.time() - call_start_time:.2f} seconds")
                print(f"Error type: {type(api_error).__name__}")
                print(f"Error details: {str(api_error)}")
                return {"error": f"API call failed: {str(api_error)}"}

        except Exception as e:
            total_duration = time.time() - start_time
            error_msg = f"Error processing chunk with DeepSeek: {str(e)}"
            print(f"Error after {total_duration:.2f} seconds: {error_msg}")
            print(f"Error type: {type(e).__name__}")
            return {"error": error_msg}