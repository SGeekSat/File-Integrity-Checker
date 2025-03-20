import os
# A test directory can be created from scratch to test the file integrity checker 
# without affecting the important system files
test_directory = "Test_Directory"
os.makedirs(test_directory, exist_ok=True) #creates a test directory if it doesn't exist in the system
print(f"'{test_directory}'created!!")
#add some sample files in the directory
for i in range(5):
    with open(f"Test_Directory/file{i+1}.txt", "w") as f:
        f.write(f"This is test file {i+1}.")
