"""
Data models for the Saarthi Environment.

The Saarthi environment is a simple test environment that echoes back messages.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

class Message(BaseModel):
    month: int = Field(..., ge=1, le=36)
    role: Literal["rm", "borrower"]
    content: str  # The actual Hinglish/English text
    action_taken: Optional[str] = None  # If role is 'rm', which action was this?

class SaarthiAction(Action):
    """Action for the Saarthi environment - just a message to echo."""

    message: str = Field(..., description="Message to echo back")


class SaarthiObservation(Observation):
    """Observation from the Saarthi environment - the echoed message."""

    echoed_message: str = Field(default="", description="The echoed message")
    message_length: int = Field(default=0, description="Length of the echoed message")
