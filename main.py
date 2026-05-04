from pathlib import Path
import asyncio
import discord
import sys
import pluralkit

CONFIG_PATH = Path(__file__).resolve().parent / "config.yml"


def load_config():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text("# Obtain from running pk;token \nPK_TOKEN: \n\n## Follow these instructions: https://gist.github.com/MarvNC/e601f3603df22f36ebd3102c501116c6/2831d42c40602157d1f313c2dc880fc5fc50a460\nDISCORD_TOKEN: \n")
        
        print(f"Created {CONFIG_PATH}. Fill in PK_TOKEN and DISCORD_TOKEN, then run again.")
        sys.exit(1)

    text = CONFIG_PATH.read_text()
    config = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        config[key.strip()] = value.strip().strip('"').strip("'")
        

    missing = [key for key in ["PK_TOKEN", "DISCORD_TOKEN"] if not config.get(key)]
    if missing:
        print(f"config.yml is missing the following values: {', '.join(missing)}")
        print(f"Update {CONFIG_PATH} and run again.")
        sys.exit(1)

    return config


config = load_config()
pk = pluralkit.Client(config["PK_TOKEN"])


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self.current_status = None
        self.loop.create_task(self.check_fronters())

    async def check_fronters(self):
        while True:
            pronouns_list = []
            name_list = []
            async for member in pk.get_fronters():
                if member.pronouns:
                    for p in member.pronouns.split('/'):
                        p = p.strip()
                        if p not in pronouns_list:
                            pronouns_list.append(p)
                if member.name:
                    name_list.append(member.name)
            combined = '/'.join(pronouns_list)
            combined = f"{', '.join(name_list)} ({combined})" if combined else ', '.join(name_list)
            if combined != self.current_status:
                self.current_status = combined
                print(combined)
                await self.change_presence(activity=discord.CustomActivity(name=combined))
                #await self.user.edit(pronouns=combined)
            await asyncio.sleep(5)


client = MyClient()
client.run(config["DISCORD_TOKEN"])