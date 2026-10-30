class CSpecialAttack:
    def __init__(self, special_info:dict) -> None:
        self.cooldown = special_info["cooldown"]
        self.remaining = 0.0

    @property
    def ready(self) -> bool:
        return self.remaining <= 0.0
