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

print(content)

content = "   "+content+"    "
content = content.replace(" ", "   ")
content = content.replace("\t", "\t\t\t")
content = content.replace("\n","\n\n\n")

rx = r"([ \t\n]HAI[ \t\n]|[ \t\n]KTHXBYE[ \t\n]|[ \t\n]BTW.*[ \t\n]|[ \t\n]OBTW[\n\r\w\W]*TLDR[ \t\n]|[ \t\n]I[ \t]+HAS[ \t]+A[ \t\n]|[ \t\n]ITZ[ \t\n]|[ \t\n]R[ \t\n]|[ \t\n]SUM[ \t]+OF[ \t\n]|[ \t\n]DIFF[ \t]+OF[ \t\n]|[ \t\n]PRODUKT[ \t]+OF[ \t\n]|[ \t\n]QUOSHUNT[ \t]+OF[ \t\n]|[ \t\n]MOD[ \t]+OF[ \t\n]|[ \t\n]BIGGR[ \t]+OF[ \t\n]|[ \t\n]SMALLR[ \t]+OF[ \t\n]|[ \t\n]BOTH[ \t]+OF[ \t\n]|[ \t\n]EITHER[ \t]+OF[ \t\n]|[ \t\n]WON[ \t]+OF[ \t\n]|[ \t\n]NOT[ \t\n]|[ \t\n]ANY[ \t]+OF[ \t\n]|[ \t\n]ALL[ \t]+OF[ \t\n]|[ \t\n]BOTH[ \t]+SAEM[ \t\n]|[ \t\n]DIFFRINT[ \t\n]|[ \t\n]SMOOSH[ \t\n]|[ \t\n]MAEK[ \t\n]|[ \t\n]A[ \t\n]|[ \t\n]IS[ \t]+NOW[ \t]+A[ \t\n]|[ \t\n]VISIBLE[ \t\n]|[ \t\n]GIMMEH[ \t\n]|[ \t\n]O[ \t]+RLY\?[ \t\n]|[ \t\n]YA[ \t]+RLY[ \t\n]|[ \t\n]MEBBE[ \t\n]|[ \t\n]NO[ \t]+WAI[ \t\n]|[ \t\n]OIC[ \t\n]|[ \t\n]WTF\?[ \t\n]|[ \t\n]OMG[ \t\n]|[ \t\n]OMGWTF[ \t\n]|[ \t\n]IM[ \t]+IN[ \t]+YR[ \t\n]|[ \t\n]UPPIN[ \t\n]|[ \t\n]NERFIN[ \t\n]|[ \t\n]YR[ \t\n]|[ \t\n]TIL[ \t\n]|[ \t\n]WILE[ \t\n]|[ \t\n]IM[ \t]+OUTTA[ \t]+YR[ \t\n]|[ \t\n]GTFO[ \t\n])|([ \t\n]-?[0-9]+[ \t\n]|^-?[0-9]+[ \t\n]|[ \t\n]-?[0-9]+$|^-?[0-9]+$|[ \t\n]-?[0-9]*\.[0-9]+[ \t\n]|^-?[0-9]*\.[0-9]+[ \t\n]|[ \t\n]-?[0-9]*\.[0-9]+$|^-?[0-9]*\.[0-9]+$|\"[^\"\n]*\"|^WIN[ \t\n]|[ \t\n]WIN[ \t\n]|[ \t\n]WIN$|^WIN$|^FAIL[ \t\n]|[ \t\n]FAIL[ \t\n]|[ \t\n]FAIL$|^FAIL$)|(^[a-zA-Z]\w*[ \t\n]|[ \t\n][a-zA-Z]\w*[ \t\n]|[ \t\n][a-zA-Z]\w*$|^[a-zA-Z]\w*$)|([^ \t\n]+)"
#(keywords)|(literals)|(identifiers)|(errors)

#print(content)
print()
lexemes = []
declaredIdentifiers = []
declaredIdentifiersType = []
results = re.findall(rx, content)
error = "NONE"

