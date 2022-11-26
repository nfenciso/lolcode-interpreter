import syntactic_analyzer

symbolTable = {
    "IT": None
}

switchCases = []

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
            symbolTable["IT"] = symbolTable[line[0][1]]
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
            if (eval):  semanticAnalyze(ifList)
            elif (len(elseList) != 0 and not eval):
                semanticAnalyze(elseList)

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
                    print("$"+str(frontRemoved))
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
                    caseList = []
                    print("$")
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
            for i in switchCases:
                print(i)

        elif (line[0] == "<boolean_operation>"):
            cnt += 1
            line = lst[cnt]
            result = get_bool_result(line)

            symbolTable["IT"] = result

        else:
            pass
            
        cnt += 1
    return 1

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
        print(f"this is the result: {temp}")

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
        bool_arguments[1] = third_arg[1]
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