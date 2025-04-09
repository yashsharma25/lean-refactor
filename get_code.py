from github import Github
#from transformers import RobertaTokenizerFast
import os
import re

import base64

#from transformers import BertTokenizer


# Load the pre-trained BERT tokenizer
#tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Connect to GitHub API
g = Github()

# Get a specific repository
repo = g.get_repo("AlexKontorovich/PrimeNumberTheoremAnd")
lean_files = []

# Specify the commit SHA
commit_sha = "bb336bd29cd77898806b2d6765bf791dfd3853a2"
old_commit_sha = "74468123a524a403a68cfe8afdb03b869b2e7ae1"

function_patterns = [
    r'lemma\s+(\w+)', 
    r'def\s+(\w+)', 
    r'theorem\s+(\w+)', 
    r'noncomputable\s+def\s+(\w+)', 
    r'noncomputable\s+abbrev\s+(\w+)'
]


def extract_changed_functions(patch):
    """
    Extract functions that were changed in the patch.
    """
    changed_functions = {}
    lines = patch.split('\n')
    current_function = None
    function_code = []
    inside_function = False

    for line in lines:
        if line.startswith('@@'):
            if current_function and function_code:
                changed_functions[current_function] = '\n'.join(function_code)
            function_code = []
            current_function = None
            inside_function = False
        elif any(re.search(pattern, line) for pattern in function_patterns):
            if current_function and function_code:
                changed_functions[current_function] = '\n'.join(function_code)
            function_code = []
            current_function = None
            inside_function = True
            match = next(re.search(pattern, line) for pattern in function_patterns if re.search(pattern, line))
            if match:
                current_function = match.group(1)
        elif inside_function:
            function_code.append(line)
    
    if current_function and function_code:
        changed_functions[current_function] = '\n'.join(function_code)
    
    return changed_functions


def extract_function_from_content(content, function_name):
    print("EXTRACTING FUNCTION WITH THE NAME ", function_name)
    """
    Extract the full function definition from the file content.
    """
    lines = content.split('\n')
    function_code = []
    inside_function = False
    function_pattern = re.compile(rf'\b{function_name}\b')

    for line in lines:
        if function_pattern.search(line):
            inside_function = True
        if inside_function:
            function_code.append(line)
            if line.strip() == "":
                break
    
    return '\n'.join(function_code)
     
def save_functions(filename, functions, commit_type):
    with open(f"{commit_type}_changed_functions_{os.path.basename(filename)}.lean", 'w') as f:
        for function, code in functions.items():
            f.write(f"-- Function: {function}\n")
            f.write(f"{code}\n")
            f.write("="*40 + "\n")

def fetch_code_from_commit(repo, commit_sha):
    try:                
        # Get the file contents at this commit
        commit = repo.get_commit(commit_sha)
        print("Commit found")
        files_changed = commit.files

        
        # Print details and code of each file
        for file in files_changed:
            print(f"Filename: {file.filename}")
            print(f"Additions: {file.additions}")
            print(f"Deletions: {file.deletions}")
            print(f"Changes: {file.changes}")
            print(f"Status: {file.status}")

            # print("******************* PATCH STARTS HERE *******************")
            # print(f"Patch:\n{file.patch}\n")
            
            # Get file contents at the commit level
            file_contents = repo.get_contents(file.filename, ref=commit_sha)
            # print(f"Code in {file.filename}:\n{file_contents.decoded_content.decode('utf-8')}\n")
            changed_functions = extract_changed_functions(file.patch)
            print("****************CHANGED FUNCTION****************")
            print(changed_functions)

            
            # Fetch the file contents at the previous commit
            print("TRYING TO FETCH OLD COMMIT")
            old_file_contents = repo.get_contents(file.filename, ref=old_commit_sha)
            print("FOUND OLD COMMIT")


            # # Decode the content
            if old_file_contents.encoding == 'base64':
                old_content = base64.b64decode(old_file_contents.content).decode('utf-8')
            else:
                old_content = old_file_contents.decoded_content.decode('utf-8')
            print("DECODED OLD CONTENT", old_content)
            
            #print("FILE CONTENTS", file_contents)

            print("Changed functions are these:", changed_functions)
            # Extract the same functions from the previous commit
            print("PREVIOUS FILE EXTRACTION")
            old_functions = {fn: extract_function_from_content(old_content, fn) for fn in changed_functions}

            # # Decode the content
            if file_contents.encoding == 'base64':
                content = base64.b64decode(file_contents.content).decode('utf-8')
            else:
                content = file_contents.decoded_content.decode('utf-8')

            print("NEW FILE EXTRACTION")

            new_functions = {fn: extract_function_from_content(content, fn) for fn in changed_functions}

            print("EXTRACTED")
            # Save the changed functions and their previous versions
            save_functions(file.filename, changed_functions, "new")
            save_functions(file.filename, old_functions, "old")
            save_functions(file.filename, new_functions, "new_full")

        
    except Exception as e:
        print(f"Error fetching file at commit {commit_sha}: {str(e)}")
        return None


# Now you have the code blocks from the specific commit
# You can process them further as needed
fetch_code_from_commit(repo, commit_sha)


def print_file_content(file_content):
    """Print the content of a file as text."""
    # Decode the byte content to string
    text = file_content.decoded_content.decode('utf-8')
    print(text)

def save_file(file_content):
    """Save the content of a file to the local system."""
    
    # Construct a full local path to save the file
    local_path = os.path.join('lean_dir', file_content.path)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Write the file content to the local file system
    with open(local_path, 'wb') as file:
        file.write(file_content.decoded_content)

def fetch_files(contents):
    """Recursively fetch files and directories."""
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            # Recurse into directories
            contents.extend(repo.get_contents(file_content.path))
        elif file_content.name.endswith('.lean'):  # Fetching only .lean files
            #print_file_content(file_content)
            #save_file(file_content)
            lean_files.append(file_content)

# Start fetching files from the root of the repository
# fetch_files(repo.get_contents(""))

# # # Extract code blocks from Python files
# code_blocks = []
# counter = 0
# for file in lean_files:
#     content = file.decoded_content.decode()
#     # Use regex or parser to extract code blocks
#     print(content)
#     encoded_input = tokenizer(content)
#     print(encoded_input)
#     counter = counter + 1
#     if counter == 5:
#         break


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def create_pairs(unrefactored_dir, refactored_dir):
    pairs = []
    # Ensure both directories list the same files
    unrefactored_files = set(os.listdir(unrefactored_dir))
    refactored_files = set(os.listdir(refactored_dir))
    
    if unrefactored_files != refactored_files:
        raise ValueError("Mismatched files in directories.")
    
    for filename in unrefactored_files:
        unrefactored_path = os.path.join(unrefactored_dir, filename)
        refactored_path = os.path.join(refactored_dir, filename)
        
        unrefactored_code = read_file(unrefactored_path)
        refactored_code = read_file(refactored_path)
        
        pairs.append((unrefactored_code, refactored_code))
    
    return pairs