import discord

from verbatim.otherThings import get_file, save_file

settings = get_file('settings.json')
TOKEN = settings["discord token"]


client = discord.Client()

COMMAND_DESCRIPTIONS = [
    ('register', ("Registers you to Verbatim's 'database' of sorts. "
                 "It makes things faster I guess, and makes it so different users can have the same path name.")),
    ('createpath `path name`', "Creates your first path"),
    ('addbranch `path name`', ("Adds a branch to a path, this is required to publish")),
    ('publish `path name` `content`', ("Publishes your messages in a typical text form through a branch "
                                      "of your choice, also you "
                                      "can't ping roles because Discord API)")),
    ('viewpaths', "View your currently registered paths, including branches"),
    ('removepath `path name`', "Deletes a path, note, there is no confirmation, so you do it once, and it's gone"),
    ('removebranch `path name` `channel ID`', "Deletes a branch, no confirmation, get channel ID with -viewpaths"),
    ('faq', ("Few some questions and answers (they aren't really 'frequently' "
            "asked because as of now the bot isn't popular enough :/)")),
]


async def print_help(summon: str, channel) -> None:
    embed_help = discord.Embed(
        title="Help",
        description="A quick how 2 on how to do things",
        color=discord.Color.dark_orange(),
    )
    for command, description in COMMAND_DESCRIPTIONS:
        embed_help.add_field(name=f'`{summon}{command}`', value=description, inline=False)
    await channel.send(embed=embed_help)


