import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import threading


class PomodoroApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pomodoro & Clock")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        self.root.configure(bg="black")  # Black theme

        # Timer and mode settings
        self.work_minutes = 25
        self.break_minutes = 5
        self.cycles = 4
        self.current_cycle = 1
        self.running = False
        self.pomodoro_mode = False  # Default to clock mode

        # Stats
        self.completed_cycles = 0
        self.total_work_time = 0
        self.total_break_time = 0
        self.history = []

        # UI Elements
        self.create_widgets()
        self.update_time()

    def create_widgets(self):
        """Creates the GUI layout."""
        # Current date and time
        self.date_time_label = tk.Label(
            self.root, text="", font=("Helvetica", 12), fg="white", bg="black"
        )
        self.date_time_label.pack(pady=10)

        # Timer display
        self.timer_label = tk.Label(
            self.root, text="", font=("Helvetica", 40), fg="white", bg="black"
        )
        self.timer_label.pack(pady=20)

        # Mode selection
        self.mode_frame = tk.Frame(self.root, bg="black")
        self.mode_frame.pack(pady=10)

        self.mode_label = tk.Label(
            self.mode_frame, text="Mode:", font=("Helvetica", 12), fg="white", bg="black"
        )
        self.mode_label.grid(row=0, column=0, padx=5)

        self.mode_var = tk.StringVar(value="Clock")
        self.clock_mode_button = tk.Radiobutton(
            self.mode_frame,
            text="Clock",
            variable=self.mode_var,
            value="Clock",
            command=self.switch_mode,
            font=("Helvetica", 10),
            fg="white",
            bg="black",
            selectcolor="gray",
        )
        self.clock_mode_button.grid(row=0, column=1, padx=5)

        self.pomodoro_mode_button = tk.Radiobutton(
            self.mode_frame,
            text="Pomodoro",
            variable=self.mode_var,
            value="Pomodoro",
            command=self.switch_mode,
            font=("Helvetica", 10),
            fg="white",
            bg="black",
            selectcolor="gray",
        )
        self.pomodoro_mode_button.grid(row=0, column=2, padx=5)

        # Settings and buttons (hidden in clock mode)
        self.settings_frame = tk.Frame(self.root, bg="black")
        self.create_pomodoro_settings()

        # Stats and history (hidden in clock mode)
        self.stats_label = tk.Label(
            self.root,
            text="Stats: Completed Cycles: 0 | Total Work: 0 min | Total Break: 0 min",
            font=("Helvetica", 10),
            fg="white",
            bg="black",
        )

        self.history_label = tk.Label(
            self.root, text="History:", font=("Helvetica", 12), fg="white", bg="black"
        )
        self.history_text = tk.Text(
            self.root, height=10, width=50, bg="black", fg="white", font=("Helvetica", 10)
        )

    def create_pomodoro_settings(self):
        """Creates Pomodoro-specific settings."""
        tk.Label(
            self.settings_frame, text="Work (min):", font=("Helvetica", 10), fg="white", bg="black"
        ).grid(row=0, column=0, padx=5)
        self.work_input = tk.Entry(self.settings_frame, width=5)
        self.work_input.insert(0, "25")
        self.work_input.grid(row=0, column=1, padx=5)

        tk.Label(
            self.settings_frame, text="Break (min):", font=("Helvetica", 10), fg="white", bg="black"
        ).grid(row=0, column=2, padx=5)
        self.break_input = tk.Entry(self.settings_frame, width=5)
        self.break_input.insert(0, "5")
        self.break_input.grid(row=0, column=3, padx=5)

        tk.Label(
            self.settings_frame, text="Cycles:", font=("Helvetica", 10), fg="white", bg="black"
        ).grid(row=0, column=4, padx=5)
        self.cycles_input = tk.Entry(self.settings_frame, width=5)
        self.cycles_input.insert(0, "4")
        self.cycles_input.grid(row=0, column=5, padx=5)

        self.start_button = tk.Button(
            self.settings_frame, text="Start", command=self.start_timer, font=("Helvetica", 12), bg="gray", fg="white"
        )
        self.start_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.stop_button = tk.Button(
            self.settings_frame, text="Stop", command=self.stop_timer, font=("Helvetica", 12), bg="gray", fg="white"
        )
        self.stop_button.grid(row=1, column=2, columnspan=2, pady=10)

    def switch_mode(self):
        """Switches between Clock and Pomodoro modes."""
        if self.mode_var.get() == "Clock":
            self.pomodoro_mode = False
            self.settings_frame.pack_forget()
            self.stats_label.pack_forget()
            self.history_label.pack_forget()
            self.history_text.pack_forget()
            self.timer_label.config(text="")
            self.update_time()
        else:
            self.pomodoro_mode = True
            self.settings_frame.pack(pady=10)
            self.stats_label.pack(pady=10)
            self.history_label.pack(pady=10)
            self.history_text.pack(pady=10)
            self.timer_label.config(text="00:00")

    def update_time(self):
        """Updates the current date and time on the GUI."""
        if not self.pomodoro_mode:
            now = datetime.now()
            self.date_time_label.config(text=now.strftime("%A, %B %d, %Y - %H:%M:%S"))
            self.timer_label.config(text=now.strftime("%H:%M:%S"))
            self.root.after(1000, self.update_time)

    def start_timer(self):
        """Starts the Pomodoro timer with custom settings."""
        try:
            self.work_minutes = int(self.work_input.get())
            self.break_minutes = int(self.break_input.get())
            self.cycles = int(self.cycles_input.get())
            self.running = True
            self.current_cycle = 1
            self.run_pomodoro()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")

    def stop_timer(self):
        """Stops the timer."""
        self.running = False
        self.timer_label.config(text="00:00")
        self.stats_label.config(
            text=f"Stats: Completed Cycles: {self.completed_cycles} | Total Work: {self.total_work_time} min | Total Break: {self.total_break_time} min"
        )

    def run_pomodoro(self):
        """Runs the Pomodoro cycles."""
        if self.running and self.current_cycle <= self.cycles:
            self.timer_label.config(text=f"Work Session {self.current_cycle}/{self.cycles}")
            self.countdown(self.work_minutes * 60, "Work")
            if self.running:
                self.timer_label.config(text=f"Break {self.current_cycle}/{self.cycles}")
                self.countdown(self.break_minutes * 60, "Break")
                self.current_cycle += 1
                self.run_pomodoro()
        elif self.running:
            self.running = False
            messagebox.showinfo("Pomodoro", "All cycles completed!")

    def countdown(self, total_seconds, session_type):
        """Countdown logic."""
        while total_seconds > 0 and self.running:
            mins, secs = divmod(total_seconds, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            total_seconds -= 1
            self.root.update()
        if self.running:
            self.log_history(session_type)

    def log_history(self, session_type):
        """Logs session history."""
        now = datetime.now().strftime("%H:%M:%S")
        self.history.append(f"{session_type} session completed at {now}")
        self.history_text.insert("end", f"{session_type} session completed at {now}\n")
        self.history_text.see("end")

    def run(self):
        """Runs the Tkinter main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = PomodoroApp()
    app.run()
