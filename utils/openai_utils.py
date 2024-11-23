import openai
import logging
from utils.config import Config

logger = logging.getLogger(__name__)

class OpenAILLM:
    def __init__(self, model='gpt-3.5-turbo'):
        """
        Initialize the OpenAI LLM.

        :param model: The OpenAI model to use (default: gpt-3.5-turbo)
        """
        config = Config()
        self.api_key = config.openai_api_key
        openai.api_key = self.api_key
        self.model = model
        logger.info(f"Initialized OpenAI LLM with model: {self.model}")

    def generate_response(self, prompt, system_prompt=None, max_tokens=500):
        """
        Generate a response from the OpenAI LLM.

        :param prompt: The user prompt to send to the LLM.
        :param system_prompt: Optional system prompt to set the assistant's behavior.
        :param max_tokens: Maximum number of tokens in the response.
        :return: The LLM's response text.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                n=1,
                temperature=0.7,
            )
            reply = response.choices[0].message['content'].strip()
            logger.debug("Generated response from OpenAI.")
            return reply
        except Exception as e:
            logger.error(f"Error generating response from OpenAI: {e}")
            return "I'm sorry, but I couldn't process your request at the moment."
