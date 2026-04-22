from uuid import uuid4
from typing import Dict, List
from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from .models import SaarthiAction, SaarthiObservation, AccountState, ProxyValues
from .utils.startup_utils import StartupUtilities
from .utils.msme_utils import MSMEEssentials

class SaarthiEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.current_month = 1
        self._hidden_world: Dict[int, ProxyValues] = {} 
        self.portfolio: List[AccountState] = []

    def reset(self) -> SaarthiObservation:
        """Initializes a new 36-month portfolio episode."""
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.current_month = 1
        self._hidden_world = {}
        self.portfolio = []
        
        # Populate World: 20 MSME, 10 Startup
        for i in range(30):
            is_startup = i >= 20
            # Ground Truth is hidden from the Observation
            self._hidden_world[i] = ProxyValues(
                health=random.uniform(0.3, 0.9),
                bias=random.uniform(0.2, 0.9) if is_startup else 0.1
            )
            self.portfolio.append(AccountState(
                account_id=i,
                account_type="startup" if is_startup else "msme",
                revealed_info={} # Empty until tool is called
            ))
        return self._get_observation()

    def step(self, actions: List[SaarthiAction]) -> SaarthiObservation:
        """Advancing the month after processing batch actions."""
        self._state.step_count += 1
        
        for action in actions:
            self._handle_action(action)

        self.current_month += 1
        done = self.current_month > 36 or self._check_failure()
        
        return self._get_observation(done=done)

    def _handle_action(self, action: SaarthiAction):
        """Routes investigation tools to specific utilities."""
        acc_id = action.account_id
        hidden = self._hidden_world[acc_id]
        acc = self.portfolio[acc_id]

        # On-demand linking of proxies
        if action.action_type == "check_github_activity":
            acc.revealed_info["github"] = StartupUtilities.get_github_activity(hidden.health)
        elif action.action_type == "verify_gst_portal":
            acc.revealed_info["gst"] = MSMEEssentials.get_gst_status(hidden.health)
        # ... other tool routing ...

    def _get_observation(self, done: bool = False) -> SaarthiObservation:
        return SaarthiObservation(
            current_month=self.current_month,
            accounts=self.portfolio,
            done=done
        )