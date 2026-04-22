from uuid import uuid4
from typing import Dict, List
from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from .models import (
        SaarthiAction, SaarthiObservation, AccountState, 
        ProxyValues, Message, ProxyData
    )
except ImportError:
    from models import (
        SaarthiAction, SaarthiObservation, AccountState, 
        ProxyValues, Message, ProxyData
    )

class SaarthiEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.current_month = 1
        self._hidden_world: Dict[int, ProxyValues] = {} 
        self.portfolio: List[AccountState] = []

    def reset(self) -> SaarthiObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.current_month = 1
        self._hidden_world = {}
        self.portfolio = []
        
        # Initialize 30 accounts with hidden ground truths
        for i in range(30):
            is_startup = i >= 20
            acc_type = "startup" if is_startup else "msme"
            
            # Link hidden proxies to account ID
            self._hidden_world[i] = ProxyValues(
                gst_regularity="regular" if not is_startup else "n/a",
                github_activity=1.0 if is_startup else 0.0
            )
            
            self.portfolio.append(AccountState(
                account_id=i,
                account_type=acc_type,
                industry_or_sector="fintech" if is_startup else "textile",
                outstanding_principal=500000.0,
                revealed_info={} # Hidden by default
            ))

        return self._get_observation()

    def step(self, action: SaarthiAction) -> SaarthiObservation:
        self._state.step_count += 1
        acc_id = action.account_id
        
        # Logic to 'Link' hidden proxies to revealed_info on demand
        if action.action_type == "check_github_activity":
            truth = self._hidden_world[acc_id].github_activity
            self.portfolio[acc_id].revealed_info["github_activity"] = truth
            
        elif action.action_type == "verify_gst_portal":
            truth = self._hidden_world[acc_id].gst_regularity
            self.portfolio[acc_id].revealed_info["gst_status"] = truth

        # Track conversation history per account
        if action.generated_text:
            self.portfolio[acc_id].convo_history.append(
                Message(month=self.current_month, role="rm", content=action.generated_text)
            )

        # Reward logic: placeholder for NPA/Recovery performance
        reward = 0.1 
        
        return self._get_observation(reward=reward)

    def _get_observation(self, reward: float = 0.0) -> SaarthiObservation:
        return SaarthiObservation(
            current_month=self.current_month,
            portfolio_npa_rate=0.0,
            accounts=self.portfolio,
            active_notifications=[a.account_id for a in self.portfolio if a.dpd > 0]
        )

    @property
    def state(self) -> State:
        return self._state