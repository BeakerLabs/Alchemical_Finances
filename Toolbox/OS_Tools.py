from pathlib import Path


# --- OS Functions --- #
def file_destination(dir_name_lst=None):
    """
    Create desired directory or check for it's existence

    :param dir_name_lst: Provide list of folders if current directory isn't desired endpoint
    :return: Returns string of the full pathway
    """
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
    file_path = gen_str_path + chr(92)

    return file_path


# --- Catchall --- #
if __name__ == '__main__':
    print("Error - Check your executable")
