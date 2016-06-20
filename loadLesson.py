import pygame
import time
import os
from os.path import join, isfile


#Initialize Mixer
pygame.mixer.pre_init(22050, -16,  2, 512)
pygame.mixer.init()


soundDir = r'/home/pi/Desktop/FileSounds/'


lessonFile = open('TestFile')
fileString = lessonFile.read()
sentenceList = fileString.lower().split('\n')
sentenceList = map(str.strip,sentenceList)
sentenceSet = set(sentenceList)
wordList = fileString.lower().split()
wordSet = set(wordList)            #converts file string into a list of unique words. Changes all uppercase letters to lower case so as to not produce duplicate words.


print(sentenceList)

espeakSetting = 'sudo espeak -ven-us+m8 -s200 '

for sentence in sentenceSet:
    if isfile('{}/{}.wav'.format(soundDir,sentence.replace(' ','_'))):
        print('{}.wav   already exists'.format(sentence.replace(' ','_')))
    else:
        print('creating file {}.wav'.format(sentence.replace(' ','_')))
        os.system('{}"{}" -w {}{}.wav '.format(espeakSetting,sentence,soundDir,sentence.replace(' ','_')))


for word in wordSet:
    if isfile('{}/{}.wav'.format(soundDir,word)):
        print('{}.wav   already exists'.format(word))
    else:
        print('creating file {}.wav'.format(word))
        os.system('{}"{}" -w {}{}.wav '.format(espeakSetting,word,soundDir,word))

soundList = os.listdir(soundDir)
soundDict = {}

for sound in soundList:
    soundDict[sound[:-4]] = pygame.mixer.Sound(join(soundDir,sound))



for sound in soundList:
    soundDict[sound[:-4]].play()
    time.sleep(2)

