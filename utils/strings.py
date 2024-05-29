# Check if a number passed is positive.
def is_positive_number(value):

    # Check if the value passed is a boolean
    # Used to avoid returning True when call float(True)
    # python float() method return 1.0 to float(True)
    if isinstance(value, bool):
        return False

    # Try to convert the value into float.
    try:
        number_string = float(value)

    # If raise ValueError, return False
    # #It was not a number
    except ValueError:
        return False

    # Check if the number generated in the float() method is
    # more than 0
    return number_string > 0
