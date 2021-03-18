from discord.ext import commands
import discord
import json
class Player(discord.PCMVolumeTransformer):
    def __init__(self,track: str,artist: str,url: str,YTurl: str,opts: dict,volume: int=0.5):
        source=discord.FFmpegPCMAudio(url,**opts)
        super().__init__(source,volume)
        self.artist=artist
        self.track=track
        self.YTurl=YTurl