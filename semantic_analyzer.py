import syntactic_analyzer

symbolTable = {
    "IT": None
}

switchCases = []

inLoop = False

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
        elif (i[0] == "Variable Identifier"):
            varValue = symbolTable[i[1]]
            try:
                cnv = float(varValue)
                checkCnv = cnv - int(varValue)
            except:
                eval = f"ERROR: {i[1]} cannot be converted to number"
                return eval

            if (checkCnv == 0):
                sublistTokens.append(int(varValue))
            else:
                sublistTokens.append(float(varValue))
    
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
                #print(sublistTokens)
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
        elif (line[0][0] == "Variable Identifier"):
            if (len(line) == 1):
                symbolTable["IT"] = symbolTable[line[0][1]]
            else:
                
                if (line[1][0] == "Assignment Keyword"):
                    if (line[2] == "<typecasted_value>"):
                        cnt += 1
                        line = lst[cnt]
                        # DO THE MAEK HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
                        pass
                        print(f"================= {line}")
                    else:
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
            #print(lst[cnt:])
            #print("###"+str(line))
            value = mathSolve(lst[cnt])
            if (isinstance(value, str)):
                return value
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
                    valueM = mathSolve(i)
                    if (isinstance(valueM, str)):
                        return valueM
                    temp += str(valueM)
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
                    valueM = mathSolve(i)
                    if (isinstance(valueM, str)):
                        return valueM
                    temp += str(valueM)
                elif (lexType == "Operand Separator"):
                    pass
            symbolTable["IT"] = temp
        elif (line[0][0] == "<if-then block>"):
            ifList = []
            cnt += 2
            while (1):
                if (lst[cnt][0][0] == "<if-end>"):
                    break
                ifList.append(lst[cnt])
                cnt += 1
            cnt += 1
            elseList = []
            if (cnt >= len(lst)):
                pass
            else:
                if (lst[cnt][0][0] == "<else>"):
                    
                    cnt += 1
                    while (1):
                        if (lst[cnt][0][0] == "<else-end>"):
                            break
                        elseList.append(lst[cnt])
                        cnt += 1
                    cnt += 1
            
            varIT = symbolTable["IT"]
            if (isinstance(varIT, str)):
                if (varIT == ""):   eval = False
                else:               eval = True
            elif (isinstance(varIT, int) or isinstance(varIT, float)):
                if (float(varIT) == 0.0):   eval = False
                else:                       eval = True
            elif (isinstance(varIT, bool)):
                eval = varIT
            else:
                eval = False
            
            #print("EVAL: "+str(eval))
            if (eval):
                tmp = semanticAnalyze(ifList)
                if (tmp == "ENDLOOP"):
                    return "ENDLOOP"
            elif (len(elseList) != 0 and not eval):
                tmp = semanticAnalyze(elseList)
                if (tmp == "ENDLOOP"):
                    return "ENDLOOP"

        elif (line[0][0] == "<switch-case block>"):
            temp = []
            #print("&&&")
            while (1):
                if (lst[cnt][0][0] == "<switch-case end>"):
                    break
                if (lst[cnt][0][0][0:6] == "<case:"):
                    caseList = []
                    endRemoved = lst[cnt][0][0][:-1]
                    frontRemoved = endRemoved[7:]
                    if (frontRemoved[0] == '"'):
                        caseVal = str(frontRemoved[1:-1])
                    elif (frontRemoved == 'WIN'):
                        caseVal = True
                    elif (frontRemoved == 'FAIL'):
                        caseVal = False
                    else:
                        cnv = float(frontRemoved)
                        checkCnv = cnv - int(frontRemoved)

                        if (checkCnv == 0):
                            caseVal = int(frontRemoved)
                        else:
                            caseVal = float(frontRemoved)

                    breakEncountered = False
                    #print("$"+str(frontRemoved))
                    while (1):
                        if (lst[cnt][0][0] == "<case-end>"):
                            break
                        
                        if (not breakEncountered):
                            caseList.append(lst[cnt])

                        if (not breakEncountered and lst[cnt][0][0] == "Break Keyword"):
                            breakEncountered = True
                        cnt += 1
                    
                    caseList.pop(0)
                    switchCases.append((caseVal, caseList))
                elif (lst[cnt][0][0] == "<default_case>"):
                    breakEncountered = False
                    caseList = []
                    #print("$")
                    while (1):
                        if (lst[cnt][0][0] == "<default-case-end>"):
                            break
                        
                        if (not breakEncountered):
                            caseList.append(lst[cnt])

                        if (not breakEncountered and lst[cnt][0][0] == "Break Keyword"):
                            breakEncountered = True
                        cnt += 1
                    caseList.pop(0)
                    switchCases.append(("$#DEFAULT#$", caseList))

                cnt += 1
            matchedCase = False
            execSucceeding = True
            #for i in switchCases:
            #    print(i)
            for i in switchCases:
                if (i[0] == "$#DEFAULT#$" and not matchedCase):
                    if (i[1][len(i[1])-1][0][0] == "Break Keyword"):
                        i[1].pop()
                        semanticAnalyze(i[1])
                        break
                    else:
                        semanticAnalyze(i[1])
                if (matchedCase and execSucceeding and i[0] != "$#DEFAULT#$"):
                    if (i[1][len(i[1])-1][0][0] == "Break Keyword"):
                        i[1].pop()
                        semanticAnalyze(i[1])
                        break
                    else:
                        semanticAnalyze(i[1])
                    continue
                if (not matchedCase and i[0] == symbolTable["IT"]):
                    matchedCase = True
                    #print("QQQ:"+str(i[1][len(i[1])-1][0]))
                    if (i[1][len(i[1])-1][0][0] == "Break Keyword"):
                        i[1].pop()
                        semanticAnalyze(i[1])
                        break
                    else:
                        semanticAnalyze(i[1])


        elif (line[0] == "<boolean_operation>"):
            cnt += 1
            line = lst[cnt]
            result = get_bool_result(line)

            symbolTable["IT"] = result

        elif (line[0] == "<comparison_operation>"):
            cnt += 1
            line = lst[cnt]
            result = get_comparison_result(line)
            if (result not in [True, False]): return result

            symbolTable["IT"] = result

        elif (line[0][0] == "<loop>"):
            cnt += 1
            loopList = []
            global inLoop
            inLoop = True
            loopIterOperation = lst[cnt][0][0]
            loopVar = lst[cnt][0][1]
            #print(":"+str(loopIterOperation))
            #print(":"+str(loopVar))
            cnt += 1
            while (1):
                if (lst[cnt][0][0] == "<loop-content-end>"):
                    break
                loopList.append(lst[cnt])
                cnt += 1
            loopList.pop(0)
            #print("***")
            #print(loopList)
            while (1):
                iterResult = semanticAnalyze(loopList)
                #print("///"+str(iterResult))
                if (iterResult == "ENDLOOP"):
                    break
                
                try:
                    temp = int(symbolTable[loopVar])
                    if (loopIterOperation == "UPPIN"):
                        temp += 1
                    else:
                        temp -= 1
                    symbolTable[loopVar] = temp
                except:
                    return f"ERROR: {loopVar} cannot be typecast to a number"
        
        elif (line[0] == "<loop>" and len(line) == 3):
            loopConditionType = line[1]
            #print(loopConditionType)
            cnt += 1
            
            #print(":::"+str(lst[cnt]))
            if (lst[cnt][0][0] == "UPPIN" or lst[cnt][0][0] == "NERFIN"):
                cnt -= 1
                loopCondition = lst[cnt][2]
                cnt += 1
                loopIterOperation = lst[cnt][0][0]
                loopVar = lst[cnt][0][1]
                #print(":"+str(loopCondition))
                #print(":"+str(loopIterOperation))
                #print(":"+str(loopVar))
                cnt += 2
            else:
                #print("^^^"+str(lst[cnt]))
                loopCondition = lst[cnt]
                cnt += 1
                loopIterOperation = lst[cnt][0][0]
                #print("^^^"+str(lst[cnt]))
                loopVar = lst[cnt][0][1]
                #print(":"+str(loopCondition))
                #print(":"+str(loopIterOperation))
                #print(":"+str(loopVar))
                cnt += 2
            
            loopList = []
            inLoop = True
            while (1):
                if (lst[cnt][0][0] == "<loop-content-end>"):
                    break
                loopList.append(lst[cnt])
                cnt += 1
            #print("***")
            #print(loopList)
            #print(loopIterOperation,loopVar)
            #print(loopConditionType,loopCondition)
            while (1):
                if (isinstance(loopCondition, list)):
                    if (loopCondition[0] in ["BOTH OF", "EITHER OF", "WON OF", "ANY OF", "ALL OF","NOT"]):
                        fulfilledExpr = get_bool_result(loopCondition)
                    elif (loopCondition[0][0] == "Arithmetic Operation"):
                        fulfilledExpr = bool(mathSolve(loopCondition))
                    else:
                        fulfilledExpr = get_comparison_result(loopCondition)
                elif (isinstance(loopCondition, str)):
                    #print("*"+loopCondition)
                    if (loopCondition == "WIN"):
                        fulfilledExpr = True
                    elif (loopCondition == "FAIL"):
                        fulfilledExpr = False
                    elif (loopCondition[0] == '"'):
                        #print("\nYARN\n")
                        if (len(loopCondition) > 0):
                            fulfilledExpr = True
                        else:
                            fulfilledExpr = False
                    elif (loopCondition[0] in ["-","0","1","2","3","4","5","6","7","8","9"]):
                        fulfilledExpr = bool(float(loopCondition))
                    else:
                        varVal = symbolTable[loopCondition]
                        if (varVal in [True,False]):
                            fulfilledExpr = varVal
                        elif (isinstance(varVal, str)):
                            if (len(varVal) > 0):
                                fulfilledExpr = True
                            else:
                                fulfilledExpr = False
                        elif (isinstance(varVal,int) or isinstance(varVal,float)):
                            fulfilledExpr = bool(varVal)
                        else:
                            fulfilledExpr = False


                if (loopConditionType == "TIL" and fulfilledExpr):
                    break
                if (loopConditionType == "WILE" and not fulfilledExpr):
                    break

                iterResult = semanticAnalyze(loopList)
                #print("///"+str(iterResult))
                if (iterResult == "ENDLOOP"):
                    break
                
                try:
                    temp = int(symbolTable[loopVar])
                    if (loopIterOperation == "UPPIN"):
                        temp += 1
                    else:
                        temp -= 1
                    symbolTable[loopVar] = temp
                except:
                    return f"ERROR: {loopVar} cannot be typecast to a number"

        elif (line[0][0] == "Break Keyword" and inLoop):
            inLoop = False
            return "ENDLOOP"

        else:
            pass
            
        cnt += 1
    return 1


