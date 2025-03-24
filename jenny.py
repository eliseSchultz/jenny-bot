import torch
import asyncio
import secret
from TTS.api import TTS
import discord
from discord import app_commands
import sys

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

listening_channel = None
voice_client = None
message_queue = []
exclusive_name = ""

device = "cuda" if torch.cuda.is_available() else "cpu"

# model examples:
# "tts_models/ja/kokoro/tacotron2-DDC"
# "tts_models/en/blizzard2013/capacitron-t2-c150_v2"
# "tts_models/tgl/fairseq/vits"
# "tts_models/es/mai/tacotron2-DDC"

if len(sys.argv) == 2:
    model_path = sys.argv[1]
    print(f"Using {model_path}")
else:
    model_path = "tts_models/en/jenny/jenny"
    print(f"Defaulting to {model_path}")

tts = TTS(model_path).to(device)

@tree.command(name = "ping", description = "am i alive?")
async def ping_command(interaction):
    await interaction.response.send_message("hi.", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

@client.event
async def on_message(message):
    print(f"See {message.content} in {message.channel}")
    print(f"Jenny's channel: {listening_channel}")
    text_to_speak = message.content
    if len(message.content) > 2000:
        text_to_speak = "I cannot say anything over 2000 characters."
    
    print("Checking message")
    if message.author == client.user:
        print("Message author is Client user (Jenny)")
        return
    if message.channel != listening_channel:
        print("Message channel is not listening channel")
        return
    if "https://" in text_to_speak:
        print("Contains URL")
        return
    if "http://" in text_to_speak:
        print("Contains URL")
        return
    if listening_channel == None:
        print("Jenny is not in a voice channel")
        return
    if not (exclusive_name == "" or message.author.display_name == exclusive_name):
        print("Exclusive name does not match")
        return

    print(f"Author: {message.author.display_name}")
    message_queue.append(text_to_speak)

    while len(message_queue) > 0 and not voice_client.is_playing():
        print("Attempting to speak...")
        try:
            await generate_voice_file(message_queue.pop(0))
            voice_client.play(discord.FFmpegPCMAudio("output.mp3"))
            while voice_client.is_playing():
                await asyncio.sleep(1)
        except Exception as e:
            print(e)
            pass
    
    print(f"Message queue: {message_queue}")


@tree.command(name="join", description="hello")
async def join_command(interaction):
    global listening_channel
    if listening_channel != None:
        await interaction.response.send_message(f"i am already listening to {listening_channel}. use /leave to change channels.", ephemeral=True, delete_after="5.0")
        return
    listening_channel = interaction.channel
    voice_channel = interaction.user.voice.channel
    global voice_client
    voice_client = await voice_channel.connect()
    await interaction.response.send_message(f"listening to {listening_channel}", ephemeral=True, delete_after="5.0")


@tree.command(name="leave", description="goodbye")
async def leave_command(interaction):
    global listening_channel
    global voice_client
    if listening_channel == None:
        await interaction.response.send_message(f"i never joined a channel?", ephemeral=True, delete_after="5.0")
        return
    await voice_client.disconnect()
    listening_channel = None
    message_queue = []
    await interaction.response.send_message("goodbye", ephemeral=True, delete_after="5.0")

@tree.command(name="exclusive", description="only listen to:")
@app_commands.describe(exclusive_display_name="display name of the exclusive person")
async def exclusive_command(interaction, exclusive_display_name: str):
    global exclusive_name
    exclusive_name = exclusive_display_name

@tree.command(name="clear_exclusive", description="listen to all who type in this channel")
async def clear_exclusive_command(interaction):
    global exclusive_name
    exclusive_name = ""

async def generate_voice_file(text):    
    tts.tts_to_file(text=text, speaker_wav="my/cloning/audio.wav", file_path="output.mp3")

client.run(secret.TOKEN)
