from matrix_lite import led, gpio
from random import randint
import time
import threading


def simon(simonList):
    # For every color simon has in the list turn on the led that color
    for color in simonList:
        led.set(color)
        time.sleep(0.40)
        # Turn it off for a bit to differentiate the list
        led.set('black')
        time.sleep(0.25)


def gameover():
    global simonList
    for i in range(3):
        led.set('red')
        time.sleep(0.5)
        led.set('white')
        time.sleep(0.5)
    led.set('black')
    nextTurn()
    simonList = []


def nextTurn():
    everloop = ['black'] * led.length
    everloop[0] = {'b':100}

    for x in range(led.length):
        everloop.append(everloop.pop(0))
        led.set(everloop)
        time.sleep(0.01)


def user(simonList):
    counter = 0
    # Check every press until you match simon's pattern
    while not (counter == len(simonList)):
        # Restart game
        if counter == -1:
            return
        if(not gpio.getDigital(bluePin)):
            counter = verifySimon('blue', bluePin, counter)
        elif(not gpio.getDigital(greenPin)):
            counter = verifySimon('green', greenPin, counter)
        elif(not gpio.getDigital(yellowPin)):
            counter = verifySimon('yellow', yellowPin, counter)
        elif(not gpio.getDigital(redPin)):
            counter = verifySimon('red', redPin, counter)
    nextTurn()

def verifySimon(color, pin, counter):
    # All push logic is opposite(!push == pushed)
    led.set(color)
    if(simonList[counter] == color):
        counter += 1
    else:
        gameover()
        return -1
    # User is holding the button, avoid double input
    while True:
        # When the user lets go break the loop
        if(gpio.getDigital(pin)):
            led.set('black')
            break
    return counter


def colorPick():
    # Pick a random number representing one of four colors
    x =  randint(0,3)

    # Return the color matching that random number
    if x == 0:
        color = 'blue'
    elif x == 1:
        color = 'green'
    elif x == 2:
        color = 'yellow'
    else:
        color = 'red'
    return color


simonList = []
bluePin = 0
greenPin = 2
yellowPin = 4
redPin = 6

gpio.setFunction(bluePin, 'DIGITAL')
gpio.setFunction(greenPin, 'DIGITAL')
gpio.setFunction(yellowPin, 'DIGITAL')
gpio.setFunction(redPin, 'DIGITAL')
gpio.setMode(bluePin, 'input')
gpio.setMode(greenPin, 'input')
gpio.setMode(yellowPin, 'input')
gpio.setMode(redPin, 'input')

while True:
    # Add color to list
    simonList.append(colorPick())
    # Show the pattern
    simon(simonList)
    # Get user to repeat the pattern
    user(simonList)
