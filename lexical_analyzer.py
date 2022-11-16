# CMSC124 B-1L
# Lexical Analyzer
# CONTRIBUTORS:
#   John Kenneth F. Manalang
#   Nathaniel F. Enciso

import re
import random


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

content = " "+content+" "
content = content.replace(" ", "   ")
content = content.replace("\t", "\t\t\t")
content = content.replace("\n","\n\n\n")

rx = r"([ \t\n]HAI[ \t\n]|[ \t\n]KTHXBYE[ \t\n]|[ \t\n]BTW.*[ \t\n]|[ \t\n]OBTW[\n\r\w\W]*TLDR[ \t\n]|[ \t\n]I[ \t]+HAS[ \t]+A[ \t\n]|[ \t\n]ITZ[ \t\n]|[ \t\n]R[ \t\n]|[ \t\n]SUM[ \t]+OF[ \t\n]|[ \t\n]DIFF[ \t]+OF[ \t\n]|[ \t\n]PRODUKT[ \t]+OF[ \t\n]|[ \t\n]QUOSHUNT[ \t]+OF[ \t\n]|[ \t\n]MOD[ \t]+OF[ \t\n]|[ \t\n]BIGGR[ \t]+OF[ \t\n]|[ \t\n]SMALLR[ \t]+OF[ \t\n]|[ \t\n]BOTH[ \t]+OF[ \t\n]|[ \t\n]EITHER[ \t]+OF[ \t\n]|[ \t\n]WON[ \t]+OF[ \t\n]|[ \t\n]NOT[ \t\n]|[ \t\n]ANY[ \t]+OF[ \t\n]|[ \t\n]ALL[ \t]+OF[ \t\n]|[ \t\n]BOTH[ \t]+SAEM[ \t\n]|[ \t\n]DIFFRINT[ \t\n]|[ \t\n]SMOOSH[ \t\n]|[ \t\n]MAEK[ \t\n]|[ \t\n]A[ \t\n]|[ \t\n]IS[ \t]+NOW[ \t]+A[ \t\n]|[ \t\n]VISIBLE[ \t\n]|[ \t\n]GIMMEH[ \t\n]|[ \t\n]O[ \t]+RLY\?[ \t\n]|[ \t\n]YA[ \t]+RLY[ \t\n]|[ \t\n]MEBBE[ \t\n]|[ \t\n]NO[ \t]+WAI[ \t\n]|[ \t\n]OIC[ \t\n]|[ \t\n]WTF\?[ \t\n]|[ \t\n]OMG[ \t\n]|[ \t\n]OMGWTF[ \t\n]|[ \t\n]IM[ \t]+IN[ \t]+YR[ \t\n]|[ \t\n]UPPIN[ \t\n]|[ \t\n]NERFIN[ \t\n]|[ \t\n]YR[ \t\n]|[ \t\n]TIL[ \t\n]|[ \t\n]WILE[ \t\n]|[ \t\n]IM[ \t]+OUTTA[ \t]+YR[ \t\n]|[ \t\n]GTFO[ \t\n]|[ \t\n]AN[ \t\n]|[ \t\n]HOW[ \t]+IZ[ \t]+I[ \t\n]|[ \t\n]IF[ \t]+U[ \t]+SAY[ \t]+SO[ \t\n]|[ \t\n]I[ \t]+IZ[ \t\n]|[ \t\n]MKAY[ \t\n])|([ \t\n]-?[0-9]+[ \t\n]|[ \t\n]-?[0-9]*\.[0-9]+[ \t\n]|\"[^\"\n]*\"|[ \t\n]WIN[ \t\n]|[ \t\n]FAIL[ \t\n])|([ \t\n][a-zA-Z]\w*[ \t\n])|([^ \t\n]+)"
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
    # captured by first regex (keywords)
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
        elif (kw == "AN"):                      lexemes.append(["Operand Separator",kw])
        elif (kw == "HOW IZ I"):                lexemes.append(["Function Delimiter",kw])
        elif (kw == "IF U SAY SO"):             lexemes.append(["Function Delimiter",kw])
        elif (kw == "I IZ"):                    lexemes.append(["Function Call",kw])
        elif (kw == "MKAY"):                    lexemes.append(["Parameter Delimiter",kw])
        else:                                   lexemes.append(["KEYWORD",kw])
    # captured by second regex (literals)
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
    # captured by third regex (identifiers)
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
    # captured by fourth regex (not a LOL lexeme)
    else:
        error = i[3].replace(" ","").replace("\t","").replace("\n","")
        break


for i in lexemes:
   print(i[0].ljust(27," ")+":\t"+i[1])
if (error != "NONE"):
    print("INTERRUPT!\nERROR: "+error)
else:
    print("\nANALYSIS COMPLETE!")

print(lexemes)
print()

