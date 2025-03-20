import os
import hashlib
import json

# computing the hash of the file
def ComputingHash(file_path,algo="sha256"):
    #the basic Secure Hash Algorithm -256 has been used 
    # that creates unique 256 hash values from the input data
    # a hash function
    '''args:
    file_path(str): Path to the file
    algo(str): hashing algorithm (SHA 256)
    
    Returns: 
    str: hexadecimal hash values of the files
    '''
    hashing = hashlib.new(algo)
    try: 
        with open(file_path,"rb") as f: #opening the file in binary format to read the contents
            while chunk := f.read(4096): #the file contents are read in chunks to handle larger files
                hashing.update(chunk)
        return hashing.hexdigest() #the computed hexadecimal hashes are returned
    except FileNotFoundError:
        return None #returning NONE if the file doesn't exist
    
#the function to generate and store initial file hashes
def InitialHashes(directory, hashFile="fileHashes.json"):
    """
    Generates and stores hash values (initial) of all the files in the created directory
    Args: 
    directory(str):
    The directory that needs to be scanned for the files
    hashFile(str): JSON file where the hashes will be stored

    this returns nothing
    """
    fileHashes = {} #this dictionary stores the hash values

    #the directory is traversed to get all the files
    for root, _, files in os.walk(directory):
        for i in files:
            file_path= os.path.join(root,i) #getting the full file path
            fileHashes[file_path]= ComputingHash(file_path)
    with open(hashFile,"w") as f:  #the hashes are saved to a JSON file for future verifications
        json.dump(fileHashes,f,indent=4)
    print("Initial File hashes have been stored successfully!!!")

def CheckingIntegrity(directory,hashFile="fileHashes.json"):

    """ compares current files' hashes with stored hashes to detect modifications
    Args: 
    directory(str): this is the directory to be scanned
    hashFile(str): JSON file with stored hashes

    this returns nothing
    """
    try:
        with open(hashFile, 'r') as f:
            storedHashes = json.load(f)
    except FileNotFoundError:
        print("⚠️ No previous hash records found, run initializations first!")
        return
    modifiedFiles =[] # tracks modified files
    missingFiles =[] #tracks missing files
    newFiles =[] #tracks newly created files 
    #Traverse stored hashes to check for changes
    for file_path, old_hash in storedHashes.items():
        new_hash = ComputingHash(file_path)

        if new_hash is None:
            missingFiles.append(file_path)  # File is missing
        elif new_hash != old_hash:
            modifiedFiles.append(file_path)  # File was modified

    # Check for new files that were not in the original record
    currentFiles = {os.path.join(root, i) for root, _, files in os.walk(directory) for i in files}
    storedFiles = set(storedHashes.keys())
    newFiles = list(currentFiles - storedFiles)

    # Print results
    if missingFiles or modifiedFiles or newFiles:
        print("\n🚨 Integrity Alert! Detected changes in files:\n")

        if modifiedFiles:
            print("🔴 Modified Files:")
            for file in modifiedFiles:
                print(f"  - {file}")

        if missingFiles:
            print("\n⚠️ Missing Files:")
            for file in missingFiles:
                print(f"  - {file}")

        if newFiles:
            print("\n🆕 New Files Detected:")
            for file in newFiles:
                print(f"  - {file}")

    else:
        print("✅ No modifications detected. All files are intact.")

# Set directory to monitor
monitored_directory = "Test_Directory"

# Step 1: Initialize hashes (run this only once)
# InitialHashes(monitored_directory)

# Step 2: Modify files manually to test integrity check
#Step 3: Run the integrity check
CheckingIntegrity(monitored_directory)


