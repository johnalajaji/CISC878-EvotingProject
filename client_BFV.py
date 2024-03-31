import tenseal as ts  # to run this file make sure to install both tenseal and numpy
import os

screen = "home"
done = False

# Get public key context for vote encryption
if os.path.isfile('./publickey_context_BFV'):
    file = open("publickey_context_BFV","r")
    hex_line = file.read()
    file.close()
    context = ts.context_from(bytes.fromhex(hex_line))
else:
    print("Context not available")
    done = True


# Begin terminal user interface
while (not done):
    if screen == "home":
        print("Select an option below:")
        print("1. Enter a vote")
        #print("2. Tabulate votes (Requires ADMIN Privileges)")
        print("2. Exit")
        screen = input("Selected option number: ")
    elif screen == "1":
        voterid = input("Please enter your assigned voter ID: ")
        screen = "vote"
    elif screen == "vote":
        print("Please choose a candidate from the list below:")
        print("1. Drake")
        print("2. Lisan al Gaib")
        print("3. Mark Zuckerberg")
        print("4. Ronald Mathew")
        print("5. Muscrat Representative")
        print("6. Salim Shady")
        print("7. Spongebob")
        print("8. Big Mac")
        print("9. Silvouplait")
        vote = input("Selected candidate number: ")
        voteVector = [int(voterid)]
        
        i = 0
        while (i<9):
            if (i+1 == int(vote)):
                voteVector.append(1)
            else:
                voteVector.append(0)
            i += 1

        encryptedVote = ts.bfv_vector(context, voteVector)
        voteVector = []  # Clear the value for voteVector
        encryptedVote = encryptedVote.serialize()
        encryptedVote = encryptedVote.hex()
        #votes.append(encryptedVote)

        # Write encrypted vote to "database"
        file = open("votes_database_BFV","a")
        file.write(encryptedVote)
        file.write(hex(13))  # Add carriage return
        file.close()

        screen = "home"
    elif screen == "2":
        done = True
    else:
        print("Please choose a valid option")


