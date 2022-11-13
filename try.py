def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def is_integer(num):
    try:
        int(num) * -1
        return True
    except:
        return False
x = "OBTW ajkwndakwn awlkndka TLDR"
# if(d):
#     print("hey")

print(len(x)) 
print(x[5:-5]) 