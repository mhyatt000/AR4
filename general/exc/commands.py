from com import COM
from gui.base import EntryField

def prog_entry():
    """docstring"""

    EntryField.active['prog'].delete(0, "end")
    EntryField.active['prog'].insert(0, progNum)
    loadProg()
    time.sleep(0.4)
    index = 0
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(index)


def call_p():
    """docstring"""

    if moveInProc == 1:
        moveInProc = 2
    tab1.lastRow = tab1.progView.curselection()[0]
    tab1.lastProg = EntryField.active['prog'].get()
    programIndex = command.find("Program -")
    progNum = str(command[programIndex + 10 :])
    prog_entry()


def return_prog():
    """docstring"""

    if moveInProc == 1:
        moveInProc = 2
    lastRow = tab1.lastRow
    lastProg = tab1.lastProg
    prog_entry()


def read_encoders():
    """docstring"""

    # TODO bring back
    # if moveInProc == 1:
        # moveInProc = 2

    command = "RE\n"

    EntryField.active['cmd_sent'].entry.delete(0, "end")
    EntryField.active['cmd_sent'].entry.insert(0, command)

    response = COM.serial_write(command)

    # TODO bring back
    # manEntryField.delete(0, "end")
    # manEntryField.insert(0, response)


def test_limit_switch():
    """docstring"""

    # if moveInProc == 1:
        # moveInProc == 2

    command = "TL\n"
    response = COM.serial_write(command)

    # manEntryField.delete(0, "end")
    # manEntryField.insert(0, response)

