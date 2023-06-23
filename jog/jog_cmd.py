from com import COM
import calibrate
from joint import JointCTRL


def modify_speed(entry_field, val):
    cur_spd = int(entry_field.get())

    if val == 0:
        cur_spd = min(100, cur_spd + 1 if cur_spd < 5 else cur_spd + 5)
    elif val == 1:
        cur_spd = max(1, cur_spd - 1 if cur_spd <= 5 else cur_spd - 5)
    elif val == 2:
        cur_spd = 5

    entry_field.delete(0, "end")
    entry_field.insert(0, str(cur_spd))
    time.sleep(0.3)


def ChgDis(val):
    modify_speed(incrementEntryField, val)


def ChgSpd(val):
    modify_speed(speedEntryField, val)


def serial_err_handle(response):
    """docstring"""

    response = serial_write(command)
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def get_loopmode():
    return sum(map(lambda x: str(x.openloop_stat.get()), JointCTRL.active))


def joint_jog(joint, value):
    """basic jog... positive or negative value indicates direction"""

    joints = JointCTRL.active
    angles = [J.angle for J in joints]

    calibrate.check_speed()

    xboxuse = None
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    if xboxUse != 1:
        for alm in COM.alms:
            alm.config(text="SYSTEM READY", style="OK.TLabel")

    # TODO is this redundant code?? 
    # see calibrate.check_speed()
    """
    speedtype = speedOption.get()
    speedPrefix = {"Seconds": "Ss", "Percent": "Sp"}.get(speedtype, None)

    if speedtype == "mm per Sec":
        OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    """

    fields = [speedEntryField, ACCspeedField, DECspeedField, ACCrampField]
    Speed, ACCspd, DECspd, ACCramp = map(lambda x: x.get(), fields)

    loopmode = get_loopmode()

    chars = ['A','B','C','D','E','F','J7','J8','J9']
    angles[joint] += value

    prefix = 'RJ'
    direction = ''.join([f'{a}{b}' for a,b in zip(chars,angles)])
    suffix = f"{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{LoopMode}\n"

    command = prefix + direction + suffix
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)

    response = serial_write(command)
    serial_err_handle(response)


def LiveJointJog(value):
    command = f"LJV{value}{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{LoopMode}\n"
    return command


def LiveCarJog(value):
    command = f"LCV{value}{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{LoopMode}\n"
    return command


def LiveToolJog(value):
    command = f"LTV{value}{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{LoopMode}\n"
    return command


def stop_jog():
    command = "S\n"
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 0:
        response = serial_write(command)
        serial_err_handle(response)


def jog_position(value, axis):
    """instead of jogging a joint, jog in x,y,z"""

    checkSpeedVals()

    xboxUse = None
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")

    speedtype = speedOption.get()
    options = {"mm per Sec": "Sm", "Seconds": "Ss", "Percent": "Sp"}
    speedPrefix = options.get(speedtype)

    fields = [speedEntryField, ACCspeedField, DECspeedField, ACCrampField]
    Speed, ACCspd, DECspd, ACCramp = map(lambda x: x.get(), fields)

    xVal = XcurPos
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = RxcurPos

    position_updates = {
        "x": lambda: xVal + value,
        "y": lambda: yVal + value,
        "z": lambda: zVal + value,
        "rx": lambda: rxVal + value,
        "ry": lambda: ryVal + value,
        "rz": lambda: rzVal + value,
    }

    update_position = position_updates.get(axis)
    if update_position:
        xVal = update_position()

    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)

    loopmode = get_loopmode()

    command = (
        f"MJX{xVal}Y{yVal}Z{zVal}Rz{rzVal}Ry{ryVal}Rx{rxVal}J7{j7Val}J8{j8Val}J9{j9Val}"
        f"{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{loopmode}\n"
    )

    response = serial_write(command)
    serial_err_handle(response)


def tjog_position(value, axis):
    """instead of jogging a joint, jog in x,y,z"""

    checkSpeedVals()

    xboxUse = None
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")

    speedtype = speedOption.get()
    options = {"mm per Sec": "Sm", "Seconds": "Ss", "Percent": "Sp"}
    speedPrefix = options.get(speedtype)

    fields = [speedEntryField, ACCspeedField, DECspeedField, ACCrampField]
    Speed, ACCspd, DECspd, ACCramp = map(lambda x: x.get(), fields)

    xVal = XcurPos
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = RxcurPos

    position_updates = {
        "x": lambda: xVal + value,
        "y": lambda: yVal + value,
        "z": lambda: zVal + value,
        "rx": lambda: rxVal + value,
        "ry": lambda: ryVal + value,
        "rz": lambda: rzVal + value,
    }

    update_position = position_updates.get(axis)
    if update_position:
        xVal = update_position()

    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)

    loopmode = get_loopmode()

    command = (
        f"MJX{xVal}Y{yVal}Z{zVal}Rz{rzVal}Ry{ryVal}Rx{rxVal}J7{j7Val}J8{j8Val}J9{j9Val}"
        f"{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{loopmode}\n"
    )

    response = serial_write(command)
    serial_err_handle(response)


def tjog_command(axis, value):

    prefixes = {"TX": "JTX", "TY": "JTY", "TZ": "JTZ", "TRx": "JTW", "TRy": "JTP", "TRz": "JTR"}

    assert axis in prefixes, f"Invalid axis: {axis}"

    prefix = prefixes[axis]
    prefix += "1" if val < 0 else "0"
    val = abs(val)

    command = f"{prefix}{value}{speedPrefix}{Speed}G{ACCspd}H{DECspd}I{ACCramp}Lm{LoopMode}\n"
    return command
