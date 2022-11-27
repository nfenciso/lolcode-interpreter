

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

he = "223"

print(float(False))