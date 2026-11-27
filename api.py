from typing import Literal
from pydantic import BaseModel, Field
from google import genai
from google.genai import errors, types

EntityLabel = Literal["PERSON", "ORG", "LOC", "DATE", "PRODUCT", "OTHER"]

class ExtractedEntity(BaseModel):
    text: str = Field(description="Exact entity substring as it appears in the source text.")
    label: EntityLabel = Field(description="Entity category.")
    start_char: int | None = Field(default=None, description="0-based start index in the source text, if determinable.")
    end_char: int | None = Field(default=None, description="0-based end index in the source text, if determinable.")

class NerResult(BaseModel):
    entities: list[ExtractedEntity]

client = genai.Client()

FALLBACK_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
]

def extract_entities(text: str, models: list[str] | None = None) -> NerResult:
    model_chain = models or FALLBACK_MODELS
    prompt = f"""Extract all named entities from the following text using only the allowed labels.
Do not invent entities that are not present in the text.

Text:
{text}
"""
    last_error = None
    for model_name in model_chain:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=NerResult,
                ),
            )
            return response.parsed
        except errors.ServerError as e:
            last_error = e
            continue

    raise last_error


SentimentLabel = Literal["POSITIVE", "NEGATIVE", "NEUTRAL", "MIXED"]

class SentimentResult(BaseModel):
    sentiment: SentimentLabel = Field(description="Overall sentiment polarity of the text.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0.")
    summary: str = Field(description="Brief one-sentence explanation of why this sentiment fits.")

def analyze_sentiment(text: str, models: list[str] | None = None) -> SentimentResult:
    prompt = f"""Analyze the sentiment of the following text using only the allowed sentiment labels.
Do not guess beyond what is supported by the text.

Text:
{text}
"""
    last_error = None
    for model_name in (models or FALLBACK_MODELS):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=SentimentResult,
                ),
            )
            return response.parsed
        except errors.ServerError as e:
            last_error = e
            continue
    raise last_error