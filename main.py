import screen_brightness_control as sbc
import PySimpleGUI as sg


def get_layout(brightness: list[int]):
    return [
        [sg.Slider(tooltip='Brightness (press Apply)', range=(1, 100), default_value=100, key='brightness',
                   orientation='horizontal')],
        [sg.Slider(tooltip='Brightness', range=(1, 100), default_value=brightness[x], key=x,
                   orientation='horizontal', enable_events=True) for x in range(len(brightness))],
        [sg.Ok('Apply')]
    ]


if __name__ == "__main__":
    sg.theme('DarkGrey8')
    br = sbc.get_brightness()
    window = sg.Window('Brightness Control', get_layout(br))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, sg.WINDOW_CLOSED, 'Exit'):
            break
        if event == 'Apply':
            sbc.set_brightness(values['brightness'])
            for i, brig in enumerate(sbc.get_brightness()):
                window[i].update(brig)
        if type(event) is int:
            sbc.set_brightness(values[event], display=event)