class TreeNode:
    def __init__(self, data, typeNode):
        self.data = data
        self.type = typeNode
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        child.parent = self
        self.children.append(child)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    
    def advance(self):
        self.index += 1
        if (self.tok_idx < len(self.tokens)):
            self.curr_tok = self.tokens[self.tok_idx]
        return self.curr_tok
    
    def parse(self):
        self.tree = TreeNode("<program>", "TNT")
        if (self.curr_tok[0] == "Code Delimeter OPEN"):
            self.tree.add_child(TreeNode("Code Delimeter OPEN", "T"), "L")



def checkIfValidMathSyntax(tokens):
    acc = []
    eval = "NO ERRORS"
    curr = 0
    math_operations = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT", "MOD OF", "BIGGR OF", "SMALLR OF"]
    sublistTokens = []
    for i in tokens:
        if (i[0] == 'Arithmetic Operation' or i[0] == 'Operand Separator'):
            sublistTokens.append(i[1])
        else:
            sublistTokens.append(random.randint(1,999))

    while (1):
        print(acc, "curr:", curr)
        if (len(acc) >= 3):
            lastElemIsNum = isinstance(acc[len(acc)-1], int) or isinstance(acc[len(acc)-1], float)
            secondLastElemIsNum = isinstance(acc[len(acc)-2], int) or isinstance(acc[len(acc)-2], float)
            if (lastElemIsNum and secondLastElemIsNum):
                firstOperand = acc[len(acc)-2]
                secondOperand = acc[len(acc)-1]
                operation = acc[len(acc)-3]
                if (operation not in math_operations): break
                if (operation == "SUM OF"):         acc[len(acc)-3] = firstOperand + secondOperand
                elif (operation == "DIFF OF"):      acc[len(acc)-3] = firstOperand - secondOperand
                elif (operation == "PRODUKT OF"):   acc[len(acc)-3] = firstOperand * secondOperand
                elif (operation == "QUOSHUNT OF"):  
                    if (secondOperand == 0): secondOperand = 1
                    acc[len(acc)-3] = firstOperand / secondOperand
                elif (operation == "MOD OF"):       acc[len(acc)-3] = firstOperand % secondOperand
                elif (operation == "BIGGR OF"):     acc[len(acc)-3] = max(firstOperand, secondOperand)
                elif (operation == "SMALLR OF"):    acc[len(acc)-3] = min(firstOperand, secondOperand)
                acc.pop()
                acc.pop()

                if (len(acc) == 1 and curr > len(tokens)-1):
                    eval = acc[0]
                    break
                continue

        if (curr == 0):
            if (sublistTokens[curr] not in math_operations): break
            else:
                acc.append(sublistTokens[curr])
                curr += 1
        else:
            lastElem = acc[len(acc)-1]
            if ((isinstance(acc[0],int) or isinstance(acc[0],float)) and curr < len(sublistTokens)):
                eval = "ERROR: Lacking arithmetic operation"
                break
            if (curr == len(sublistTokens)):
                eval = "ERROR: Lacking AN and an operand"
                break
            toBeInserted = sublistTokens[curr]
            
            if (lastElem in math_operations and toBeInserted == "AN"):  
                eval = "ERROR: Lacking operand after arithmetic operation"
                break
            if (lastElem == "AN" and toBeInserted == "AN"):      
                eval = "ERROR: Lacking operand between AN"       
                break
            lastElemIsNum = isinstance(lastElem, int) or isinstance(lastElem, float)
            toBeInsertedIsNum = isinstance(toBeInserted, int) or isinstance(toBeInserted, float)
            if (lastElemIsNum and toBeInsertedIsNum):     
                eval = "ERROR: Lacking AN"              
                break
            if (toBeInserted == "AN"):
                curr += 1
                if (curr == len(sublistTokens)):
                    eval = "ERROR: Lacking operand after AN" 
                    break
                toBeInserted = sublistTokens[curr]
            
            #print("TO BE INSERTED: "+str(toBeInserted))
            acc.append(toBeInserted)
            curr += 1

    if (eval == "NO ERRORS"):
        return tokens
    else:
        return eval

accumulatedMathTokens = [['Arithmetic Operation', 'SUM OF'], ['Arithmetic Operation', 'BIGGR OF'], ['Arithmetic Operation', 'SUM OF'], ['NUMBR Literal', '4'], ['Operand Separator', 'AN'], ['NUMBR Literal', '2'], ['Operand Separator', 'AN'], ['NUMBR Literal', '2'], ['Operand Separator', 'AN'], ['Arithmetic Operation', 'DIFF OF'], ['NUMBR Literal', '10'], ['Operand Separator', 'AN'], ['NUMBR Literal', '7']]
print(checkIfValidMathSyntax(accumulatedMathTokens))