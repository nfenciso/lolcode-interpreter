import syntactic_analyzer

symbolTable = {
    "IT": None
}

def mathSolve(tokens):
    acc = []
    eval = "NO ERRORS"
    curr = 0
    math_operations = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]
    sublistTokens = []
    for i in tokens:
        if (i[0] == 'Arithmetic Operation' or i[0] == 'Operand Separator'):
            sublistTokens.append(i[1])
        elif (i[0] == "NUMBR Literal"):
            sublistTokens.append(int(i[1]))
        elif (i[0] == "NUMBAR Literal"):
            sublistTokens.append(float(i[1]))
        elif (i[0] == "YARN Literal"):
            try:
                cnv = float(i[1])
                checkCnv = cnv - int(i[1])

                if (checkCnv == 0):
                    sublistTokens.append(int(i[1]))
                else:
                    sublistTokens.append(float(i[1]))
            except:
                eval = f"ERROR: {i[1]} cannot be converted to number"
                return eval
        elif (i[0] == "TROOF Literal"):
            if (i[1] == "WIN"): sublistTokens.append(1)
            else:               sublistTokens.append(0)
    
    while (1):
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
            toBeInserted = sublistTokens[curr]

            if (toBeInserted == "AN"):
                curr += 1
                toBeInserted = sublistTokens[curr]
            
            acc.append(toBeInserted)
            curr += 1
    
    return eval

