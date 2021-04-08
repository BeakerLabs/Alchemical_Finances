def alpha_numeric_check(userValue: str):
    """
    Function used to ensure the input only has desired alphanumeric values.
    if false input fails.

    :param userValue: string
    :return: bool
    """
    validCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    letterCount = 0
    for letter in userValue:
        if letter.capitalize() in validCharacters:
            letterCount += 1
        else:
            pass
    if letterCount > 0:
        return True
    else:
        return False


def check_characters(question: str, focus="general"):
    """
    Checks user inputs for unwanted characters. Different input types have different restrictions.
    If false the string fails the check.

    :param question: the input string
    :param focus: the type of user input
    :return: bool
    """
    checkString = question
    x = 0
    focus_dic = {
        "login": ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "=", ":",
                  "+", "<", "?", ";", "'", "[", "]", "{", "}", '"', "-", ".", ",", "/", chr(92)],
        "general": ["~", "!", "@", "#", "$", "%", "^", "*", "(", ")", "=",
                    "+", "<", "?", ";", "[", "]", "{", "}", '"', chr(92)],
        "monetary": ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "=", ":",
                     "+", "<", "?", ";", "'", "[", "]", "{", "}", '"', "-", ",", "/", chr(92)],
    }

    badCharacters = focus_dic[focus]

    for piece in checkString:
        if piece in badCharacters:
            x += 1
        else:
            pass
    if x >= 1:
        return False
    if x == 0:
        return True


def check_numerical_inputs(userInput: str):
    """
    Simple function to check strings for float compatibility
    :param userInput: str
    :return: bool
    """
    try:
        float(userInput)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def find_character(userValue: str):
    """
    checks string to ensure alphanumeric value

    :param userValue: str
    :return: bool
    """
    validCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    letterCount = 0
    for letter in userValue:
        if letter.capitalize() in validCharacters:
            letterCount += 1
        else:
            pass
    if letterCount > 0:
        return True
    else:
        return False


def first_character_check(userValue: str):
    """
    Checks string to ensure it is a letter.
    if false input fails.

    :param userValue: string
    :return: bool
    """
    tableName = userValue
    validCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    try:
        if tableName[0].capitalize() in validCharacters:
            return True
        else:
            return False
    except IndexError:
        return False


def spacing_check(user_value: str):
    """
    Function designed to quickly check for unwanted blank spacers in a string.
    if false input fails.

    :param user_value: string value
    :return: bool
    """
    unverified = user_value
    for letter in unverified:
        if letter == " ":
            return False
        else:
            pass
    return True


# --- Catchall --- #
if __name__ == '__main__':
    print("Error - Check your executable")
