from healer import execute_self_healing_code_system


# Test Function 1: List Processing
def process_list(lst, index):
    return lst[index] * 2


# Test Function 2: String Parsing
def parse_date(date_string):
    year, month, day = date_string.split("-")
    return {"year": int(year), "month": int(month), "day": int(day)}


# Original division function
def divide_two_numbers(a, b):
    return a / b


def test_division_function():
    print("*******************************")
    print("*******************************")
    print("** Testing Division Function **")
    print("*******************************")
    print("*******************************")
    execute_self_healing_code_system(divide_two_numbers, [10, 0])
    execute_self_healing_code_system(divide_two_numbers, ["a", 0])


def test_list_processing():
    print("**************************************")
    print("**************************************")
    print("** Testing List Processing Function **")
    print("**************************************")
    print("**************************************")
    # Test 1: Index out of range
    execute_self_healing_code_system(process_list, [[1, 2, 3], 5])
    # Test 2: Invalid input type
    execute_self_healing_code_system(process_list, [None, 1])


def test_date_parsing():
    print("***********************************")
    print("***********************************")
    print("** Testing Date Parsing Function **")
    print("***********************************")
    print("***********************************")
    # Test 1: Invalid format
    execute_self_healing_code_system(parse_date, ["2024/01/01"])
    # Test 2: Invalid data types
    execute_self_healing_code_system(parse_date, ["abc-def-ghi"])


if __name__ == "__main__":
    test_division_function()
    test_list_processing()
    test_date_parsing()