def semanticAnalyze(lst):
    temp = ""
    tempList = []
    cnt = 0
    while (cnt < len(lst)):
        line = lst[cnt]
        if (line[0][0] == "Code Delimiter OPEN"):
            pass
        elif (line[0][0] == "Variable Declaration"):
            var = line[1][1]
            if var in symbolTable:
                return f"ERROR: {var} has already been declared"
            else:
                symbolTable[var] = None
                if (len(line) > 2):
                    if (isinstance(line[3], str)):
                        typeChild = line[3]
                        if (typeChild == "<math_arguments>"):
                            cnt += 1
                            value = mathSolve(lst[cnt])
                            if (isinstance(value, str)):
                                return value
                            allInt = True
                            for i in lst[cnt]:
                                if (i[0] == "NUMBAR Literal"):
                                    allInt = False
                                    break
                                elif (i[0] == "YARN Literal"):
                                    temp = float(i[1])
                                    checkTemp = temp - int(i[1])
                                    if (checkTemp != 0):
                                        allInt = False
                                        break
                            if (allInt):
                                symbolTable[var] = int(value)
                            else:
                                symbolTable[var] = value

                    elif (isinstance(line[3], list)):
                        valType = line[3][0]
                        value = line[3][1]

                        if (valType == "NUMBR Literal"): 
                            symbolTable[var] = int(value)
                        elif (valType == "NUMBAR Literal"):
                            symbolTable[var] = float(value)
                        elif (valType == "YARN Literal"):
                            symbolTable[var] = value
                        elif (valType == "TROOF Literal"):
                            if (value == "WIN"):
                                symbolTable[var] = True
                            else:
                                symbolTable[var] = False
        elif (line[0][0] == "Arithmetic Operation"):
            value = mathSolve(line)
            symbolTable["IT"] = value
        elif (line[0][0] in ["NUMBR Literal","NUMBAR Literal","TROOF Literal","YARN Literal"]):
            type = line[0][0]
            value = line[0][1]
            if (type == "NUMBR Literal"):
                symbolTable["IT"] = int(value)
            elif (type == "NUMBAR Literal"):
                symbolTable["IT"] = float(value)
            elif (type == "YARN Literal"):
                symbolTable["IT"] = value
            elif (type == "TROOF Literal"):
                if (value == "WIN"):
                    symbolTable["IT"] = True
                else:
                    symbolTable["IT"] = False
        elif (line[0][0] == "Input Keyword"):
            temp = input()
            var = line[1][1]
            symbolTable[var] = temp
        elif (line[0][0] == "Output Keyword"):
            numVisibleArgs = line[0][2]
            tempList = []
            smooshIndex = -1
            tempCnt = 0
            while (tempCnt < numVisibleArgs):
                #print(":::"+str(lst[cnt]))
                cnt += 1
                tempList.append(lst[cnt])

                if (lst[cnt][0] == "<math_arguments>"):
                    tempList.pop()
                    cnt += 1
                    tempList.append(lst[cnt])
                    tempCnt += len(lst[cnt])-1
                # boolean
                # comparison

                if (lst[cnt][0][0] == "Concatenation Keyword"):
                    smooshIndex = cnt
                
                tempCnt += 1
                #print("tempCnt: "+str(tempCnt))
            #print("III")
            #print(tempList)
            if (smooshIndex != -1):
                numSmooshArgs = lst[smooshIndex][0][2]
                tempCnt = 0
                while (tempCnt < numSmooshArgs):
                    cnt += 1
                    tempList.append(lst[cnt])

                    if (lst[cnt][0] == "<math_arguments>"):
                        tempList.pop()
                        cnt += 1
                        tempList.append(lst[cnt])
                        tempCnt += len(lst[cnt])-1
                    # boolean
                    # comparison
                    
                    tempCnt += 1
            
            temp = ""
            for i in tempList:
                #print("::",str(i))
                lexType = i[0][0]
                value = i[0][1]
                if (lexType in ["NUMBR Literal","NUMBAR Literal","TROOF Literal","YARN Literal"]):
                    temp += str(value)
                elif (lexType == "Variable Identifier"):
                    if (symbolTable[value] == None):
                        eval = f"ERROR: Variable {value} of type NOOB cannot be implicitly typecasted to YARN."
                        return eval
                    else:
                        temp += str(symbolTable[value])
                elif (lexType == "Arithmetic Operation"):
                    temp += str(mathSolve(i))
                elif (lexType == "Operand Separator"):
                    pass
            # Don't comment out this print statement
            print(temp)
            # # # # # # # # # # # # # # # # # # # #

        elif (line[0][0] == "Concatenation Keyword"):
            numSmooshArgs = line[0][2]
            tempList = []
            tempCnt = 0
            while (tempCnt < numSmooshArgs):
                cnt += 1
                tempList.append(lst[cnt])

                if (lst[cnt][0] == "<math_arguments>"):
                    tempList.pop()
                    cnt += 1
                    tempList.append(lst[cnt])
                    tempCnt += len(lst[cnt])-1
                # boolean
                # comparison
                
                tempCnt += 1
            
            temp = ""
            for i in tempList:
                lexType = i[0][0]
                value = i[0][1]
                if (lexType in ["NUMBR Literal","NUMBAR Literal","TROOF Literal","YARN Literal"]):
                    temp += str(value)
                elif (lexType == "Variable Identifier"):
                    if (symbolTable[value] == None):
                        eval = f"ERROR: Variable {value} of type NOOB cannot be implicitly typecasted to YARN."
                        return eval
                    else:
                        temp += str(symbolTable[value])
                elif (lexType == "Arithmetic Operation"):
                    temp += str(mathSolve(i))
                elif (lexType == "Operand Separator"):
                    pass
            symbolTable["IT"] = temp
        else:
            pass
            
            
        cnt += 1
    
    return 1

def semantic_main():
    syntax = syntactic_analyzer.syntax_main()
    
    try:
        tmp = isinstance(syntax.getResult(), str)
    except:
        tmp = True
    if (tmp):
        pass
    else:
        lst = syntax.getResult().get_list([])
        for i in lst:
           print(i)
        semanticResult = semanticAnalyze(lst)

        print("\n### SYMBOL TABLE ###")
        for i in symbolTable:
            if (isinstance(symbolTable[i], str)):
                print(f"{i.rjust(10)}: \"{symbolTable[i]}\"")
            else:
                print(f"{i.rjust(10)}: {symbolTable[i]}")
        if (semanticResult != 1):
            print("\n"+semanticResult)

if __name__ == "__main__":
    semantic_main()