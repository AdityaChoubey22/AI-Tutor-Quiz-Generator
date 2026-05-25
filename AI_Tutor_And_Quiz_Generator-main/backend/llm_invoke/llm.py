import os
import re
import time
import random
import requests
from dotenv import load_dotenv
from config.logging import logger

# Load environment variables from .env file
load_dotenv()

# ─── Helper: collect numbered keys from .env ─────────────────────────────────
def _collect_keys(prefix: str) -> list[str]:
    """
    Collect all keys matching PREFIX_1, PREFIX_2, PREFIX_3, ... from env.
    Skips any that are empty or look like placeholders.
    """
    keys = []
    i = 1
    while True:
        val = os.getenv(f"{prefix}_{i}", "").strip()
        if not val:
            break
        if "your_" not in val.lower() and len(val) > 8:
            keys.append(val)
        i += 1
    # Also check for the plain version without a number (e.g. GEMINI_API_KEY)
    plain = os.getenv(prefix, "").strip()
    if plain and "your_" not in plain.lower() and len(plain) > 8 and plain not in keys:
        keys.insert(0, plain)
    return keys


# ─── Pollinations Fallback LLM (keyless) ─────────────────────────────────────
class PollinationsLLM:
    """A simple fallback LLM using Pollinations.ai (no API key needed)."""
    def __init__(self, model="openai", temperature=0.7):
        self.model = model
        self.temperature = float(temperature)

    def invoke(self, messages):
        prompt = messages[-1].content
        random_seed = random.randint(1, 1_000_000)
        response = requests.post(
            "https://text.pollinations.ai/",
            json={
                "messages": [{"role": "user", "content": prompt}],
                "model": self.model,
                "seed": random_seed,
            },
            timeout=120,
        )
        if response.status_code == 200:
            class _Resp:
                def __init__(self, content): self.content = content
            return _Resp(response.text)
        raise Exception(f"Pollinations API error: {response.status_code}")


# ─── Key-Rotating LLM wrapper ────────────────────────────────────────────────
class RotatingLLM:
    """
    Wraps multiple (provider, key) pairs and automatically rotates to the
    next one whenever a rate-limit (429) or quota error is encountered.
    Falls back to Pollinations.ai as the final option.
    """

    def __init__(self, providers: list[tuple[str, str]], temperature: float = 0.7):
        """
        providers: list of ("gemini" | "groq" | "openai", api_key) tuples
        """
        self.providers = providers          # [(provider_name, api_key), ...]
        self.temperature = temperature
        self._current_index = 0            # which provider we are currently using
        self._llm_cache: dict[int, object] = {}  # index → instantiated LLM

    def _make_llm(self, index: int):
        """Lazily create the LangChain LLM for a given index."""
        if index in self._llm_cache:
            return self._llm_cache[index]

        provider, key = self.providers[index]
        llm = None

        if provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=key,
                temperature=self.temperature,
                timeout=120,
                max_retries=3,
            )
        elif provider == "huggingface":
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(
                model_name="meta-llama/Meta-Llama-3-8B-Instruct",
                openai_api_key=key,
                openai_api_base="https://api-inference.huggingface.co/v1/",
                temperature=self.temperature,
                timeout=120,
                max_retries=3,
            )
        elif provider == "openrouter":
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(
                model_name=os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free"),
                openai_api_key=key,
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=self.temperature,
                timeout=120,
                max_retries=3,
            )

        self._llm_cache[index] = llm
        return llm

    @staticmethod
    def _is_rate_limit(exc: Exception) -> bool:
        """Return True if the exception looks like a 429 / quota error."""
        msg = str(exc).lower()
        rate_limit_signals = ["429", "rate limit", "quota", "resource exhausted",
                              "too many requests", "ratelimit"]
        return any(sig in msg for sig in rate_limit_signals)

    def invoke(self, messages):
        total = len(self.providers)
        # Try each provider in round-robin from the current index
        for attempt in range(total):
            idx = (self._current_index + attempt) % total
            provider, _ = self.providers[idx]
            try:
                llm = self._make_llm(idx)
                if llm is None:
                    raise Exception(f"Could not instantiate LLM for provider: {provider}")
                result = llm.invoke(messages)
                # Success — stay on this index for the next call
                self._current_index = idx
                logger.info(f"[RotatingLLM] Used provider '{provider}' (slot {idx+1}/{total})")
                return result

            except Exception as exc:
                if self._is_rate_limit(exc):
                    logger.warning(
                        f"[RotatingLLM] Provider '{provider}' (slot {idx+1}) hit rate limit. "
                        f"Rotating to next key... ({exc})"
                    )
                    time.sleep(1)          # tiny pause before trying next key
                    continue
                else:
                    # Non-rate-limit error — re-raise immediately
                    raise

        # All provider keys exhausted → fall back to Pollinations
        logger.warning("[RotatingLLM] All API keys exhausted. Falling back to Pollinations.ai.")
        return PollinationsLLM().invoke(messages)


# ─── Public factory ───────────────────────────────────────────────────────────
def get_llm(temperature: float | None = None) -> RotatingLLM | PollinationsLLM:
    """
    Build and return the best available LLM.

    Priority order:
      Gemini keys → Groq keys → OpenAI keys → Pollinations (keyless fallback)
    """
    if temperature is None:
        temperature = float(os.getenv("TEMPERATURE", "0.7"))

    providers: list[tuple[str, str]] = []

    # 1. OpenRouter keys
    for key in _collect_keys("OPENROUTER_API_KEY"):
        providers.append(("openrouter", key))

    # 2. Hugging Face keys
    for key in _collect_keys("HUGGINGFACE_API_KEY"):
        providers.append(("huggingface", key))

    # 2. Gemini keys
    for key in _collect_keys("GEMINI_API_KEY"):
        providers.append(("gemini", key))

    if providers:
        logger.info(
            f"[get_llm] Loaded {len(providers)} API key(s): "
            + ", ".join(f"{p}({i+1})" for i, (p, _) in enumerate(providers))
        )
        return RotatingLLM(providers, temperature=temperature)

    # No keys at all → Pollinations
    logger.info("[get_llm] No API keys found. Using Pollinations.ai (keyless).")
    return PollinationsLLM(temperature=temperature)
