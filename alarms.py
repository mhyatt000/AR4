def alarm_warn(text):
    """docstring"""

    almStatusLab.config(text=text, style="Warn.TLabel")
    almStatusLab2.config(text=text, style="Warn.TLabel")

def alarm_raise(text):
    """docstring"""

    almStatusLab.config(text=text, style="Alarm.TLabel")
    almStatusLab2.config(text=text, style="Alarm.TLabel")

def alarm_ok(text):
    """docstring"""

    almStatusLab.config(text=text, style="OK.TLabel")
    almStatusLab2.config(text=text, style="OK.TLabel")
