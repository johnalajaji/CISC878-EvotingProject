import tenseal as ts  # to run this file make sure to install both tenseal and numpy
import os
import time
import sys
import time
import random

# Start timer for benchmark
start_time = time.time()

screen = "home"
done = False

# Get public key context for vote encryption
if os.path.isfile('./publickey_context_BFV_benchmark'):
    file = open("publickey_context_BFV_benchmark","r")
    hex_line = file.read()
    file.close()
    context = ts.context_from(bytes.fromhex(hex_line))
else:
    print("Context not available")
    done = True

# Get previously voted voterIDs (if any)
if os.path.isfile('./votes_database_BFV_benchmark'):
    file = open("./votes_database_BFV_benchmark","r")
    buff = file.read()
    file.close()
    gotvotes = True
else:
    gotvotes = False

votedID = []
if gotvotes:
    hexVotes = buff.split(hex(13))  # Split on carriage return to get voterIDs and votes
    i = 0
    while i<len(hexVotes)-1:
        votedID.append(hexVotes[i])
        i += 2


# Generate random votes
samplesize = 1000
j = 0

while j < samplesize:
    voteVector = []
    vote = random.randint(1,8)
    i = 0
    while (i<8):
        if (i+1 == int(vote)):
            voteVector.append(1)
        else:
            voteVector.append(0)
        i += 1

    encryptedVote = ts.bfv_vector(context, voteVector)
    voteVector = []  # Clear the value for voteVector
    encryptedVote = encryptedVote.serialize()
    encryptedVote = encryptedVote.hex()

    # Write encrypted vote to "database"
    file = open("votes_database_BFV_benchmark","a")
    file.write(str(random.randint(1,99999999)))
    file.write(hex(13))  # Add carriage return
    file.write(encryptedVote)
    file.write(hex(13))  # Add carriage return
    file.close()
    j += 1


# Get run time
print("--- %s seconds ---" % (time.time() - start_time))
