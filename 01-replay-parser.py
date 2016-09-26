#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse, sc2reader, time
from sc2reader import events # Use the LOTV branch for sc2reader!
from multiprocessing import Pool as ThreadPool


args = None # command line arguments, see main


# Map to parse replay on mutiple cores.
def multi_parse_replay(filenames, threads):
    pool = ThreadPool(threads)
    results = pool.map(parse_replay, filenames)
    pool.close()
    pool.join()
    return results


# Parse a single replay
def parse_replay(filename):
    global args
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
                if event.second > args.NBSEC: break
                if action_count > args.NBAC: break
                if event.second - last >= args.TW:
                    while event.second - last > args.TW:
                        last += args.TW
                        player_trace += ",t" + str(last)
                if isinstance(event, sc2reader.events.game.SelectionEvent):
                    elements = [o.name for o in event.objects]
                    if "Nexus" in elements or "Hatchery" in elements or "Command Center" in elements:
                        player_trace += ",Base"
                        action_count += 1
                    if "MineralField" in elements and len(elements) == 1:
                        player_trace += ",SingleMineral"
                        action_count += 1
                elif isinstance(event, sc2reader.events.game.ControlGroupEvent):
                    player_trace += ",hotkey" + str(event.hotkey) + str(event.update_type)
                    action_count += 1
            result += player_trace+"\n"
        return result
    except:
        return ""

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


def main():
    parser = argparse.ArgumentParser(description="""@TODO""") #@TODO Give a clear description of the script.
    parser.add_argument('DIR', type=str, help="The directory with replays you want to analyze")
    parser.add_argument('NBAC', type=int, help="The number of actions to consider for a sequence")
    parser.add_argument('NBSEC', type=int, help="The number of seconds to consider for a sequence")
    parser.add_argument('TW', type=int, help="The size of the timestamp windows", nargs='?')
    parser.add_argument('OUT', type=str, help="The filename of the output")

    global args
    args = parser.parse_args()
    if args.TW is None: args.TW = 10 # set a default value to this argument
    replays_to_parse = sc2reader.utils.get_files(args.DIR)
    results = multi_parse_replay(replays_to_parse, 4)
    with open(args.OUT, "w") as text_file:
        for r in results:
            if len(r) > 0:
                text_file.write(r)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- Finished in " + str(int(time.time() - start_time)) + " seconds ---")
