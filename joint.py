import tkinter as tk

class JointCTRL:
    """A robotic joint controller"""

    active = []  # all axis
    main = []  # 6 main axis
    external = []  # external axis

    # pos, neg
    limits = [
        [170, 170],
        [90, 42],
        [52, 89],
        [165, 165],
        [105, 105],
        [155, 155],
        [340, 0],
        [340, 0],
        [340, 0],
    ]

    def __init__(self, gui):

        self.gui = gui

        JointCTRL.active.append(self)
        if len(JointCTRL.main) < 6:
            JointCTRL.main.append(self)
        else:
            JointCTRL.external.append(self)

        self.idx = len(JointCTRL.active) - 1
        self.name = f"J{self.idx+1}"

        # int
        self.open_loop_stat = None
        self.cal_stat = [tk.IntVar(), tk.IntVar()]

        self.limits = JointCTRL.limits[self.idx]
        self.range = sum(self.limits)
        self.limits = {"pos": self.limits[0], "neg": self.limits[1]}

        self.angle = None
        self.open_loop = False


