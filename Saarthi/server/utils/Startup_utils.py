import random

class StartupUtilities:
    @staticmethod
    def get_github_activity(hidden_health: float) -> float:
        """
        Simulates code commit frequency. 
        Lower health often correlates with code stagnation or key dev departures.
        """
        # Add slight noise to the ground truth health
        activity = hidden_health + random.uniform(-0.15, 0.05)
        return round(max(0.0, min(1.0, activity)), 2)

    @staticmethod
    def get_linkedin_pulse(hidden_health: float, optimism_bias: float) -> dict:
        """
        Simulates hiring posts vs. reality. 
        High optimism bias founders post 'hiring' even when health is low.
        """
        is_hiring_post_present = optimism_bias > 0.7 or hidden_health > 0.6
        
        # In reality, hiring is frozen if health is very low
        actual_status = "active" if hidden_health > 0.5 else "frozen"
        if hidden_health < 0.3:
            actual_status = "layoffs_detected"

        return {
            "recent_posts": "we_are_hiring" if is_hiring_post_present else "thought_leadership",
            "verified_status": actual_status
        }