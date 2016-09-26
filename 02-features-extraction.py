import argparse, time
from collections import Counter

arg = None


def main(args):
    features = []
    races = []
    urls = []
    with open(args.IN, "r") as traces:
        for trace in traces:
            trace = trace[:len(trace)-1]  # remove the '\n'
            actions = trace.split(",")
            urls += [actions[0]]
            races += [actions[1]]
            if "t"+str(args.MAX_SEC) in actions: actions = actions[:actions.index("t"+str(args.MAX_SEC))]
            actions = actions[2:]
            actions = [a for a in actions if not a[0]=="t"]
            dico = Counter(actions)
            features += [dico]
    features_name_list = sorted(set([action for f in features for action in f.keys()]))

    with open(args.OUT, "w") as text_file:
        text_file.write(",".join(features_name_list) + ",race,battleneturl\n" )
        index = 0
        for f in features:
            text_file.write(",".join([str(f[k]) for k in features_name_list]) + "," + races[index] + "," + urls[index] + '\n')
            index += 1

if __name__ == '__main__':
    start_time = time.time()
    global args
    parser = argparse.ArgumentParser(description="""@TODO""")  # @TODO Give a clear description of the script.
    parser.add_argument('IN', type=str, help="INPUT")
    parser.add_argument('OUT', type=str, help="OUTPUT")
    parser.add_argument('MAX_SEC', type=int, help="MAX_SEC")
    args = parser.parse_args()
    main(args)
    print("--- Finished in " + str(int(time.time() - start_time)) + " seconds ---")
