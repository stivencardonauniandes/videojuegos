class CCooldownText:
    def __init__(self, interface_cfg:dict, font) -> None:
        self.cfg = interface_cfg["special"]
        self.font = font
        self.last_text = None
