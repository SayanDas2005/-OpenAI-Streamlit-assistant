"""OpenAI integration for the Streamlit chat interface."""

import os
from collections.abc import Sequence
from typing import TypedDict

from openai import APIConnectionError, APIStatusError, AuthenticationError, OpenAI, RateLimitError


DEFAULT_MODEL = "gpt-4.1-mini"
SYSTEM_PROMPT = "You are a helpful, accurate, and concise AI assistant."
MAX_HISTORY_MESSAGES = 20


class ChatMessage(TypedDict):
    role: str
    content: str


class AIServiceError(Exception):
    """An error that is safe to display in the user interface."""


def _recent_messages(messages: Sequence[ChatMessage]) -> list[ChatMessage]:
    """Keep requests bounded while retaining the most recent conversation context."""
    return list(messages[-MAX_HISTORY_MESSAGES:])


def generate_reply(messages: Sequence[ChatMessage]) -> str:
    """Send the recent conversation to OpenAI and return its text reply."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        raise AIServiceError("Missing OPENAI_API_KEY. Copy .env.example to .env and add your API key.")

    try:
        response = OpenAI(api_key=api_key).chat.completions.create(
            model=os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *_recent_messages(messages),
            ],
        )
    except AuthenticationError as error:
        raise AIServiceError("Your OpenAI API key was rejected. Check the value in .env.") from error
    except RateLimitError as error:
        raise AIServiceError("Request limit reached. Please wait a moment and try again.") from error
    except APIConnectionError as error:
        raise AIServiceError("Could not reach OpenAI. Check your internet connection and try again.") from error
    except APIStatusError as error:
        raise AIServiceError("OpenAI could not complete the request. Please try again shortly.") from error
    except Exception as error:
        raise AIServiceError("The AI request failed. Check your model setting and try again.") from error

    content = response.choices[0].message.content
    return content.strip() if content and content.strip() else "I couldn't generate a response. Please try again."
