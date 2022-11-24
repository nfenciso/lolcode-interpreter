# CMSC124 B-1L
# Lexical Analyzer
# CONTRIBUTORS:
#   John Kenneth F. Manalang
#   Nathaniel F. Enciso

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

rx = r"([ \t]TROOF[ \t]|[ \t]YARN[ \t]|[ \t]NUMBR[ \t]|[ \t]NUMBAR[ \t]|[ \t]HAI[ \t]|[ \t]KTHXBYE[ \t]|[ \t]BTW.*[ \t]|[ \t]OBTW[\r\w\W]*TLDR[ \t]|[ \t]I[ \t]+HAS[ \t]+A[ \t]|[ \t]ITZ[ \t]|[ \t]R[ \t]|[ \t]SUM[ \t]+OF[ \t]|[ \t]DIFF[ \t]+OF[ \t]|[ \t]PRODUKT[ \t]+OF[ \t]|[ \t]QUOSHUNT[ \t]+OF[ \t]|[ \t]MOD[ \t]+OF[ \t]|[ \t]BIGGR[ \t]+OF[ \t]|[ \t]SMALLR[ \t]+OF[ \t]|[ \t]BOTH[ \t]+OF[ \t]|[ \t]EITHER[ \t]+OF[ \t]|[ \t]WON[ \t]+OF[ \t]|[ \t]NOT[ \t]|[ \t]ANY[ \t]+OF[ \t]|[ \t]ALL[ \t]+OF[ \t]|[ \t]BOTH[ \t]+SAEM[ \t]|[ \t]DIFFRINT[ \t]|[ \t]SMOOSH.*[ \t]|[ \t]MAEK[ \t]|[ \t]A[ \t]|[ \t]IS[ \t]+NOW[ \t]+A[ \t]|[ \t]VISIBLE.*[ \t]|[ \t]GIMMEH[ \t]|[ \t]O[ \t]+RLY\?[ \t]|[ \t]YA[ \t]+RLY[ \t]|[ \t]MEBBE[ \t]|[ \t]NO[ \t]+WAI[ \t]|[ \t]OIC[ \t]|[ \t]WTF\?[ \t]|[ \t]OMG[ \t]|[ \t]OMGWTF[ \t]|[ \t]IM[ \t]+IN[ \t]+YR[ \t]|[ \t]UPPIN[ \t]|[ \t]NERFIN[ \t]|[ \t]YR[ \t]|[ \t]TIL[ \t]|[ \t]WILE[ \t]|[ \t]IM[ \t]+OUTTA[ \t]+YR[ \t]|[ \t]GTFO[ \t]|[ \t]AN[ \t]|[ \t]HOW[ \t]+IZ[ \t]+I[ \t]|[ \t]IF[ \t]+U[ \t]+SAY[ \t]+SO[ \t]|[ \t]I[ \t]+IZ[ \t]|[ \t]MKAY[ \t])|([ \t]-?[0-9]+[ \t]|[ \t]-?[0-9]*\.[0-9]+[ \t]|\"[^\"]*\"|[ \t]WIN[ \t]|[ \t]FAIL[ \t])|([ \t][a-zA-Z]\w*[ \t])|([\n]+)|([^ \t]+)"
rxVisible = r"([ \t]TROOF[ \t]|[ \t]YARN[ \t]|[ \t]NUMBR[ \t]|[ \t]NUMBAR[ \t]|[ \t]HAI[ \t]|[ \t]KTHXBYE[ \t]|[ \t]BTW.*[ \t]|[ \t]OBTW[\r\w\W]*TLDR[ \t]|[ \t]I[ \t]+HAS[ \t]+A[ \t]|[ \t]ITZ[ \t]|[ \t]R[ \t]|[ \t]SUM[ \t]+OF[ \t]|[ \t]DIFF[ \t]+OF[ \t]|[ \t]PRODUKT[ \t]+OF[ \t]|[ \t]QUOSHUNT[ \t]+OF[ \t]|[ \t]MOD[ \t]+OF[ \t]|[ \t]BIGGR[ \t]+OF[ \t]|[ \t]SMALLR[ \t]+OF[ \t]|[ \t]BOTH[ \t]+OF[ \t]|[ \t]EITHER[ \t]+OF[ \t]|[ \t]WON[ \t]+OF[ \t]|[ \t]NOT[ \t]|[ \t]ANY[ \t]+OF[ \t]|[ \t]ALL[ \t]+OF[ \t]|[ \t]BOTH[ \t]+SAEM[ \t]|[ \t]DIFFRINT[ \t]|[ \t]SMOOSH.*[ \t]|[ \t]MAEK[ \t]|[ \t]A[ \t]|[ \t]IS[ \t]+NOW[ \t]+A[ \t]|[ \t]VISIBLE[ \t]|[ \t]GIMMEH[ \t]|[ \t]O[ \t]+RLY\?[ \t]|[ \t]YA[ \t]+RLY[ \t]|[ \t]MEBBE[ \t]|[ \t]NO[ \t]+WAI[ \t]|[ \t]OIC[ \t]|[ \t]WTF\?[ \t]|[ \t]OMG[ \t]|[ \t]OMGWTF[ \t]|[ \t]IM[ \t]+IN[ \t]+YR[ \t]|[ \t]UPPIN[ \t]|[ \t]NERFIN[ \t]|[ \t]YR[ \t]|[ \t]TIL[ \t]|[ \t]WILE[ \t]|[ \t]IM[ \t]+OUTTA[ \t]+YR[ \t]|[ \t]GTFO[ \t]|[ \t]AN[ \t]|[ \t]HOW[ \t]+IZ[ \t]+I[ \t]|[ \t]IF[ \t]+U[ \t]+SAY[ \t]+SO[ \t]|[ \t]I[ \t]+IZ[ \t]|[ \t]MKAY[ \t])|([ \t]-?[0-9]+[ \t]|[ \t]-?[0-9]*\.[0-9]+[ \t]|\"[^\"]*\"|[ \t]WIN[ \t]|[ \t]FAIL[ \t])|([ \t][a-zA-Z]\w*[ \t])|([\n]+)|([^ \t\n]+)"
rxSmoosh = r"([ \t]TROOF[ \t]|[ \t]YARN[ \t]|[ \t]NUMBR[ \t]|[ \t]NUMBAR[ \t]|[ \t]HAI[ \t]|[ \t]KTHXBYE[ \t]|[ \t]BTW.*[ \t]|[ \t]OBTW[\r\w\W]*TLDR[ \t]|[ \t]I[ \t]+HAS[ \t]+A[ \t]|[ \t]ITZ[ \t]|[ \t]R[ \t]|[ \t]SUM[ \t]+OF[ \t]|[ \t]DIFF[ \t]+OF[ \t]|[ \t]PRODUKT[ \t]+OF[ \t]|[ \t]QUOSHUNT[ \t]+OF[ \t]|[ \t]MOD[ \t]+OF[ \t]|[ \t]BIGGR[ \t]+OF[ \t]|[ \t]SMALLR[ \t]+OF[ \t]|[ \t]BOTH[ \t]+OF[ \t]|[ \t]EITHER[ \t]+OF[ \t]|[ \t]WON[ \t]+OF[ \t]|[ \t]NOT[ \t]|[ \t]ANY[ \t]+OF[ \t]|[ \t]ALL[ \t]+OF[ \t]|[ \t]BOTH[ \t]+SAEM[ \t]|[ \t]DIFFRINT[ \t]|[ \t]SMOOSH[ \t]|[ \t]MAEK[ \t]|[ \t]A[ \t]|[ \t]IS[ \t]+NOW[ \t]+A[ \t]|[ \t]VISIBLE.*[ \t]|[ \t]GIMMEH[ \t]|[ \t]O[ \t]+RLY\?[ \t]|[ \t]YA[ \t]+RLY[ \t]|[ \t]MEBBE[ \t]|[ \t]NO[ \t]+WAI[ \t]|[ \t]OIC[ \t]|[ \t]WTF\?[ \t]|[ \t]OMG[ \t]|[ \t]OMGWTF[ \t]|[ \t]IM[ \t]+IN[ \t]+YR[ \t]|[ \t]UPPIN[ \t]|[ \t]NERFIN[ \t]|[ \t]YR[ \t]|[ \t]TIL[ \t]|[ \t]WILE[ \t]|[ \t]IM[ \t]+OUTTA[ \t]+YR[ \t]|[ \t]GTFO[ \t]|[ \t]AN[ \t]|[ \t]HOW[ \t]+IZ[ \t]+I[ \t]|[ \t]IF[ \t]+U[ \t]+SAY[ \t]+SO[ \t]|[ \t]I[ \t]+IZ[ \t]|[ \t]MKAY[ \t])|([ \t]-?[0-9]+[ \t]|[ \t]-?[0-9]*\.[0-9]+[ \t]|\"[^\"]*\"|[ \t]WIN[ \t]|[ \t]FAIL[ \t])|([ \t][a-zA-Z]\w*[ \t])|([\n]+)|([^ \t]+)"
#(keywords)|(literals)|(identifiers)|(newlines)|(errors)

