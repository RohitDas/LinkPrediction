test_days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

never_singleton = []
already_removed = []

for test_day in test_days:
    with open('Communities/communities-2009-12-' + str(test_day) + '.txt','r') as f:
        for line in f:
            count = 0
            for word in line.split():
                count = count+1
                if word not in never_singleton and word not in already_removed:
                    never_singleton.append(word)

            if count == 1:
                if word not in already_removed:
                    already_removed.append(word)

                while word in never_singleton: 
                    never_singleton.remove(word)


never_singleton_output = open("never_singleton.txt", "a+")
for node in never_singleton:
    never_singleton_output.write(node)
    never_singleton_output.write("\n")