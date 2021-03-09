import machine
import utime

def ac_on(button):
    button.on()

def ac_off(button):
    button.off()

button = machine.Pin(16, machine.Pin.OUT)

while True:
    ac_on()
    utime.sleep(10)
    ac_off()
    utime.sleep(10)