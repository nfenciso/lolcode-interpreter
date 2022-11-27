

# dicta = {
#     "one": "sad",
#     "two": 12
# }

# # for i in dicta:
# #     if (isinstance(dicta[i], str)):
# #         print(f"{i.rjust(10)}: \"{dicta[i]}\"")
# #     else:
# #         print(f"{i.rjust(10)}: {dicta[i]}")

def check_string_to_int(value):
    try:
        int(value)
        return True
    except:
        return False

def check_string_to_float(value):
    try:
        float(value)
        return True
    except:
        return False

def count_elements(lst):
    count = 0

    return count

lst = ['BOTH OF', ['NUMBR Literal', '1'], ['BOTH OF', ['NUMBR Literal', '1'], ['NUMBR Literal', '2'], ''], '']

print(f"{lst.remove(['NUMBR Literal', '1'])}")


    