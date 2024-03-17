import os
import discord
from discord.ext import commands
from PIL import Image
import yaml

with open('info.yml', 'r') as info_file:
    image_data = yaml.safe_load(info_file)

image_data = {}

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def color(ctx):
    for file_name in image_data:
        if image_data[file_name] is True:
            file_path = f'images/{file_name}'
            await ctx.send(file=discord.File(file_path))
            break

@bot.command()
async def notcolor(ctx):
    for file_name in image_data:
        if image_data[file_name] is False:
            file_path = f'images/{file_name}'
            await ctx.send(file=discord.File(file_path))
            break

GRAY_THRESHOLD = 50

def process_images(image_data):
    for file_name in os.listdir('images'):
        if file_name.endswith('.jpg') or file_name.endswith('.png'):
            file_path = f'images/{file_name}'
            image = Image.open(file_path)
            pixels = image.load()
            has_color = False
            grayscale_count = 0
            total_pixels = image.size[0] * image.size[1]

            for y in range(image.size[1]):
                for x in range(image.size[0]):
                    r, g, b = pixels[x, y]
                    grayscale = (r + g + b) // 3
                    difference = abs(r - g) + abs(g - b) + abs(b - r)

                    if difference < GRAY_THRESHOLD:
                        grayscale_count += 1

            if (grayscale_count / total_pixels) >= 0.9:
                has_color = False
            else:
                has_color = True

            image_data[file_name] = has_color

    with open('info.yml', 'w') as info_file:
        yaml.dump(image_data, info_file, default_flow_style=False)

process_images(image_data)
bot.run("")
