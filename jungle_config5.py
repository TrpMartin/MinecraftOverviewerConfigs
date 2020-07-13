### MO config file for jungle map in raspi server
import sys
#add my markers
sys.path.append("/home/pi/Minecraft-Overviewer/") # so python can find my_markers file
from my_markers import *

# Define the path to your world here. 'My World' in this case will show up as
# the world name on the map interface. If you change it, be sure to also change
# the referenced world names in the render definitions below.
worlds["jungle"] = "/home/pi/.minecraft/saves/jungle_world/"
#worlds["nether"] = "/home/martin/.minecraft/saves/jungle_world/world_nether"
#world_name = "In the jungle"
#nether_name = "Nether"

# Define where to put the output here.
outputdir = "/home/pi/www/jungle_map_cropped"


## server jar downloaded from mojang website, unsure if necessary, still getting black spots
texturepath = "/home/pi/.minecraft/versions/1.16/1.16.1.jar"

## This is an item usually specified in a renders dictionary below, but if you
## set it here like this, it becomes the default for all renders that don't
## define it. Try "smooth_lighting" for even better looking maps!
#rendermode = "smooth_lighting" ## gives black spots?

#define my own end lighting taken from internet config
end_smooth_lighting = [Base(), EdgeLines(), SmoothLighting(strength=0.85)]

##### functions of the things to display extra than default (=nothing) #####

#POI Filters
def townFilter(poi):
    if poi['id'] == 'Town' or poi['id'] == 'minecraft:town':
        return poi['name']

# mein versuch, towns automatisch zu annotieren mit dem meeting point als id. funzt nicht.
#def plainstownFilter(poi):
#    if poi['id'] == 'minecraft:plains_meeting_point_4' or poi['id'] == 'minecraft:plains_meeting_point_5':
#        return "Plains Town"+poi['name']

def hutFilter(poi):
    if poi['id'] == 'Hut':
        return poi['name']

def monumentFilter(poi):
    if poi['id'] == 'Monument':
        return poi['name']

def pyramidFilter(poi):
    if poi['id'] == 'Pyramid':
        return poi['name']

def portalFilter(poi):
    if poi['id'] == 'Portal':
        return poi['name']

def lighthouseFilter(poi):
    if poi['id'] == 'Lighthouse':
        return poi['name']

def shipFilter(poi):
    if poi['id'] == 'Ship' or poi['id'] == 'minecraft:ship': ## gibt es eine ship id?
        return poi['name']

def towerFilter(poi):
    if poi['id'] == 'Tower' or poi['id'] == 'minecraft:tower': ## gibt es eine tower id?
        return poi['name']

def templeFilter(poi):
    if poi['id'] == 'Temple' or poi['id'] == 'minecraft:temple':
        return poi['name']

def playerIcons(poi):
    if poi['id'] == 'Player':
        poi['icon'] = "http://overviewer.org/avatar/%s" % poi['EntityId']
        return "Last known location for %s" % poi['EntityId']

def signFilter(poi):
    if poi['id'] == 'Sign' or poi['id'] == 'minecraft:sign':
        return "\n".join([poi['Text1'], poi['Text2'], poi['Text3'], poi['Text4']])

def chestFilter(poi):
    if poi['id'] == 'Chest' or poi['id'] == 'minecraft:chest':
        #return "Chest with %d items" % len(poi['minecraft:items'])
        return "Chest"

def spawnerFilter(poi):
    if poi['id'] == 'MobSpawner' or poi['id'] == 'minecraft:mob_spawner' or poi['id'] == 'minecraft:spawner{BlockEntityTag:{SpawnData:{id:"zombie"}}}':
        if "EntityId" in poi:
          monster = poi["EntityId"]
        elif "SpawnPotentials" in poi:
            monster = poi["SpawnPotentials"][0]["Entity"]["id"]
        else:
            return None
        info = "[MobSpawner] \n%s \n" % monster
        info += ", ".join(map(str, [poi["x"], poi["y"], poi["z"]]))
        return info

