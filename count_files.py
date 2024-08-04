""" Counts the number of lines for all files of specific extensions within 
folders in the same directory as this program.
 2024.08.01
"""

__author__ = "Liam Anthian"

# --- Imports ---
import subprocess


# For each extension
EXTENSIONS = ['\\.py', '\\.java', '\\.c', '\\.h', '\\.ipynb']
WINDOWS = True

wsl = "wsl " if WINDOWS else ""

# Find all files in this directory
# Sourced from https://stackoverflow.com/a/54931757, by gkimsey
proc = subprocess.Popen(wsl + "ls", shell=True, stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE)
out, _ = proc.communicate()

# Get repositories
reps = out.decode().strip().split('\n')
this_file = __file__.split('\\')[-1]
reps.remove(this_file)
print(reps)

tallies = {}

# For each file type, summing across repositories
for ex in EXTENSIONS:
    tally = 0
    for dir in reps:
        command = "cd %s & git ls-files | %sgrep %s | %sxargs wc -l" % (dir, wsl, ex, wsl)

        proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, _ = proc.communicate()
        outcome = out.decode().strip()

        # Extract total count and add to tally for file extension lines
        num = outcome.split('\n')[-1].strip().split(" ")[0]
        tally += int(num)

    # Store line count
    tallies[ex] = tally

print(tallies)