declaredIdentifiers = []
declaredIdentifiersType = []

def LexAnalyze(results, main):
    lexemes = []
    if (main == -1):
        results = re.findall(rxVisible, results)
        numVisibleLex = 0
        #print(">>>>")
        #print(results)
    if (main == -2):
        results = re.findall(rxSmoosh, results)
        numSmooshLex = 0
        #print("<<<<<")
        #print(results)

    for i in results:
        if (main == -1):
            numVisibleLex += 1
        elif (main == -2):
            numSmooshLex += 1
        # captured by first capture group (keywords)
        if (i[0]):
            kw = i[0]
            # removing whitespaces
            while (kw[0] == " " or kw[0] == "\t" or kw[0] == "\n"):
                kw = kw[1:]
            while (kw[len(kw)-1] == " " or kw[len(kw)-1] == "\t" or kw[len(kw)-1] == "\n"):
                kw = kw[:-1]

            kw = ' '.join(kw.split())
            #print(kw)

            # storing valid keyword lexemes and their classifications
            if (kw == "HAI"):                       lexemes.append(["Code Delimiter OPEN",kw])
            elif (kw == "KTHXBYE"):                 lexemes.append(["Code Delimiter CLOSE",kw])
            elif (kw == "NUMBAR"):                 lexemes.append(["NUMBAR keyword",kw])
            elif (kw == "NUMBR"):                 lexemes.append(["NUMBR keyword",kw])
            elif (kw == "YARN"):                 lexemes.append(["YARN keyword",kw])
            elif (kw == "TROOF"):                 lexemes.append(["TROOF keyword",kw])
            elif (kw[0:3] == "BTW"):
                pass
                #lexemes.append(["Single Comment Keyword",kw[0:3]])
                #lexemes.append(["Comment",kw[4:]])
            elif (kw[0:4] == "OBTW" and kw[-4:] == "TLDR"):
                pass
                #lexemes.append(["Multiple Comment Delimiter", "OBTW"])
                #lexemes.append(["Multiple Comment", kw[5:-5]])
                #lexemes.append(["Multiple Comment Delimiter", "TLDR"])
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
            elif (kw[0:6] == "SMOOSH"):                  
                if (main != -2):
                    #print("***")
                    #print(kw)
                    smooshContent = kw[6:].replace(" ","   ").replace("\t","\t\t\t")
                    smooshContent = " "+smooshContent+" "
                    
                    smooshLex = LexAnalyze(smooshContent, -2)
                    #print(":***:")
                    #print(smooshLex)
                    if (smooshLex == "ERROR"):
                        error = "ERROR: Another SMOOSH cannot be an argument of SMOOSH"
                        lexemes.insert(0, error)
                        return lexemes
                    elif (smooshLex == "ERROR1"):
                        error = "ERROR: VISIBLE cannot be an argument of SMOOSH"
                        lexemes.insert(0, error)
                        return lexemes
                    elif (smooshLex[0][0:5] == "ERROR"):
                        error = smooshLex.pop(0)
                        smooshLex.insert(0, ['Concatenation Keyword', 'SMOOSH', "err"])
                        for j in smooshLex:
                            lexemes.append(j)
                        lexemes.insert(0, error)
                        return lexemes
                    for j in smooshLex:
                        lexemes.append(j)
                    
                else:
                    error = "ERROR"
                    return error
            elif (kw == "MAEK"):                    lexemes.append(["Typecast Keyword (new value)",kw])
            elif (kw == "A"):                       lexemes.append(["Typecast Noise Word",kw])
            elif (kw == "IS NOW A"):                lexemes.append(["Typecast Keyword",kw])
            elif (kw[0:7] == "VISIBLE"):            
                if (main == 1):
                    visibleContent = kw[7:].replace(" ","   ").replace("\t","\t\t\t")
                    visibleContent = " "+visibleContent+" "
                    visibleLex = LexAnalyze(visibleContent, -1)
                    if (visibleLex == "ERROR"):
                        error = "ERROR: Another VISIBLE cannot be an argument of VISIBLE"
                        lexemes.insert(0, error)
                        return lexemes
                    elif (visibleLex[0][0:5] == "ERROR"):
                        error = visibleLex.pop(0)
                        visibleLex.insert(0, ['Output Keyword', 'VISIBLE', "err"])
                        for j in visibleLex:
                            lexemes.append(j)
                        lexemes.insert(0, error)
                        return lexemes
                    for j in visibleLex:
                        lexemes.append(j)
                else:
                    error = "ERROR"
                    if (main == -2):
                        error = "ERROR1"
                    return error
            elif (kw == "GIMMEH"):                  lexemes.append(["Input Keyword",kw])
            elif (kw == "O RLY?"):                  lexemes.append(["If-Then Delimiter",kw])
            elif (kw == "YA RLY"):                  lexemes.append(["If Keyword",kw])
            elif (kw == "MEBBE"):                   lexemes.append(["Else If Keyword",kw])
            elif (kw == "NO WAI"):                  lexemes.append(["Else Keyword",kw])
            elif (kw == "OIC"):                     lexemes.append(["Conditional Delimiter",kw])
            elif (kw == "WTF?"):                    lexemes.append(["Switch-Case Delimiter",kw])
            elif (kw == "OMG"):                     lexemes.append(["Case Keyword",kw])
            elif (kw == "OMGWTF"):                  lexemes.append(["Default Case Keyword",kw])
            elif (kw == "IM IN YR"):                lexemes.append(["Loop Delimiter OPEN",kw])
            elif (kw == "UPPIN"):                   lexemes.append(["Loop Operation",kw])
            elif (kw == "NERFIN"):                  lexemes.append(["Loop Operation",kw])
            elif (kw == "YR"):                      lexemes.append(["Loop Keyword",kw])
            elif (kw == "TIL"):                     lexemes.append(["Loop Condition",kw])
            elif (kw == "WILE"):                    lexemes.append(["Loop Condition",kw])
            elif (kw == "IM OUTTA YR"):             lexemes.append(["Loop Delimiter CLOSE",kw])
            elif (kw == "GTFO"):                    lexemes.append(["Break Keyword",kw])
            elif (kw == "AN"):                      lexemes.append(["Operand Separator",kw])
            elif (kw == "HOW IZ I"):                lexemes.append(["Function Delimiter",kw])
            elif (kw == "IF U SAY SO"):             lexemes.append(["Function Delimiter",kw])
            elif (kw == "I IZ"):                    lexemes.append(["Function Call",kw])
            elif (kw == "MKAY"):                    lexemes.append(["Parameter Delimiter",kw])
            else:                                   lexemes.append(["KEYWORD",kw])
        # captured by second capture group (literals)
        elif (i[1]):
            lit = i[1]
            # removing whitespaces
            while (lit[0] == " " or lit[0] == "\t" or lit[0] == "\n"):
                lit = lit[1:]
            while (lit[len(lit)-1] == " " or lit[len(lit)-1] == "\t" or lit[len(lit)-1] == "\n"):
                lit = lit[:-1]

            # storing valid literals and their classifications
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
        # captured by third capture group (identifiers)
        elif (i[2]):
            ident = i[2]
            # removing whitespaces
            while (ident[0] == " " or ident[0] == "\t" or ident[0] == "\n"):
                ident = ident[1:]
            while (ident[len(ident)-1] == " " or ident[len(ident)-1] == "\t" or ident[len(ident)-1] == "\n"):
                ident = ident[:-1]

            # if identifier is already declared, save the next occurence to lexeme table
            if (ident in declaredIdentifiers):
                index = declaredIdentifiers.index(ident)
                lexemes.append([declaredIdentifiersType[index],ident])
            else:
                # classifying what kind of identifier is being declared
                if (len(lexemes) != 0):
                    previousLexeme = lexemes[len(lexemes)-1][1]
                    declaredIdentifiers.append(ident)
                    if (previousLexeme == "I HAS A"):       
                        lexemes.append(["Variable Identifier",ident])
                        declaredIdentifiersType.append("Variable Identifier")
                    elif (previousLexeme == "IM IN YR"):
                        lexemes.append(["Loop Identifier",ident])
                        declaredIdentifiersType.append("Loop Identifier")
                    elif (previousLexeme == "HOW IZ I"):
                        lexemes.append(["Function Identifier",ident])
                        declaredIdentifiersType.append("Function Identifier")
                    else:
                        error = "ERROR: Undeclared identifier"
                        lexemes.insert(0, error)
                        return lexemes
                else:
                    error = "ERROR: Undeclared identifier"
                    lexemes.insert(0, error)
                    return lexemes
        
        elif (i[3]):
            if (len(lexemes) != 0):
                previousCategory = lexemes[len(lexemes)-1][0]
                if (previousCategory != "NEWLINE"):
                    lexemes.append(["NEWLINE", "\\n"])
        # captured by fourth capture group (not a LOL lexeme)
        else:
            error = i[4].replace(" ","").replace("\t","").replace("\n","")
            error = "ERROR: "+error
            lexemes.insert(0, error)
            return lexemes
    
    if (main == -1):
        lexemes.insert(0,["Output Keyword", "VISIBLE", numVisibleLex])
        #lexemes.insert(0,["Output Keyword", "VISIBLE"])
        #print(lexemes)
    elif (main == -2):
        lexemes.insert(0,["Concatenation Keyword", "SMOOSH", numSmooshLex])
        #print("::::")
        #print(lexemes)
    return lexemes

