class CInputCommand:
    def __init__(self, name:str, key:int, is_mouse:bool = False) -> None:
        self.name = name
        self.key = key
        self.is_mouse = is_mouse
        self.phase = "NA"
        self.mouse_pos = (0, 0)
