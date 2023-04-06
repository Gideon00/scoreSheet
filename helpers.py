

# Determine start
def get_start(n):
    if (n + 4) % 5 == 0:
        return n
    return 0

# Convert list to string
def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
           str1 += f"{ele}  ,"
    # return string
    return str1