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

rx = r"([ \t\n]HAI[ \t\n]|[ \t\n]KTHXBYE[ \t\n]|[ \t\n]BTW.*[ \t\n]|[ \t\n]OBTW[\n\r\w\W]*TLDR[ \t\n]|[ \t\n]I[ \t]+HAS[ \t]+A[ \t\n]|[ \t\n]ITZ[ \t\n]|[ \t\n]R[ \t\n]|[ \t\n]SUM[ \t]+OF[ \t\n]|[ \t\n]DIFF[ \t]+OF[ \t\n]|[ \t\n]PRODUKT[ \t]+OF[ \t\n]|[ \t\n]QUOSHUNT[ \t]+OF[ \t\n]|[ \t\n]MOD[ \t]+OF[ \t\n]|[ \t\n]BIGGR[ \t]+OF[ \t\n]|[ \t\n]SMALLR[ \t]+OF[ \t\n]|[ \t\n]BOTH[ \t]+OF[ \t\n]|[ \t\n]EITHER[ \t]+OF[ \t\n]|[ \t\n]WON[ \t]+OF[ \t\n]|[ \t\n]NOT[ \t\n]|[ \t\n]ANY[ \t]+OF[ \t\n]|[ \t\n]ALL[ \t]+OF[ \t\n]|[ \t\n]BOTH[ \t]+SAEM[ \t\n]|[ \t\n]DIFFRINT[ \t\n]|[ \t\n]SMOOSH[ \t\n]|[ \t\n]MAEK[ \t\n]|[ \t\n]A[ \t\n]|[ \t\n]IS[ \t]+NOW[ \t]+A[ \t\n]|[ \t\n]VISIBLE.*[ \t\n]|[ \t\n]GIMMEH[ \t\n]|[ \t\n]O[ \t]+RLY\?[ \t\n]|[ \t\n]YA[ \t]+RLY[ \t\n]|[ \t\n]MEBBE[ \t\n]|[ \t\n]NO[ \t]+WAI[ \t\n]|[ \t\n]OIC[ \t\n]|[ \t\n]WTF\?[ \t\n]|[ \t\n]OMG[ \t\n]|[ \t\n]OMGWTF[ \t\n]|[ \t\n]IM[ \t]+IN[ \t]+YR[ \t\n]|[ \t\n]UPPIN[ \t\n]|[ \t\n]NERFIN[ \t\n]|[ \t\n]YR[ \t\n]|[ \t\n]TIL[ \t\n]|[ \t\n]WILE[ \t\n]|[ \t\n]IM[ \t]+OUTTA[ \t]+YR[ \t\n]|[ \t\n]GTFO[ \t\n]|[ \t\n]AN[ \t\n]|[ \t\n]HOW[ \t]+IZ[ \t]+I[ \t\n]|[ \t\n]IF[ \t]+U[ \t]+SAY[ \t]+SO[ \t\n]|[ \t\n]I[ \t]+IZ[ \t\n]|[ \t\n]MKAY[ \t\n])|([ \t\n]-?[0-9]+[ \t\n]|[ \t\n]-?[0-9]*\.[0-9]+[ \t\n]|\"[^\"\n]*\"|[ \t\n]WIN[ \t\n]|[ \t\n]FAIL[ \t\n])|([ \t\n][a-zA-Z]\w*[ \t\n])|([^ \t\n]+)"
rxVisible = r"([ \t\n]HAI[ \t\n]|[ \t\n]KTHXBYE[ \t\n]|[ \t\n]BTW.*[ \t\n]|[ \t\n]OBTW[\n\r\w\W]*TLDR[ \t\n]|[ \t\n]I[ \t]+HAS[ \t]+A[ \t\n]|[ \t\n]ITZ[ \t\n]|[ \t\n]R[ \t\n]|[ \t\n]SUM[ \t]+OF[ \t\n]|[ \t\n]DIFF[ \t]+OF[ \t\n]|[ \t\n]PRODUKT[ \t]+OF[ \t\n]|[ \t\n]QUOSHUNT[ \t]+OF[ \t\n]|[ \t\n]MOD[ \t]+OF[ \t\n]|[ \t\n]BIGGR[ \t]+OF[ \t\n]|[ \t\n]SMALLR[ \t]+OF[ \t\n]|[ \t\n]BOTH[ \t]+OF[ \t\n]|[ \t\n]EITHER[ \t]+OF[ \t\n]|[ \t\n]WON[ \t]+OF[ \t\n]|[ \t\n]NOT[ \t\n]|[ \t\n]ANY[ \t]+OF[ \t\n]|[ \t\n]ALL[ \t]+OF[ \t\n]|[ \t\n]BOTH[ \t]+SAEM[ \t\n]|[ \t\n]DIFFRINT[ \t\n]|[ \t\n]SMOOSH[ \t\n]|[ \t\n]MAEK[ \t\n]|[ \t\n]A[ \t\n]|[ \t\n]IS[ \t]+NOW[ \t]+A[ \t\n]|[ \t\n]VISIBLE[ \t\n]|[ \t\n]GIMMEH[ \t\n]|[ \t\n]O[ \t]+RLY\?[ \t\n]|[ \t\n]YA[ \t]+RLY[ \t\n]|[ \t\n]MEBBE[ \t\n]|[ \t\n]NO[ \t]+WAI[ \t\n]|[ \t\n]OIC[ \t\n]|[ \t\n]WTF\?[ \t\n]|[ \t\n]OMG[ \t\n]|[ \t\n]OMGWTF[ \t\n]|[ \t\n]IM[ \t]+IN[ \t]+YR[ \t\n]|[ \t\n]UPPIN[ \t\n]|[ \t\n]NERFIN[ \t\n]|[ \t\n]YR[ \t\n]|[ \t\n]TIL[ \t\n]|[ \t\n]WILE[ \t\n]|[ \t\n]IM[ \t]+OUTTA[ \t]+YR[ \t\n]|[ \t\n]GTFO[ \t\n]|[ \t\n]AN[ \t\n]|[ \t\n]HOW[ \t]+IZ[ \t]+I[ \t\n]|[ \t\n]IF[ \t]+U[ \t]+SAY[ \t]+SO[ \t\n]|[ \t\n]I[ \t]+IZ[ \t\n]|[ \t\n]MKAY[ \t\n])|([ \t\n]-?[0-9]+[ \t\n]|[ \t\n]-?[0-9]*\.[0-9]+[ \t\n]|\"[^\"\n]*\"|[ \t\n]WIN[ \t\n]|[ \t\n]FAIL[ \t\n])|([ \t\n][a-zA-Z]\w*[ \t\n])|([^ \t\n]+)"
#(keywords)|(literals)|(identifiers)|(errors)

