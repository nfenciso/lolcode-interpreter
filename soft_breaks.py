import re

content = 'HAI\n\tI HAS A var,55\n\t"Hello, World!"\nKTHXBYE'
newContent = ''
rxSoftBreak = r"(\".*,.*\")|(,)|([\w\W \t\n])"



results = re.findall(rxSoftBreak, content)
for i in results:
    if (i[1]):
        newContent += "\n"
    elif (i[0]):
        newContent += i[0]
    elif (i[2]):
        newContent += i[2]

print(content)
print(results)
print(newContent)