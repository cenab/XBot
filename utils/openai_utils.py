# utils/openai_utils.py

import openai
import logging
from utils.config import Config

logger = logging.getLogger(__name__)

class OpenAILLM:
    def __init__(self, model='gpt-4', llm_settings=None, character_profile=None):
        """
        Initialize the OpenAI LLM.

        :param model: The OpenAI model to use (default: gpt-4)
        :param llm_settings: Dictionary of LLM settings from configuration.
        :param character_profile: Dictionary containing the character's detailed profile.
        """
        config = Config()
        self.api_key = config.openai_api_key
        openai.api_key = self.api_key
        self.model = model
        self.llm_settings = llm_settings or {}
        self.character_profile = character_profile or {}
        logger.info(f"Initialized OpenAI LLM with model: {self.model}")

    def generate_system_prompt(self):
        """
        Generate a comprehensive system prompt based on the character profile.

        :return: The system prompt string.
        """
        system_prompt = f"You are {self.character_profile.get('name', 'an AI assistant')}."
        system_prompt += f" {self.character_profile.get('description', '')}\n\n"

        # History
        history = self.character_profile.get('history', {})
        if history:
            system_prompt += "### History\n"
            system_prompt += f"Creation Date: {history.get('creation_date', 'Unknown')}.\n"
            system_prompt += f"Creator: {history.get('creator', 'Unknown')}.\n"
            system_prompt += f"Purpose: {history.get('purpose', 'Unknown')}.\n\n"

        # Background
        background = self.character_profile.get('background', {})
        if background:
            system_prompt += "### Background\n"
            education = background.get('education', {})
            if education:
                system_prompt += "Education:\n"
                for degree_level, details in education.items():
                    system_prompt += f"- {degree_level.capitalize()}: {details.get('degree', 'Unknown')} from {details.get('institution', 'Unknown')} ({details.get('graduation_year', 'Unknown')}).\n"
            experience = background.get('experience', '')
            if experience:
                system_prompt += f"\nExperience: {experience}\n\n"

        # Life Story
        life_story = self.character_profile.get('life_story', '')
        if life_story:
            system_prompt += "### Life Story\n"
            system_prompt += f"{life_story}\n\n"

        # Personal Anecdotes
        anecdotes = self.character_profile.get('personal_anecdotes', [])
        if anecdotes:
            system_prompt += "### Personal Anecdotes\n"
            for anecdote in anecdotes:
                system_prompt += f"- {anecdote}\n"
            system_prompt += "\n"

        # Personality Traits
        traits = self.character_profile.get('personality_traits', {})
        active_traits = [trait.replace('_', ' ').capitalize() for trait, value in traits.items() if value]
        if active_traits:
            system_prompt += f"### Personality Traits\n{', '.join(active_traits)}.\n\n"

        # Likes & Dislikes
        likes = self.character_profile.get('likes', [])
        dislikes = self.character_profile.get('dislikes', [])
        if likes:
            system_prompt += f"### Likes\n{', '.join(likes)}.\n\n"
        if dislikes:
            system_prompt += f"### Dislikes\n{', '.join(dislikes)}.\n\n"

        # Things It Is Against
        things_against = self.character_profile.get('things_it_is_against', [])
        if things_against:
            system_prompt += f"### Do Not Engage In\n{', '.join(things_against)}.\n\n"

        # Communication Style & Tone
        communication_style = self.character_profile.get('communication_style', '')
        tone = self.character_profile.get('tone', '')
        if communication_style:
            system_prompt += f"### Communication Style\n{communication_style}.\n\n"
        if tone:
            system_prompt += f"### Tone\n{tone}.\n\n"

        # Response Format
        response_format = self.character_profile.get('response_format', {})
        if response_format:
            system_prompt += f"### Response Format\n"
            for key, value in response_format.items():
                system_prompt += f"- {key.replace('_', ' ').capitalize()}: {value}.\n"
            system_prompt += "\n"

        # Additional Instructions
        additional_instructions = self.character_profile.get('additional_instructions', '')
        if additional_instructions:
            system_prompt += f"### Additional Instructions\n{additional_instructions}\n\n"

        return system_prompt

    def generate_response(self, user_query):
        """
        Generate a response from the OpenAI LLM.

        :param user_query: The user's query string.
        :return: The LLM's response text.
        """
        system_prompt = self.generate_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]

        try:
            response = openai.ChatCompletion.create(
                model=self.llm_settings.get('model', self.model),
                messages=messages,
                max_tokens=self.llm_settings.get('max_tokens', 150),
                temperature=self.llm_settings.get('temperature', 0.7),
                top_p=self.llm_settings.get('top_p', 0.9),
                frequency_penalty=self.llm_settings.get('frequency_penalty', 0.0),
                presence_penalty=self.llm_settings.get('presence_penalty', 0.6),
                stop=self.llm_settings.get('stop_sequences', ["\n", " User:", f" {self.character_profile.get('name', 'Alexandra')}:"]),
            )
            reply = response.choices[0].message['content'].strip()
            logger.debug("Generated response from OpenAI.")
            return reply
        except Exception as e:
            logger.error(f"Error generating response from OpenAI: {e}")
            fallback_responses = self.llm_settings.get('fallback_responses', [
                "I'm sorry, but I couldn't process your request at the moment.",
                "Apologies, I'm having trouble understanding that. Could you please rephrase?",
                "I'm here to help! Let's try a different question."
            ])
            return fallback_responses[0] if fallback_responses else "I'm sorry, but I couldn't process your request at the moment."