async def register(message, channel):
    path_file = get_file('pathfile.json')
    is_user = False
    for user in path_file:
        if user == str(message.author.id):
            is_user = True
    if is_user:
        await channel.send("you've already registered!")
        return
    path_file[message.author.id] = {
        "paths": {}
    }
    await channel.send(f'Registered {message.author}')
    save_file(path_file, 'pathfile.json')

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


    #check for summon
    summon = '-'
    summons = get_file('summons.json')
    if str(message.guild.id) in summons:
        summon = summons[str(message.guild.id)]
    theMessage = message.content.lower().split(' ')
    header = theMessage[0].lower()
    channel = message.channel


    #it's the help page u maga 4head
    if header == f'{summon}help':
        await print_help(summon=summon, channel=channel)

    #registers a user to the bot
    if header == f'{summon}register':
        pathFile = get_file('../../pathfile.json')
        isUser = False
        for user in pathFile:
            if user == str(message.author.id):
                isUser = True
        if isUser:
            await channel.send("you've already registered!")
            return
        pathFile[message.author.id] = {
            "paths":{}
        }
        await channel.send(f'Registered {message.author}')
        save_file(pathFile, '../../pathfile.json')

    #creates a path
    if header == f'{summon}createpath':


        stringId = str(message.author.id)
        stringChannelId = str(message.channel.id)

        #-----------------------------
        #prelim checks
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("You can't set a path in a DM")
            return
        if len(theMessage) > 2 or len(theMessage) < 2:
            await channel.send("Path names have to be one string, no spaces")
            return
        pathFile = get_file('../../pathfile.json')

        if stringId not in pathFile:
            await channel.send("You have to -register first before creating a path")

        userPaths = pathFile[stringId]["paths"]

        if userPaths != 0:
            for path in userPaths:
                if path == theMessage[1]:
                    await channel.send(f"You already have a path by the name of {theMessage[1]}")
                    return

        userPaths[theMessage[1]] = {
                "pathserver":message.channel.guild.id,
                "pathbranches":[
                ]
            }
        await channel.send(f'Path created with name `{theMessage[1]}`')
        save_file(pathFile, '../../pathfile.json')

    #adds a branch
    if header == f'{summon}addbranch':

        pathFile = get_file('../../pathfile.json')
        pathName = theMessage[1]
        stringId = str(message.author.id)

        #-----------------------------
        #prelim checks
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("Do this in a server")
            return
        if len(theMessage) > 2:
            await channel.send("Path names have to be one 'word', with no spaces")
            return
        #-----------------------------


        if stringId not in pathFile:
            await channel.send("You must first register before adding branches")
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

        save_file(pathFile, '../../pathfile.json')
        await channel.send(f'Successfully added `#{message.channel.name}` to path `{pathName}`')

    #views paths
    if header == f'{summon}viewpaths':

        pathFile = get_file('../../pathfile.json')
        stringId = str(message.author.id)


        #-----------------------------
        #checks

        if stringId not in pathFile:
            await channel.send("You have to register first, and then create a path")
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
            embedPath = discord.Embed(title = f'Path: {pathname}', color = discord.Color.dark_orange())
            branches = ""
            if path["pathbranches"] == []:
                embedPath.add_field(name = "Branches", value = "You have to first set a branch!", inline = False)
            else:
                for branch in path["pathbranches"]:
                    branchchannel = client.get_channel(branch)
                    branches += f"\t`#{branchchannel.name}` in server `{branchchannel.guild.name}`\n\tChannel ID: `{branch}`\n"
                embedPath.add_field(name = "Branches", value = branches, inline = False)
            await dmChannel.send(embed = embedPath)
        await channel.send("Check your DM's")

    #publishes a message
    if header == f'{summon}publish':

        pathName = theMessage[1]
        pathFile = get_file('../../pathfile.json')
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

        pathFile = get_file('../../pathfile.json')
        stringId = str(message.author.id)
        pathName = theMessage[1]
        userPaths = pathFile[stringId]["paths"]

        if stringId not in pathFile:
            await channel.send("You have to register first!")
            return

        if userPaths == {}:
            await channel.send("You have to first have a path before you can remove one")
            return

        if pathName not in userPaths:
            await channel.send(f"You don't have a path under the name of `{pathName}`, use `-viewpaths` to view your created paths")
            return

        del(pathFile[stringId]["paths"][pathName])
        await channel.send("lol ok")
        await channel.send(f"Deleted path `{pathName}`")
        save_file(pathFile, '../../pathfile.json')

    #deletes a branch from a path
    if header == f'{summon}removebranch':
        if len(theMessage) < 3:
            await channel.send("You're missing some variables there")
            return
        elif len(theMessage) > 3:
            await channel.send("Uh, you might think this bot excepts a lot of variables... there's 3, actually")
            return

        pathFile = get_file('../../pathfile.json')
        stringId = str(message.author.id)
        pathName = theMessage[1]
        pathBranch = int(theMessage[2])
        paths = pathFile[stringId]["paths"]

        if stringId not in pathFile:
            await channel.send("You have to first register!")
            return

        if paths == {}:
            await channel.send("You have to first have a path, and then branches on that path...")
            return

        if pathName not in paths:
            await channel.send(f"You don't have a path under the name of `{pathName}`, use `-viewpaths` to view your created paths")
            return

        if paths[pathName]["pathbranches"] == []:
            await channel.send("Your path first has to have branches before I can remove them ")
            return

        if pathBranch not in paths[pathName]["pathbranches"]:
            await channel.send("So like, `{client.get_channel(pathBranch).name}`'s not, that's not a branch you have installed on your path (pro tip: use -viewpaths)")
            return

        paths[pathName]["pathbranches"].remove(pathBranch)
        await channel.send(f"Sucessfully deleted branch `#{client.get_channel(pathBranch).name}` from path `{pathName}`")
        save_file(pathFile, '../../pathfile.json')

    #changes the summon for a thing
    if header == f'{summon}summon':
        if len(theMessage) != 2:
            await channel.send("Summons have to be 1 string only, with no spaces")

        else:
            strGuild = str(message.guild.id)
            summons = get_file('summons.json')
            summons[strGuild] = theMessage[1]
            save_file(summons, 'summons.json')
            await channel.send(f'Changed the summon for Verbatim in server {message.guild.name} to {theMessage[1]}')

    #faq
    if header == f'{summon}faq':
        embedFaq = discord.Embed(title = "FAQ", description = "Frequently asked questions that aren't frequently asked")
        await channel.send(embed = embedFaq)

client.run(TOKEN)
