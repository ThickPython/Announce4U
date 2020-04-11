import discord
import json

def isAdmin():
    return True

def getFile(filename):
    with open(filename, 'r') as filenameAsJson:
        return json.load(filenameAsJson)

def saveFile(savethis, filename):
    with open(filename, 'w') as filenameAsJson:
        json.dump(savethis, filenameAsJson, indent = 4)