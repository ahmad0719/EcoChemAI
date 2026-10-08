import os
from pathlib import Path

from dotenv import load_dotenv

try:
    import groq
    from groq import Groq
except ImportError:  # Allows the rest of the application to report a safe error.
    groq = None
    Groq = None

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DEFAULT_MODEL = "openai/gpt-oss-120b"
REQUEST_TIMEOUT_SECONDS = 30.0



class LLMError(RuntimeError):
    """Base exception for safe, user-facing LLM failures."""


class LLMConfigurationError(LLMError):
    """Raised when the Groq client cannot be configured safely."""


class LLMServiceError(LLMError):
    """Raised when Groq cannot complete a model request."""


def _get_model() -> str:
    """Return the configured Groq model, falling back to the supported default."""
    return os.getenv("GROQ_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def _get_client():
    """Create a configured Groq client without exposing credentials."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise LLMConfigurationError(
            "GROQ_API_KEY is not configured. Add it to the environment and try again."
        )

    if Groq is None:
        raise LLMConfigurationError(
            "The Groq client library is unavailable. Install the project's dependencies."
        )

    return Groq(api_key=api_key, timeout=REQUEST_TIMEOUT_SECONDS)


def ask_llm(prompt: str) -> str:
    """Send a grounded EcoChemAI prompt to Groq with safe error handling."""
    client = _get_client()

    try:
        response = client.chat.completions.create(
            model=_get_model(),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are EcoChemAI, an expert Chemical Engineer who explains "
                        "ingredients in simple language."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
    except groq.APITimeoutError as exc:
        raise LLMServiceError(
            "The Groq request timed out. Please try again."
        ) from exc
    except groq.APIConnectionError as exc:
        raise LLMServiceError(
            "EcoChemAI could not reach Groq. Check your network connection and try again."
        ) from exc
    except groq.APIStatusError as exc:
        raise LLMServiceError(
            "The selected Groq model is unavailable or the request was rejected. "
            "Check GROQ_MODEL and try again."
        ) from exc
    except groq.APIError as exc:
        raise LLMServiceError("Groq could not complete the request. Please try again.") from exc
    except (OSError, TimeoutError) as exc:
        raise LLMServiceError(
            "A network error occurred while contacting Groq. Please try again."
        ) from exc

    if not response.choices or response.choices[0].message.content is None:
        raise LLMServiceError("Groq returned an empty response. Please try again.")

    return response.choices[0].message.content
