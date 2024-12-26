import sys
import subprocess
import os
from pathlib import Path
import time
import pickle
current_dir = Path(__file__).resolve().parent
# Save the first argument as the output file
tmp_file = sys.argv[1]
# The rest are the command and its arguments
command = sys.argv[2:]
# Execute the command
result = subprocess.run(command)

data_to_save = {
    'returncode': result.returncode,
    'stdout': result.stdout,
    'stderr': result.stderr,
    'args':result.args
}


with open(f"{tmp_file}.done", 'wb')as file:
    pickle.dump(data_to_save, file)

os.remove(tmp_file)
time.sleep(1)


