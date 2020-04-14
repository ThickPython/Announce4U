import discord
import json


def is_admin():
    return True


def get_file(filename):
    with open(filename, 'r') as filenameAsJson:
        return json.load(filenameAsJson)


def save_file(savethis, filename):
    with open(filename, 'w') as filenameAsJson:
        json.dump(savethis, filenameAsJson, indent = 4)