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

class AccountState(BaseModel):
    account_id: int
    account_type: Literal["msme", "startup"]
    industry_or_sector: str  # e.g., 'auto_ancillary' or 'fintech'
    
    # Financial State
    outstanding_principal: float
    dpd: int = Field(default=0, ge=0)
    payment_history: List[int] = []  # List of DPDs over time to detect patterns
    
    # it shows the signals of the borrower
    # Dict to allow flexible signals like {'gst_status': 1.0, 'github_commits': 0.6}
    proxies: Dict[str, float] = {} 
    
    # Relationship Tracking
    trust_score: float = Field(default=1.0, ge=0.0, le=1.0)
    convo_history: List[Message] = []  # Track of conversation per account
    
    is_npa: bool = False  # Terminal state for this account

class SaarthiAction(Action):
    """Action for the Saarthi environment - just a message to echo."""

    message: str = Field(..., description="Message to echo back")


class SaarthiObservation(Observation):
    """Observation from the Saarthi environment - the echoed message."""

    echoed_message: str = Field(default="", description="The echoed message")
    message_length: int = Field(default=0, description="Length of the echoed message")
