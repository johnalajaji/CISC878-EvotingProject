import tenseal as ts  # to run this file make sure to install both tenseal and numpy
import os
import sys
import time

# Start timer for benchmark
start_time = time.time()


# Get public key context
if os.path.isfile('./publickey_context_CKKS_benchmark'):
    file = open("publickey_context_CKKS_benchmark","r")
    hex_line = file.read()
    file.close()
    context = ts.context_from(bytes.fromhex(hex_line))
else:
    print("Context not available")
    done = True


# Get votes from votes_database file
if os.path.isfile('./votes_database_CKKS_benchmark'):
    file = open("./votes_database_CKKS_benchmark","r")
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

resultstring = results.serialize()
resultstring = resultstring.hex()

# Write encrypted result to text file
file = open("tabulation_result_CKKS_benchmark","w")
file.write(resultstring)
file.close()


# Get run time
print("--- %s seconds ---" % (time.time() - start_time))
