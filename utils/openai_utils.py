# utils/openai_utils.py

import openai
import logging
from utils.config import Config

logger = logging.getLogger(__name__)

class OpenAILLM:
    def __init__(self, model='gpt-3.5-turbo', llm_settings=None):
        """
        Initialize the OpenAI LLM.

        :param model: The OpenAI model to use (default: gpt-3.5-turbo)
        :param llm_settings: Dictionary of LLM settings from configuration.
        """
        config = Config()
        self.api_key = config.openai_api_key
        openai.api_key = self.api_key
        self.model = model
        self.llm_settings = llm_settings or {}
        logger.info(f"Initialized OpenAI LLM with model: {self.model}")

    def generate_response(self, prompt, system_prompt=None):
        """
        Generate a response from the OpenAI LLM.

        :param prompt: The user prompt to send to the LLM.
        :param system_prompt: Optional system prompt to set the assistant's behavior.
        :return: The LLM's response text.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = openai.ChatCompletion.create(
                model=self.llm_settings.get('model', self.model),
                messages=messages,
                max_tokens=self.llm_settings.get('max_tokens', 150),
                temperature=self.llm_settings.get('temperature', 0.7),
                top_p=self.llm_settings.get('top_p', 0.9),
                frequency_penalty=self.llm_settings.get('frequency_penalty', 0.0),
                presence_penalty=self.llm_settings.get('presence_penalty', 0.6),
                stop=self.llm_settings.get('stop_sequences', ["\n", " User:", " XBot:"]),
                # Additional settings can be added here
            )
            reply = response.choices[0].message['content'].strip()
            logger.debug("Generated response from OpenAI.")
            return reply
        except Exception as e:
            logger.error(f"Error generating response from OpenAI: {e}")
            fallback_responses = self.llm_settings.get('fallback_responses', ["I'm sorry, but I couldn't process your request at the moment."])
            return fallback_responses[0] if fallback_responses else "I'm sorry, but I couldn't process your request at the moment."
