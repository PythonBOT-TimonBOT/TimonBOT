import discord
from discord.ext import commands
import datetime
from discord.utils import get
import youtube_dl
import os
import requests
from PIL import Image, ImageFont, ImageDraw
import io


PREFIX = '-'
bad_words = [ 'gandon', 'agarka', 'pornik', 'qunac', 'qunem', 'cces', 'klir', 'putanga', 'xlesh', 'suka', 'dalbaeb', 'dalbayob', 'puc', 'vor', 'jaj' ]

client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event

async def on_ready():
	print( 'BOT connected' )

	await client.change_presence( status = discord.Status.online, activity = discord.Game( '-help' ) )

@client.event
async def on_command_error( ctx, error ):
	pass

@client.event
async def on_member_join( member ):
	channel = client.get_channel( 723371882979786786 )

	role = discord.utils.get( member.guild.roles, id = 742336162370158682 )

	await member.add_roles( role )
	await channel.send( embed = discord.Embed(description = f'Օգտատերը ՝ ՝{ member.name }՝ ՝, միացավ մեզ։ ',
	                     color = 0x3ec95d ) )
#filter
@client.event
async def on_message( message ):
	await client.process_commands( message )

	msg = message.content.lower()

	if msg in bad_words:
		await message.delete()
		await message.author.send( f'{ message.author.name }, Այդպիսի բառեր ել չգրես թեչե կստանաս չատի արգելափակում!' )

