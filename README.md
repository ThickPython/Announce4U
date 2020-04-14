# Verbatim
## The Problem
 So you're an admin. You moderate 16 servers, and you'd like to inform all of them of important news. How do you do it? Indeed, copy and pasting the same message across all your servers would be a pain. Then you have to monotonous act with a different message, in different channels to only a select group of your servers. It's time consuming, it's boring, and it's inefficient.

## The Partial Solution
 You believe that you've found the answer, Discord Channel following. With that, you'd be able to follow all your Discord servers to one channel. But you've run into a problem. Your server is not verified. That means you're not allowed to set up an announcements channel to follow. You just want to project a message, but unfortunately you're not a game developer, or an esports team, and you don't want to pay the big bucks either. 

## The Real Solution
 Introducing Verbatim, the bot that brings this Discord announcements feature to your server for free, no gimmicks, no bs, it does what it's meant to do and it does it good. With this you can set up as many announcement channels as you'd like for whatever purpose, add channels from other servers to that announcement channel, and broadcast out to everyone. Pings? It does that. @here? yes. @everyone? It does that too.

<sub> note that Discord doesn't allow pinging roles (to my knowledge) so you can't do that <sub>


# How it works and how to use it in at least 3 commands

### 1. Creating the path

In Verbatim there is something called a `Path`. It's most likely what you think it is, a path on which the message walks. How do you create one? Start in the server you wish to publish your message from. It doesn't matter what channel you're in, because paths are assigned to the server, not a channel. 

Use command `-createpath [pathname]` (and yes ignore the brackets)

### 2. Adding the branches

So you know where the paths starts, where does it go then? In Verbatim there is something called a `Branch`, potential naming ideas include `forks` and `receivers` but you get the point. These are the channels where all your messages will go. So go to the channel you wish to add (this can even be in the server where you created the path, but there isn't much of a reason to do that). 

To do this you need, 1. the name of the path you intend to add this branch to, 2. your server ID, as paths are unique to servers (you can get this via right clicking on your server in Dev mode or typing `-serverid`)

Use command `-branch add [serverid] [pathname]` 

### 3. Sending a message

You've got your path set up, all the branches attached and ready to receive content. When you have something to say, go to the server you set up the path in. It doesn't matter what channel you're in just know the path you're going to send your message down.

Use command `-publish [pathname] [content]`

Maybe you have some questions so let's get into the FAQ

# FAQ

#### *What if I forget my path name? Or what if I forget where my paths lead?*

We saw this coming, indeed it's easy to forget about paths and where they go. That's why there is the built in command `-viewpaths` to view all paths assigned to the server, all the branches for those paths, branch names, their respective servers, and channel IDs. That may sound like a lot, but just try it for yourself. Promise it's not too messy.

#### *What if I want to remove a branch? A path?*

Just how you can add a branch and create a path, both can be removed and deleted.

For branches navigate to the channel you wish to delete, then type

`-branch remove [server id of the server the path was created in] [name of path to remove it from]` 

and it's gone

For paths it's even easier, start in the server where the path was made, and type

`-pathremove [pathname]` 

Do note however that removing paths has no confirmation, and will delete them permanently without mercy.



#### *It says "no gimmicks, no bs." That means it can't do much but publish right?*

Er, no. No gimmicks as in it's not a bot you install to do function X, but later you find out the bot can also ban trolls, play 8ball, and do your taxes. 

This bot focuses purely on it's sole function which is to publish messages. In fact it comes with a lot of tools to improve upon it's function. This includes a whitelist which allows select people to publish messages and view paths, but no admin functionality such as delete/create paths and add/remove branches.



So that's Verbatim, we hope that you enjoy it. If you have any extra questions, concerns, or bugs to report, you can contact me personally at `Rez#4270`
