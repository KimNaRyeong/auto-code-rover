"""
Interfacing with Together.ai cloud.
"""

import os
import sys
from typing import Literal

import litellm
from litellm.utils import Choices, Message, ModelResponse
from litellm.exceptions import RateLimitError, ServiceUnavailableError
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

from app.log import log_and_print
from app.model import common
from app.model.common import Model

class TogetherModel(Model):
    _instances = {}

    def __new__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
            cls._instances[cls]._initialized = False
        return cls._instances[cls]
    
    def __init__(
        self,
        name: str,
        cost_per_input: float,
        cost_per_output: float,
        parallel_tool_call: bool = False,
    ):
        if self._initialized:
            return
        super().__init__(name, cost_per_input, cost_per_output, parallel_tool_call)
        self._initialized = True

    def setup(self) -> None:
        """
        Check TogetherAI API key.
        """
        self.check_api_key()

    def check_api_key(self) -> str:
        """
        Check for the TOGETHER_API_KEY environment variable.
        """
        key = os.environ.get("TOGETHER_API_KEY")
        if not key:
            log_and_print("Please set the TOGETHER_API_KEY env var")
            sys.exit(1)
        return key
    
    def extract_resp_content(self, chat_message: Message) -> str:
        """
        Given a chat completion message, extract the content from it.
        """
        content = chat_message.content
        if content is None:
            return ""
        else:
            return content
    
    def _merge_consecutive_messages(self, messages: list[dict]) -> list[dict]:
        if not messages:
            return messages
        
        merged = []

        current_msg = messages[0].copy()

        for next_msg in messages[1:]:
            if next_msg['role'] == current_msg['role']:
                current_msg['content'] = str(current_msg['content']) + "\n\n" + str(next_msg['content'])
            else:
                merged.append(current_msg)
                current_msg = next_msg.copy()
        merged.append(current_msg)
        return merged

    
    @retry(
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6),
        retry=retry_if_exception_type((RateLimitError, ServiceUnavailableError))
    )
    def call(
        self,
        messages: list[dict],
        top_p=1,
        tools=None,
        response_format: Literal["text", "json_object"] = "text",
        **kwargs,
    ):
        
        try:
            # prefill_content = "{"
            if response_format == "json_object":  # prefill
                
                json_instruction = {
                    "role": "user",
                    "content": "Stop your response after a valid json is generated"
                }

                messages.append(json_instruction)
                # messages.append({"role": "assistant", "content": prefill_content})

            if self.name == 'together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1':

                current_messages = [m.copy() for m in messages]
                final_messages = self._merge_consecutive_messages(current_messages)
            else:
                final_messages = messages

            response = litellm.completion(
                model=self.name,
                messages=final_messages,
                temperature=common.MODEL_TEMP,
                max_tokens=1024,
                top_p=top_p,
                stream=False,
            )
            assert isinstance(response, ModelResponse)
            resp_usage = response.usage
            assert resp_usage is not None
            input_tokens = int(resp_usage.prompt_tokens)
            output_tokens = int(resp_usage.completion_tokens)
            cost = self.calc_cost(input_tokens, output_tokens)

            common.thread_cost.process_cost += cost
            common.thread_cost.process_input_tokens += input_tokens
            common.thread_cost.process_output_tokens += output_tokens

            first_resp_choice = response.choices[0]
            assert isinstance(first_resp_choice, Choices)
            resp_msg: Message = first_resp_choice.message
            content = self.extract_resp_content(resp_msg)

            # if response_format == "json_object":
            #     # prepend the prefilled character
            #     if not content.startswith(prefill_content):
            #         content = prefill_content + content

            return content, cost, input_tokens, output_tokens

        except Exception as e:
            if isinstance(e, RateLimitError):
                log_and_print(f">> TogetherAI Rate Limit Hit. Retrying...")
                raise e

            log_and_print(f"!! TogetherAI API Error !!: {e}")
            raise e

class Together_GPT_OSS_20B(TogetherModel):
    def __init__(self):
        super().__init__(
            "together_ai/openai/gpt-oss-20b",
            0.00000005,
            0.0000002,
            parallel_tool_call=True
        )

class Together_Mixtral_8x7B(TogetherModel):
    def __init__(self):
        super().__init__(
            "together_ai/mistralai/Mixtral-8x7B-Instruct-v0.1",
            0.0000006,
            0,
            parallel_tool_call=True
        )