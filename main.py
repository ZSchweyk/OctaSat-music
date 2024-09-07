import RPi.GPIO as GPIO
from time import sleep
import csv
import os
from sys import exit
#
from songs.Buzzer import Buzzer  # Assuming your Buzzer class is in a 'modules' folder

class SongPlayer:
    def __init__(self, buzzer_pin, song_folder="songs"):
        self.buzzer = Buzzer(buzzer_pin)
        self.song_folder = song_folder

    def play_song(self, song_name):
        song_path = os.path.join(self.song_folder, f"{song_name}.csv")
        if not os.path.exists(song_path):
            print(f"[!] Song '{song_name}' not found in folder '{self.song_folder}'")
            return

        print(f"[+] Playing '{song_name}'...")
        with open(song_path, newline='') as csvfile:
            song_reader = csv.reader(csvfile)
            for row in song_reader:
                if len(row) < 2:
                    continue
                frequency = int(row[0])
                duration = float(row[1])
                self.buzzer.play_tone(frequency, duration)
                sleep(0.05)  # Short pause between notes

    def cleanup(self):
        self.buzzer.destroy()

if __name__ == "__main__":
    BUZZER_PIN = 12
    player = SongPlayer(BUZZER_PIN)

    try:
        # Play the songs in order
        player.play_song('tetris')  # Tetris theme song
        player.play_song('scale')   # Simple scale
        player.play_song('simple_song')  # Another song

    except KeyboardInterrupt:
        print("[!] Interrupted. Cleaning up...")
    finally:
        player.cleanup()