def get_comparison_value(comp_arguments, comp_type):
    UNMATCH_TYPE_ERROR = f"ERROR: Values must be of the same type (NUMBR or NUMBAR)"
    comp_type = comp_type
    to_evaluate = [comp_arguments[0], "", ""]

    # ============= first value ===================
    if (isinstance(comp_arguments[1], str)): # if string, sure to be a variable
        value = symbolTable[comp_arguments[1]]
        if ((isinstance(value, str)) or (value == None)): # value is not an integer or a float
            return f"ERROR: (Comparison) Value of '{comp_arguments[1]}' must be of type NUMBR or NUMBAR"
        else:
            if (isinstance(value, int)):
                temp_type = "integer"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value
            else:
                temp_type = "float"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value   
    elif (isinstance(comp_arguments[1], list)):       # if another comparison, BIGGR SMALLR OF
        value = get_comparison_value(comp_arguments[1], comp_type)
        if (isinstance(value, str)): return value
        if (isinstance(value, int)):
            temp_type = "integer"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[1] = value
        else:
            temp_type = "float"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[1] = value  
    elif (isinstance(comp_arguments[1], int)):             # integer
        temp_type = "integer"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[1] = comp_arguments[1]
    else:                                   # float
        temp_type = "float"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[1] = comp_arguments[1]  

    # ============= second value ===================
    if (isinstance(comp_arguments[2], str)): # if string, sure to be a variable
        value = symbolTable[comp_arguments[2]]
        if ((isinstance(value, str)) or (value == None)): # value is not an integer or a float
            return f"ERROR: (Comparison) Value of '{comp_arguments[2]}' must be of type NUMBR or NUMBAR"
        else:
            if (isinstance(value, int)):
                temp_type = "integer"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value
            else:
                temp_type = "float"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value   
    elif (isinstance(comp_arguments[2], list)):       # if another comparison, BIGGR SMALLR OF
        value = get_comparison_value(comp_arguments[2], comp_type)
        if (isinstance(value, str)): return value
        if (isinstance(value, int)):
            temp_type = "integer"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[2] = value
        else:
            temp_type = "float"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[2] = value  
    elif (isinstance(comp_arguments[2], int)):             # integer
        temp_type = "integer"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[2] = comp_arguments[2]
    else:                                   # float
        temp_type = "float"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[2] = comp_arguments[2]  

    # ====== at this point, we can now compare the value of index 1 and 2 ========
    if (comp_arguments[0] == "BIGGR OF"):
        return max(to_evaluate[1], to_evaluate[2])
    else: # SMALLR OF
        return min(to_evaluate[1], to_evaluate[2])

