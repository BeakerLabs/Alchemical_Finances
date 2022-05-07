#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import pickle
import platform
import sys

from pathlib import Path


# --- OS Functions --- #
def file_destination(dir_name_lst=None, starting_point=None):
    """ Create desired directory or check for it's existence """
    if starting_point is None:
        starting_point = Path.cwd()

    if dir_name_lst is None:
        dir_name_lst = []

    if dir_name_lst[0] == "..":
        # Should I depreciate this? I dont' think I use a ".."
        current_dir = Path.cwd()
        current_dir = str(current_dir)
    else:
        current_dir = str(starting_point)

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


def obtain_storage_dir():
    """Determine, which operating system is in use. Then determine where to store software files

    :return -- user_pathway
    """
    operating_system = platform.system()

    if operating_system == "Windows":
        user_pathway = os.path.expanduser('~/Onedrive/documents')

        if os.path.isdir(user_pathway) is False:
            user_pathway = os.path.expanduser('~/documents')

        if os.path.isdir(user_pathway) is False:
            user_pathway = Path.cwd()

    else:
        user_pathway = Path.cwd()
        # Will need to return to this to develop for Mac and Linux

    return user_pathway


def obtain_screen_dimensions():
    user_pathway = obtain_storage_dir()
    screen_dimensions_path = file_destination(dir_name_lst=['Alchemical Finances', 'data', 'account'], starting_point=user_pathway)
    screen_dimensions_path = screen_dimensions_path + "dimensions.pkl"
    screen_dimensions_path = Path(screen_dimensions_path)

    screen_dimensions_file = open(screen_dimensions_path, "rb")
    screen_dimensions = pickle.load(screen_dimensions_file)
    screen_dimensions_file.close()
    return screen_dimensions, screen_dimensions_path


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")

