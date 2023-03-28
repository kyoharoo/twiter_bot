
# Twitch bot
import requests
import schedule
import re
import discord
from discord.ext import commands
from time import sleep
import subprocess
import sys
import os 
import asyncio


# Twitch tokens 
access_token = "kxn84gsonjgzcsgllh7w3rtbqf6h2q"
client_id = "gp762nuuoqcoxypju8c569th9wz7q5"

# Open usernames check list files
with open("usernames.txt", "r") as f:
    usernames = [line.strip() for line in f]

# Dictionary to keep track of online status for each user
online_status = {username: False for username in usernames}

# Check if each streamer is live or not
def twitch_check():
    try:
        global live_message
        for username in usernames:
            # Construct API request
            url = f"https://api.twitch.tv/helix/streams?user_login={username}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Client-ID": client_id
            }
            response = requests.get(url, headers=headers).json()

            # Check if streamer is live or not
            if "data" in response and response["data"]:
                if not online_status[username]:
                    online_status[username] = True
                    print(username)
                    live_message = f"{username} is now live on Twitch! \nCheck out their stream at https://www.twitch.tv/{username}"
                    return live_message

            else:
                online_status[username] = False

        live_message = None
        return None
    except Exception as gg:
        print(gg)

        

# Schedule Twitch check every 2 minutes
schedule.every(200).seconds.do(twitch_check)

# Discord bot token
bot_tocken = ""
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    try:
        await client.change_presence(activity=discord.Game(name="OAN"))
        global last_part
        last_part = ""

        while True:
            try:
                await asyncio.sleep(20)                
                schedule.run_pending()
                channel = client.get_channel(987114499637141504) # Replace channel_id with the ID of the channel you want to send the message to
                live_message = twitch_check()
                if live_message is not None:
                    #send to spicifc channel if nao
                    if "naovtuberen" in live_message:
                        channel = client.get_channel(987051677456670784)
                        nao = """
يا اميراتي و امرائي الاعزاء ،حضرة الدوق ناو يبث بثا نبيلا في قاعة الحفلات الامبراطورية ، انتم جميعا مدعوون لقصر تويتش 
ملاحظة: الذي يتاخر او لا يحضر ،سوف يتم اقصاؤه من المملكة"""
                        live_message = f" naovtuberen is now live on Twitch! @everyone\nCheck out their stream\{nao}\n https://www.twitch.tv/naovtuberen"
                        await channel.send(live_message)
                    else:
                        await channel.send(live_message)
                    #grep users
                async for message in channel.history(limit=1):
                    if message.content.startswith("/grep_users"):
                        with open("usernames.txt", "r") as f:
                            usernames = [line.strip() for line in f]
                        await channel.send(usernames)
                    #append users
                    if message.content.startswith("append"):
                        last_message = message.content
                        Reg_ip = re.compile(r"append (.*)")
                        convert_ip = Reg_ip.findall(last_message)
                        last_part = "".join(convert_ip)
                        with open("usernames.txt", "a") as f:
                            f.write(f'{last_part}\n')    
                        await channel.send(f"{last_part} was successfully added\nPlease restart the bot to check the new appended users")
                        with open("usernames.txt", "r") as f:
                            usernames = [line.strip() for line in f]
                    #delete users
                    if message.content.startswith("rm"):
                        last_message = message.content
                        Reg_ip = re.compile(r"rm (.*)")
                        convert_ip = Reg_ip.findall(last_message)
                        last_part = "".join(convert_ip)
                        with open("usernames.txt", "r") as f:
                            lines = f.readlines()
                        lines = [line for line in lines if last_part not in line]
                        with open("usernames.txt", "w") as f:
                            f.writelines(lines)
                        await channel.send(f"{last_part} was successfully deleted\nPlease restart the bot")
                    #restart the bot  
                    if message.content.startswith("restart"):
                        await channel.send("Restarting...")
                        sleep(2)
                        print("restart")
                        script_path = '/home/container/AI_test1.py'
                        python = sys.executable
                        os.execl(python, python, script_path)
                

                
            except Exception as dd:
                print(dd)
                await asyncio.sleep(300)                
                print("restart")
                script_path = '/home/container/AI_test1.py'
                python = sys.executable
                os.execl(python, python, script_path)

    except Exception as ee:
        print(ee)
        print("restart")
        await asyncio.sleep(300)                
        script_path = '/home/container/AI_test1.py'
        python = sys.executable
        os.execl(python, python, script_path)
        
client.run(bot_tocken)