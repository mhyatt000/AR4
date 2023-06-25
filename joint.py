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

        # TODO use list?
        self.no_calibrate = tk.IntVar()
        self.no_calibrate2 = tk.IntVar()

        self.limits = JointCTRL.limits[self.idx]
        self.range = sum(self.limits)
        self.limits = {"pos": self.limits[0], "neg": self.limits[1]}

        # TODO should angle be initialized to something else?
        # ie: read encoder?
        # maybe not
        self.angle = 0.0
        self.open_loop = tk.IntVar()