declaredIdentifiers = []
declaredIdentifiersType = []

def LexAnalyze(results, main):
    lexemes = []
    if (not main):
        results = re.findall(rxVisible, results)
        numVisibleLex = 0
    for i in results:
        comment = False
        if (not main):
            numVisibleLex += 1
        # captured by first capture group (keywords)
        if (i[0]):
            kw = i[0]
            # removing whitespaces
            while (kw[0] == " " or kw[0] == "\t" or kw[0] == "\n"):
                kw = kw[1:]
            while (kw[len(kw)-1] == " " or kw[len(kw)-1] == "\t" or kw[len(kw)-1] == "\n"):
                kw = kw[:-1]

            kw = ' '.join(kw.split())

            # storing valid keyword lexemes and their classifications
            if (kw == "HAI"):                       lexemes.append(["Code Delimeter OPEN",kw])
            elif (kw == "KTHXBYE"):                 lexemes.append(["Code Delimeter CLOSE",kw])
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
            elif (kw == "SMOOSH"):                  lexemes.append(["Concatenation Keyword",kw])
            elif (kw == "MAEK"):                    lexemes.append(["Typecast Keyword",kw])
            elif (kw == "A"):                       lexemes.append(["Typecast Noise Word",kw])
            elif (kw == "IS NOW A"):                lexemes.append(["Typecast Keyword",kw])
            elif (kw[0:7] == "VISIBLE"):            
                if (main):
                    visibleContent = kw[7:].replace(" ","   ").replace("\t","\t\t\t")
                    visibleContent = " "+visibleContent+" "
                    visibleLex = LexAnalyze(visibleContent, False)
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
                    return error
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
                if (not main):
                    numVisibleLex += 2
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
                        lexemes.append(["IDENTIFIER",ident])
                        declaredIdentifiersType.append("IDENTIFIER")
                else:
                    lexemes.append(["IDENTIFIER",ident])
                    declaredIdentifiersType.append("IDENTIFIER")
        # captured by fourth capture group (not a LOL lexeme)
        else:
            error = i[3].replace(" ","").replace("\t","").replace("\n","")
            error = "ERROR: "+error
            lexemes.insert(0, error)
            return lexemes
    
    if (not main):
        lexemes.insert(0,["Output Keyword", "VISIBLE", numVisibleLex])
    return lexemes

def lex_main():
    fileHandle = open("sample.lol","r")
    content = fileHandle.read()
    fileHandle.close()

    print(content+"\n")

    content = " "+content+" "
    content = content.replace(" ", "   ")
    content = content.replace("\t", "\t\t\t")
    content = content.replace("\n","\n\n\n")
    categoriesAndLexemes = []
    error = "NONE"
    results = re.findall(rx, content)
    categoriesAndLexemes = LexAnalyze(results, True)
    #print(categoriesAndLexemes)
    if (isinstance(categoriesAndLexemes[0], str)):
        error = categoriesAndLexemes.pop(0)
        for i in categoriesAndLexemes:
            print(i[0].ljust(27," ")+":\t"+i[1])

        print("INTERRUPT!\n"+error)
    else:
        for i in categoriesAndLexemes:
           print("\n",i[0].ljust(27," ")+":\t"+i[1], end="")
           if (i[0] == "Output Keyword"):
               print(" ("+str(i[2])+" next lexemes)",end="")

        if (error != "NONE"):
            print("INTERRUPT!\nERROR: "+error)
        else:
            print("\nLEXICAL ANALYSIS COMPLETE!")
            return categoriesAndLexemes

        #for i in categoriesAndLexemes:
        #    print(i)
        #print()
