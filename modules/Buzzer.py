import RPi.GPIO as GPIO
from time import sleep

class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setwarnings(False)  # Disable GPIO warnings
        GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BCM
        GPIO.setup(self.pin, GPIO.OUT)  # Set pin as output
        self.pwm = GPIO.PWM(self.pin, 1)  # Set PWM on the pin, start with 1Hz frequency

    def init(self):
        # Play a startup melody, could be removed if not needed
        for frequency in [440, 523, 600, 990]:
            self.play_tone(frequency, 0.1)
            sleep(0.0005)
    
    def play_tone(self, frequency, duration):
        """Plays a tone with the specified frequency and duration."""
        self.pwm.start(50)  # Start PWM with 50% duty cycle
        self.pwm.ChangeFrequency(frequency)  # Change frequency to play the note
        sleep(duration)  # Play for the given duration
        self.pwm.stop()  # Stop PWM after the note is played

    def destroy(self):
        """Stops the buzzer and cleans up GPIO."""
        # Play a shutdown melody, could be removed if not needed
        for frequency in [990, 600, 523, 440]:
            self.play_tone(frequency, 0.1)
            sleep(0.0005)
        print("[!] Buzzer -- cleaning up GPIO")
        GPIO.cleanup(self.pin)  # Cleanup the specific GPIO pin used by the buzzer
