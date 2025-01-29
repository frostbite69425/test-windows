import time
import os
import platform

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def play_alert():
    """Plays a sound to alert the user."""
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(440, 500)  # Beep at 440Hz for 500ms
    else:
        # Use `say` on macOS or `aplay`/`paplay` on Linux (install if necessary)
        os.system('say "Session over"' if platform.system() == 'Darwin' else 'echo -e "\a"')

def countdown(minutes, label):
    """Displays a live countdown for the specified minutes."""
    seconds = minutes * 60
    try:
        while seconds > 0:
            clear_screen()
            mins, secs = divmod(seconds, 60)
            print(f"{label}: {mins:02d}:{secs:02d}")
            time.sleep(1)
            seconds -= 1
    except KeyboardInterrupt:
        print("\nTimer interrupted. Exiting...")
        exit()
    play_alert()
    print(f"{label} is over! Time for the next session.")

def pomodoro(work_minutes=25, break_minutes=5, cycles=4):
    """Runs the Pomodoro timer with the specified durations."""
    for cycle in range(1, cycles + 1):
        print(f"Cycle {cycle}/{cycles}: Work session starting!")
        countdown(work_minutes, "Work")
        if cycle < cycles:
            print(f"Cycle {cycle}/{cycles}: Break time!")
            countdown(break_minutes, "Break")
    print("Pomodoro session complete! Great job!")
    play_alert()

if __name__ == "__main__":
    # Customize your Pomodoro timer settings here
    work_minutes = int(input("Enter work session duration (minutes): "))
    break_minutes = int(input("Enter break duration (minutes): "))
    cycles = int(input("Enter number of cycles: "))
    
    pomodoro(work_minutes, break_minutes, cycles)
