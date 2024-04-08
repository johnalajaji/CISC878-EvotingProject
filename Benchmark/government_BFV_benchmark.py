import tenseal as ts  # to run this file make sure to install both tenseal and numpy
import os
import sys
import time

# Start timer for benchmark
start_time = time.time()


# Get private key context for vote tabulation + decryption
if os.path.isfile('./privatekey_context_BFV_benchmark'):
    file = open("privatekey_context_BFV_benchmark","r")
    hex_line = file.read()
    file.close()
    context = ts.context_from(bytes.fromhex(hex_line))
else:
    print("Context not available")
    sys.exit()

# Get private key context for vote tabulation + decryption
if os.path.isfile('./tabulation_result_BFV_benchmark'):
    file = open("tabulation_result_BFV_benchmark","r")
    hex_line = file.read()
    file.close()
    results = ts.bfv_vector_from(context,bytes.fromhex(hex_line))
else:
    print("Tabulation not available")
    sys.exit()

resultvector = results.decrypt()

print("-----------------------------------------------")
print("Election results:")
candidates = ["Drake", "Lisan al Gaib", "Mark Zuckerberg", "Ronald Mathew",
               "Muscrat Representative", "Salim Shady", "Spongebob", "Big Mac", "Silvouplait"]
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


# Get run time
print("--- %s seconds ---" % (time.time() - start_time))