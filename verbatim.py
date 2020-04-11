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

    #===
    #role check

    if message.author.bot:
        return

    ''' if message.author.top_role.permissions.manage_guild == False:
        return '''


    theMessage = message.content.lower().split(' ')
    header = theMessage[0].lower()
    channel = message.channel

    
    #it's the help page u maga 4head
    if header == f'{summon}help':
        embedHelp = discord.Embed(title = "Help", description = "A quick how 2 on how to do things")
        embedHelp.add_field(name = f'{summon}register `a nickname`', value = "Registers you to Verbatim's 'database' of sorts. It makes things faster I guess, and makes it so different users can have the same path name.", inline = False)
        embedHelp.add_field(name = f'{summon}createpath `path name`', value = "Creates your first path and automatically assigns the hub to your current channel.", inline = False)
        embedHelp.add_field(name = f'{summon}sethub `path name`', value = "Assigns a hub for your path, this is where you do all your publishing, it helps optimize things and prevents cluttering", inline = False)
        embedHelp.add_field(name = f'{summon}addbranch `path name`', value = "Adds a branch to a path, this way you can publish in the hub and all those messages will be passed down to the branches", inline = False)
        embedHelp.add_field(name = f'{summon}publish `path name` `content`', value = "Publishes your messages in a typical text form through a branch of your choice\n(Remember to do this in your path's hub, also you can't ping roles because Discord API)", inline = False)
        embedHelp.add_field(name = f'{summon}viewpaths', value = "View your currently registered paths, including branches", inline = False)
        embedHelp.add_field(name = f'{summon}removepath `path name`', value = "Deletes a path, note, there is no confirmation, so you do it once, and it's gone", inline = False)
        embedHelp.add_field(name = f'{summon}removebranch `path name` `channel ID`', value = "Deletes a branch, no confirmation, get channel ID with -viewpaths")
        embedHelp.add_field(name = f'{summon}faq', value = "Few some questions and answers (they aren't really 'frequently' asked because as of now the bot isn't popular enough :/)", inline = False)
        await channel.send(embed = embedHelp)

    #registers a user to the bot
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

    #creates a path
    if header == f'{summon}createpath':


        stringId = str(message.author.id)
        stringChannelId = str(message.channel.id)

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

        if userPaths != 0:
            for path in userPaths:
                if path == theMessage[1]:
                    await channel.send(f"You already have a path by the name of {theMessage[1]}")
                    return
        #-----------------------------
        
        approvedHubs = getFile('approvedhubs.json')

        if stringChannelId in approvedHubs:
            #see if there is a path registered under that hub for that user
            if stringId in approvedHubs[stringChannelId]:
                await channel.send(f'You already have a path with a hub registered to `#{message.channel.name}` by the name of `{approvedHubs[stringChannelId][stringId]}`')
                return


            #if there isn't a path registered under that channel for that user, add it
            if stringId not in approvedHubs[stringChannelId]: #is a string because dictionaries are weird
                approvedHubs[stringChannelId][stringId] = theMessage[1]

        
        if stringChannelId not in approvedHubs:
            approvedHubs[stringChannelId] = {
                stringId:theMessage[1]
            }
        #-----------------------------
        
        userPaths[theMessage[1]] = {
                "pathserver":message.channel.guild.id,
                "pathhub":str(message.channel.id),
                "pathbranches":[
                ]
            }
        await channel.send(f'Path created with name `{theMessage[1]}`, path hub automatically set to `{message.channel}`, use -setHub in a channel in `{message.channel.guild.name}` to change hub for this path.')
        saveFile(pathFile, 'pathfile.json')
        saveFile(approvedHubs, 'approvedhubs.json')
   
    #sets the hub
    if header == f'{summon}sethub':
        
        pathFile = getFile('pathfile.json')
        approvedHubs = getFile('approvedhubs.json') 
        if len(theMessage) == 1:
            await channel.send("I don't know what path you're assigning this hub to, so, uh, use command correct yes?")
            return
        pathName = theMessage[1]
        stringId = str(message.author.id)
        stringHubId = str(message.channel.id)
        

        #-----------------------------
        #prelim checks
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("Do this in a server, and do it in the channel you intend to be the hub")
            return
        if len(theMessage) > 2:
            await channel.send("Path names have to be one 'word', with no spaces")
            return
        
        if stringId not in pathFile:
            await channel.send("You must first register before creating your path... before then, assigning a hub...")
            return
        
        userPaths = pathFile[stringId]["paths"]
        if len(userPaths) == 0:
            await channel.send("You haven't created a path yet, how are you gonna set up a hub :thonk:")
            return
        
        if pathName not in userPaths:
            await channel.send("You haven't made a path under that name yet")
            return


        oldStringHubId = pathFile[stringId]["paths"][pathName]["pathhub"]
        if str(message.channel.id) == oldStringHubId:
            await channel.send("This path is already set to this channel!")
            return
        #-----------------------------
        
        

        if pathName in userPaths:
            del(approvedHubs[oldStringHubId][stringId])
            
            #if the hub isn't registered
            if stringHubId not in approvedHubs:
                userPaths[pathName]["pathhub"] = stringHubId
                approvedHubs[stringHubId] = {
                    stringId:pathName
                }
                await channel.send(f'Successfully set the hub for `{pathName}` to channel `#{message.channel.name}`')
            #if the hub is already registered
            elif stringHubId in approvedHubs:
                approvedHubs[stringHubId][stringId] = pathName
                userPaths[pathName]["pathhub"] = stringHubId
                await channel.send(f'Successfully set the hub for `{pathName}` to channel `#{message.channel.name}`')
        saveFile(approvedHubs, 'approvedhubs.json')
        saveFile(pathFile, 'pathfile.json')
        
    #adds a branch
    if header == f'{summon}addbranch':

        pathFile = getFile('pathfile.json')
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

    #views paths
    if header == f'{summon}viewpaths':

        pathFile = getFile('pathfile.json')
        stringId = str(message.author.id)
        

        #-----------------------------
        #checks

        if stringId not in pathFile:
            await channel.send("You have to first have an account to view your paths")
            return
        
        if len(pathFile[stringId]["paths"]) == 0:
            await channel.send("You don't have any paths!")
            return

        if message.author.dm_channel == None:
            await message.author.create_dm()
        dmChannel = message.author.dm_channel
        await dmChannel.send("Your paths here")
        for pathname in pathFile[stringId]["paths"]:
            path = pathFile[stringId]["paths"][pathname]
            embedPath = discord.Embed(title = f'Path: {pathname}')
            hub = client.get_channel(int(path["pathhub"]))
            embedPath.add_field(name = "Hub", value = f'Your hub is set to `#{hub.name}` in the server `{hub.guild.name}`', inline = False)
            branches = ""
            if path["pathbranches"] == []:
                embedPath.add_field(name = "Branches", value = "You've got no branches bud", inline = False)
            else:
                for branch in path["pathbranches"]:
                    branchchannel = client.get_channel(branch)
                    branches += f"\t`#{branchchannel.name}` in server `{branchchannel.guild.name}`\n\tChannel ID: `{branch}`"
                embedPath.add_field(name = "Branches", value = branches, inline = False)
            await dmChannel.send(embed = embedPath)
        await channel.send("You've been DM'ed a list of your path and their respective information, do with that what you will")

    #publishes a message
    if header == f'{summon}publish':
        
        approvedHubs = getFile('approvedhubs.json')
        pathName = theMessage[1]
        pathFile = getFile('pathfile.json')
        stringUserId = str(message.author.id)
        stringChannelId = str(message.channel.id)

        
        #checks

        if stringUserId not in pathFile:
            await channel.send("You have to register, create a path, and add branches before publishing a message")
            return
        
        if len(pathFile[stringUserId]["paths"]) == 0:
            await channel.send("You haven't created any paths yet, how are you gonna send again? :think:")
            return
        
        if pathName not in pathFile[stringUserId]["paths"]:
            await channel.send(f"You haven't created a path under the name `{pathName}` yet")
            return

        if len(pathFile[stringUserId]["paths"][pathName]["pathbranches"]) == 0:
            await channel.send("You haven't added any branches to this path first, do that and then publish a message")
            return

        if len(theMessage) < 3:
            await channel.send("Your message actually needs to have content")
            return
        #-----------------------------
        
        for branch in pathFile[stringUserId]["paths"][pathName]["pathbranches"]:
            if len(theMessage) > 3:
                content = ' '.join(theMessage[2:])
            elif len(theMessage) == 3:
                content = theMessage[2]
            channel2send2 = client.get_channel(branch)
            await channel2send2.send(content)

    #deletes a path
    if header == f'{summon}removepath':

        if len(theMessage) < 2:
            await channel.send("You have to specificy a path to delete!")
            return
        
        pathFile = getFile('pathfile.json')
        stringId = str(message.author.id)
        pathName = theMessage[1]
        approvedHubs = getFile('approvedhubs.json')
        userPaths = pathFile[stringId]["paths"]

        if stringId not in pathFile:
            await channel.send("You're not registered m8 how can you have any paths?")
            return

        if userPaths == {}:
            await channel.send("You don't have any paths, what are you trying to remove? :think:")
            return

        if pathName not in userPaths:
            await channel.send(f"You don't have a path under the name of `{pathName}`, use `-viewpaths` to view your created paths")
            return
        
        del(approvedHubs[userPaths[pathName]["pathhub"]][stringId])
        saveFile(approvedHubs, 'approvedhubs.json')

        del(pathFile[stringId]["paths"][pathName])
        await channel.send("lol ok")
        await channel.send(f"Deleted path `{pathName}`")
        saveFile(pathFile, 'pathfile.json')

    #deletes a branch from a path
    if header == f'{summon}removebranch':
        if len(theMessage) < 3:
            await channel.send("Now i don't know what you forgot, but this command excepts 3 variables, and you forgot some")
            return
        elif len(theMessage) > 3:
            await channel.send("Uh, you might think this bot excepts a lot of variables... there's 3, actually")
            return

        pathFile = getFile('pathfile.json')
        stringId = str(message.author.id)
        pathName = theMessage[1]
        pathBranch = int(theMessage[2])
        paths = pathFile[stringId]["paths"]

        if stringId not in pathFile:
            await channel.send("You're not registered m8 how can you have any paths?")
            return

        if paths == {}:
            await channel.send("You don't have any paths, what are you trying to remove? :think:")
            return

        if pathName not in paths:
            await channel.send(f"You don't have a path under the name of `{pathName}`, use `-viewpaths` to view your created paths")
            return

        if paths[pathName]["pathbranches"] == []:
            await channel.send("So ah, yeah, your path has no branches, what am I to remove again (use -help to see how to use things ye)")
            return
        
        if pathBranch not in paths[pathName]["pathbranches"]:
            await channel.send("So like, `{client.get_channel(pathBranch).name}`'s not, that's not a branch you have installed on your path (pro tip: use -viewpaths)")
            return
        
        paths[pathName]["pathbranches"].remove(pathBranch)
        await channel.send(f"Sucessfully deleted branch `#{client.get_channel(pathBranch).name}` from path `{pathName}`")
        saveFile(pathFile, 'pathfile.json')

client.run(TOKEN)
