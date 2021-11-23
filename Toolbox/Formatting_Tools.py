#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import secrets


# --- miscellaneous
def add_comma(value, number: int):
    """
    Function made to add a comma for a monetary value.
    yes I learned later about "Common string operations"

    :param value: monetary value of interest
    :param number: number of decimal places
    :return: str
    """
    if value is None:
        value = 0.0
    if value < 0:
        num = 1
    else:  # value >= 0:
        num = 0

    value_as_string = str(value)
    split_value = value_as_string.split('.')

    try:
        split_value[1]
    except IndexError:
        split_value.append("00")

    qty_change_units = len(split_value[1])
    if qty_change_units > number:
        reduce_by = qty_change_units - number
        modified_change = split_value[1][:(qty_change_units - reduce_by)]
        new_value = split_value[0] + modified_change
    elif qty_change_units < number:
        increase_by = number - qty_change_units
        new_units = str(10 ** increase_by)
        new_value = split_value[0] + split_value[1] + new_units[1:]
    else:
        new_value = split_value[0] + split_value[1]

    value_as_string = new_value[num:]
    number_of_digits = len(value_as_string)
    value_of_change = value_as_string[number_of_digits - number:]
    value_of_bills = value_as_string[: number_of_digits - number]
    if len(value_of_bills) == 0:
        value_of_bills = "0"

    inverse_bills = value_of_bills[::-1]
    final_value = ""
    count = 0
    for digit in inverse_bills:
        if count == 0:
            final_value += digit
            count += 1
        elif count % 3 != 0:
            final_value += digit
            count += 1
        elif count % 3 == 0:
            final_value += "," + digit
            count += 1
    final_value = final_value[::-1] + "." + value_of_change
    return final_value


def add_space(user_input: str):
    """
    Simple re-usable function to replace an underscore with a space
    :param user_input: string value
    :return: string value w spaces
    """
    modifiedvalue = ""
    for letter in user_input:
        if letter == "_":
            modifiedvalue += " "
        else:
            modifiedvalue += letter
    return modifiedvalue


def cash_format(value: float, deciplace: int):
    """
    takes float values and formats value for a ledger representation of money.

    :param value: raw float value
    :param deciplace: number of places after the decimal
    :return: list [wo comma, format]
    """
    if type(value) is not float:
        try:
            value = float(value)
        except ValueError:
            value = 0

    if value < 0:
        moneyWComma = add_comma(value, deciplace)
        moneyWOComma = "-" + remove_comma(moneyWComma)
        formatString = " ($  " + moneyWComma + ")"
        graphString = f"($ {moneyWComma})"
        moneylist = [moneyWOComma, formatString, graphString]
        return moneylist
    if value == 0:
        moneyWOComma = "0.00"
        formatString = "  $  -  "
        graphString = f"$ 0.00"
        moneylist = [moneyWOComma, formatString, graphString]
        return moneylist
    else:
        moneyWComma = add_comma(value, deciplace)
        moneyWOComma = remove_comma(moneyWComma)
        formatString = "  $  " + moneyWComma + " "
        graphString = f"$ {moneyWComma}"
        moneylist = [moneyWOComma, formatString, graphString]
        return moneylist


def decimal_places(value: str, number: int):
    """
    turns the string (of float) into a DECIMAL with a set number of decimal places

    :param value: string
    :param number: int
    :return: DECIMAL
    """
    from decimal import Decimal
    if value == "" or value == " ":
        value = round(Decimal(0.00), number)
        return value
    else:
        final = round(Decimal(value), number)
        return final


def gen_rand_str(length: int, letters=False, symbols=False):
    """
    Generates a randomized numeric Key - Not recommended for passwords
    """
    pos_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    pos_symbols = "~!@#$%^&*-"

    max_symbols = round(length/2)
    symbol_count = 0

    finalString = ""

    for num in range(0, length + 1, 1):
        option = secrets.randbelow(3)
        if option == 1 and letters is True:
            random_pos = secrets.randbelow(len(pos_letters))
            finalString += pos_letters[random_pos]
        elif option == 2 and symbols is True and symbol_count < max_symbols:
            random_pos = secrets.randbelow(len(pos_symbols))
            finalString += pos_symbols[random_pos]
            symbol_count += 1
        else:  # Option 0 and False for Letters and Symbols
            random_num = str(secrets.randbelow(10))
            finalString += random_num

    return finalString


def remove_comma(value: str):
    """
    Function to remove commas from monetary values. Allows conversion from string to int/float

    :param value: str
    :return: str
    """
    displayValue = ""
    for digit in value:
        if digit == ",":
            pass
        elif digit == "-":
            pass
        elif digit == ".":
            displayValue += digit
        else:
            displayValue += digit
    return displayValue


def remove_space(user_input: str):
    """
    Simple reusable function to replace a space with an underscore

    :param user_input: string value
    :return: string value w/o spaces
    """
    modifiedvalue = ""
    for letter in user_input:
        if letter == " ":
            modifiedvalue += "_"
        else:
            modifiedvalue += letter
    return modifiedvalue


def convert_to_float(datapoint):
    if type(datapoint) != float:
        try:
            datapoint = float(datapoint)
        except ValueError:
            datapoint = float(0)

    return datapoint


# --- Catchall --- #
if __name__ == '__main__':
    print("Error - Check your executable")
