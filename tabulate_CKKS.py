import tenseal as ts  # to run this file make sure to install both tenseal and numpy
import os
import sys


# Get private key context for vote tabulation + decryption
if os.path.isfile('./privatekey_context_CKKS'):
    file = open("privatekey_context_CKKS","r")
    hex_line = file.read()
    file.close()
    context = ts.context_from(bytes.fromhex(hex_line))
else:
    print("Context not available")
    sys.exit()


# Get votes from votes_database file
if os.path.isfile('./votes_database_CKKS'):
    file = open("./votes_database_CKKS","r")
    buff = file.read()
    file.close()
else:
    print("Votes unavailable")
    sys.exit()

hexVotes = buff.split(hex(13))  # Split on carriage return to get votes
votes = []
i = 1
while i<len(hexVotes)-1:
    votes.append(ts.ckks_vector_from(context,bytes.fromhex(hexVotes[i])))
    i += 2


# Tabulate votes
results = votes[0]
i = 1
while i < len(votes):
    results += votes[i]
    i += 1

resultvector = results.decrypt()

i = 0
while i < len(resultvector):
    resultvector[i] = round(resultvector[i])
    i += 1


print("Election results:")
candidates = ["Drake", "Lisan al Gaib", "Mark Zuckerberg", "Ronald Mathew",
               "Muscrat Representative", "Salim Shady", "Spongebob", "Big Mac"]
i = 0
max = 0
maxIndex = 1
while i < len(resultvector):
    print(candidates[i] + ": " + str(resultvector[i]) + " votes")
    if resultvector[i] > max:
        max = resultvector[i]
        maxIndex = i
    i+=1

# Assume that there are no ties
print("-----------------------------------------------")
print(candidates[maxIndex] + " won the election with " + str(resultvector[maxIndex]) + " votes")
print("-----------------------------------------------")
