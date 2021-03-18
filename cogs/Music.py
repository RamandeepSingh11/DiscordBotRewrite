import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Tools.Messages import Message
import discord
from Tools.Player import Player
from discord.ext import commands
from Tools.Songs import YT
class Music(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
	@commands.command(aliases=['queue'])
	@commands.guild_only()
	async def play(self,ctx,*args):
		if(ctx.author.bot):return
		if(ctx.voice_client is None):
			return
		url="".join(args)
		async with ctx.typing():
			res=await YT.grab(url,self.bot.database,ctx.guild.id,self.bot.musicopts['ytdl_opts'],self.bot.loop)
		if(res is None):
			await ctx.send(embed=Message.invalidLink(ctx.author,ctx.guild))
			return
		if(res is False):
			await ctx.send(embed=Message.Error(ctx.author,ctx.guild))
			return
		await ctx.send(embed=Message.addedQueue(ctx.author,ctx.guild,res))
		if(ctx.voice_client.is_playing()):
			e=Message.addQueue(ctx.author,ctx.guild,res)
			await ctx.send(embed=e)
		song=self.bot.database.get_song(ctx.guild.id)
		player=Player(*song,self.bot.musicopts['ffmpeg_opts'])
		await self.startPlaying(ctx,player)

	async def startPlaying(self,ctx,player):
		ctx.voice_client.play(player,after=lambda x: self.bot.loop.create_task(self.done(ctx)))
		e=Message.NowPlaying(ctx.author,ctx.guild,player.artist,player.track, player.YTurl)
		await ctx.send(embed=e,delete_after=10)

	@commands.command()
	async def pause(self,ctx):
		if(ctx.author.bot): return
		if(not self.is_connected(ctx)):
			return
		if(ctx.voice_client.is_paused()):
			await ctx.send(embed=Message.alreadyPaused(ctx.author,ctx.guild))
			return
		ctx.voice_client.pause()
		await ctx.send(embed=Message.paused(ctx.author,ctx.guild),delete_after=10)

	@commands.command()
	async def stop(self,ctx):
		if(ctx.author.bot): return
		if(not self.is_connected(ctx)):
			return
		if(ctx.voice_client.source is None):
			await ctx.send(embed=Message.nothingPlaying(ctx.author,ctx.guild))
			return
		ctx.voice_client.stop()
		self.bot.database.removeQueue(ctx.guild.id)
		await ctx.send(embed=Message.stop(ctx.author,ctx.guild),delete_after=10)

	@commands.command()
	async def resume(self,ctx):
		if(ctx.author.bot): return
		if(not self.is_connected(ctx)):
			return
		if(ctx.voice_client.is_playing()):
			await ctx.send(embed=Message.alreadyPlaying(ctx.author,ctx.guild))
			return
		ctx.voice_client.resume()
		await ctx.send(embed=Message.resumed(ctx.author,ctx.guild),delete_after=10)

	@commands.command()
	async def move(self,ctx):
		if(ctx.author.bot):return
		if(ctx.author.voice is None):
			await ctx.send(embed=Message.userNotConnected(ctx.author,ctx.guild))
			return
		if(ctx.voice_client is None):
			await ctx.author.voice.connect()
		else:
			await ctx.voice_client.move_to(ctx.author.voice.channel)

	# @commands.command()
	# async def jump(self,ctx,*args):
	# 	if(ctx.author.bot):return
	# 	res=''.join(args)
	# 	data=self.bot.database.getSimilarSongs(ctx.guild.id,res)
	# 	if data is None:
	# 		await ctx.send(embed=Message.foundNothing(ctx.author,ctx.guild,res))
	# 		return
		
	async def done(self,ctx):
		song=self.bot.database.get_song(ctx.guild.id)
		if song is None:
			await ctx.send(embed=Message.queueEmpty(ctx.guild))
			await ctx.voice_client.disconnect()
			return
		player=Player(*song,self.bot.musicopts['ffmpeg_opts'])
		await self.startPlaying(ctx,player)

	@commands.Cog.listener('on_voice_state_update')
	async def checker(self,user,before,after):
		if(before.channel is None):
			return
		if(user.id==self.bot.user.id and after.channel is None):
			self.bot.database.removeQueue(user.guild.id)
			return
		if(len(before.channel.members)==1):
			for i in self.bot.voice_clients:
				if(i.guild==user.guild):
					self.bot.database.removeQueue(i.guild.id)
					await i.disconnect()

	async def is_connected(self,ctx):
		if(ctx.author.voice is None):
			await ctx.send(embed=Message.userNotConnected(ctx.author,ctx.guild))
			return False
		if(ctx.voice_client is None):
			await ctx.send(embed=Message.botNotConnected(ctx.author,ctx.guild))
			return False
		if(ctx.author.voice.channel!=ctx.voice_client.channel):
			await ctx.send(embed=Message.differentChannel(ctx.author,ctx.guild))
			return False
		return True

	@commands.command(aliases=['np','nowplaying'])
	@commands.guild_only()
	async def now(self,ctx):
		if(ctx.author.bot):return
		if(ctx.voice_client is None):
			ctx.send(embed=Message.botNotConnected(ctx.author,ctx.guild))
			return
		if(not ctx.voice_client.is_playing()):
			await ctx.send(embed=Message.nothingPlaying(ctx.author,ctx.guild))
			return
		source=ctx.voice_client.source
		await ctx.send(embed=Message.NowPlaying(ctx.author,ctx.guild,source.artists,source.track.source.YTurl))
	@commands.command()
	@play.before_invoke
	async def join(self,ctx):
		if(ctx.author.bot):return
		if(ctx.voice_client is None):
			if(ctx.author.voice):
				await ctx.author.voice.channel.connect()
			else:
				await ctx.send(embed=Message.userNotConnected(ctx.author,ctx.guild))
				return
		elif(ctx.voice_client.channel.id!=ctx.author.voice.channel.id):
			await ctx.voice_client.move_to(ctx.author.voice.channel)
	
def setup(bot):
	bot.add_cog(Music(bot))