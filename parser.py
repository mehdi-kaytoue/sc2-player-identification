#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sc2reader, time
from sc2reader import events # Use the LOTV branch for sc2reader!
from multiprocessing import Pool as ThreadPool


global params
# arguments to be shared for all threads.
params = {}
params["dir"] = "./replay-data/"
params["nbac"] = 300
params["nbsec"] = 30
params["tw"] = 5
params["out"] = "replay-traces.txt"


# Parse a single replay
def parse_replay(filename):
    global params
    print("Parsing: " + str(filename))
    try:
        result = ""
        replay = sc2reader.load_replay(filename, load_level=4, debug=True)
        # @TODO: Do we really get players only? No observator, refeerees, ...?
        players = [t.players for t in replay.teams]
        players = [y for x in players for y in x]
        for i in range(1, len(players) + 1):
            player_trace = players[i - 1].url
            player_trace += "," + players[i - 1].play_race
            last = 0
            action_count = 0
            for event in replay.player[i].events:
                if event.second > params["nbsec"]: break
                if action_count > params["nbac"]: break
                if event.second - last >= params["tw"]:
                    while event.second - last >= params["tw"]:
                        last += params["tw"]
                        player_trace += ",t" + str(last)
                if isinstance(event, sc2reader.events.game.SelectionEvent):
                    elements = [o.name for o in event.objects]
                    if "Nexus" in elements or "Hatchery" in elements or "Command Center" in elements:
                        player_trace += ",Base"
                        action_count += 1
                    if "MineralField" in elements and len(elements) == 1:
                        player_trace += ",SingleMineral"
                        action_count += 1
                    player_trace += ",s"
                elif isinstance(event, sc2reader.events.game.ControlGroupEvent):
                    player_trace += ",hotkey" + str(event.hotkey) + str(event.update_type)
                    action_count += 1
            result += player_trace+"\n"
        return result
    except:
        print("Unable to parse this replay:" + filename)
        return ""


def replays2traces(dir, nbac, nbsec, tw, out):
    global params
    params["dir"] = dir
    params["nbac"] = nbac
    params["nbsec"] = nbsec
    params["tw"] = tw
    params["out"] = out
    replays_to_parse = sc2reader.utils.get_files(dir)
    pool = ThreadPool(4)
    results = pool.map(parse_replay, replays_to_parse)
    pool.close()
    pool.join()
    with open(out, "w") as text_file:
        for r in results:
            if len(r) > 0:
                text_file.write(r)




'''  # // NOTE // #
# Events that we don't use.
if isinstance(event, sc2reader.events.message.ProgressEvent): continue
elif isinstance(event, sc2reader.events.game.UserOptionsEvent): continue
elif isinstance(event, sc2reader.events.game.CameraEvent): continue
elif isinstance(event, sc2reader.events.message.ChatEvent): continue
elif isinstance(event, sc2reader.events.game.PlayerLeaveEvent): continue
elif isinstance(event, sc2reader.events.game.DataCommandEvent): continue
elif isinstance(event, sc2reader.events.game.BasicCommandEvent): continue
elif isinstance(event, sc2reader.events.game.TargetPointCommandEvent): continue
elif isinstance(event, sc2reader.events.game.TargetUnitCommandEvent): continue
    # print(event.ability.name + ":" + event.target.name)
'''