def get_comparison_result(line):
    UNMATCH_TYPE_ERROR = f"ERROR: Values must be of the same type (NUMBR or NUMBAR)"
    comp_type = ""
    to_evaluate = [line[0], "", ""]
    # line[0] contains if == or !=

    # ============= first value ===================
    if (isinstance(line[1], str)): # if string, sure to be a variable
        value = symbolTable[line[1]]
        if ((isinstance(value, str)) or (value == None)): # value is not an integer or a float
            return f"ERROR: (Comparison) Value of '{line[1]}' must be of type NUMBR or NUMBAR"
        else:
            if (isinstance(value, int)):
                temp_type = "integer"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value
            else:
                temp_type = "float"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[1] = value   
    elif (isinstance(line[1], list)):       # if another comparison, BIGGR SMALLR OF
        value = get_comparison_value(line[1], comp_type)
        if (isinstance(value, str)): return value
        if (isinstance(value, int)):
            temp_type = "integer"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[1] = value
        else:
            temp_type = "float"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[1] = value  
    elif (isinstance(line[1], int)):             # integer
        temp_type = "integer"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[1] = line[1]
    else:                                   # float
        temp_type = "float"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[1] = line[1]  

    # ============= second value ===================
    if (isinstance(line[2], str)): # if string, sure to be a variable
        value = symbolTable[line[2]]
        if ((isinstance(value, str)) or (value == None)): # value is not an integer or a float
            return f"ERROR: (Comparison) Value of '{line[2]}' must be of type NUMBR or NUMBAR"
        else:
            if (isinstance(value, int)):
                temp_type = "integer"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value
            else:
                temp_type = "float"
                if (comp_type == ""): comp_type = temp_type
                else:
                    if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
                to_evaluate[2] = value   
    elif (isinstance(line[2], list)):       # if another comparison, BIGGR SMALLR OF
        value = get_comparison_value(line[2], comp_type)
        if (isinstance(value, str)): return value
        if (isinstance(value, int)):
            temp_type = "integer"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[2] = value
        else:
            temp_type = "float"
            if (comp_type == ""): comp_type = temp_type
            else:
                if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
            to_evaluate[2] = value  
    elif (isinstance(line[2], int)):             # integer
        temp_type = "integer"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[2] = line[2]
    else:                                   # float
        temp_type = "float"
        if (comp_type == ""): comp_type = temp_type
        else:
            if (comp_type != temp_type): return UNMATCH_TYPE_ERROR
        to_evaluate[2] = line[2]  

    # ====== at this point, we can now compare the value of index 1 and 2 ========
    if (line[0] == "BOTH SAEM"):
        if (to_evaluate[1] == to_evaluate[2]): return True
        else: return False
    else: # DIFFRINT
        if (to_evaluate[1] != to_evaluate[2]): return True
        else: return False



