import pygame
import os
from os.path import join, isfile
import time


def brailleSounds():
    soundDir = r'/home/pi/Desktop/AlphabetWav/'  # file path for lesson sounds
    soundList = os.listdir(soundDir)
    soundDict = {}
    for sound in soundList:
        soundDict[sound[:-4]] = pygame.mixer.Sound(join(soundDir,sound))
    return soundDict

   
def lessonInit():
    lessonSoundDir = r'/home/pi/Desktop/FileSounds/'
    lessonFile = open('TestFile')
    fileString = lessonFile.read()
    sentenceList = fileString.lower().split('\n')
    sentenceList = map(str.strip,sentenceList)
    sentenceSet = set(sentenceList)
    wordList = fileString.lower().split()
    wordSet = set(wordList)            #converts file string into a list of unique words. Changes all uppercase letters to lower case so as to not produce duplicate words.

    espeakSetting = 'sudo espeak -ven-us+m8 -s200 '

    for sentence in sentenceSet:
        if isfile('{}/{}.wav'.format(lessonSoundDir,sentence.replace(' ','_'))):
            print('{}.wav   already exists'.format(sentence.replace(' ','_')))
        else:
            print('creating file {}.wav'.format(sentence.replace(' ','_')))
            os.system('{}"{}" -w {}{}.wav '.format(espeakSetting,sentence,lessonSoundDir,sentence.replace(' ','_')))

    for word in wordSet:
        if isfile('{}/{}.wav'.format(lessonSoundDir,word)):
            print('{}.wav   already exists'.format(word))
        else:
            print('creating file {}.wav'.format(word))
            os.system('{}"{}" -w {}{}.wav '.format(espeakSetting,word,lessonSoundDir,word))

    lessonSoundList = os.listdir(lessonSoundDir)
    lessonDict = {}

    for sound in lessonSoundList:
        lessonDict[sound[:-4]] = pygame.mixer.Sound(join(lessonSoundDir,sound))

    return sentenceList,lessonDict

def playHold(dictName,dictKey):
    dictName[dictKey].play()
    lengthMSeconds = int(dictName[dictKey].get_length() * 1000)
    pygame.time.delay(lengthMSeconds)
