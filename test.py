import os
test_dir = r"D:\My Files\business\businexhtml-101\businex\src"

# # traverse through the entire dir
# for root, dirs, files in os.walk(test_dir):
#     for file in files:
#         filepath = os.path.join(root, file)
#         print(filepath)

test = os.getenv('OPENAI_API_KEY')
print(test)