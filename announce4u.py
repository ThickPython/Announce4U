import discord
import json
from otherThings import getFile, saveFile

settings = getFile('settings.json')
TOKEN = settings["discord token"]
summon = '-'

client = discord.Client()

@client.event
async def on_ready():
    print('lets get this party started')

@client.event
async def on_message(message): 
    theMessage = message.content.split(' ')
    header = theMessage[0].lower()
    channel = message.channel

    if header == f'{summon}setleader':
        userList = getFile('users.json')
        for user in userList:
            if user['id'] == message.author.id:
                await channel.send("you're already registered in our database")
                break
        userList.append(
            {
                "id": message.author.id
            }   
        )
        saveFile(userList, 'users.json')
            
    if header == f'{summon}sethub':
        if isinstance(message.channel , discord.DMChannel):
            await channel.send("do this in a discord server first!")
        userList = getFile('users.json')
        for user in userList:
            if user['id'] == message.author.id:
                await channel.send("set yourself as leader first!")
                break
        channelList = getFile('channels.json')
        for user in channelList:
            if user['leaderID'] == message.author.id:
                user['hubID'] == message.guilds
    

    #creates a path
    if header == f'{summon}createpath':

        #-----------------------------
        #prelim checks
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("do this in your main hub server")
            return
        if len(theMessage) > 2 or len(theMessage) < 2:
            await channel.send("path names have to be one string, no spaces")
            return
        pathFile = getFile('pathfile.json')
        for path in pathFile:
            if theMessage[1] == path["pathname"]:
                await channel.send("this pathname already exists, try something else")
                return
        #-----------------------------

        pathFile = getFile("pathfile.json")
        pathFile.append(
            {
                "pathname":theMessage[1],
                "pathserver":message.channel.guild.id,
                "pathleaders": [
                    message.author.id
                ],
                "pathhub":message.channel.id,
                "pathbranches":[

                ]
            }
        )
        await channel.send(f'Path created with name {theMessage[1]}, path hub automatically set to {message.channel}, use -setHub in a channel in {message.channel.guild.name} to change hub for this path.')
        saveFile(pathFile, 'pathfile.json')

    #sets the hub
    if header == f'{summon}sethub':

        #-----------------------------
        #prelim checks
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("do this in a server, and do it in the channel you intend to be the hub")
            return
        if len(theMessage) > 2:
            await channel.send("path names have to be one 'word', with no spaces")
            return
        #-----------------------------

        pathFile = getFile('pathfile.json')
        path2Edit = []
        for paths in pathFile:
            if paths['pathname'] == theMessage[1]:
                path2Edit = paths

        #-----------------------------
        #more checks
        if path2Edit == []:
            await channel.send("oops, I don't think that path exists yet. use -createpath {nameofpath} to create a path")
            return
        #-----------------------------

        pathLeaders = path2Edit['pathleaders']

        #-----------------------------
        #even more checks
        isLeader = False
        for leader in pathLeaders:
            if message.author.id == leader:
                isLeader = True
        if isLeader == False:
            await channel.send("Oops, you're not a leader of this path, so you can't edit it. :feelsbadman:")
            return
        #-----------------------------

        path2Edit[3] = message.channel.id
        await channel.send(f'Successfully set Path hub to {message.channel.name}')
        

    return

client.run(TOKEN)
