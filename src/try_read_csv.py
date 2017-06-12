import fileinput

# read from stdin or file on command line.
topics_labels = []
for line in fileinput.input():

    topics_labels.append(line.replace('\n',''))

print(topics_labels)
