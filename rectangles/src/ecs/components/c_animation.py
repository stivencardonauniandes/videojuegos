class AnimationData:
    def __init__(self, name:str, start:int, end:int, framerate:float) -> None:
        if end < start:
            raise ValueError(f"Animación {name}: end < start")
        if framerate == 0:
            raise ValueError(f"Animación {name}: framerate no puede ser 0")
        self.name = name
        self.start = start
        self.end = end
        self.framerate = framerate

class CAnimation:
    def __init__(self, anim_info:dict) -> None:
        self.number_frames = anim_info["number_frames"]
        self.animations = {
            a["name"]: AnimationData(a["name"], a["start"], a["end"],
                                     a["framerate"])
            for a in anim_info["list"]
        }
        self.curr_anim_name = anim_info["list"][0]["name"]
        self.curr_anim_time = 0.0
        self.curr_frame = self.animations[self.curr_anim_name].start
        self.finished = False

    def set_animation(self, name:str) -> None:
        if name == self.curr_anim_name:
            return
        self.curr_anim_name = name
        self.curr_anim_time = 0.0
        self.curr_frame = self.animations[name].start
        self.finished = False
