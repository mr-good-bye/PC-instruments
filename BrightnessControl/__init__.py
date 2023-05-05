import screen_brightness_control as sbc


class BrightnessControl:
    def __init__(self, SimpleGUI):
        self.sg = SimpleGUI
        self.br = sbc.get_brightness()
        self.window = None

    def get_layout(self):
        return [
            [self.sg.Slider(tooltip='Brightness (press Apply)', range=(1, 100), default_value=100, key='brightness',
                              orientation='horizontal')],
            [self.sg.Slider(tooltip='Brightness', range=(1, 100), default_value=self.br[x], key=x,
                              orientation='horizontal', enable_events=True) for x in range(len(self.br))],
            [self.sg.Ok('Apply')]
        ]

    def start_loop(self):
        self.window = self.sg.Window('Brightness Control', self.get_layout())
        while True:
            event, values = self.window.read()
            if event in (self.sg.WIN_CLOSED, self.sg.WINDOW_CLOSED, 'Exit'):
                break
            if event == 'Apply':
                sbc.set_brightness(values['brightness'])
                for i, brig in enumerate(sbc.get_brightness()):
                    self.window[i].update(brig)
            if type(event) is int:
                sbc.set_brightness(values[event], display=event)
