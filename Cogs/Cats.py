import asyncio
import discord
import random
import requests
import time
import xmltodict
from   os.path import splitext
from   discord.ext import commands
from   Cogs import Settings
from   Cogs import GetImage

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# This module grabs Reddit posts and selects one at random

class Cats:

	# Init with the bot reference, and a reference to the settings var and xp var
	def __init__(self, bot, settings, posts : int = 100):
		self.bot = bot
		self.settings = settings
		if not type(posts) == int:
			posts = 100
		self.posts = posts
		self.ua = 'CorpNewt DeepThoughtBot'
			
	def canDisplay(self, server):
		# Check if we can display images
		lastTime = int(self.settings.getServerStat(server, "LastPicture"))
		threshold = int(self.settings.getServerStat(server, "PictureThreshold"))
		if not GetImage.canDisplay( lastTime, threshold ):
			# await self.bot.send_message(channel, 'Too many images at once - please wait a few seconds.')
			return False
		
		# If we made it here - set the LastPicture method
		self.settings.setServerStat(server, "LastPicture", int(time.time()))
		return True

	@commands.command(pass_context=True)
	async def randomcat(self, ctx):
		"""Meow."""
		
		channel = ctx.message.channel
		author  = ctx.message.author
		server  = ctx.message.server
		
		if not self.canDisplay(server):
			return
		
		url = 'http://thecatapi.com/api/images/get?format=xml&results_per_page=1'

		# Grab our image url
		r = requests.get(url, headers = {'User-agent': self.ua})
		# Decode the xml
		decoded = xmltodict.parse(r.content)
		catURL = decoded['response']['data']['images']['image']['url']
		
		await GetImage.get(catURL, self.bot, channel, 'A cat for you!', self.ua)