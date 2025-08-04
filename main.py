from iw4m import IW4MWrapper
from gsc_events import GSCClient
import os, time

client = GSCClient()

iw4m = IW4MWrapper(
    base_url  = os.environ['IW4M_URL'],
    server_id = os.environ['IW4M_ID'],
    cookie    = os.environ['IW4M_HEADER']
)

player   = iw4m.Player(iw4m)
server   = iw4m.Server(iw4m)
commands = iw4m.Commands(iw4m)

weapon_list: list[str] = [
    "fiveseven",
    "fnp45+silencer",
    "mp7",
    "saiga12+steadyaim",
    "ksg",
    "mk48+grip+reflex",
    "svu+swayreduc+vzoom",
    "usrpg",
    "crossbow+stackfire",
    "knife_ballistic"
]

player_progress: dict[str, int] = {}

@client.on("player_connected")
def on_connected(client: str) -> None:
    commands.say("^7Welcome to ^5custom gun game ^7created by budiworld")
    commands.say("^7This works ^2fully with ^7python, ^1no gsc ^7required")
    player_progress[client] = 0

@client.on("player_spawned")
def on_spawned(client: str) -> None:
    client_id = player.player_client_id_from_name(client)
    commands.takeweapons(f"@{client_id}")

    level: int  = player_progress.get(client, 0)
    weapon: str = weapon_list[level]
    commands.giveweapon(f"{client_id}", weapon)

@client.on("player_killed")
def on_kill(attacker: str, victim: str, reason: str) -> None:
    if attacker == victim: return

    current_level = player_progress.get(attacker, 0)
    if current_level + 1 < len(weapon_list):
        player_progress[attacker] = current_level + 1
    else:
        commands.say(f"{attacker} has ^2won the game!")
        for player in server.get_players():
            commands.takeweapons(player['name'])
        
        time.sleep(5)
        commands.maprotate()

if __name__ == '__main__':
    commands.say("Gun Game starting")
    time.sleep(2)
    commands.maprotate()
    client.run()