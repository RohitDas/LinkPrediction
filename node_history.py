test_days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

node_history = dict()
all_nodes = []

for test_day in test_days:
    with open('Communities/communities-2009-12-' + str(test_day) + '.txt','r') as f:
        for line in f:
            for word in line.split():
                if word not in all_nodes:
                    all_nodes.append(word)

for test_day in test_days:
    with open('Communities/communities-2009-12-' + str(test_day) + '.txt','r') as f:
        for line in f:
            count = 0
            for word in line.split():
                if (word not in node_history):
                    node_history[word] = []

                node_history[word].append(line.rstrip())

    for single_node in all_nodes:
        if test_day == 1:
            if single_node not in node_history:
                node_history[str(single_node)] = ["-1"]
        else:
            if len(node_history[str(single_node)]) != test_day:
                node_history[str(single_node)].append("-1")


''' Node History across 21 days '''
# -1 means the node did not exist in that day
node_history_output = open("node_history.txt", "a+")
for node in node_history:
    str_to_write = ""
    str_to_write += node
    str_to_write += ": "

    for history in node_history[node]:
        str_to_write += history
        str_to_write += ","

    str_to_write = str_to_write.rstrip(',')
    node_history_output.write(str_to_write)
    node_history_output.write("\n")