for i in results:
    comment = False
    if (i[0]):
        kw = i[0]
        while (kw[0] == " " or kw[0] == "\t" or kw[0] == "\n"):
            kw = kw[1:]
        while (kw[len(kw)-1] == " " or kw[len(kw)-1] == "\t" or kw[len(kw)-1] == "\n"):
            kw = kw[:-1]

        kw = ' '.join(kw.split())

        if (kw == "HAI" or kw == "KTHXBYE"):    lexemes.append(["Code Delimeter",kw])
        elif (kw[0:3] == "BTW"):
            lexemes.append(["Single Comment Keyword",kw[0:3]])
            lexemes.append(["Comment",kw[4:]])
        elif (kw[0:4] == "OBTW" and kw[-4:] == "TLDR"):
            lexemes.append(["Multiple Comment Delimiter", "OBTW"])
            lexemes.append(["Multiple Comment", kw[5:-5]])
            lexemes.append(["Multiple Comment Delimiter", "TLDR"])
        elif (kw == "I HAS A"):                 lexemes.append(["Variable Declaration",kw])
        elif (kw == "ITZ"):                     lexemes.append(["Variable Assignment",kw])
        elif (kw == "R"):                       lexemes.append(["Assignment Keyword",kw])
        elif (kw == "SUM OF"):                  lexemes.append(["Arithmetic Operation",kw])
        elif (kw == "DIFF OF"):                 lexemes.append(["Arithmetic Operation",kw])
        elif (kw == "PRODUKT OF"):              lexemes.append(["Arithmetic Operation",kw])
        elif (kw == "QUOSHUNT OF"):             lexemes.append(["Arithmetic Operation",kw])
        elif (kw == "MOD OF"):                  lexemes.append(["Arithmetic Operation",kw])
        elif (kw == "BIGGR OF"):                lexemes.append(["Arithmetic Operation",kw])
        elif (kw == "SMALLR OF"):               lexemes.append(["Arithmetic Operation",kw])
        elif (kw == "BOTH OF"):                 lexemes.append(["Boolean Operation",kw])
        elif (kw == "EITHER OF"):               lexemes.append(["Boolean Operation",kw])
        elif (kw == "WON OF"):                  lexemes.append(["Boolean Operation",kw])
        elif (kw == "NOT"):                     lexemes.append(["Boolean Operation",kw])
        elif (kw == "ANY OF"):                  lexemes.append(["Boolean Operation",kw])
        elif (kw == "ALL OF"):                  lexemes.append(["Boolean Operation",kw])
        elif (kw == "BOTH SAEM"):               lexemes.append(["Comparison Operation",kw])
        elif (kw == "DIFFRINT"):                lexemes.append(["Comparison Operation",kw])
        elif (kw == "SMOOSH"):                  lexemes.append(["Concatenation Keyword",kw])
        elif (kw == "MAEK"):                    lexemes.append(["Typecast Keyword",kw])
        elif (kw == "A"):                       lexemes.append(["Typecast Noise Word",kw])
        elif (kw == "IS NOW A"):                lexemes.append(["Typecast Keyword",kw])
        elif (kw == "VISIBLE"):                 lexemes.append(["Output Keyword",kw])
        elif (kw == "GIMMEH"):                  lexemes.append(["Input Keyword",kw])
        elif (kw == "O RLY?"):                  lexemes.append(["If-Then Delimeter",kw])
        elif (kw == "YA RLY"):                  lexemes.append(["If Keyword",kw])
        elif (kw == "MEBBE"):                   lexemes.append(["Else If Keyword",kw])
        elif (kw == "NO WAI"):                  lexemes.append(["Else Keyword",kw])
        elif (kw == "OIC"):                     lexemes.append(["Conditional Delimeter",kw])
        elif (kw == "WTF?"):                    lexemes.append(["Switch-Case Delimeter",kw])
        elif (kw == "OMG"):                     lexemes.append(["Case Keyword",kw])
        elif (kw == "OMGWTF"):                  lexemes.append(["Default Case Keyword",kw])
        elif (kw == "IM IN YR"):                lexemes.append(["Loop Delimeter",kw])
        elif (kw == "UPPIN"):                   lexemes.append(["Loop Operation",kw])
        elif (kw == "NERFIN"):                  lexemes.append(["Loop Operation",kw])
        elif (kw == "YR"):                      lexemes.append(["Loop Keyword",kw])
        elif (kw == "TIL"):                     lexemes.append(["Loop Condition",kw])
        elif (kw == "WILE"):                    lexemes.append(["Loop Condition",kw])
        elif (kw == "IM OUTTA YR"):             lexemes.append(["Loop Delimeter",kw])
        elif (kw == "GTFO"):                    lexemes.append(["Break Keyword",kw])
        #more keywords
        else:                                   lexemes.append(["KEYWORD",kw])
    elif (i[1]):
        lit = i[1]
        while (lit[0] == " " or lit[0] == "\t" or lit[0] == "\n"):
            lit = lit[1:]
        while (lit[len(lit)-1] == " " or lit[len(lit)-1] == "\t" or lit[len(lit)-1] == "\n"):
            lit = lit[:-1]

        if (is_integer(lit)):
            lexemes.append(["NUMBR Literal",lit])
        elif (is_float(lit)):
            lexemes.append(["NUMBAR Literal",lit])
        elif (lit == "WIN" or lit == "FAIL"):
            lexemes.append(["TROOF Literal",lit])
        else:
            lexemes.append(["String Delimiter", "\""])
            lexemes.append(["YARN Literal", (lit)[1:-1].replace("   ", " ").replace("\t\t\t","\t") ]) # removing double quotes
            lexemes.append(["String Delimiter", "\""])
    elif (i[2]):
        ident = i[2]
        while (ident[0] == " " or ident[0] == "\t" or ident[0] == "\n"):
            ident = ident[1:]
        while (ident[len(ident)-1] == " " or ident[len(ident)-1] == "\t" or ident[len(ident)-1] == "\n"):
            ident = ident[:-1]

        if (ident in declaredIdentifiers):
            index = declaredIdentifiers.index(ident)
            lexemes.append([declaredIdentifiersType[index],ident])
        else:
            if (len(lexemes) != 0):
                previousLexeme = lexemes[len(lexemes)-1][1]
                declaredIdentifiers.append(ident)
                if (previousLexeme == "I HAS A"):       
                    lexemes.append(["Variable Identifier",ident])
                    declaredIdentifiersType.append("Variable Identifier")
                elif (previousLexeme == "IM IN YR"):
                    lexemes.append(["Loop Identifier",ident])
                    declaredIdentifiersType.append("Loop Identifier")
                #one more for loop identifier func identifier
                else:
                    lexemes.append(["IDENTIFIER",ident])
                    declaredIdentifiersType.append("IDENTIFIER")
            else:
                lexemes.append(["IDENTIFIER",ident])
                declaredIdentifiersType.append("IDENTIFIER")
    else:
        error = i[3].replace(" ","").replace("\t","").replace("\n","")
        break


for i in lexemes:
   print(i[0].ljust(27," ")+":\t"+i[1])
if (error != "NONE"):
    print("INTERRUPT!\nERROR: "+error)
else:
    print("\nANALYSIS COMPLETE!")

#print(results)