def lex_main():
    fileHandle = open("sample.lol","r")
    content = fileHandle.read()
    fileHandle.close()

    print(content+"\n")

    content = " "+content+"\n "
    content = content.replace(" ", "   ")
    content = content.replace("\t", "\t\t\t")
    content = content.replace("\n"," \n\n ")
    categoriesAndLexemes = []
    error = "NONE"
    results = re.findall(rx, content)
    categoriesAndLexemes = LexAnalyze(results, 1)
    #print(categoriesAndLexemes)
    print("===================================================================")
    if (isinstance(categoriesAndLexemes[0], str)):
        error = categoriesAndLexemes.pop(0)
        for i in categoriesAndLexemes:
            print(i[0].ljust(27," ")+":\t"+i[1])

        print("INTERRUPT!\n"+error)
    else:
        for i in categoriesAndLexemes:
            if (i[0] != "NEWLINE"):
                print("\n\t",i[0].ljust(27," ")+":\t"+i[1], end="")
                #if (i[0] == "Output Keyword"):
                #    print(" ("+str(i[2])+" next lexemes or smoosh)",end="")
                

        if (error != "NONE"):
            print("INTERRUPT!\nERROR: "+error)
        else:
            print("\n\nLEXICAL ANALYSIS COMPLETE!")
            print("===================================================================")
            return categoriesAndLexemes

        #for i in categoriesAndLexemes:
        #    print(i)
        #print()
#lex_main()

if __name__ == "__main__":
    lex_main()