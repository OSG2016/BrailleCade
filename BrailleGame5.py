################### BRAILLECADE #########################
# Braille Cade is an pygame for learning and teaching braille
# it was written in Python for the Raspberry Pi B+.  The hardware layout consists
# of six keys with 6 small vibrating motors.  ........




################ SETUP STUFF ##########################

### IMPORT MODULES ###
import pygame                       # Main Module that this program runs on
import RPi.GPIO as GPIO             # This is the library for Raspberry Pi input/ouput pins
import os
from os.path import join
from random import choice
import brailleIO                    # This library holds functions that link braille to letters and button presses
from brailleIO import button2Braille,button2Key, letter2Vibrator, vibrateKeys, vibrateHint, vibrateButtons
import time
import settings
from brailleSoundsInits import brailleSounds, lessonInit, playHold


### INIT SOUNDS ####
#Initialize Mixer               # For some reason initializing this library early in the code prevents a buggy delay with the sound
pygame.mixer.pre_init(22050, -16,  2, 512)
pygame.mixer.init()

soundDict = brailleSounds()
brailleIO.setupGPIO()               # Calls function from brailleIO to assign GPIO pins to buttons and vibrators

### GAME FLAGS ###                  # Here we initialize booliean flags which control what part of the game we are in.
quitGame = False
mainMenu = True                     
learnLetter = False
testLetter = False 
brailleNWail = False
whackADot = False
changingApp = True                  # This true when on the first enter the program or when you switch out of a game or main menu.  Used to announce program titles and games and instructions.  After this it is cleared.
lessons = False
lessonLoaded = False
message = False
### GAME VARIABLES ###              # here we initialize data needed in various games
attempts = 0
score = 0
question = True
### OTHER VARIABLES ###
letterModule1 = 'abcd'              # this is a stand-in variable that holds the string of letters from which the TestLetter game picks. 
whackModule = [settings.vib1,settings.vib2,settings.vib3,settings.vib4,settings.vib5,settings.vib6]
speakString = ''
bString = ''

############## SETUP PYGAME #################
pygame.init()
white = (255,255,255)               # Define Colors
black = (0,0,0)                     # Define Colors
red = (255,0,0)                     # Define Colors
displayWitdth = 800                 
displayHeight = 600                 
gameDisplay = pygame.display.set_mode((displayWitdth,displayHeight))        # Create display object 
bg = pygame.image.load("arcade.jpg")
pygame.display.set_caption('BrailleCade')                                   # Sets caption in game window
pygame.display.update()                                                     
clock = pygame.time.Clock()                                                 # Instantiate Clock.  We use this to define the frame rate of the game
font = pygame.font.SysFont(None,80)                                         # Define font we use this font to write letters to the screen

def message_to_screen(msg,color):                                           # We use this function to write messages to the screen, we specify messages and color
    screenText = font.render(msg,True,color)                                
    textPos = screenText.get_rect()                                         # save the center point object of the text box to the variable textBox.  Not exactly sure why we do it this way, we don't use the initial data probably just need the appropriate object to use in the blit function
    textPos.centerx = gameDisplay.get_rect().centerx                        # change the x position of textBox to the center of the display
    textPos.centery = gameDisplay.get_rect().centery                        #     ''     y                         ''
    gameDisplay.blit(screenText, textPos)                                   # the blit object updates the screen

def lessonMessage(msgU,colorU,msgL,colorL):
    screenTextU = font.render(msgU,True,colorU)
    textPosU = screenTextU.get_rect()
    textPosU.centerx = gameDisplay.get_rect().centerx
    textPosU.centery = gameDisplay.get_rect().centery - (font.get_height()/2)    
    gameDisplay.blit(screenTextU, textPosU)                               

    screenTextL = font.render(msgL,True,colorL)
    textPosL = screenTextL.get_rect()
    textPosL.x = textPosU.x
    textPosL.centery = gameDisplay.get_rect().centery + (font.get_height()/2)    
    gameDisplay.blit(screenTextL, textPosL) 

############## MAIN GAME LOOP #####################
# This is the main while loop of the braillecade. Pygame cycles through this loop
# once every frame.  Event handling and everything else is handled once a frame.
# The minimum frame rate is set by the clock.tick() function at the end of the loop.
# Actual frame time is dependent on processing needs.
#Calling espeak or another program may delay frame update.

