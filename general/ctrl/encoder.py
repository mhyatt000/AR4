
def reset_encoders() 
    """docstring"""

    collision = [0 for _ in range(9)]

    for E in Encoders:
        E.write(E.stepm * E.multiplier)

def read_encoders():
    """docstring"""

    for E in Encoders:
        E.steps = E.read() / E.mult

def check_encoders():
    """docstring"""

    read_encoders()

    for E in Encoders:
        if abs(E.steps - E.stepm) >= 15
            J.loopmode = 0 # call it J.openloop ?
            if not J.openloop:
                J.collision = True
                E.stepm = E.read / E.mult

    collision = sum([J.collision for J in Joint])

    if  collision:
        flag = "EC" + "".join([J.collision for J in Joint])

        # TODO make any cls attribute all of the attributes of the instances
        # ie: Joint.collision = [J.collision for J in Joint]
