#!usr/bin/env python3

import time
import PySimpleGUI as ps
import threading


class MainWindow:
    def __init__(self):
        ps.theme('Black')
        self.layout = [
            [ps.Text('Hours', size=(15, 1)), ps.InputText(size=(10, 1))],
            [ps.Text('Minutes', size=(15, 1)), ps.InputText(size=(10, 1))],
            [ps.Text('Seconds', size=(15, 1)), ps.InputText(size=(10, 1))],
            [ps.Listbox(size=(7, 1), key="condition", font=("Helvetica", 64), values=('00:00:00',),
                        background_color=("Black"))],
            [ps.Button('Start')], [ps.Button('Stop')], [ps.Button('Resume')],
        ]
        self.window = ps.Window('Timer', self.layout)
        self.need_stop = False

    def run(self):
        countdown = []
        while True:
            event, values = self.window.read()
            try:
                if event == 'Start':
                    if not values[0]:
                        countdown.append(0)
                    else:
                        countdown.append(int(values[0]))
                    if not values[1]:
                        countdown.append(0)
                    else:
                        countdown.append(int(values[1]))
                    if not values[2]:
                        countdown.append(0)
                    else:
                        countdown.append(int(values[2]))
                    self.window.Element("condition").Update(values=(f'{countdown[0]}:{countdown[1]}:{countdown[2]}',))
                    th = threading.Thread(target=self.start, args=(countdown,))
                    th.daemon = True
                    th.start()
            except ValueError:
                ps.Popup('Not numb')
                pass
            if event == 'Stop':
                if th.is_alive():
                    self.need_stop = True
                else:
                    self.window.Element("condition").Update(values=('00:00:00',))
                    pass
            elif event == 'Resume':
                if th.is_alive():
                    pass
                else:
                    self.need_stop = False
                    th = threading.Thread(target=self.start, args=(countdown,))
                    th.daemon = True
                    th.start()
            elif event == ps.WIN_CLOSED:  # if user closes window
                if th.is_alive():
                    self.need_stop = True
                break
            time.sleep(0.2)

    def start(self, countdown):
        seconds = countdown[0] * 3600 + countdown[1] * 60 + countdown[2]
        while seconds:
            if self.need_stop:
                break
            time.sleep(1)
            seconds = seconds - 1
            countdown[0] = seconds // 3600
            countdown[1] = (seconds - countdown[0] * 3600) // 60
            countdown[2] = seconds - (countdown[0] * 3600 + countdown[1] * 60)
            self.window.Element("condition").Update(values=(f'{countdown[0]}:{countdown[1]}:{countdown[2]}',))


if __name__ == "__main__":
    w = MainWindow()
    w.run()
