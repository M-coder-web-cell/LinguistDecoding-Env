class MSMEEssentials:
    @staticmethod
    def get_gst_status(hidden_health: float) -> str:
        """
        Returns official portal filing status. 
        MSMEs in distress often miss GST deadlines before they miss loan EMIs.
        """
        if hidden_health > 0.75: return "filed_on_time"
        if hidden_health > 0.45: return "delayed_last_2_months"
        return "irregular_filing_gap_detected"

    @staticmethod
    def get_ally_verification(hidden_health: float, trust_score: float) -> str:
        """
        Simulates a call to a supplier or a business ally.
        Genuine MSMEs have allies who provide specific business details.
        """
        if hidden_health < 0.4 and trust_score < 0.5:
            return "allies_reporting_payment_delays"
        return "vouched_for_by_local_association"