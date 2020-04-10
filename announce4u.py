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

    if header == f'{summon}register':
        pathFile = getFile('pathfile.json')
        isUser = False
        for user in pathFile:
            if user == str(message.author.id):
                isUser = True
        if isUser:
            await channel.send("you've already registered!")
            return
        pathFile[message.author.id] = {
            "name":theMessage[1],
            "paths":{}
        }
        await channel.send(f'Registered {message.author} as {theMessage[1]}')
        saveFile(pathFile, 'pathfile.json')

    if header == f'{summon}sethub':
        if isinstance(message.channel , discord.DMChannel):
            await channel.send("Do this in a discord server first!")
        userList = getFile('users.json')
        for user in userList:
            if user['id'] == message.author.id:
                await channel.send("Set yourself as leader first!")
                break
        channelList = getFile('channels.json')
        for user in channelList:
            if user['leaderID'] == message.author.id:
                user['hubID'] == message.guilds
    

    #creates a path
    if header == f'{summon}createpath':

        stringId = str(message.author.id)

        #-----------------------------
        #prelim checks
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("Do this in your main hub server")
            return
        if len(theMessage) > 2 or len(theMessage) < 2:
            await channel.send("Path names have to be one string, no spaces")
            return
        pathFile = getFile('pathfile.json')

        if stringId not in pathFile:
            await channel.send("You must first register before creating your first path")

        userPaths = pathFile[stringId]["paths"]
        #-----------------------------
        
        if userPaths != 0:
            for path in userPaths:
                if path["pathname"] == theMessage[1]:
                    await channel.send(f"You already have a path by the name of {theMessage[1]}")
                    return
        

        userPaths[theMessage[1]] = {
                "pathserver":message.channel.guild.id,
                "pathhub":message.channel.id,
                "pathbranches":[
                ]
            }
        await channel.send(f'Path created with name `{theMessage[1]}`, path hub automatically set to `{message.channel}`, use -setHub in a channel in `{message.channel.guild.name}` to change hub for this path.')
        saveFile(pathFile, 'pathfile.json')

        approvedHubs = getFile('approvedhubs.json')
        if message.channel.id not in approvedHubs:
            approvedHubs.append(message.channel.id)
        saveFile(approvedHubs, 'approvedhubs.json')

    #sets the hub
    if header == f'{summon}sethub':

        pathName = theMessage[1]
        stringId = str(message.author.id)

        #-----------------------------
        #prelim checks
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("Do this in a server, and do it in the channel you intend to be the hub")
            return
        if len(theMessage) > 2:
            await channel.send("Path names have to be one 'word', with no spaces")
            return
        #-----------------------------

        pathFile = getFile('pathfile.json')
        if stringId not in pathFile:
            await channel.send("You must first register before creating your path... before then, assigning a hub...")
            return
        
        userPaths = pathFile[stringId]["paths"]
        if len(userPaths) == 0:
            await channel.send("You haven't created a path yet, how are you gonna set up a hub :thonk:")
            return
        
        if pathName not in userPaths:
            await channel.send("You haven't made a path uner that name yet")
            return

        elif pathName in userPaths:

            approvedHubs = getFile('approvedhubs.json') 
            approvedHubs.remove(userPaths[pathName]["pathhub"])
            approvedHubs.append(message.channel.id)
            saveFile(approvedHubs, 'approvedhubs.json')

            userPaths[pathName]["pathhub"] = message.channel.id
            saveFile(pathFile, 'pathfile.json')

            await channel.send(f'Successfully set the hub for `{pathName}` to channel `#{message.channel.name}`')

        
    
    if header == f'{summon}addbranch':

        pathName = theMessage[1]
        stringId = str(message.author.id)

        #-----------------------------
        #prelim checks
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("Do this in a server, and do it in the channel you intend to be the hub")
            return
        if len(theMessage) > 2:
            await channel.send("Path names have to be one 'word', with no spaces")
            return
        #-----------------------------

        pathFile = getFile('pathfile.json')
        if stringId not in pathFile:
            await channel.send("You must first register before creating your path... before then, assigning a hub...")
            return

        userPaths = pathFile[stringId]["paths"]

        if len(userPaths) == 0 or pathName not in userPaths:
            await channel.send("You can't add a branch to a path that doesn't exist!")
            return
        
        branches = userPaths[pathName]["pathbranches"]
        if message.channel.id in branches:
            await channel.send("You've already added this channel!")
            return
        branches.append(message.channel.id)

        saveFile(pathFile, 'pathfile.json')
        await channel.send(f'Successfully added `#{message.channel.name}` to path `{pathName}`')

    if header == f'{summon}publish':
        
        #-----------------------------
        #checks
        if len(theMessage) < 3:
            await channel.send("Your message actually needs to have content")
            return

        if message.channel.id in getFile('approvedhubs.json'):
            content = ' '.join(theMessage[2:])
            pathFile = getFile('pathfile.json')
            for path in pathFile:
                if path["pathhub"] == message.channel.id:
                    if len(path["pathbranches"]) != 0:
                        for branch in path["pathbranches"]:
                            channel2send2 = client.get_channel(branch)
                            await channel2send2.send(content)


client.run(TOKEN)
