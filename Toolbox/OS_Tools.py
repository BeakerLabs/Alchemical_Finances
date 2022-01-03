#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
from pathlib import Path
import sys


# --- OS Functions --- #
def file_destination(dir_name_lst=None):
    """ Create desired directory or check for it's existence """
    if dir_name_lst is None:
        dir_name_lst = []

    if dir_name_lst[0] == "..":
        current_dir = ".." / Path.cwd()
        current_dir = str(current_dir)
    else:
        current_dir = str(Path.cwd())

    gen_str_path = current_dir

    if len(dir_name_lst) > 0:
        for name in dir_name_lst:
            gen_str_path += chr(92) + str(name)
            # chr(92) == /

    dir_path = Path(gen_str_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    os.chmod(dir_path, 0o777)
    file_path = gen_str_path + chr(92)

    return file_path


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")