def convert_value_to_bool(value):
    if (value in ['WIN', 'FAIL']): # value is already a TROOF
        return value
    elif (isinstance(value, str)): # value is YARN
        if (len(value) > 0): return 'WIN'
        else: return 'FAIL'
    else:                          # value will now fall on either NUMBR or NUMBAR
        if (value > 0): return 'WIN'
        else: return 'FAIL'

# use this to get the value of boolean operation
def get_bool_result(line):
    if (line[0] in ["BOTH OF", "EITHER OF", "WON OF"]):
        bool_arguments = [line[0], line[1], line[2]]
        result = get_bool_result_2(bool_arguments)
    elif (line[0] == "NOT"):
        bool_arguments = [line[0], line[1]]
        result = get_bool_result_not(bool_arguments)
    else:
        result = get_bool_result_all(line)

    result = True if result=="WIN" else False

    return result

def get_bool_result_all(bool_arguments):

    for i in range(1, len(bool_arguments)):
        
        temp = ""
        if ((bool_arguments[i][0] == "TROOF Literal")): # if already a TROOF
            temp = bool_arguments[i][1]
        else: 
            if (bool_arguments[i][0] in ["BOTH OF", "EITHER OF", "WON OF"]): 
                temp = get_bool_result_2(bool_arguments[i])
            elif (bool_arguments[i][0] in ["NOT"]): 
                temp = get_bool_result_not(bool_arguments[i])
            elif (bool_arguments[i][0] == "NUMBR Literal"):
                if (int(bool_arguments[i][1]) > 0): temp = 'WIN'
                else: temp = 'FAIL'
            elif (bool_arguments[i][0] == "NUMBAR Literal"):
                if (float(bool_arguments[i][1]) > 0): temp = 'WIN'
                else: temp = 'FAIL'
            elif (bool_arguments[i][0] == "YARN Literal"):
                if (len(bool_arguments[i][1]) > 0): temp = 'WIN'
                else: temp = 'FAIL'
            elif (bool_arguments[i][0] == "Variable Identifier"): # get value from symbol table
                var = bool_arguments[i][1]
                if (symbolTable[var] == None): temp = 'FAIL'
                else: temp = convert_value_to_bool(symbolTable[var])
        # checker if break from loop
        x = True if temp == 'WIN' else False

        if(bool_arguments[0] == "ALL OF"): # infinite and (break if false)
            if (not x): return "FAIL" 
        else:                              # infinite or (break if true)
            if (x): return "WIN"

    if(bool_arguments[0] == "ALL OF"): # infinite and (did not break, so return true)
        return "WIN" 
    else:                              # infinite or (did not break, so return false)
        return "FAIL"