#clear
@client.command( pass_context = True )
async def clear( ctx, amount : int ):
	emb = discord.Embed( title = 'Մաքրում', colour = discord.Color.green() )
	await ctx.channel.purge( limit = amount )

	emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
	emb.add_field( name = 'Չատի մաքրում', value = 'Ես մաքրեցի {} տեքստ'.format( amount ) )
	emb.set_footer( text = 'Չատը մաքրվեց {} -ի կողմից'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

	author = ctx.message.author

	await ctx.send( embed = emb )
	#await ctx.send(f'Ես ջնջեցի {amount} տեքստ { author.mention }'.format(str(amount)))

#kick
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def kick( ctx , member: discord.Member, *, reason = '' ):
	emb = discord.Embed( title = 'Դուրս հանել օգտատիրոջը', colour = discord.Color.red() )
	await ctx.channel.purge( limit = 1 )

	emb.set_author( name = member.name, icon_url = member.avatar_url )
	emb.add_field( name = 'Դուրս հանել օգտատիրոջը', value = 'Ես դուրս հանեցի {} -ին սերվերից'.format( member.mention ) )
	emb.set_footer( text = 'Դուրս եկավ {} -ի կողմից'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

	await member.kick( reason = reason )

	await ctx.send( embed = emb )
	#await ctx.send( f'Ես դուրս հանեցի { member.mention }-ին սերվերից, Պատճառ: {reason}' )

#ban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = '' ):
	emb = discord.Embed( title = 'Արգելափակում', colour = discord.Color.red() )
	await ctx.channel.purge( limit = 1 )

	await member.ban( reason = reason )

	emb.set_author( name = member.name, icon_url = member.avatar_url )
	emb.add_field( name = 'Արգելափակում օգտատիրոջը', value = 'Ես արգելափակեցի {} -ին սերվերից'.format( member.mention ) )
	emb.set_footer( text = 'Արգելափակվեց {} -ի կողմից'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

	await ctx.send( embed = emb )

	#await ctx.send( f'Ես արգելափակեցի { member.mention }-ին սերվերից, Պատճառ: {reason}' )

#Unban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
	emb = discord.Embed( title = 'Հետ արգելափակում', colour = discord.Color.green() )
	await ctx.channel.purge( limit = 1 )

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban( user )

		await ctx.send( embed = emb )
		await ctx.send( f'Ես հետ վերցրեցի { user.mention }-ի արգելափակումը' )

		return

#help
@client.command( pass_context = True )
async def help( ctx ):
	await ctx.channel.purge( limit = 1 )
	emb = discord.Embed( title = 'Հրամանների Բաժին', colour = discord.Color.green() )

	emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Չատի մաքրում, Օգտագործում: -clear (Թիվը)' )
	emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Դուրս հանել օգտատիրոջը սերվերից, Օգտագործում: -kick (օգտատերը) (պատճառ)' )
	emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Արգելափակել օգտատիրոջը սերվերից, Օգտագործում: -ban (օգտատերը) (պատճառ)' )
	emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Հետ վերցնել արգելափակումը օգտատիրոջից, Օգտագործում: -unban (օգտատերը)' )
	emb.add_field( name = '{}time'.format( PREFIX ), value = 'Իմանալ ժամանակը, Օգտագործում: -time')
	emb.add_field( name = '{}profile'.format( PREFIX ), value = 'Տեսնել օգտատիրոջ քարտը, Օգտագործում: -profile')
	emb.add_field( name = '{}join'.format( PREFIX ), value = 'Բոտին միացնել ձայնային ալիքին, Օգտագործում: -join')
	emb.add_field( name = '{}leave'.format( PREFIX ), value = 'Բոտին դուրս հանել ձայնային ալիքից, Օգտագործում: -leave')

	await ctx.send( embed = emb )

#mute
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def mute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )
	emb = discord.Embed( title = 'Չատի արգելափակում', colour = discord.Color.red() )

	emb.set_author( name = member.name, icon_url = member.avatar_url )
	emb.add_field( name = 'Չատի արգելափակում օգտատիրոջը', value = 'Ես արգելափակեցի {} -ի չատը'.format( member.mention ) )
	emb.set_footer( text = 'Չատը արգելափակվեց {} -ի կողմից'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'mute' ) 


	await member.add_roles( mute_role )

	await ctx.send( embed = emb )

#test
@client.command( pass_context = True )

async def time( ctx ):
	emb = discord.Embed( title = 'Ժամացույց', description = 'Դուք կարող եք իմանալ ժամանակը', url = 'https://www.timeserver.ru/cities/kz/taldykorgan' )

	emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
	emb.set_footer( text = 'Շնորհակալ եմ որ ընտրեր եք մեր բոտը' )
	#emb.set_image( url = 'https://sun9-35.userapi.com/c200724/v100724757/14f24/BL06miiOGVd8.jpg' )
	emb.set_thumbnail( url = 'https://sun9-35.userapi.com/c200724/v100724757/14f24/BL06miiOGVd8.jpg' )

	now_date = datetime.datetime.now()
	emb.add_field( name = 'Ժամանակ', value = 'Ժամանակ: {}'.format( now_date ))

	await ctx.send( embed = emb )

@client.command( pass_context = True )
async def join( ctx ):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get( client.voice_clients, guild = ctx.guild )

	if voice and voice.is_connected():
		await voice.move_to( channel )
	else:
		voice = await channel.connect()
		await ctx.send( f'Բոտը միացավ { channel } ալիքին!' )

@client.command( pass_context = True )
async def leave( ctx ):
	channel = ctx.message.author.voice.channel
	voice = get( client.voice_clients, guild = ctx.guild )

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await channel.connect()
		await ctx.send( f'Բոտը դուրս եկավ { channel } ալիքից!' )

@client.command( pass_context = True )
async def play( ctx, url : str ):
	song_there = os.path.isfile('son.mp3')

	try:
		if song_there:
			os.remove('song.mp3')
			print('[log] Հին ֆայլը ջնջված է!')
	except PermissionError:
		print('[log] Չստացվեց ջնջել ֆայլը!')

	await ctx.send('Խնդրում եմ սպասեք!')

	voice = get(client.voice_clients, guild = ctx.guild)

	ydl_opts = {
		'format' :'bestaudio/best',
		'postprocessors' : [{
			'key' : 'FFmpegExtractAudio',
			'preferredcodec' : 'mp3',
			'preferredquality' : '192'
		}]
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print('[log] Բեռնում եմ երգը...')
		ydl.download([url])

	for file in os.listdir('-/'):
		if file.endswith('.mp3'):
			name = file
			print('[log] Անվանափոխում եմ ֆայլը: {file}')
			os.rename(file, 'song.mp3')
	voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print( f'[log] { name }, Երգը վերջացավ!' ))
	voice.source = discord.PCMVolumeTransformer( voice.source )
	voice.source.volume = 0.07

	song_name = name.rsplit('-', 2)
	await ctx.send(f'Հիմա խաղում է { song_name[0] } երգը')

@client.command()
async def profile(ctx):
	await ctx.channel.purge(limit = 1)

	img = Image.new('RGBA', (400, 200), '#232529') 
	url = str(ctx.author.avatar_url)[:-10]

	response = requests.get(url, stream = True)
	response = Image.open(io.BytesIO(response.content))
	response = response.convert('RGBA')
	response = response.resize((100, 100), Image.ANTIALIAS)

	img.paste(response, (15, 15, 115, 115))

	idraw = ImageDraw.Draw(img)
	name = ctx.author.name
	tag = ctx.author.discriminator

	headline = ImageFont.truetype('arial.ttf', size = 20)
	undertext = ImageFont.truetype('arial.ttf', size =12)

	idraw.text((145, 15), f'{name}#{tag}', font = headline)
	idraw.text((145, 50), f'ID: {ctx.author.id}', font = undertext)

	img.save('profile.png')

	await ctx.send(file = discord.File(fp = 'profile.png'))

@clear.error
async def clear_error( ctx, error ):
	if isinstance( error, commands.MissingRequiredArgument ):
		await ctx.send( f'{ ctx.author.name }, Ամպայման գրեք թիվը!')

@mute.error
async def mute_error( ctx, error ):
	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( f'{ ctx.author.name }, Ձեզ հասանելի չէ այս հրամանը!' )

@ban.error
async def ban_error( ctx, error ):
	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( f'{ ctx.author.name }, Ձեզ հասանելի չէ այս հրամանը!' )

@kick.error
async def kick_error( ctx, error ):
	if isinstance( error, commands.MissingPermissions ):
		await ctx.send( f'{ ctx.author.name }, Ձեզ հասանելի չէ այս հրամանը!' )

#get token
token = open( 'token.txt', 'r' ).readline()

client.run( token )