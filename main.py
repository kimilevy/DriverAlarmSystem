import tkinter as tk

from DasGuiScBehavior import DasGuiBehavior
from alarm_statechart import AlarmStatechart




class Callback:
    """State machine uses callback operations (here: _synchronize()_).
    """

    def __init__(self, statemachine, gui):
        gui.sm = self.sm = statemachine
        self.gui = gui
        self.is_btn_exit_pressed = False

    def synchronize(self):

        # from GUI to statemachine
        if self.gui.run_engine_request_pressed():
            self.sm.raise_starting_the_engine()
        if self.gui.stop_engine_request_pressed():
            self.sm.raise_turning_off_the_engine()
        if self.gui.is_music_on_request_pressed():
            self.sm.raise_toggle_audio()
        if self.gui.is_blinking_request_pressed():
            self.sm.raise_swipe_lever()
        if self.gui.car_is_moving_pressed_request():
            self.sm.speed = self.gui.speed.get()
            if self.sm.speed == 0:
                self.sm.raise_car_standing()
            else:
                self.sm.raise_car_moved()
        if self.gui.is_btn_exit_pressed:
            self.is_btn_exit_pressed = True

        # from statemachine to GUI
        self.gui.set_car_speed(self.sm.speed)
        if isinstance(self.sm.system_state, str):
            self.gui.set_engine_state(self.sm.system_state)
        if isinstance(self.sm.music_state, str):
            self.gui.set_audio_state(self.sm.music_state)
        if isinstance(self.sm.signal_level_state, str):
            self.gui.set_blinking_state(self.sm.signal_level_state)
        if isinstance(self.sm.car_standing, str):
            self.gui.set_car_state(self.sm.car_standing)

        # clear GUI events
        self.gui.clear_events()


class Main:

    def __init__(self):
        self.sm = AlarmStatechart()
        self.root = tk.Tk()  # init GUI
        self.root.title("DAS SYSTEM")
        self.root.geometry("500x500")
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.gui = DasGuiBehavior()  # create GUI
        self.cb = Callback(self.sm, self.gui)

    def close_window(self):
        self.gui.is_btn_exit_pressed = True

    def run(self):
        self.gui.create_gui(self.root)
        self.sm.operation_callback = self.cb
        self.sm.enter()

        while self.root.winfo_exists and not self.cb.is_btn_exit_pressed:
            self.sm.run_cycle()
            #this is a loop that replaces the main_loop of tk
            self.root.update_idletasks()
            self.root.update()
        self.shutdown()

    def shutdown(self):
        print('State machine shuts down.')
        self.sm.exit()
        self.root.destroy()
        print('Bye!')


if __name__ == '__main__':
    m = Main()
    m.run()





