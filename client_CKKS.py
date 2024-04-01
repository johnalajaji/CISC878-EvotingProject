import tenseal as ts  # to run this file make sure to install both tenseal and numpy
import os
import time
import sys

screen = "home"
done = False

# Get public key context for vote encryption
if os.path.isfile('./publickey_context_CKKS'):
    file = open("publickey_context_CKKS","r")
    hex_line = file.read()
    file.close()
    context = ts.context_from(bytes.fromhex(hex_line))
else:
    print("Context not available")
    done = True

# Get previously voted voterIDs (if any)
if os.path.isfile('./votes_database_CKKS'):
    file = open("./votes_database_CKKS","r")
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

# Begin terminal user interface
while (not done):
    # Home screen
    if screen == "home":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Select an option below:")
        print("1. Enter a vote")
        print("2. Exit")
        screen = input("Selected option number: ")
    # Want to enter a vote (first enter voterID)
    elif screen == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        voterid = input("Please enter your assigned voter ID: ")

        if (voterid in votedID):
            print("Voter ID already used")
            time.sleep(0.7)
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.7)
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.7)
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.7)
            screen = "home"
        elif not voterid.isdigit():
            print("Voter ID is invalid") 
            desire = input("Press 1 to try again or 2 to return to the home screen: ")
            if desire == "1":
                screen = "home"
            else:
                screen = "1"
        else:
            votedID.append(voterid)
            screen = "vote"
    # Input vote
    elif screen == "vote":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Please choose a candidate from the list below:")
        print("1. Drake")
        print("2. Lisan al Gaib")
        print("3. Mark Zuckerberg")
        print("4. Ronald Mathew")
        print("5. Muscrat Representative")
        print("6. Salim Shady")
        print("7. Spongebob")
        print("8. Big Mac")

        # Get valid vote
        valid = ["1","2","3","4","5","6","7","8"]
        vote = input("Selected candidate number: ")
        if vote in valid:
            voteVector = []
            i = 0
            while (i<8):
                if (i+1 == int(vote)):
                    voteVector.append(1)
                else:
                    voteVector.append(0)
                i += 1

            encryptedVote = ts.ckks_vector(context, voteVector)
            voteVector = []  # Clear the value for voteVector
            encryptedVote = encryptedVote.serialize()
            encryptedVote = encryptedVote.hex()

            # Write encrypted vote to "database"
            file = open("votes_database_CKKS","a")
            file.write(voterid)
            file.write(hex(13))  # Add carriage return
            file.write(encryptedVote)
            file.write(hex(13))  # Add carriage return
            file.close()

            screen = "home"
        else:
            print("Vote invalid. Please choose one of the available options.")
            time.sleep(0.7)
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.7)
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.7)
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.7)
            screen = "vote"
    # Want to terminate program
    elif screen == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        done = True
    # Invalid resquest
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Please choose a valid option")
        time.sleep(0.7)
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.7)
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.7)
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.7)
        screen = "home"