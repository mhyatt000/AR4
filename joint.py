# pos, neg
axis_limits = [
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


class Joint:
    """A robotic joint"""

    def __init__(self):

        self.name = "Unnamed Joint"

        # int
        self.open_loop_stat = None
        self.cal_stat = [None, None]
        self.axis_limits = [None, None]
        self.axis_total = sum(self.axis_limits)


joints = [Joint() for _ in range(6)]