while not quitGame:                                                         #The variable quitGame can be set true by the game or by user input.
    gameDisplay.fill(white)
    if speakString!= '':                                                    # If a string has been assigned to speakString from last time then say that now.
        os.system('sudo espeak -ven+f3 -s150 "{}"'.format(speakString))         # use espeak to say it
        speakString = ''                                                        # now that you said it shut up
        
    ######## EVENT HANDLING #########
    # this code checks to see if someone has pressed a button
    # since the last time we whent throught the game loop
    bCode = 0                                                               # Clear bCode.  bCode is a number (psuedo binary) that represents which of the braille keyboard keys, (or keys S,D,F,J,K,L) have been pressed 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                       # if the window "x" has been pressed quit the game
            quitGame = True
        if event.type == pygame.KEYDOWN:                                    # the following lines are event detection for braille key presses.  Notice that each adds (+=) 1 to a different decimal place of bCode 
            if event.key == pygame.K_f:
                bCode += 100000
            if event.key == pygame.K_d:
                bCode += 10000
            if event.key == pygame.K_s:
                bCode += 1000
            if event.key == pygame.K_j:
                bCode += 100
            if event.key == pygame.K_k:
                bCode += 10
            if event.key == pygame.K_l:
                bCode += 1
            if event.key == pygame.K_q:                                     # Typing q on the keyboard exits any game module by setting game flags to return to main menu
                mainMenu = True
                learnLetter = False
                testLetter = False 
                brailleNWail = False
                question = True
                changingApp = True
                message = False
                attempts = 0
                score = 0
            if event.key == pygame.K_SPACE:                                 # This needs to be changed, but space bar trumps all letter presses creates a space
                bCode = 99
                
    if GPIO.event_detected(settings.button1):                               # same as above but uses detects key presses on external buttons.
        bCode += 100000
    if GPIO.event_detected(settings.button2):
        bCode += 10000
    if GPIO.event_detected(settings.button3):
        bCode += 1000
    if GPIO.event_detected(settings.button4):
        bCode += 100
    if GPIO.event_detected(settings.button5):
        bCode += 10
    if GPIO.event_detected(settings.button6):
        bCode += 1
    if GPIO.event_detected(settings.button9):
        bCode = 99
    if GPIO.event_detected(settings.button7) and GPIO.event_detected(settings.button8):
            mainMenu = True
            learnLetter = False
            testLetter = False 
            brailleNWail = False
            question = True
            changingApp = True
            attempts = 0


    ########### GAME LOGIC #############
    # Here is the meat of the game.  It structured nested if-ifelse statements.
    # Which block of the code is executed is controlled by the gameflags

    ### MAIN MENU ####
    # Here user can navigate to games by pressing one of the braille buttons.
    # In the future I would like to have the main menu navigated by arrow keys
    if mainMenu == True:
        if changingApp == True:                         # First time here or returning?  
            changingApp = False                         # clear this flag so we don't have to hear this crap again
            displayText = 'Welcome'
            menuSelection = 0                           # Variable for represents choice of games
            soundDict['welcomeTo'].play()                          # Play Welcome message and instructions
            pygame.time.delay(500)                      # Delay game and allow message to play
            soundDict['brailleCade'].play()                        # Play Welcome message and instructions
            pygame.time.delay(500)                      # Delay game and allow message to play
            soundDict['instruction'].play()                       # Play Welcome message and instructions
            pygame.time.delay(1000)                     # Delay game and allow message to play
        if bCode == 100000:
            displayText = 'Test Letter'
            soundDict['testLetter'].play()
            menuSelection = 1
        if bCode == 10000:
            displayText = 'Braille-N Wail'
            soundDict['brailleNWail'].play()
            menuSelection = 2
        if bCode == 1000:
            displayText = 'Whack-A-Dot'
            soundDict['whackADot'].play()
            menuSelection = 3
        if bCode == 100:
            displayText = 'Lessons'
            soundDict['lessons'].play()
            menuSelection = 4
        if bCode == 99 and choice != 0:                 # if user has made a choice and then pressed space bar set flags to go to that game on the next loop.
            if menuSelection == 1:
                testLetter = True
            if menuSelection == 2:
                brailleNWail = True
            if menuSelection == 3:
                whackADot = True
            if menuSelection == 4:
                lessons = True
            mainMenu = False
            changingApp = True


    ### TEST LETTER ###
    elif testLetter == True:
        if changingApp == True:
            changingApp = False
            soundDict['welcomeTo'].play()
            pygame.time.delay(700)
            soundDict['testLetter'].play()
            pygame.time.delay(1000)
            pygame.display.update()
            question = True
            attempts = 0
        elif question == True:
            currentLetter = choice(letterModule1)
            displayText = currentLetter
            soundDict[currentLetter].play()
            question = False
        else:    
            bString = '{}'.format(button2Braille(bCode))
            if not bCode == 0:
                print(bCode)
                if bString == currentLetter:
                    soundDict['ding'].play()
                    pygame.time.delay(500)                    
                    question = True
                    attempts = 0
                else:
                  if attempts < 1:
                     attempts +=1
                     soundDict['try'].play()
                     pygame.time.delay(1000)
                     brailleIO.clearInputs()
                     soundDict[currentLetter].play()
                  else:
                     attempts = 0
                     soundDict['hint'].play()
                     pygame.time.delay(1000)
                     vibrateHint(letter2Vibrator(currentLetter),100,1)
                     brailleIO.clearInputs()

    ### BRAILLE AND WAIL ###
    elif brailleNWail == True:
        if changingApp == True:
            changingApp = False
            soundDict['brailleNWail'].play()
            pygame.display.update()
            bigString = ''
            lastWord = ''
        else:    
            bString = '{}'.format(button2Braille(bCode))
            if bString != '':
                if bString != ' ':
                    soundDict[button2Braille(bCode)].play()
                    bigString +=bString
                    lastWord += bString
                    displayText = bigString
                else:
                    speakString = lastWord
                    lastWord = ''
                    bigString +=bString
    ### WHACK-A-DOT###
    elif whackADot == True:
        if changingApp == True:
            soundDict['welcomeTo'].play()
            pygame.time.delay(700)
            soundDict['whackADot'].play()
            pygame.time.delay(1000)
            changingApp = False
        elif question == True:
            currentKey = choice(range(6))
            print(currentKey + 1)
            vibrateButtons(whackModule[currentKey],100)
            question = False
            attempts = 0
        else:    
            if not bCode == 0:
                print(bCode)
                keyNum = button2Key(bCode)
                print(keyNum)
                if keyNum == currentKey + 1:
                    soundDict['ding'].play()
                    pygame.time.delay(500)                    
                    question = True
                    score += (5 - attempts)*100
                    displayText = '{}'.format(score)
                else:
                    soundDict['try'].play()
                    pygame.time.delay(1000)
                    brailleIO.clearInputs()
                    attempts += 1
            else:
                vibrateButtons(whackModule[currentKey],100)
                attempts += 1

    ### LESSONS ###
    elif lessons == True:
        if changingApp == True:
            changingApp = False
            message = True
            soundDict['lessons'].play()
            sentPos = 0
            letterPos = 0
            bigString = ''
            lastWord = ''
            pygame.display.update() 
            if lessonLoaded == False:
               sentenceList, lessonDict = lessonInit()
               print(sentenceList)
               lessonLoaded == True
        elif question == True:
            if letterPos > len(sentenceList[sentPos])-1:
                print('end of line')
                sentPos += 1
                letterPos = 0
                print(letterPos)
                playHold(lessonDict,bigString.replace(' ','_'))
                bigString = ''
                lastWord = ''
                if sentPos > len(sentenceList)-1:
                    lesson = False
                    mainMenu = True
                    changingApp == True
                    message = False
            else:
                currentLetter = sentenceList[sentPos][letterPos]
                print(letterPos)
                if currentLetter == ' ':
                    soundDict['space'].play()
                else:
                    soundDict[currentLetter].play()
                question = False
        else:    
            bString = '{}'.format(button2Braille(bCode))
            if not bCode == 0:
                print(bCode)
                if bString == currentLetter:
                    soundDict['ding'].play()
                    pygame.time.delay(500)
                    bigString += bString
                    question = True
                    attempts = 0
                    letterPos += 1
                    if bString == ' ':
                        playHold(lessonDict,lastWord)
                        lastWord = ''
                    else:
                        lastWord += bString
                        
                    
                else: 
                  if attempts < 1:
                     attempts +=1
                     soundDict['try'].play()
                     pygame.time.delay(1000)
                     brailleIO.clearInputs()
                     if currentLetter == ' ':
                        soundDict['space'].play()
                     else:
                        soundDict[currentLetter].play()
                  else:
                     attempts = 0
                     soundDict['hint'].play()
                     pygame.time.delay(1000)
                     vibrateHint(letter2Vibrator(currentLetter),100,1)
                     brailleIO.clearInputs()

            

            
                
    gameDisplay.fill(white)
    gameDisplay.blit(bg,(0,0))
    if message == True:
        lessonMessage(sentenceList[sentPos],white,bigString,red)
    else:
        message_to_screen(displayText,white)
    pygame.display.update()

    clock.tick(5)



pygame.quit()
GPIO.cleanup()

quit()


