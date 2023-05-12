import os
import re
import pkg_resources
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate a requirements.txt file by scanning Python scripts.')
parser.add_argument('rootdir', metavar='rootdir', type=str, nargs='?', default=os.getcwd(),
                    help='the directory to scan (defaults to current directory)')
args = parser.parse_args()

rootdir = args.rootdir  # the directory to scan
exclude_dirs = ['venv', '__pycache__', '.git']  # directories to exclude from scanning
packages = set()  # a set to hold the package names

for foldername, subfolders, filenames in os.walk(rootdir):
    # skip excluded directories
    if any(exclude in foldername for exclude in exclude_dirs):
        continue

    for filename in filenames:
        if filename.endswith('.py'):
            with open(os.path.join(foldername, filename), 'r') as f:
                content = f.read()
                # find 'import' and 'from ... import' statements
                matches = re.findall(r'(?:from\s+([a-zA-Z0-9_.]+)\s+import|import\s+([a-zA-Z0-9_.]+))', content)
                for match in matches:
                    # add the base package name (the part before the first dot, if any)
                    packages.add(match[0].split('.')[0] if match[0] else match[1].split('.')[0])

# filter out packages that are not installed in the current environment
installed_packages = {pkg.key for pkg in pkg_resources.working_set}
packages = packages.intersection(installed_packages)

# write the packages to the requirements.txt file
with open('requirements.txt', 'w') as f:
    for package in sorted(packages):
        f.write(f'{package}\n')
