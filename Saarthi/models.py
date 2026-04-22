from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Union

# --- Hidden Proxy Data (The Ground Truth) ---

class ProxyValues(BaseModel):
    """
    The 'Ground Truth' data stored in the Environment's hidden state.
    Linked to the account but NOT visible in the observation by default.
    """
    # MSME Truths
    gst_regularity: str = "regular" 
    guarantor_trust: float = 0.8
    
    # Startup Truths
    github_activity: float = 1.0  # 1.0 = Normal, 0.5 = 50% drop
    hiring_status: str = "hiring"
    investor_sentiment: float = 0.9

# --- Observable Models ---

class Message(BaseModel):
    month: int
    role: Literal["rm", "borrower"]
    content: str
    action_type: Optional[str] = None

class AccountState(BaseModel):
    """
    The LLM's view of a business. Proxies only appear here when asked.
    """
    account_id: int
    account_type: Literal["msme", "startup"]
    industry_or_sector: str
    dpd: int = 0
    is_npa: bool = False
    
    # Track of conversation per account
    convo_history: List[Message] = []
    
    # REVEALED PROXIES: Linked here ONLY after an investigation action
    # If the LLM hasn't asked, this dictionary remains empty.
    revealed_info: Dict[str, Union[str, float]] = Field(default_factory=dict)

# --- The Global Observation (What the Agent Sees) ---

class SaarthiObservation(BaseModel):
    current_month: int
    portfolio_npa_rate: float
    accounts: List[AccountState]
    active_notifications: List[int]  # List of accounts needing RM attention