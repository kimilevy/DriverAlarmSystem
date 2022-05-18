from tkinter import *
from tkinter import ttk


class DasGuiWithBehavior:

    def __init__(self):
        self.root = None
        self.is_engine_running = False
        self.is_music_on = False
        self.is_blinking = False
        self.car_is_moving = False
        self.is_btn_exit_pressed = False

        # Layout
        self.row = 0
        self.column = 0
        self.pad_x = 4
        self.pad_y = 4

        self.speed = None

        # Widgets
        self.disable_when_engine_not_running = list()
        self.is_engine_runningText = None
        self.start_engine_btn = None
        self.start_engine_btn_text = None
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
        self.start_engine_btn, self.start_engine_btn_text = self.create_button("Start engine",
                                                                               command=self.on_engine_button, width=20)

        self.next_row()

        self.is_music_onText = self.create_text_entry(initial_text="Audio off", width=20)
        self.next_col()
        self.audio_btn, self.audio_btn_text = self.create_button("🔉", command=self.on_toggle_audio_button,
                                                                 disabled=True, width=20)
        self.disable_when_engine_not_running.append(self.audio_btn)

        self.next_row()

        self.is_blinkingText = self.create_text_entry(initial_text="Blinking off", width=20)
        self.next_col()
        self.radio_button_combo_box = self.create_combo_box(["Off", "On"], command=self.on_blinker_choice,
                                                            initial_value=0, disabled=True, width=20)
        self.disable_when_engine_not_running.append(self.radio_button_combo_box)

        self.next_row()

        self.speed = DoubleVar()
        self.car_is_moving = Scale(from_=0, to=240, orient=HORIZONTAL, variable=self.speed, state='disabled', command=self.on_scale_move)
        self.set_layout_options(self.car_is_moving)
        self.disable_when_engine_not_running.append(self.car_is_moving)

        self.next_row()
        self.car_is_movingText = self.create_text_entry(initial_text="Car is standing", width=20)

    def on_engine_button(self):
        if self.is_engine_running:
            self.is_engine_running = False
            self.is_engine_runningText.set("Off")
            self.start_engine_btn_text.set("Start engine")
            self.disable_buttons()
        else:
            self.is_engine_running = True
            self.is_engine_runningText.set("On")
            self.start_engine_btn_text.set("Stop engine")
            self.enable_buttons()

    def on_toggle_audio_button(self):
        if self.is_music_on:
            self.is_music_on = False
            self.is_music_onText.set("Audio off")
            self.audio_btn_text.set("🔉")
        else:
            self.is_music_on = True
            self.is_music_onText.set("Audio on")
            self.audio_btn_text.set("🔉")

    def enable_buttons(self):
        for button in self.disable_when_engine_not_running:
            if button is not None:
                button["state"] = "normal"

        pass

    def disable_buttons(self):
        for button in self.disable_when_engine_not_running:
            if button is not None:
                button["state"] = "disabled"
        pass

    def on_blinker_choice(self, event):
        value = self.radio_button_combo_box.get()
        if value != "Off":
            self.is_blinking = True
        self.is_blinkingText.set("Blinker " + value)

    def on_scale_move(self, event):
        var = self.speed.get()
        if var != 0:
            self.car_is_moving = True
            self.car_is_movingText.set("Car is moving")
        else:
            self.car_is_moving = False
            self.car_is_movingText.set("Car is standing")




