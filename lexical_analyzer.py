import re

fileHandle = open("sample.lol","r")
content = fileHandle.read()
fileHandle.close()

rx = r"(\bHAI\b|\bKTHXBYE\b|\bBTW\b|\bOBTW\b|\bTLDR\b|\bI HAS A\b|\bITZ\b|\bR\b|\bSUM OF\b|\bDIFF OF\b|\bPRODUKT OF\b|\bQUOSHUNT OF\b|\bMOD OF\b|\bBIGGR OF\b|\bSMALLR OF\b|\bBOTH OF\b|\bEITHER OF\b|\bWON OF\b|\bNOT\b|\bANY OF\b|\bALL OF\b|\bBOTH SAEM\b|\bDIFFRINT\b|\bSMOOSH\b|\bMAEK\b|\bA\b|\bIS NOW A\b|\bVISIBLE\b|\bGIMMEH\b|\bO RLY\?\B|\bMEBBE\b|\bNO WAI\b|\bOIC\b|\bWTF\?\B|\bOMG\b|\bOMGWTF\b|\bIM IN YR\b|\bUPPIN\b|\bNERFIN\b|\bYR\b|\bTIL\b|\bWILE\b|\bIM OUTTA YR\b)|(\B\.[0-9]+\b|\b[0-9]+\.[0-9]+\b|\B-[0-9]*\.[0-9]+\b|\b[0-9]+\b|\B-[0-9]+\b|\".*\")|(\b[a-zA-Z]\w*\b)"
#(keywords)|(literals)|(identifiers)

print(content)
print()
lexemes = []
declaredIdentifiers = []
declaredIdentifiersType = []
results = re.findall(rx, content)

for i in results:
    if (i[0]):
        kw = i[0]
        if (kw == "HAI" or kw == "KTHXBYE"):    lexemes.append(["Code Delimeter",i[0]])
        elif (kw == "I HAS A"):                 lexemes.append(["Variable Declaration",i[0]])
        elif (kw == "ITZ"):                     lexemes.append(["Variable Assignment",i[0]])
        elif (kw == "VISIBLE"):                 lexemes.append(["Output Keyword",i[0]])
        #more keywords
        else:                                   lexemes.append(["KEYWORD",i[0]])
    elif (i[1]):
        lexemes.append(["LITERAL",i[1]])
    elif (i[2]):
        if (i[2] in declaredIdentifiers):
            index = declaredIdentifiers.index(i[2])
            lexemes.append([declaredIdentifiersType[index],i[2]])
        else:
            previousLexeme = lexemes[len(lexemes)-1][1]
            declaredIdentifiers.append(i[2])
            if (previousLexeme == "I HAS A"):       
                lexemes.append(["Variable Identifier",i[2]])
                declaredIdentifiersType.append("Variable Identifier")
            #one more for loop identifier (also func identifier)
            else:
                lexemes.append(["IDENTIFIER",i[2]])
                declaredIdentifiersType.append("IDENTIFIER")

for i in lexemes:
    print(i[0].ljust(22," ")+":\t"+i[1])
