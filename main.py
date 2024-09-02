import subprocess
import os
import json

from typer import Typer

app = Typer()

if os.path.exists("profiles.json"):
    profiles = json.load(open("profiles.json"))
else:
    profiles = {}

@app.command()
def save(name: str):
    current_items = subprocess.Popen(["dockutil", "--list"], stdout=subprocess.PIPE).communicate()[0].decode().splitlines()
    apps = []
    for item in current_items:
        itemdata = item.split("\t")
        if itemdata[2] == "persistentApps":
            apps.append(itemdata[1].replace("%20", " "))
    profiles[name] = apps
    with open("profiles.json", "w") as profilesfile:
        json.dump(profiles, profilesfile)
    print("Saved profile successfully")

@app.command()
def load(name: str):
    if name in profiles.keys():
        subprocess.run(["dockutil", "--remove", "all"])
        for item in profiles[name]:
            subprocess.run(["dockutil", "--add", item], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["killall", "Dock"], stderr=subprocess.PIPE)
        print("Loaded profile")
    else:
        print("Profile not found")

if __name__ == "__main__":
    app()