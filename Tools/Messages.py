import discord
class Message:
    @staticmethod
    def getDefault(author,guild):
        e=discord.Embed(title=guild.name,colour=discord.Colour.red())
        e.set_author(name=author.name,icon_url=author.avatar_url)
        return e
    @staticmethod
    def NowPlaying(author,guild,artist: str,track: str,url: str):
        e=Message.getDefault(author,guild)
        e.description='Now Playing'
        e.add_field(name='Track',value='[{}]({})'.format(track,url))
        if(artist is not None and artist!='Unknown' and artist!='None'):
            e.add_field(name='Artist', value=artist)
        return e
    @staticmethod
    def addQueue(author,guild,num: int):
        e=Message.getDefault(author,guild)
        e.description='Added {} Song{} in Queue.'.format(num,'s' if num>1 else '')
        return e
    @staticmethod
    def botNotConnected(author,guild):
        e=Message.getDefault(author,guild)
        e.description='Bot Not Connected To any Voice Channel'
        return e
    @staticmethod
    def invalidLink(author,guild):
        e=Message.getDefault(author,guild)
        e.description='The Given link is Invalid.'
        return e
    @staticmethod
    def Error(author,guild):
        e=Message.getDefault(author,guild)
        e.description='Some Unknown Error Occurred. Please try Again.'
        return e
    @staticmethod
    def nothingPlaying(author,guild):
        e=Message.getDefault(author,guild)
        e.description='Nothing is Playing Currently.'
        return e
    @staticmethod
    def userNotConnected(author,guild):
        e=Message.getDefault(author,guild)
        e.description='Please Join a voice Channel'
        return e
    @staticmethod
    def queueEmpty(guild):
        e=discord.Embed(title=guild.name,colour=discord.Colour.red())
        e.description='Queue is Empty\nDisconnecting.........'
        return e
    @staticmethod
    def paused(author,guild):
        e=Message.getDefault(author,guild)
        e.description='Paused'
        return e
    @staticmethod
    def alreadyPaused(author,guild):
        e=Message.getDefault(author,guild)
        e.descrtiption='Bot Already Paused.'
        return e
    @staticmethod
    def resumed(author,guild):
        e=Message.getDefault(author,guild)
        e.description='Resumed'
        return e
    @staticmethod
    def alreadyPlaying(author,guild):
        e=Message.getDefault(author,guild)
        e.description='Already Playing'
        return e
    @staticmethod
    def differentChannel(author,guild):
        e=Message.getDefault(author,guild)
        e.description='It Seems Like That Bot is Already in use in some Other Channel.'
        return e
    @staticmethod
    def nothingPlaing(author,guild):
        e=Message.getDefault(author,guild)
        e.description='Nothing is Playing Currently.'
        return e
    @staticmethod
    def stop(author,guild):
        e=Message.getDefault(author,guild)
        e.description='Bot Stopped'
        return e
    @staticmethod
    def foundNothing(author,guild,name:str):
        e=Message.getDefault(author,guild)
        e.description='No Song Found By Name '+name
        return e
    @staticmethod
    def addedQueue(author,guild,num: int):
        e=Message.getDefault(author,guild)
        if(num==1):
            e.description='Added 1 Song to The Queue.'
        else:
            e.description='Added {} Songs to The Queue.'.format(num)
        return e