from tkinter import *
from tkinter import ttk


class DasGuiBehavior:

    def __init__(self):
        self.root = None
        self._run_engine_request_pressed = False
        self._stop_engine_request_pressed = False
        self._is_music_on_request_pressed = False
        self._is_blinking_request_pressed = False
        self.car_is_moving_request_pressed = False
        self.is_btn_exit_pressed = False
        self.sm = None

        # Layout
        self.row = 0
        self.column = 0
        self.pad_x = 4
        self.pad_y = 4

        self.speed = None

        # Widgets
        self.is_engine_runningText = None
        self.start_engine_btn = None
        self.engine_btn_text = None
        self.is_music_onText = None
        self.audio_btn = None
        self.audio_btn_text = None
        self.is_blinkingText = None
        self.blinker_text = None
        self.radio_button_combo_box = None
        self.car_is_movingText = None

    def next_row(self):
        self.row += 1
        self.column = 0

    def next_col(self):
        self.column += 1

    def set_layout_options(self, item: Widget):
        item.grid(row=self.row, column=self.column, padx=self.pad_x, pady=self.pad_y)

    def create_button(self, text, command, disabled=False, width=None):
        text_var = StringVar()
        text_var.set(text)
        b = Button(self.root, textvariable=text_var, command=command, width=width,
                   state="disabled" if disabled else "normal")
        self.set_layout_options(b)
        return b, text_var

    def create_text_entry(self, can_edit=False, disabled=False, initial_text=None, width=None):
        text_var = StringVar()
        entry = Entry(self.root, textvariable=text_var, width=width,
                      state="normal" if can_edit else "disabled" if disabled else "readonly")
        self.set_layout_options(entry)
        if initial_text:
            text_var.set(initial_text)
        return text_var

    def create_combo_box(self, values, command=None, disabled=False, can_edit=False, initial_value=None, width=None):
        comboExample = ttk.Combobox(self.root, values=values, width=width,
                                    state="normal" if can_edit else "disabled" if disabled else "readonly")
        comboExample.bind("<<ComboboxSelected>>", command)
        self.set_layout_options(comboExample)
        if initial_value is not None:
            comboExample.current(initial_value)
        return comboExample

    def create_gui(self, root):
        self.root = root

        self.is_engine_runningText = self.create_text_entry(initial_text="Engine off", width=20)
        self.next_col()
        self.start_engine_btn, self.engine_btn_text = self.create_button("Start engine",
                                                                         command=self.on_engine_button, width=20)

        self.next_row()

        self.is_music_onText = self.create_text_entry(initial_text="Audio off", width=20)
        self.next_col()
        self.audio_btn, self.audio_btn_text = self.create_button("🔉", command=self.on_toggle_audio_button, width=20)

        self.next_row()

        self.is_blinkingText = self.create_text_entry(initial_text="Blinking off", width=20)
        self.next_col()
        self.radio_button_combo_box = self.create_combo_box(["Off", "On"], command=self.on_blinker_choice,
                                                            initial_value=0, width=20)

        self.next_row()

        self.speed = DoubleVar()
        self.car_speed = Scale(from_=0, to=240, orient=HORIZONTAL, variable=self.speed, command=self.on_scale_move)
        self.set_layout_options(self.car_speed)

        self.next_row()
        self.car_is_movingText = self.create_text_entry(initial_text="Car is standing", width=20)

    def on_engine_button(self):
        if self.engine_btn_text.get() == "Stop engine":
            self._stop_engine_request_pressed = True
        elif self.engine_btn_text.get() == "Start engine":
            self._run_engine_request_pressed = True

    def on_toggle_audio_button(self):
        self._is_music_on_request_pressed = True

    def on_blinker_choice(self, event):
        self._is_blinking_request_pressed = True

    def on_scale_move(self, event):
        self.car_is_moving_request_pressed = True

    # statechart synchronization events
    def run_engine_request_pressed(self):
        return self._run_engine_request_pressed

    def stop_engine_request_pressed(self):
        return self._stop_engine_request_pressed

    def is_music_on_request_pressed(self):
        return self._is_music_on_request_pressed

    def is_blinking_request_pressed(self):
        return self._is_blinking_request_pressed

    def car_is_moving_pressed_request(self):
        return self.car_is_moving_request_pressed

    def set_car_speed(self, speed):
        self.car_speed.set(speed)

    def clear_events(self):
        self._run_engine_request_pressed = False
        self._stop_engine_request_pressed = False
        self._is_music_on_request_pressed = False
        self._is_blinking_request_pressed = False
        self.car_is_moving_request_pressed = False

    def set_engine_state(self, state):
        self.is_engine_runningText.set(state)
        if state != "Off":
            self.audio_btn["state"] = "normal"
            self.car_speed["state"] = "normal"
            self.radio_button_combo_box["state"] = "normal"
            self.engine_btn_text.set("Stop engine")
        else:
            self.audio_btn["state"] = "disabled"
            self.car_speed["state"] = "disabled"
            self.radio_button_combo_box["state"] = "disabled"
            self.engine_btn_text.set("Start engine")

    def set_audio_state(self, state):
        self.is_music_onText.set(state)
        self.audio_btn_text.set("🔉")

    def set_blinking_state(self, state):
        self.is_blinkingText.set("Blinker " + state)

    def set_car_state(self, state):
        self.car_is_movingText.set(state)

    def is_btn_exit_pressed(self):
        return self.is_btn_exit_pressed
