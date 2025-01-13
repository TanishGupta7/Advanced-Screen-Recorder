import cv2
import pyautogui
from win32api import GetSystemMetrics
import numpy as np
import time
import threading
import os
from pynput import keyboard

# Constants for screen dimensions
WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)
DIM = (WIDTH, HEIGHT)

# Global variables for stopping the recording
is_recording = True
record_start_time = None

def stop_recording():
    """Stops the recording when Ctrl+Q is pressed."""
    global is_recording
    print("\nRecording stopped manually.")
    is_recording = False

def record_video(output_path, duration, frame_rate=30):
    """Records the screen with the specified duration and frame rate."""
    global is_recording
    global record_start_time

    # Initialize video writer
    codec = cv2.VideoWriter_fourcc(*"mp4v")
    output = cv2.VideoWriter(output_path, codec, frame_rate, DIM)

    # Calculate the time per frame
    frame_time = 1 / frame_rate
    end_time = time.time() + duration

    print("Recording in progress...")
    record_start_time = time.time()

    while is_recording and time.time() < end_time:
        start_time = time.time()

        # Capture screenshot and convert to a frame
        image = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        output.write(frame)

        # Display the elapsed recording time
        elapsed_time = time.time() - record_start_time
        print(f"\rRecording... Elapsed: {elapsed_time:.2f}s", end="")

        # Maintain frame rate
        elapsed_frame_time = time.time() - start_time
        sleep_time = frame_time - elapsed_frame_time
        if sleep_time > 0:
            time.sleep(sleep_time)

    output.release()
    print("\nRecording completed! Saved to:", output_path)

def on_press(key):
    """Detects key presses for stopping the recording."""
    if key == keyboard.Key.ctrl_l:  # Ctrl + Q shortcut
        try:
            if keyboard.is_pressed("q"):
                stop_recording()
        except AttributeError:
            pass

def start_listener():
    """Starts a listener for the stop recording shortcut."""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def main():
    print("Welcome to the Screen Recorder!\n")
    
    # Get user inputs
    output_folder = input("Enter the folder to save the recording (default: current directory): ").strip() or "."
    file_name = input("Enter the file name (default: 'recording.mp4'): ").strip() or "recording.mp4"
    duration = int(input("Enter the recording duration in seconds (default: 10): ").strip() or "10")

    # Validate and prepare the output path
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, file_name)

    # Start the recording in a separate thread
    recording_thread = threading.Thread(target=record_video, args=(output_path, duration))
    recording_thread.start()

    # Start listening for the stop shortcut in the main thread
    print("Press Ctrl+Q to stop the recording manually.")
    start_listener()

if __name__ == "__main__":
    main()
