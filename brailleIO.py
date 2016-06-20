import RPi.GPIO as GPIO
import time
import pygame
import settings


def setupGPIO():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(settings.button1,GPIO.IN ,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(settings.button1, GPIO.FALLING, bouncetime = 200)

    GPIO.setup(settings.button2,GPIO.IN ,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(settings.button2, GPIO.FALLING, bouncetime = 200)

    GPIO.setup(settings.button3,GPIO.IN ,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(settings.button3, GPIO.FALLING, bouncetime = 200)

    GPIO.setup(settings.button4,GPIO.IN ,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(settings.button4, GPIO.FALLING, bouncetime = 200)

    GPIO.setup(settings.button5,GPIO.IN ,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(settings.button5, GPIO.FALLING, bouncetime = 200)

    GPIO.setup(settings.button6,GPIO.IN ,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(settings.button6, GPIO.FALLING, bouncetime = 200)

    GPIO.setup(settings.button7,GPIO.IN ,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(settings.button7, GPIO.FALLING, bouncetime = 200)

    GPIO.setup(settings.button8,GPIO.IN ,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(settings.button8, GPIO.FALLING, bouncetime = 200)

    GPIO.setup(settings.button9,GPIO.IN ,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(settings.button9, GPIO.FALLING, bouncetime = 200)


    GPIO.setup(settings.vib1,GPIO.OUT)
    GPIO.setup(settings.vib2,GPIO.OUT)
    GPIO.setup(settings.vib3,GPIO.OUT)
    GPIO.setup(settings.vib4,GPIO.OUT)
    GPIO.setup(settings.vib5,GPIO.OUT)
    GPIO.setup(settings.vib6,GPIO.OUT)
    GPIO.setup(settings.vib9,GPIO.OUT)


def clearGPIO():
    GPIO.event_detected(settings.button1)
    GPIO.event_detected(settings.button2)
    GPIO.event_detected(settings.button3)
    GPIO.event_detected(settings.button4)
    GPIO.event_detected(settings.button5)
    GPIO.event_detected(settings.button6)
    GPIO.event_detected(settings.button7)
    GPIO.event_detected(settings.button8)
    GPIO.event_detected(settings.button9)

def clearInputs():
    clearGPIO()
    pygame.event.clear()

def button2Braille(arg):
    switcher = {
        100000: 'a',
        110000: 'b',
        100100: 'c',
        100110: 'd',
        100010: 'e',
        110100: 'f',
        110110: 'g',
        110010: 'h',
        10100: 'i',
        10110: 'j',
        101000: 'k',
        111000: 'l',
        101100: 'm',
        101110: 'n',
        101010: 'o',
        111100: 'p',
        111110: 'q',
        111010: 'r',
        11100: 's',
        11110: 't',
        101001: 'u',
        111001: 'v',
        10111: 'w',
        101101: 'x',
        101111: 'y',
        101011: 'z',
        99: ' '
        }
    return switcher.get(arg, '')

def button2Key(arg):
    switcher = {
        100000: 1,
        10000: 2,
        1000: 3,
        100: 4,
        10: 5,
        1: 6,
        }
    return switcher.get(arg,0)

def letter2Vibrator(letter):
    # To Do: put error check for having all vibrators defined
    vib1 = settings.vib1
    vib2 = settings.vib2
    vib3 = settings.vib3
    vib4 = settings.vib4
    vib5 = settings.vib5
    vib6 = settings.vib6
    vib9 = settings.vib9
    switcher = {
        'a':[vib1],
        'b':[vib1,vib2],
        'c':[vib1,vib4],
        'd':[vib1,vib4,vib5],
        'e':[vib1,vib5],
        'f':[vib1,vib2,vib4],
        'g':[vib1,vib2,vib4,vib5],
        'h':[vib1,vib2,vib5],
        'i':[vib2,vib4],
        'j':[vib2,vib4,vib5],
        'k':[vib1,vib3],
        'l':[vib1,vib2,vib3],
        'm':[vib1,vib3,vib4],
        'n':[vib1,vib3,vib4,vib5],
        'o':[vib1,vib3,vib5],
        'p':[vib1,vib2,vib3,vib4],
        'q':[vib1,vib2,vib3,vib4,vib5],
        'r':[vib1,vib2,vib3,vib5],
        's':[vib2,vib3,vib4],
        't':[vib2,vib3,vib4,vib5],
        'u':[vib1,vib3,vib6],
        'v':[vib1,vib2,vib3,vib6],
        'w':[vib2,vib4,vib5,vib6],
        'x':[vib1,vib3,vib4,vib6],
        'y':[vib1,vib3,vib4,vib5,vib6],
        'z':[vib1,vib3,vib5,vib6],
        ' ':[vib9]
        }
    return switcher.get(letter)


def vibrateKeys(pause,times):
    for i in range(times):
        for v in setting.vibs:
            GPIO.output(v,1)
        pygame.time.delay(pause)
        for v in vibs:
           GPIO.output(v,0)
        pygame.time.delay(pause)

def vibrateHint(vibs,pause,times):
    for i in range(times):
        for v in vibs:
            GPIO.output(v,1)
            pygame.time.delay(pause)
            GPIO.output(v,0)
            pygame.time.delay(pause)
def vibrateButtons(v,pause):
        GPIO.output(v,1)
        pygame.time.delay(pause)
        GPIO.output(v,0)
        pygame.time.delay(2 * pause)
