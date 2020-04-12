import discord

from verbatim.otherThings import get_file, save_file

settings = get_file('settings.json')
TOKEN = settings["discord token"]
embed_color = settings["color"]


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
    ('ping', ("Gets your latency and things like that"))
]


class Error(Exception):
    def __init__(self, err_msg):
        self.err_msg = err_msg


async def print_help(summon: str, channel) -> None:
    embed_help = discord.Embed(
        title="Help",
        description="A quick how 2 on how to do things",
        color=discord.Colour(embed_color),
    )
    for command, description in COMMAND_DESCRIPTIONS:
        embed_help.add_field(name=f'{summon}{command}', value=description, inline=False)
    await channel.send(embed=embed_help)


async def register(message, channel) -> None:
    path_file = get_file('pathfile.json')
    for user in path_file:
        if user == str(message.author.id):
            raise Error(err_msg="You've already registered!")
    path_file[message.author.id] = {
        "paths": {}
    }
    await channel.send(f'Registered {message.author}')
    save_file(path_file, 'pathfile.json')


@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity= discord.Game(name = "-help"))
    print('Ready to start b r a n c h i n g out, haha get it?')

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
    the_message = message.content.lower().split(' ')
    header = the_message[0].lower()
    channel = message.channel

    try:
        # it's the help page u maga 4head`
        if header == f'{summon}help':
            await print_help(summon=summon, channel=channel)

        # registers a user to the bot
        elif header == f'{summon}register':
            await register(message, channel)
    except Error as e:
        await channel.send(e.err_msg)
        return

    #creates a path
    if header == f'{summon}createpath':

        stringId = str(message.author.id)

        #-----------------------------
        #prelim checks
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("You can't set a path in a DM")
            return
        if len(the_message) > 2 or len(the_message) < 2:
            await channel.send("Path names have to be one string, no spaces")
            return
        path_file = get_file('pathfile.json')

        if stringId not in path_file:
            await channel.send("You have to -register first before creating a path")

        userPaths = path_file[stringId]["paths"]

        if userPaths != 0:
            for path in userPaths:
                if path == the_message[1]:
                    await channel.send(f"You already have a path by the name of {the_message[1]}")
                    return

        userPaths[the_message[1]] = {
                "pathserver":message.channel.guild.id,
                "pathbranches":[
                ]
            }
        await channel.send(f'Path created with name `{the_message[1]}`')
        save_file(path_file, '../../pathfile.json')

    #adds a branch
    if header == f'{summon}addbranch':

        path_file = get_file('pathfile.json')
        path_name = the_message[1]
        string_id = str(message.author.id)

        #-----------------------------
        #prelim checks
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("Do this in a server")
            return
        if len(the_message) > 2:
            await channel.send("Path names have to be one 'word', with no spaces")
            return
        #-----------------------------

        if stringId not in path_file:
            await channel.send("You must first register before adding branches")
            return

        userPaths = path_file[stringId]["paths"]

        if len(userPaths) == 0 or path_name not in userPaths:
            await channel.send("You can't add a branch to a path that doesn't exist!")
            return

        branches = userPaths[path_name]["pathbranches"]
        if message.channel.id in branches:
            await channel.send("You've already added this channel!")
            return
        branches.append(message.channel.id)

        save_file(path_file, 'pathfile.json')
        await channel.send(f'Successfully added `#{message.channel.name}` to path `{path_name}`')

    #views paths
    if header == f'{summon}viewpaths':

        path_file = get_file('pathfile.json')
        string_id = str(message.author.id)

        #-----------------------------
        #checks

        if stringId not in path_file:
            await channel.send("You have to register first, and then create a path")
            return

        if len(path_file[stringId]["paths"]) == 0:
            await channel.send("You don't have any paths!")
            return
        #-----------------------------


        if message.author.dm_channel == None:
            await message.author.create_dm()
        dmChannel = message.author.dm_channel
        await dmChannel.send("Your paths here")
        for path_name in path_file[stringId]["paths"]:
            path = path_file[stringId]["paths"][path_name]
            embedPath = discord.Embed(title = f'Path: {path_name}', color = discord.Color.dark_orange())
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

        path_name = the_message[1]
        path_file = get_file('pathfile.json')
        string_user_id = str(message.author.id)

        #-----------------------------
        #checks

        if string_user_id not in path_file:
            await channel.send("You have to register, create a path, and add branches before publishing a message")
            return

        if len(path_file[string_user_id]["paths"]) == 0:
            await channel.send("You haven't created any paths yet, how are you gonna send again? :think:")
            return

        if path_name not in path_file[string_user_id]["paths"]:
            await channel.send(f"You haven't created a path under the name `{path_name}` yet")
            return

        if len(path_file[string_user_id]["paths"][path_name]["pathbranches"]) == 0:
            await channel.send("You haven't added any branches to this path first, do that and then publish a message")
            return

        if len(the_message) < 3:
            await channel.send("Your message actually needs to have content")
            return
        #-----------------------------

        for branch in path_file[string_user_id]["paths"][path_name]["pathbranches"]:
            if len(the_message) > 3:
                content = ' '.join(the_message[2:])
            elif len(the_message) == 3:
                content = the_message[2]
            channel2send2 = client.get_channel(branch)
            await channel2send2.send(content)

    #deletes a path
    if header == f'{summon}removepath':

        #-----------------------------
        #checks

        if len(the_message) < 2:
            await channel.send("You have to specificy a path to delete!")
            return

        path_file = get_file('pathfile.json')
        string_id = str(message.author.id)
        path_name = the_message[1]
        user_paths = path_file[string_id]["paths"]

        if stringId not in path_file:
            await channel.send("You have to register first!")
            return

        if userPaths == {}:
            await channel.send("You have to first have a path before you can remove one")
            return

        if path_name not in userPaths:
            await channel.send(f"You don't have a path under the name of `{path_name}`, use `-viewpaths` to view your created paths")
            return
        #-----------------------------

        del(path_file[stringId]["paths"][path_name])
        await channel.send("lol ok")
        await channel.send(f"Deleted path `{path_name}`")
        save_file(path_file, 'pathfile.json')

    #deletes a branch from a path
    if header == f'{summon}removebranch':

        #-----------------------------
        #checks

        if len(the_message) < 3:
            await channel.send("You're missing some variables there")
            return
        elif len(the_message) > 3:
            await channel.send("Uh, you might think this bot excepts a lot of variables... there's 3, actually")
            return

        path_file = get_file('pathfile.json')
        string_id = str(message.author.id)
        path_name = the_message[1]
        path_branch = int(the_message[2])
        paths = path_file[string_id]["paths"]

        if stringId not in path_file:
            await channel.send("You have to first register!")
            return

        if paths == {}:
            await channel.send("You have to first have a path, and then branches on that path...")
            return

        if path_name not in paths:
            await channel.send(f"You don't have a path under the name of `{path_name}`, use `-viewpaths` to view your created paths")
            return

        if paths[path_name]["pathbranches"] == []:
            await channel.send("Your path first has to have branches before I can remove them ")
            return

        if path_branch not in paths[path_name]["pathbranches"]:
            await channel.send("So like, `{client.get_channel(path_branch).name}`'s not, that's not a branch you have installed on your path (pro tip: use -viewpaths)")
            return
        #-----------------------------

        paths[path_name]["pathbranches"].remove(path_branch)
        await channel.send(
            f"Sucessfully deleted branch `#{client.get_channel(path_branch).name}` from path `{path_name}`"
        )
        save_file(path_file, 'pathfile.json')

    #changes the summon for a thing
    if header == f'{summon}summon':
        if len(the_message) != 2:
            await channel.send("Summons have to be 1 string only, with no spaces")

        else:
            strGuild = str(message.guild.id)
            summons = get_file('summons.json')
            summons[strGuild] = the_message[1]
            save_file(summons, 'summons.json')
            await channel.send(f'Changed the summon for Verbatim in server {message.guild.name} to {the_message[1]}')

    #faq
    if header == f'{summon}faq':
        embedFaq = discord.Embed(title = "FAQ", description = "Frequently asked questions that aren't frequently asked")
        await channel.send(embed = embedFaq)

    if header == f'{summon}ping':
        embedPing = discord.Embed(title = "Ping!", description = f'Ping! {round(client.latency, 2)} ms', color = discord.Colour(embed_color))
        await channel.send(embed = embedPing)

client.run(TOKEN)
