import RPi.GPIO as GPIO
from time import sleep
import csv
import os
from sys import exit
from modules.Buzzer import Buzzer  # Importing the Buzzer class from the modules folder

class SongPlayer:
    def __init__(self, buzzer_pin, song_folder="songs"):
        self.buzzer = Buzzer(buzzer_pin)  # Initialize the Buzzer class with the specified pin
        self.song_folder = song_folder  # Path to the folder containing the songs

    def play_song(self, song_name):
        # Construct the full path to the song file
        song_path = os.path.join(self.song_folder, f"{song_name}.csv")
        
        # Check if the song exists
        if not os.path.exists(song_path):
            print(f"[!] Song '{song_name}' not found in folder '{self.song_folder}'")
            return

        print(f"[+] Playing '{song_name}'...")
        with open(song_path, newline='') as csvfile:
            song_reader = csv.reader(csvfile)
            
            # Read each note (frequency, duration) and play it
            for row in song_reader:
                if len(row) < 2:
                    continue  # Skip invalid rows
                try:
                    frequency = float(row[0])  # Use float to handle decimal frequencies
                    duration = float(row[1])   # Duration is also a float
                    self.buzzer.play_tone(frequency, duration)
                    sleep(0.05)  # Short pause between notes
                except ValueError as e:
                    print(f"[!] Error reading line: {row} - {e}")

    def cleanup(self):
        """Clean up the buzzer after playing the song."""
        self.buzzer.destroy()

if __name__ == "__main__":
    BUZZER_PIN = 12  # Define the GPIO pin used for the buzzer
    player = SongPlayer(BUZZER_PIN)  # Create an instance of SongPlayer

    try:
        # Play the songs in sequence
        player.play_song('tetris')  # Play the Tetris theme song
        player.play_song('scale')   # Play a simple scale
        player.play_song('simple_song')  # Play another sample song
        player.play_song('twinkle')  # Play the new Twinkle song

    except KeyboardInterrupt:
        print("[!] Interrupted. Cleaning up...")
    finally:
        # Ensure that GPIO is cleaned up properly
        player.cleanup()
