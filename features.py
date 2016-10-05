from collections import Counter

def traces2features(inputfile, outputfile, maxsec):
    features = []
    races = []
    urls = []
    with open(inputfile, "r") as traces:
        for trace in traces:
            trace = trace[:len(trace)-1]  # remove the '\n'
            actions = trace.split(",")
            urls += [actions[0]]
            races += [actions[1]]
            if "t"+str(maxsec) in actions:
                actions = actions[:actions.index("t"+str(maxsec))]
            actions = actions[2:]
            actions = [a for a in actions if not a[0] == "t"]
            dico = Counter(actions)
            features += [dico]
    features_name_list = sorted(set([action for f in features for action in f.keys()]))

    with open(outputfile, "w") as text_file:
        text_file.write(",".join(features_name_list) + ",race,battleneturl\n" )
        index = 0
        for f in features:
            text_file.write(",".join([str(f[k]) for k in features_name_list]) + "," + races[index] + "," + urls[index] + '\n')
            index += 1
