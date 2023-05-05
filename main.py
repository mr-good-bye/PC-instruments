from BrightnessControl import BrightnessControl
from TimeTools import TimeTools
import PySimpleGUI as SimpleGUI


def get_main_layout():
    CHUNK_SIZE = 5
    m = [SimpleGUI.Button(x, expand_x=True) for x in modules]
    return [m[x: x+CHUNK_SIZE] for x in range(0, len(m), CHUNK_SIZE)]


SimpleGUI.theme('DarkGrey8')
t = BrightnessControl(SimpleGUI)
tt = TimeTools(SimpleGUI)

modules = {
    'Brightness tool': t,
    'Time tools': tt,
}

w = SimpleGUI.Window('Dristarts Instruments', get_main_layout())
while True:
    e, v = w.read()
    if e in (SimpleGUI.WIN_CLOSED, SimpleGUI.WINDOW_CLOSED, 'Exit'):
        break
    if e in modules:
        w.hide()
        modules[e].start_loop()
        w.un_hide()
