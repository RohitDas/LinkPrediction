
import os
import csv
directory = '/home/rohittulu/Semester3/LinkPrediction/travian_data/Messages-Network-CSV'

def get_files(directory):
    return os.listdir(directory)

def read_files(directory):
    files = get_files(directory)
    day_csv = {}
    for idx, fname in enumerate(files):
        fpath = os.path.join(directory, fname)
        csvfile = open(fpath, 'r')
        day_csv.update({
                idx: csv.reader(csvfile, delimiter=",")
        })
    return day_csv

def get_player_ids(day_csv):
    players = set()
    for day, reader in day_csv.iteritems():
        print("Reading file: ", str(day))
        for row in reader:
            try:
                ts, play1, play2 = row
            except Exception as e:
                print(e)
            players.update([play1,play2])
    return players

def get_summary_per_day(day_csv_reader):
    info_dict = {}
    for ts, play1, play2 in day_csv_reader:
        info_dict.setdefault(play1, {}).setdefault(play2,0)
        info_dict[play1][play2] += 1
    return info_dict

def get_info_summary(day_to_csv_dict):
    day_to_info_summary = {}
    for day, reader in day_to_csv_dict.iteritems():
        try:
            day_to_info_summary.update({
                day: get_summary_per_day(reader)
            })
        except Exception as e:
            print(e)
    return day_to_info_summary

def save_day_file(day, summary, info_type):
    """
        type here can be either be attack, trade or messages.
    """
    save_fname = os.path.join(info_type +"_stats", str(day) + ".csv")
    with open(save_fname, "wb")  as csvfile:
        writer = csv.writer(csvfile, delimiter="|", quoting=csv.QUOTE_MINIMAL)
        for player, targets in summary.iteritems():
            line = []
            for target, n in targets.iteritems():
                line.append(str(target) + "(" + str(n) + ")")
            writer.writerow([player] + line)
            

def get_aggregrate_info(day_to_info_summary, info_type):
    aggregrate_summary = {}
    for day, info_summary in day_to_info_summary.iteritems():
        save_day_file(day, info_summary, info_type)
        for player1, targets in info_summary.iteritems():
            for target, n in targets.iteritems():
                aggregrate_summary.setdefault(player1, {}).setdefault(target, 0)
                aggregrate_summary[player1][target] += n
    return aggregrate_summary

day_csv = read_files(directory)
summary = get_info_summary(day_csv)
aggregrate_summary = get_aggregrate_info(summary, "messages")

save_file = "attack_summary.csv"
with open(save_file, "wb") as csvfile:
    writer = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
    for player, targets in aggregrate_summary.iteritems():
        line = []
        for target, n in targets.iteritems():
            line.append(str(target) + "(" + str(n) + ")")

        writer.writerow([player] + line)
