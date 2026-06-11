import os

import streamlit as st
from dotenv import load_dotenv


load_dotenv()


def get_secret(name: str, default: str | None = None) -> str | None:
    """
    Lee secretos desde Streamlit Cloud o desde variables de entorno locales.

    Prioridad:
    1. st.secrets
    2. os.environ
    3. default
    """
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return os.getenv(name, default)


def get_tavily_api_key() -> str:
    api_key = get_secret("TAVILY_API_KEY")

    if not api_key:
        raise ValueError(
            "No se ha encontrado TAVILY_API_KEY. "
            "Configúrala en Streamlit Secrets o en un archivo .env local."
        )

    return api_key