import datetime as dt
import time


class TimeTools:
    def __init__(self, SimpleGUI):
        self.sg = SimpleGUI
        self.window = None
        self.timer = {x: None for x in ('status', 'start', 'end')}
        self.sw = {'running': False, 'time': 0, 'last': dt.datetime.now()}

    def timer_start(self, timedelta: dt.timedelta):
        self.timer['status'] = True
        self.timer['start'] = dt.datetime.now()
        self.timer['end'] = dt.datetime.now()+timedelta

    def timer_to_end(self):
        if not self.timer['status']:
            return None
        delta = self.timer['end'] - dt.datetime.now()
        if delta.total_seconds() <= 0:
            self.timer['status'] = False
            return dt.timedelta(0)
        return delta

    def timer_wait(self):
        delta = self.timer_to_end()
        if delta is None or delta.total_seconds() == 0:
            return
        time.sleep(delta.total_seconds())

    def get_layout(self):
        return [
            [self.sg.Text('', key='time_now')],
            [self.sg.Input(tooltip='Seconds', key='secs', size=5), self.sg.Text('secs'),
             self.sg.Input(tooltip='Minutes', key='mins', size=5), self.sg.Text('mins')],
            [self.sg.Button('Start timer')],
            [self.sg.Text('Stopwatch: '), self.sg.Button('Start/Pause', k='p_s'),
             self.sg.Button('Reset', k='r_s')],
            [self.sg.Text('', k='stopwatch')]
        ]

    def sw_time(self):
        if self.sw['running']:
            self.sw['time'] += (dt.datetime.now() - self.sw['last']).total_seconds()
            self.sw['last'] = dt.datetime.now()
        mins = self.sw['time'] // 60
        secs = round(self.sw['time'] % 60, 2)
        return f"{mins} minutes, {secs} seconds" if mins > 0 else f"{secs} seconds"

    def start_loop(self):
        self.window = self.sg.Window('TimeTools', self.get_layout())
        while True:
            event, values = self.window.read(timeout=10)
            if event in (self.sg.WIN_CLOSED, self.sg.WINDOW_CLOSED, 'Exit'):
                break
            if event == 'Start timer':
                try:
                    if values['secs']:
                        secs = int(values['secs'])
                    else:
                        secs = 0
                except ValueError:
                    self.window['secs'].update('Must be a number!')
                    continue

                try:
                    if values['mins']:
                        mins = int(values['mins'])
                    else:
                        mins = 0
                except ValueError:
                    self.window['mins'].update('Must be a number!')
                    continue

                self.timer_start(dt.timedelta(seconds=secs, minutes=mins))
                must_be = mins*60 + secs
                if must_be == 0:
                    continue
                self.window.hide()
                timer = time.time()
                while True:
                    to_end = self.timer_to_end()
                    if to_end is None:
                        to_end = 0
                    else:
                        to_end = int(to_end.total_seconds())+1

                    if not self.sg.one_line_progress_meter('Timer', must_be-to_end, must_be):
                        break

                    if to_end == 0:
                        break
                self.window.un_hide()
                print(time.time()-timer)
            if event == 'p_s':
                self.sw['running'] = not self.sw['running']
                self.sw['last'] = dt.datetime.now()
            if event == 'r_s':
                self.sw['running'] = False
                self.sw['time'] = 0

            self.window['time_now'].update(str(dt.datetime.now().strftime('%A %d %b %Y %H:%M:%S')))
            self.window['stopwatch'].update(self.sw_time())


if __name__ == '__main__':
    t = TimeTools()
    t.start_loop()
    timer = time.time()
    t.timer_start(dt.timedelta(seconds=2))
    t.timer_wait()
    print(time.time() - timer)
