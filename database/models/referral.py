# database/models/referral.py

from datetime import datetime

class Referral:
    def __init__(
        self,
        referrer_id: int,
        referred_id: int,
        created_at: datetime = None,
        reward_given: bool = False
    ):
        self.referrer_id = referrer_id  # jo invite kar raha hai
        self.referred_id = referred_id  # jo join kar raha hai
        self.created_at = created_at or datetime.utcnow()
        self.reward_given = reward_given

    def mark_reward_given(self):
        """Mark that referral reward has been granted."""
        self.reward_given = True

    def to_dict(self):
        return {
            "referrer_id": self.referrer_id,
            "referred_id": self.referred_id,
            "created_at": self.created_at.isoformat(),
            "reward_given": self.reward_given,
        }