def get_bool_result_not(bool_arguments):
    second_arg = bool_arguments[1]

    # =========== second argument ============ (first operand)
    if ((second_arg[0] == "TROOF Literal")): # if already a TROOF
        bool_arguments[1] = second_arg[1]
    else:
        if (second_arg[0] in ["BOTH OF", "EITHER OF", "WON OF"]): 
            bool_arguments[1] = get_bool_result_2(second_arg)
        elif (second_arg[0] in ["NOT"]): 
            bool_arguments[1] = get_bool_result_not(second_arg)
        elif (second_arg[0] in ["ANY OF", "ALL OF"]):
            bool_arguments[1] = get_bool_result_all(second_arg)
        elif (second_arg[0] == "NUMBR Literal"):
            if (int(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "NUMBAR Literal"):
            if (float(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "YARN Literal"):
            if (len(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "Variable Identifier"): # get value from symbol table
            var = second_arg[1]
            if (symbolTable[var] == None): bool_arguments[1] = 'FAIL'
            else: bool_arguments[1] = convert_value_to_bool(symbolTable[var])

    # ======= at this point, value can now be evaluated using second argument =========
    x = True if bool_arguments[1] == 'WIN' else False
    if (x): return 'FAIL'
    else: return 'WIN'
     
def get_bool_result_2(bool_arguments):
    first_arg = bool_arguments[0]
    second_arg = bool_arguments[1]
    third_arg = bool_arguments[2]

    # =========== second argument ============ (first operand)
    if ((second_arg[0] == "TROOF Literal")): # if already a TROOF
        bool_arguments[1] = second_arg[1]
    else:
        if (second_arg[0] in ["BOTH OF", "EITHER OF", "WON OF"]): # if not, do your thing
            bool_arguments[1] = get_bool_result_2(second_arg)
        elif (second_arg[0] in ["NOT"]): 
            bool_arguments[1] = get_bool_result_not(second_arg)
        elif (second_arg[0] in ["ANY OF", "ALL OF"]):
            bool_arguments[1] = get_bool_result_all(second_arg)
        elif (second_arg[0] == "NUMBR Literal"):
            if (int(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "NUMBAR Literal"):
            if (float(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "YARN Literal"):
            if (len(second_arg[1]) > 0): bool_arguments[1] = 'WIN'
            else: bool_arguments[1] = 'FAIL'
        elif (second_arg[0] == "Variable Identifier"): # get value from symbol table
            var = second_arg[1]
            if (symbolTable[var] == None): bool_arguments[1] = 'FAIL'
            else: bool_arguments[1] = convert_value_to_bool(symbolTable[var])

    # =========== third argument ============ (second operand)
    if ((third_arg[0] == "TROOF Literal")): # if already a TROOF
        bool_arguments[2] = third_arg[1]
    else:
        if (third_arg[0] in ["BOTH OF", "EITHER OF", "WON OF"]): # if not, do your thing
            bool_arguments[2] = get_bool_result_2(third_arg)
        elif (third_arg[0] in ["NOT"]): 
            bool_arguments[2] = get_bool_result_not(third_arg)
        elif (second_arg[0] in ["ANY OF", "ALL OF"]):
            bool_arguments[2] = get_bool_result_all(third_arg)
        elif (third_arg[0] == "NUMBR Literal"):
            if (int(third_arg[1]) > 0): bool_arguments[2] = 'WIN'
            else: bool_arguments[2] = 'FAIL'
        elif (third_arg[0] == "NUMBAR Literal"):
            if (float(third_arg[1]) > 0): bool_arguments[2] = 'WIN'
            else: bool_arguments[2] = 'FAIL'
        elif (third_arg[0] == "YARN Literal"):
            if (len(third_arg[1]) > 0): bool_arguments[2] = 'WIN'
            else: bool_arguments[2] = 'FAIL'
        elif (third_arg[0] == "Variable Identifier"): # get value from symbol table
            var = third_arg[1]
            if (symbolTable[var] == None): bool_arguments[2] = 'FAIL'
            else: bool_arguments[2] = convert_value_to_bool(symbolTable[var])

    # ======= at this point, value can now be evaluated using second and third argument =========
    x = True if bool_arguments[1] == 'WIN' else False
    y = True if bool_arguments[2] == 'WIN' else False
    print(f" ====== {bool_arguments[1]} :::: {bool_arguments[2]}")

    if (first_arg == "BOTH OF"): # and
        if (x and y): return 'WIN'
        else: return 'FAIL'
    elif (first_arg == "EITHER OF"): # or
        if (x or y): return 'WIN'
        else: return 'FAIL'
    else:                         # fall in xor
        if (x ^ y): return 'WIN'
        else: return 'FAIL'      


def semantic_main():
    syntax = syntactic_analyzer.syntax_main()

    # print("==============")
    # print(syntax.getResult().print_tree())

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