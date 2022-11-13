import re

def is_integer(num):
    try:
        int(num) * -1
        return True
    except:
        return False

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

fileHandle = open("sample.lol","r")
content = fileHandle.read()
fileHandle.close()

rx = r"(\bHAI\b|\bKTHXBYE\b|\bBTW .*\b|OBTW[\n\r\w\W]*TLDR|\bI HAS A\b|\bITZ\b|\bR\b|\bSUM OF\b|\bDIFF OF\b|\bPRODUKT OF\b|\bQUOSHUNT OF\b|\bMOD OF\b|\bBIGGR OF\b|\bSMALLR OF\b|\bBOTH OF\b|\bEITHER OF\b|\bWON OF\b|\bNOT\b|\bANY OF\b|\bALL OF\b|\bBOTH SAEM\b|\bDIFFRINT\b|\bSMOOSH\b|\bMAEK\b|\bA\b|\bIS NOW A\b|\bVISIBLE\b|\bGIMMEH\b|\bO RLY\?\B|\bYA RLY\b|\bMEBBE\b|\bNO WAI\b|\bOIC\b|\bWTF\?\B|\bOMG\b|\bOMGWTF\b|\bIM IN YR\b|\bUPPIN\b|\bNERFIN\b|\bYR\b|\bTIL\b|\bWILE\b|\bIM OUTTA YR\b)|(\B\.[0-9]+\b|\b[0-9]+\.[0-9]+\b|\B-[0-9]*\.[0-9]+\b|\b[0-9]+\b|\B-[0-9]+\b|\".*\"|\bWIN\b|\bFAIL\b)|(\b[a-zA-Z]\w*\b)"#|(\b.*\b)"
#(keywords)|(literals)|(identifiers)

print(content)
print()
lexemes = []
declaredIdentifiers = []
declaredIdentifiersType = []
results = re.findall(rx, content)

for i in results:
    comment = False
    if (i[0]):
        kw = i[0]
        if (kw == "HAI" or kw == "KTHXBYE"):    lexemes.append(["Code Delimeter",i[0]])
        elif (kw[0:3] == "BTW"):
            lexemes.append(["Single Comment Keyword",kw[0:3]])
            lexemes.append(["Comment",kw[4:]])
        elif (kw[0:4] == "OBTW" and kw[-4:] == "TLDR"):
            lexemes.append(["Multiple Comment Delimiter", "OBTW"])
            lexemes.append(["Multiple Comment", kw[5:-5]])
            lexemes.append(["Multiple Comment Delimiter", "TLDR"])
        # elif (kw == "OBTW"):                    lexemes.append(["comment multiline",i[0]])
        # elif (kw == "TLDR"):                    lexemes.append(["... ",i[0]])
        elif (kw == "I HAS A"):                 lexemes.append(["Variable Declaration",i[0]])
        elif (kw == "ITZ"):                     lexemes.append(["Variable Assignment",i[0]])
        elif (kw == "R"):                       lexemes.append([".... ",i[0]])
        elif (kw == "SUM OF"):                  lexemes.append([".... ",i[0]])
        elif (kw == "DIFF OF"):                 lexemes.append([".... ",i[0]])
        elif (kw == "PRODUKT OF"):              lexemes.append([".... ",i[0]])
        elif (kw == "QUOSHUNT OF"):             lexemes.append([".... ",i[0]])
        elif (kw == "MOD OF"):                  lexemes.append([".... ",i[0]])
        elif (kw == "BIGGR OF"):                lexemes.append([".... ",i[0]])
        elif (kw == "SMALLR OF"):               lexemes.append([".... ",i[0]])
        elif (kw == "BOTH OF"):                 lexemes.append([".... ",i[0]])
        elif (kw == "EITHER OF"):               lexemes.append([".... ",i[0]])
        elif (kw == "WON OF"):                  lexemes.append([".... ",i[0]])
        elif (kw == "NOT"):                     lexemes.append([".... ",i[0]])
        elif (kw == "ANY OF"):                  lexemes.append([".... ",i[0]])
        elif (kw == "ALL OF"):                  lexemes.append([".... ",i[0]])
        elif (kw == "BOTH SAEM"):               lexemes.append([".... ",i[0]])
        elif (kw == "DIFFRINT"):                lexemes.append([".... ",i[0]])
        elif (kw == "SMOOSH"):                  lexemes.append([".... ",i[0]])
        elif (kw == "MAEK"):                    lexemes.append([".... ",i[0]])
        elif (kw == "A"):                       lexemes.append([".... ",i[0]])
        elif (kw == "IS NOW A"):                lexemes.append([".... ",i[0]])
        elif (kw == "VISIBLE"):                 lexemes.append(["Output Keyword",i[0]])
        elif (kw == "GIMMEH"):                  lexemes.append([".... ",i[0]])
        elif (kw == "O RLY?"):                  lexemes.append([".... ",i[0]])
        elif (kw == "YA RLY"):                  lexemes.append([".... ",i[0]])
        elif (kw == "MEBBE"):                   lexemes.append([".... ",i[0]])
        elif (kw == "NO WAI"):                  lexemes.append([".... ",i[0]])
        elif (kw == "OIC"):                     lexemes.append([".... ",i[0]])
        elif (kw == "WTF?"):                    lexemes.append([".... ",i[0]])
        elif (kw == "OMG"):                     lexemes.append([".... ",i[0]])
        elif (kw == "OMGWTF"):                  lexemes.append([".... ",i[0]])
        elif (kw == "IM IN YR"):                lexemes.append([".... ",i[0]])
        elif (kw == "UPPIN"):                   lexemes.append([".... ",i[0]])
        elif (kw == "NERFIN"):                  lexemes.append([".... ",i[0]])
        elif (kw == "YR"):                      lexemes.append([".... ",i[0]])
        elif (kw == "TIL"):                     lexemes.append([".... ",i[0]])
        elif (kw == "WILE"):                    lexemes.append([".... ",i[0]])
        elif (kw == "IM OUTTA YR"):             lexemes.append([".... ",i[0]])
        #more keywords
        else:                                   lexemes.append(["KEYWORD",i[0]])
    elif (i[1]):
        if (i[1].isnumeric()):
            lexemes.append(["NUMBR Literal",i[1]])
        elif (is_integer(i[1])):
            lexemes.append(["signed NUMBR Literal",i[1]])
        elif (is_float(i[1])):
            lexemes.append(["NUMBAR Literal",i[1]])
        elif (i[1] == "WIN" or i[1] == "FAIL"):
            lexemes.append(["TROOF Literal",i[1]])
        else:
            lexemes.append(["String Delimiter", "\""])
            lexemes.append(["YARN Literal",(i[1])[1:-1]]) # removing double quotes
            lexemes.append(["String Delimiter", "\""])


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
    # else:
    #     print("->", i[3])
        # bug found: when adding .*   , seems that the sequence in regex is broken 

for i in lexemes:
    print(i[0].ljust(22," ")+":\t"+i[1])
