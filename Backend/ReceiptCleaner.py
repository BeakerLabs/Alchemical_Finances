#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

# Function of this script is to clean your Receipt Repository and Database. Removing files that are not referenced
# in the database and vice versa. This script may in the future be upgraded to allow users to delete/archive older receipts
# to free up space on their system. For now it just cleans up gaps.


import os
import sys

if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")