### marker dictionary
markers_dict = [dict(name="All Signs", filterFunction=signFilter),
	dict(name="Chests", filterFunction=chestFilter, icon="icons/my_chest.png", createInfoWindow=False), ###mtbo addition, added in icons dir overviewer_core
	dict(name="Players", filterFunction=playerIcons, checked=True),
	dict(name="Spawner", filterFunction=spawnerFilter), ##TODO get picture
	dict(name="Ships", filterFunction=shipFilter, icon="icons/marker_ship.png", checked=True),
        dict(name="Towers", filterFunction=towerFilter, icon="icons/marker_tower.png", checked=True),
        dict(name="Monument", filterFunction=monumentFilter, icon="icons/monument.png", checked=True),
        dict(name="Pyramid", filterFunction=pyramidFilter, icon="icons/pyramid.png", checked=True),
        dict(name="Portal", filterFunction=portalFilter, icon="icons/portal.png", checked=True),
        dict(name="Lighthouse", filterFunction=lighthouseFilter, icon="icons/lighthouse.png", checked=True),
        dict(name="Temple", filterFunction=templeFilter, icon="icons/temple.png", checked=True),
        dict(name="Towns", filterFunction=townFilter, icon="icons/marker_town.png", checked=True),
        dict(name="Hut", filterFunction=hutFilter, icon="icons/hut.png", checked=True)
]


##### the rendering to be done ####

renders["Tag"] = {
    "world": "jungle",
    "title": "Dschungel Tag",
    "dimension": "overworld",
    "crop": (-500,-500,500,500), # set a 1000x1000 tile boundary for smaller map to faster render test stuff
    "markers": markers_dict,
    "manualpois": manualmarkers,
    "rendermode": "normal",
}

## This example is the same as above, but rotated
#renders["Tag Osten"] = {
#    "world": "jungle",
#    "northdirection": "upper-right",
#    "title": "Dschungel gedreht",
#    "markers": markers_dict,
#    "manualpois": manualmarkers,
#    "rendermode": "normal",
#}

### Overworld caves
#renders["Tunnel"] = {
#        "world": "jungle",
#        "title": "Dschungel Tunnels",
#        "rendermode": cave,
#        "dimension": "overworld",
##        "overlay" : ["jungle", worlds], # from web but results in syntax error
#        "markers": [dict(name="All signs", filterFunction=signFilter),
#                    dict(name="Chests", filterFunction=chestFilter, icon="icons/my_chest.png", createInfoWindow=True),
#                    dict(name="Players", filterFunction=playerIcons, createInfoWindow=True)]
#}

## Nacht
renders["Nacht"] = {
        "world": "jungle",
        "title": "Dschungel Nacht",
        "dimension": "overworld",
        "crop": (-500,-500,500,500), # set a 1000x1000 tile boundary for smaller map to faster render test stuff
        #"rendermode": "smooth_night",
        "rendermode": "night",
}


renders["biomeover"] = {
    "world": "jungle",
    "rendermode": [ClearBase(), BiomeOverlay()],
    "crop": (-500,-500,500,500), # set a 1000x1000 tile boundary for smaller map to faster render test stuff
    "title": "Biome Coloring Overlay",
    "overlay": ['Tag']
}

renders["mineralover"] = {
    "world": "jungle",
    "rendermode": [ClearBase(), MineralOverlay()],
    "crop": (-500,-500,500,500), # set a 1000x1000 tile boundary for smaller map to faster render test stuff
    "title": "Mineral Overlay",
    "overlay": ['Tag']
}


## The Nether!
renders["Nether"] = {
        "world": "jungle",
        "title": "Dschungel Nether",
        "dimension": "nether",
        "crop": (-500,-500,500,500),
##        "rendermode": nether_smooth_lighting, # das kann das problem mit dem nether sein
        "rendermode": "nether",
}

## The End!
renders["The End"] = {
        "world": "jungle",
        "title": "Dschungel - The End",
        "dimension": "end",
        "crop": (-500,-500,500,500),
        #"rendermode": end_smooth_lighting, # defined on top of this file, gab black spots
        "rendermode": "normal",
}


