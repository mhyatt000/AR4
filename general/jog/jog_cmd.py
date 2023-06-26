import calibrate
from gui.base import EntryField
from com import COM
from gui.base import GUI
from joint import JointCTRL

# TODO this should totally go in util.py
def record_command(command):
    EntryField.active['cmd_sent'].entry.delete(0, "end")
    EntryField.active['cmd_sent'].entry.insert(0, command)

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

    if response[:1] == "E":
        print('handle')
        handle_error(response)
    else:
        print('display pos')
        calibrate.display_position(response)


def get_loopmode():
    return "".join([str(x.open_loop.get()) for x in  JointCTRL.active])



def joint_jog(joint, value):
    """basic jog... positive or negative value indicates direction"""

    joints = JointCTRL.active
    angles = [J.angle for J in joints]


    if not GUI.use_xbox:
        COM.alarm("SYSTEM READY", False)

    # TODO is this redundant code??
    # see calibrate.check_speed()

    calibrate.check_speed()
    speed_type = GUI.speed_option.get()
    speed_prefix = {"Seconds": "Ss", "Percent": "Sp"}.get(speed_type, None)

    if speed_type == "mm per Sec":
        OptionMenu(tab1, speed_option, "Percent", "Percent", "Seconds", "mm per Sec")
        speed_prefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")

    fields = [
        EntryField.active["speed"],
        EntryField.active["ACCspeed"],
        EntryField.active["DECspeed"],
        EntryField.active["ACCramp"],
    ]
    Speed, ACCspd, DECspd, ACCramp = map(lambda x: x.entry.get(), fields)

    loopmode = get_loopmode()

    chars = ["A", "B", "C", "D", "E", "F", "J7", "J8", "J9"]
    angles[joint] += value

    prefix = "RJ"
    direction = "".join([f"{a}{b}" for a, b in zip(chars, angles)])
    WC = "F" if float(JointCTRL.active[4].angle) > 0 else "N"
    suffix = f"{speed_prefix }{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{loopmode}\n"

    command = prefix + direction + suffix
    # TODO add in
    record_command(command)

    response = COM.serial_write(command)
    print(response)
    serial_err_handle(response)


def LiveJointJog(value):
    command = f"LJV{value}{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{loopmode}\n"
    return command


def live_car_jog(value):
    command = f"LCV{value}{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{loopmode}\n"
    return command


def LiveToolJog(value):
    command = f"LTV{value}{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{loopmode}\n"
    return command


def stop_jog():
    command = "S\n"
    is_increment = int(GUI.is_increment.get())
    if not is_increment:
        response = COM.serial_write(command)
        serial_err_handle(response)


def car_jog(value, axis):
    """cartesian jog"""
    """instead of jogging a joint, jog in x,y,z"""

    checkSpeedVals()

    if not GUI.use_xbox:
        COM.alarm("SYSTEM READY", False)

    speedtype = speed_option.get()
    options = {"mm per Sec": "Sm", "Seconds": "Ss", "Percent": "Sp"}
    speedPrefix = options.get(speedtype)

    fields = [speedEntryField, ACCspeedField, DECspeedField, ACCrampField]
    Speed, ACCspd, DECspd, ACCramp = map(lambda x: x.get(), fields)

    positions = {k:A.position for A in Axisframe.active.items()}
    positions[axis] += value

    j7,j8,j9 = [J.position for J in JointCTRL.external]

    loopmode = get_loopmode()

    command = (
        f"MJX{pos['x']}Y{pos['y']}Z{pos['z']}Rz{pos['rx']}Ry{pos['ry']}Rx{pos['rz']}"+
        f'J7{j7}J8{j8}J9{j9}'
        f"{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{loopmode}\n"
    )

    response = COM.serial_write(command)
    serial_err_handle(response)


def tjog_position(value, axis):
    """instead of jogging a joint, jog in x,y,z"""

    checkSpeedVals()

    if not GUI.use_xbox:
        COM.alarm("SYSTEM READY", False)

    speedtype = speed_option.get()
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
