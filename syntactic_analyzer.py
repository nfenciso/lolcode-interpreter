import random
import lexical_analyzer


canBeLevelTwo = ["Arithmetic Operation","Output Keyword","Variable Declaration","Code Delimiter CLOSE"]
mathRelatedLex = ["Arithmetic Operation","Operand Separator","NUMBR Literal","NUMBAR Literal","YARN Literal","TROOF Literal","Variable Identifier","String Delimiter"]
literals = ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "String Delimiter"]
expressions = ["Arithmetic Operation"]
types = ["NUMBAR keyword", "NUMBR keyword", "YARN keyword", "TROOF keyword"]
boolTwoOperands = ["BOTH OF", "EITHER OF", "WON OF"]
boolMoreOperand = ["ANY OF", "ALL OF"]
comparator = ["BIGGR OF", "SMALLR OF", "BOTH SAEM", "DIFFRINT"]

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    
    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 4
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + str(self.data))
        if self.children:
            for child in self.children:
                child.print_tree()

class Parser:
    def __init__(self, tokens, arg):
        self.tokens = tokens
        self.tok_idx = -1
        self.error = "NONE"
        self.HAI_used = False
        if (arg == 1):
            self.isMain = 1
        else:
            self.isMain = 0
            self.tree = arg
        self.advance()
        self.startParse()
    
    def advance(self):
        self.tok_idx += 1
        if (self.tok_idx < len(self.tokens)):
            self.curr_tok = self.tokens[self.tok_idx]
        else:
            self.curr_tok = "END OF TOKENS"
        return self.curr_tok
    
    def goBackToSpecificIdx(self, index):
        self.tok_idx = index - 1
        return self.advance()
    
    def startParse(self):
        if (self.isMain == 1):
            if (self.curr_tok[0] == "Code Delimiter OPEN"):
                self.tree = TreeNode("<program>")
                numOfLvlTwoNodes = self.lookAhead()
                #print(numOfLvlTwoNodes)
                self.parse(numOfLvlTwoNodes)
                if (self.error != "NONE"):
                    return self.error
                else:
                    return 1
            else:
                self.error = "ERROR: Must begin the program with HAI"
                return self.error
        elif (self.isMain == 0):
            # self.tree = 
            #
            numOfLvlTwoNodes = self.lookAhead()
            self.parse(numOfLvlTwoNodes)
            if (self.error != "NONE"):
                    return self.error
            else:
                return 1

    def lookAhead(self):
        
        return self.tokens.count(["NEWLINE", "\\n"])

    def getResult(self):
        if (self.error != "NONE"):
            return self.error
        else:
            return self.tree

    def parse(self, numOfLvlTwoNodes):
        nodeContent = []
        finishedNode = True
        cnt = numOfLvlTwoNodes
        while (cnt > 0): 
            #print(self.curr_tok)
            if (self.curr_tok[0] == "Code Delimiter OPEN"):
                if (not self.HAI_used):
                    self.tree.add_child(TreeNode(self.curr_tok))
                    self.advance()
                    if (self.curr_tok[0] == "NEWLINE"):
                        self.advance()
                        self.HAI_used = True
                    else:
                        self.error = "ERROR: There must not be anything after HAI"
                        return self.error
                else:
                    self.error = "ERROR: Can only use HAI once"
                    return self.error   
            elif (self.curr_tok[0] == "Variable Declaration"):
                if (self.isMain != 1):
                    self.error = "ERROR: Variables must not be declared inside any program block (if-else, loops, etc)"
                nodeContent = []
                nodeContent.append(self.curr_tok)
                self.advance()
                if (self.curr_tok[0] == "Variable Identifier"):
                    nodeContent.append(self.curr_tok)
                    self.advance()
                    if (self.curr_tok[0] == "NEWLINE"):
                        self.tree.add_child(TreeNode(nodeContent))
                        self.advance()
                        nodeContent = []
                    else:
                        if (self.curr_tok[0] == "Variable Assignment"):
                            nodeContent.append(self.curr_tok)
                            self.advance()
                            if (self.curr_tok[0] == "String Delimiter"):
                                nodeContent.append(self.curr_tok)
                                self.advance()
                                nodeContent.append(self.curr_tok)
                                self.advance()
                                nodeContent.append(self.curr_tok)
                                self.advance()
                                if (self.curr_tok[0] == "NEWLINE"):
                                    self.tree.add_child(TreeNode(nodeContent))
                                    self.advance()
                                    nodeContent = []
                                else:
                                    self.error = "ERROR: ITZ expression must only have one argument"
                            elif (self.curr_tok[0] == "NUMBR Literal" or self.curr_tok[0] == "NUMBAR Literal" or self.curr_tok[0] == "TROOF Literal"):
                                nodeContent.append(self.curr_tok)
                                self.advance()
                                if (self.curr_tok[0] == "NEWLINE"):
                                    self.tree.add_child(TreeNode(nodeContent))
                                    self.advance()
                                    nodeContent = []
                                else:
                                    self.error = "ERROR: ITZ expression must only have one argument"
                                    return self.error
                            elif (self.curr_tok[0] == "Arithmetic Operation"):
                                finishedNode = False
                                continue
                            elif (self.curr_tok[0] == "Boolean Operation"):
                                nodeContent.append("<boolean_operation>")
                                self.tree.add_child(TreeNode(nodeContent))
                                
                                boolList = generateBooleanStatement(self) 

                                if (isinstance(boolList, str)):
                                    self.error = boolList
                                    return self.error
                                else:
                                    self.tree.children[len(self.tree.children)-1].add_child(TreeNode(boolList))
                                    self.advance()
                            elif (self.curr_tok[0] == "Comparison Operation"):
                                nodeContent.append("<comparison_operation>")

                                self.tree.add_child(TreeNode(nodeContent))
                                operand_type = ["NULL"]
                                compareList = getComparison(self, operand_type)

                                if (isinstance(compareList, str)):
                                    self.error = compareList
                                    return self.error
                                else:
                                    self.tree.children[len(self.tree.children)-1].add_child(TreeNode(compareList))
                                    self.advance()
                            else:
                                self.error = "ERROR: ITZ expression must have a value, variable, or expression as argument"
                                return self.error
                        else:
                            self.error = "ERROR: There must be an ITZ after the variable"
                            return self.error
                else:
                    self.error = "ERROR: There must be a Variable Identifier after I HAS A"
                    return self.error
            elif (self.curr_tok[0] == "Arithmetic Operation"):
                mathList = []
                mathList.append(self.curr_tok)
                self.advance()
                while (True):
                    if (self.curr_tok[0] in mathRelatedLex):
                        if (self.curr_tok[0] != "String Delimiter"):
                            mathList.append(self.curr_tok)
                        self.advance()
                    else:
                        break
                evalMathList = checkIfValidMathSyntax(mathList)
                if (isinstance(evalMathList, str)):
                    self.error = evalMathList
                    return self.error
                else:
                    if (not finishedNode):
                        nodeContent.append("<math_arguments>")
                        self.tree.add_child(TreeNode(nodeContent))
                        self.tree.children[len(self.tree.children)-1].add_child(TreeNode(mathList)) # connect to last child
                        finishedNode = True
                        if (nodeContent[0] == "<loop>"):
                            if (self.curr_tok[0] == "NEWLINE"):
                                self.advance()

                                while (1):
                                    if (self.curr_tok[0] == "Loop Delimiter CLOSE"):
                                        loopList.append(self.curr_tok)
                                        self.advance()
                                        if (self.curr_tok[0] == "Loop Identifier"):
                                            if (loopLabel == self.curr_tok[1]):
                                                loopList.pop()
                                                self.advance()
                                                if (self.curr_tok[0] == "NEWLINE"):
                                                    break
                                                else:
                                                    self.error = "ERROR: IM OUTTA YR <label> must be alone in its line"
                                                    return self.error
                                            else:
                                                continue
                                    if (self.curr_tok == "END OF TOKENS"):
                                        self.error = "ERROR: Lacking IM OUTTA YR"
                                        return self.error
                                    loopList.append(self.curr_tok)
                                    self.advance()
                                #print(loopList)
                                loopSyntax = Parser(loopList, TreeNode("<loop content>"))
                                loopList = []
                                if (isinstance(loopSyntax.getResult(), str)):
                                    self.error = loopSyntax.getResult()
                                    return self.error
                                else:
                                    self.tree.children[len(self.tree.children)-1].add_child(loopSyntax.getResult())
                            else:
                                self.error = "ERROR: Unexpected end of Loop IM IN YR line"
                                return self.error
                    else:
                        self.tree.add_child(TreeNode(mathList))
                    nodeContent = []
                    if (self.curr_tok[0] == "NEWLINE"):
                        self.advance()
                        continue
                    else:
                        self.error = "ERROR: Unexpected end of arithmetic expression"
                        return self.error
            elif (self.curr_tok[0] == "Output Keyword"):
                outputList = []
                outputList.append(self.curr_tok)
                outputList.append("<output_arguments>")
                self.tree.add_child(TreeNode(outputList))
                outputList = [] # unused?
                self.advance()
                while (1):
                    #print("XX", self.curr_tok)
                    if (self.curr_tok[0] == "NEWLINE"):
                        self.advance()
                        break
                    if (self.curr_tok[0] in ["Variable Identifier","NUMBAR Literal","NUMBR Literal","TROOF Literal"]):
                        self.tree.children[len(self.tree.children)-1].add_child(TreeNode(self.curr_tok))
                        self.advance()
                    elif (self.curr_tok[0] == "String Delimiter"):
                        self.tree.children[len(self.tree.children)-1].add_child(TreeNode(self.curr_tok))
                        self.advance()
                        self.tree.children[len(self.tree.children)-1].add_child(TreeNode(self.curr_tok))
                        self.advance()
                        self.tree.children[len(self.tree.children)-1].add_child(TreeNode(self.curr_tok))
                        self.advance()
                        #print(self.curr_tok)
                    elif (self.curr_tok[0] == "Arithmetic Operation"):
                        mathList = []
                        mathList.append(self.curr_tok)
                        self.advance()
                        while (True):
                            #print(self.curr_tok)
                            if (self.curr_tok[0] in mathRelatedLex):
                                if (self.curr_tok[0] != "String Delimiter"):
                                    mathList.append(self.curr_tok)
                                self.advance()
                            else:
                                break
                        evalMathList = checkIfValidMathSyntax(mathList)
                        #stringsNotIncluded = 0


                        while (1):
                            if (isinstance(evalMathList, str)):
                                if (evalMathList == "ERROR: Lacking arithmetic operation"):
                                    if (mathList[len(mathList)-1][0] == "YARN Literal"): 
                                        mathList.pop()
                                        self.tok_idx -= 5
                                        self.advance()
                                        if (mathList[len(mathList)-1][0] == "Operand Separator"):
                                            mathList.pop()
                                            evalMathList = evalMathList = checkIfValidMathSyntax(mathList)
                                    elif (mathList[len(mathList)-1][0] in ["Variable Identifier", "TROOF Literal","NUMBR Literal","NUMBAR Literal"]): 
                                        mathList.pop()
                                        self.tok_idx -= 3
                                        self.advance()
                                        if (mathList[len(mathList)-1][0] == "Operand Separator"):
                                            mathList.pop()
                                            evalMathList = evalMathList = checkIfValidMathSyntax(mathList)
                                    elif (mathList[len(mathList)-1][0] in "Operand Separator"):
                                        mathList.pop()
                                        self.tok_idx -= 2
                                        self.advance()
                                        evalMathList = evalMathList = checkIfValidMathSyntax(mathList)
                                    else:
                                        break
                                else: break
                            else: break
                            #print(evalMathList)

                        if (isinstance(evalMathList, str)):
                            self.error = evalMathList
                            return self.error
                        else:
                            self.tree.children[len(self.tree.children)-1].add_child(TreeNode("<math_arguments>"))
                            child = self.tree.children[len(self.tree.children)-1]
                            child.children[len(child.children)-1].add_child(TreeNode(mathList))
                    elif (self.curr_tok[0] == "Boolean Operation"):
                        boolList = generateBooleanStatement(self)
                        if (isinstance(boolList, str)):
                            self.error = boolList
                            return self.error
                        else:
                            self.tree.children[len(self.tree.children)-1].add_child(TreeNode("<boolean_operation>"))
                            child = self.tree.children[len(self.tree.children)-1]
                            child.children[len(child.children)-1].add_child(TreeNode(boolList))

                    elif (self.curr_tok[0] == "Comparison Operation"):
                        operand_type = ["NULL"]
                        compareList = getComparison(self, operand_type)

                        if (isinstance(compareList, str)):
                            self.error = compareList
                            return self.error
                        else:
                            self.tree.children[len(self.tree.children)-1].add_child(TreeNode("<comparison_operation>"))
                            child = self.tree.children[len(self.tree.children)-1]
                            child.children[len(child.children)-1].add_child(TreeNode(compareList))
                    elif (self.curr_tok[0] == "Operand Separator"):
                        self.advance()
                        if (self.curr_tok[0] == "NEWLINE"):
                            self.error = "ERROR: Extra AN at end of VISIBLE line"
                            return self.error
                        continue
                    else:
                        self.error = "ERROR: (VISIBLE) Token not valid: " + str(self.curr_tok)
                        return self.error
                    #comparison
            elif (self.curr_tok[0] == "Input Keyword"): 
                inputList = []
                inputList.append(self.curr_tok)
                # inputList.append("<output_arguments>")
                self.advance()
                if (self.curr_tok[0] == "Variable Identifier"):
                    inputList.append(self.curr_tok)
                    self.advance()
                    if (self.curr_tok[0] == "NEWLINE"):
                        self.advance()
                        self.tree.add_child(TreeNode(inputList))

                    else:
                        self.error = "ERROR: Unexpected non-variable identifier"
                        return self.error
                else:
                    self.error = "ERROR: Must be variable identifier to store the input"
                    return self.error
                # pass      
            elif (self.curr_tok[0] == "Variable Identifier"):
                # assignList = []
                # assignList.append("<assignment_arguments>")
                # self.tree.add_child(TreeNode(assignList))
                assignList = []
                assignList.append(self.curr_tok)
                self.advance()
                if (self.curr_tok[0] == "NEWLINE"):
                    # self.tree.children[len(self.tree.children)-1].add_child(TreeNode(assignList))
                    self.tree.add_child(TreeNode(assignList))

                    self.advance()
                elif (self.curr_tok[0] == "Assignment Keyword"): # using R
                    assignList.append(self.curr_tok)
                    self.advance()
                    if (self.curr_tok[0] in literals): # assigning literal
                        assignList.append(self.curr_tok)
                        self.advance()
                        if (self.curr_tok[0] == "NEWLINE"):
                            # self.tree.children[len(self.tree.children)-1].add_child(TreeNode(assignList))
                            self.tree.add_child(TreeNode(assignList))

                            self.advance()
                        else:
                            self.error = "ERROR: (R) Must only assign single literal at a time"
                            return self.error
                    elif (self.curr_tok[0] in expressions): # assigning value from expression
                        if (self.curr_tok[0] == "Arithmetic Operation"):
                            assignList.append("<math_arguments>")
                            # self.tree.children[len(self.tree.children)-1].add_child(TreeNode(assignList))
                            self.tree.add_child(TreeNode(assignList))

                            mathList = []
                            mathList.append(self.curr_tok)
                            self.advance()
                            while (True):
                                if (self.curr_tok[0] in mathRelatedLex):
                                    if (self.curr_tok[0] != "String Delimiter"):
                                        mathList.append(self.curr_tok)
                                    self.advance()
                                else:
                                    break
                            evalMathList = checkIfValidMathSyntax(mathList)
                            if (isinstance(evalMathList, str)):
                                self.error = evalMathList
                                return self.error
                            else:
                                child = self.tree.children[len(self.tree.children)-1]
                                child.add_child(TreeNode(mathList))
                                self.advance()
                                # self.tree.children[len(self.tree.children)-1].add_child(TreeNode("<math_arguments>"))
                    elif (self.curr_tok[0] == "Typecast Keyword (new value)"):  # reassign (MAEK)
                        assignList.append("<typecasted_value>")
                        # self.tree.children[len(self.tree.children)-1].add_child(TreeNode(assignList))
                        self.tree.add_child(TreeNode(assignList))
                        maekList = []
                        maekList.append(self.curr_tok)
                        self.advance()
                        if (self.curr_tok[0] == "Variable Identifier"):
                            maekList.append(self.curr_tok)
                            to_be_casted = self.curr_tok # not yet used (can check the value here if it can be casted. ex. "wow" -> NUMBR, error)
                            self.advance()
                            if (self.curr_tok[0] in types):
                                maekList.append(self.curr_tok)
                                self.advance()
                                if (self.curr_tok[0] == "NEWLINE"):
                                    child = self.tree.children[len(self.tree.children)-1]
                                    child.add_child(TreeNode(maekList))
                                    self.advance()
                                    # child.children[len(child.children)-1].add_child(TreeNode(maekList))
                                    # self.tree.children[len(self.tree.children)-1].add_child(TreeNode(assignList))
                                else:
                                    self.error = "ERROR: (MAEK) only accepts two arguments"
                            else:
                                self.error = "ERROR: (MAEK) second argument should be a variable type"
                                return self.error   
                        else:
                            self.error = "ERROR: (MAEK) first argument should be a variable"
                            return self.error      
                    else:
                        self.error = "ERROR: Must assign value to the variable identifier"
                        return self.error
                elif (self.curr_tok[0] == "Typecast Keyword"): # IS NOW A
                    assignList.append(self.curr_tok)
                    self.advance()
                    if (self.curr_tok[0] in types):
                        assignList.append(self.curr_tok)
                        self.advance()
                        if (self.curr_tok[0] == "NEWLINE"):
                            self.tree.add_child(TreeNode(assignList))
                            self.advance()
                        else:
                            self.error = "ERROR: (IS NOW A) only accepts single argument"
                            return self.error

                    else:
                        self.error = "ERROR: (IS NOW A) only accepts variable type)"
                        return self.error
            elif (self.curr_tok[0] == "Typecast Keyword (new value)"):  # reassign (MAEK)
                assignList = []
                assignList.append("<typecasted_value>")
                # self.tree.children[len(self.tree.children)-1].add_child(TreeNode(assignList))
                self.tree.add_child(TreeNode(assignList))
                maekList = []
                maekList.append(self.curr_tok)
                self.advance()
                if (self.curr_tok[0] == "Variable Identifier"):
                    maekList.append(self.curr_tok)
                    to_be_casted = self.curr_tok # not yet used (can check the value here if it can be casted. ex. "wow" -> NUMBR, error)
                    self.advance()
                    if (self.curr_tok[0] in types):
                        maekList.append(self.curr_tok)
                        self.advance()
                        if (self.curr_tok[0] == "NEWLINE"):
                            child = self.tree.children[len(self.tree.children)-1]
                            child.add_child(TreeNode(maekList))
                            self.advance()
                            # child.children[len(child.children)-1].add_child(TreeNode(maekList))
                            # self.tree.children[len(self.tree.children)-1].add_child(TreeNode(assignList))
                        else:
                            self.error = "ERROR: (MAEK) only accepts two arguments"
                    else:
                        self.error = "ERROR: (MAEK) second argument should be a variable type"
                        return self.error   
                else:
                    self.error = "ERROR: (MAEK) first argument should be a variable"
                    return self.error
            elif (self.curr_tok[0] == "Code Delimiter CLOSE"):
                self.tree.add_child(TreeNode(self.curr_tok))
                self.advance()
                while (self.curr_tok[0] == "NEWLINE"):
                    self.advance()
                if (self.curr_tok == "END OF TOKENS"):
                    # self.advance()
                # else:
                    #print(self.curr_tok)
                    break
                else:
                    self.error = "ERROR: There must not be anything after KTHXBYE"
                    return self.error
            # else:
            #     self.error = "ERROR: Unknown function (or not yet implemented)"
            #     return self.error

            elif (self.curr_tok[0] == "If-Then Delimiter"):
                self.tree.add_child(TreeNode("<if-then block>"))
                ifList = []
                # skip appending O RLY?
                self.advance()
                if (self.curr_tok[0] == "NEWLINE"):
                    self.advance()
                else:
                    self.error = "ERROR: O RLY? must be alone in its line"
                if (self.curr_tok[0] == "If Keyword"):
                    # skip appending YA RLY
                    self.advance()
                else:
                    self.error = "ERROR: Must have YA RLY"
                    return self.error
                if (self.curr_tok[0] == "NEWLINE"):
                    self.advance()
                else:
                    self.error = "ERROR: YA RLY must be alone in its line"
                while (1):
                    if (self.curr_tok[0] == "Else Keyword" or self.curr_tok[0] == "Conditional Delimiter"):
                        break
                    if (self.curr_tok == "END OF TOKENS"):
                        self.error = "ERROR: Lacking OIC"
                        return self.error
                    ifList.append(self.curr_tok)
                    self.advance()
                ifSyntax = Parser(ifList, TreeNode("<if>"))
                print(ifList)
                if (isinstance(ifSyntax.getResult(), str)):
                    self.error = ifSyntax.getResult()
                    return self.error
                else:
                    self.tree.children[len(self.tree.children)-1].add_child(ifSyntax.getResult())

                ifList = []
                # skip appending OIC or NO WAI
                if (self.curr_tok[0] == "Else Keyword"):
                    self.advance()
                    if (self.curr_tok[0] == "NEWLINE"):
                        self.advance()
                    else:
                        self.error = "ERROR: NO WAI must be alone in its line"
                    while (1):
                        if (self.curr_tok[0] == "Else Keyword"):
                            self.error = "ERROR: There cannot be more than one NO WAI of the same level in a single IF-THEN code block"
                            return self.error
                        if (self.curr_tok[0] == "Conditional Delimiter"):
                            break
                        if (self.curr_tok == "END OF TOKENS"):
                            self.error = "ERROR: Lacking OIC"
                            return self.error
                        ifList.append(self.curr_tok)
                        self.advance()
                    
                    elseSyntax = Parser(ifList, TreeNode("<else>"))
                    if (isinstance(elseSyntax.getResult(), str)):
                        self.error = elseSyntax.getResult()
                        return self.error
                    else:
                        self.tree.children[len(self.tree.children)-1].add_child(elseSyntax.getResult())
                
                self.advance()
                if (self.curr_tok[0] == "NEWLINE"):
                    self.advance()
                else:
                    self.error = "ERROR: OIC must be alone in its line"
                    return self.error
                
            elif (self.curr_tok[0] == "Boolean Operation"):
                boolList = []
                boolList.append("<boolean_operation>")
                self.tree.add_child(TreeNode(boolList))
                
                boolList = generateBooleanStatement(self) 

                if (isinstance(boolList, str)):
                    self.error = boolList
                    return self.error
                else:
                    self.tree.children[len(self.tree.children)-1].add_child(TreeNode(boolList))
                    self.advance()
                
            elif (self.curr_tok[0] == "Comparison Operation"):
                compareList = []
                compareList.append("<comparison_operation>")
                # self.tree.children[len(self.tree.children)-1].add_child(TreeNode(assignList))
                self.tree.add_child(TreeNode(compareList))
                operand_type = ["NULL"]
                compareList = getComparison(self, operand_type)

                if (isinstance(compareList, str)):
                    self.error = compareList
                    return self.error
                else:
                    self.tree.children[len(self.tree.children)-1].add_child(TreeNode(compareList))
                    self.advance()

            elif (self.curr_tok[0] in literals):

                if (self.curr_tok[0] == "String Delimiter"):
                    self.advance()
                    self.tree.add_child(TreeNode(self.curr_tok))
                    self.advance()
                    self.advance()
                else:
                    self.tree.add_child(TreeNode(self.curr_tok))
                    self.advance()

                if (self.curr_tok[0] == "NEWLINE"):
                    self.advance()
                else:
                    self.error = "ERROR: Starting a line with literal must only contain one token"
            
            
            elif (self.curr_tok[0] == "Switch-Case Delimiter"):
                self.tree.add_child(TreeNode("<switch-case block>"))
                hasAtLeastOneCase = False
                calledDefault = False
                switchList = []
                #switchList.append(self.curr_tok)
                self.advance()
                if (self.curr_tok[0] == "NEWLINE"):
                    #switchList.append(self.curr_tok)
                    self.advance()
                else:
                    self.error = "ERROR: WTF? must be alone in its line"
                while (1):

                    if (self.curr_tok[0] == "Case Keyword" and not calledDefault):
                        #switchList.append(self.curr_tok)
                        switchList = []
                        self.advance()
                        if (self.curr_tok[0] in ["String Delimiter","NUMBAR Literal","NUMBR Literal","TROOF Literal"]):
                            caseValue = ""
                            if (self.curr_tok[0] == "String Delimiter"):
                                #switchList.append(self.curr_tok)
                                self.advance()
                                #switchList.append(self.curr_tok)
                                caseValue = "\""+self.curr_tok[1]+"\""
                                self.advance()
                                #switchList.append(self.curr_tok)
                                self.advance()
                            else:
                                #switchList.append(self.curr_tok)
                                caseValue = self.curr_tok[1]
                                self.advance()

                            if (self.curr_tok[0] == "NEWLINE"):
                                #switchList.append(self.curr_tok)
                                self.advance()
                                print("x",self.curr_tok)
                                while (1):
                                    if (self.curr_tok[0] in ["Case Keyword", "Default Case Keyword", "Conditional Delimiter"]):
                                        break
                                    if (self.curr_tok == "END OF TOKENS"):
                                        self.error = "ERROR: Switch-case must end with OIC"
                                        return self.error
                                    switchList.append(self.curr_tok)
                                    self.advance()

                                switchSyntax = Parser(switchList, TreeNode("<case: "+caseValue+">"))
                                if (isinstance(switchSyntax.getResult(), str)):
                                    self.error = switchSyntax.getResult()
                                    return self.error
                                else:
                                    self.tree.children[len(self.tree.children)-1].add_child(switchSyntax.getResult())

                                switchList = []
                                if (self.curr_tok[0] in ["Case Keyword", "Default Case Keyword", "Conditional Delimiter"]):
                                    hasAtLeastOneCase = True
                                    continue

                            else:
                                self.error = "ERROR: OMG and one literal must be alone in their own line"
                                return self.error
                        else:
                            self.error = "ERROR: There must be a constant value next to OMG"
                            return self.error
                    elif (not hasAtLeastOneCase and self.curr_tok[0] not in ["Case Keyword", "Default Case Keyword", "Conditional Delimiter"]):
                        self.error = "ERROR: Must have OMG"
                        return self.error

                    elif (self.curr_tok[0] == "Default Case Keyword" and not calledDefault and hasAtLeastOneCase):
                        calledDefault = True
                        self.advance()
                        if (self.curr_tok[0] == "NEWLINE"):
                            self.advance()
                            switchList = []
                            while (1):
                                if (self.curr_tok[0] == "Conditional Delimiter"):
                                    break
                                if (self.curr_tok[0] == "Default Case Keyword"):
                                    self.error = "ERROR: OMGWTF can only be used once"
                                    return self.error
                                if (self.curr_tok[0] == "Case Keyword"):
                                    self.error = "ERROR: OMG cannot be used after OMGWTF"
                                    return self.error
                                if (self.curr_tok == "END OF TOKENS"):
                                    self.error = "ERROR: Switch-case must end with OIC"
                                    return self.error
                                switchList.append(self.curr_tok)
                                self.advance()
                                print(self.curr_tok)
                            print(switchList)
                            switchSyntax = Parser(switchList, TreeNode("<default_case>"))
                            if (isinstance(switchSyntax.getResult(), str)):
                                self.error = switchSyntax.getResult()
                                return self.error
                            else:
                                self.tree.children[len(self.tree.children)-1].add_child(switchSyntax.getResult())
                            switchList = []
                        else:
                            self.error = "ERROR: OMGWTF must be alone in its line"
                            return self.error
                    elif (self.curr_tok[0] == "Conditional Delimiter" and hasAtLeastOneCase):
                        self.advance()
                        if (self.curr_tok[0] == "NEWLINE"):           
                            self.advance()                     
                            break
                        else:
                            self.error = "ERROR: OIC must be alone in its line"
                            return self.error
                    elif (self.curr_tok[0] == "Default Case Keyword" and not hasAtLeastOneCase):
                        self.error = "ERROR: Must have at least one OMG"
                        return self.error
            elif (self.curr_tok[0] == "Break Keyword" and self.isMain == 0 and ("case" in self.tree.data)):
                self.tree.add_child(TreeNode(self.curr_tok))
                self.advance()
                if (self.curr_tok[0] != "NEWLINE"):
                    self.error = "ERROR: GTFO must be alone in its line"
                    return self.error
                self.advance()
            elif (self.curr_tok[0] == "Loop Delimiter OPEN"):
                loopList = []
                loopLabel = ""
                loopCondition = ""
                self.advance()
                if (self.curr_tok[0] == "Loop Identifier"):
                    loopLabel = self.curr_tok[1]
                    self.advance()
                    if (self.curr_tok[0] == "Loop Operation"):
                        self.advance()
                        if (self.curr_tok[0] == "Loop Keyword"):
                            self.advance()
                            if (self.curr_tok[0] == "Variable Identifier"):
                                self.advance()
                                if (self.curr_tok[0] == "NEWLINE"):
                                    self.advance()

                                    while (1):
                                        if (self.curr_tok[0] == "Loop Delimiter CLOSE"):
                                            loopList.append(self.curr_tok)
                                            self.advance()
                                            if (self.curr_tok[0] == "Loop Identifier"):
                                                if (loopLabel == self.curr_tok[1]):
                                                    loopList.pop()
                                                    self.advance()
                                                    if (self.curr_tok[0] == "NEWLINE"):
                                                        self.advance()
                                                        break
                                                    else:
                                                        self.error = "ERROR: IM OUTTA YR <label> must be alone in its line"
                                                        return self.error
                                                else:
                                                    continue
                                        if (self.curr_tok == "END OF TOKENS"):
                                            self.error = "ERROR: Lacking IM OUTTA YR"
                                            return self.error
                                        loopList.append(self.curr_tok)
                                        self.advance()
                                    self.tree.add_child(TreeNode("<loop>"))
                                    loopSyntax = Parser(loopList, TreeNode("<loop content>"))
                                    loopList = []
                                    if (isinstance(loopSyntax.getResult(), str)):
                                        self.error = loopSyntax.getResult()
                                        return self.error
                                    else:
                                        self.tree.children[len(self.tree.children)-1].add_child(loopSyntax.getResult())
                                    
                                elif (self.curr_tok[0] == "Loop Condition"):
                                    loopCondition = self.curr_tok[1]
                                    self.advance()
                                    if (self.curr_tok[0] in ["Arithmetic Operation","Boolean Operation","Comparison Operation","NUMBAR Literal","NUMBR Literal","TROOF Literal","Variable Identifier","String Delimiter"]):
                                        if (self.curr_tok[0] == "Arithmetic Operation"):
                                            nodeContent = []
                                            nodeContent.append("<loop>")
                                            nodeContent.append(loopCondition)
                                            finishedNode = False
                                            continue
                                        elif (self.curr_tok[0] == "Boolean Operation"):
                                            nodeContent = []
                                            nodeContent.append("<loop>")
                                            nodeContent.append(loopCondition)
                                            nodeContent.append("<boolean_operation>")
                                            self.tree.add_child(TreeNode(nodeContent))
                                            
                                            boolList = generateBooleanStatement(self) 

                                            if (isinstance(boolList, str)):
                                                self.error = boolList
                                                return self.error
                                            else:
                                                self.tree.children[len(self.tree.children)-1].add_child(TreeNode(boolList))
                                        elif (self.curr_tok[0] == "Comparison Operation"):
                                            nodeContent = []
                                            nodeContent.append("<loop>")
                                            nodeContent.append(loopCondition)
                                            nodeContent.append("<comparison_operation>")

                                            self.tree.add_child(TreeNode(nodeContent))
                                            operand_type = ["NULL"]
                                            compareList = getComparison(self, operand_type)

                                            if (isinstance(compareList, str)):
                                                self.error = compareList
                                                return self.error
                                            else:
                                                self.tree.children[len(self.tree.children)-1].add_child(TreeNode(compareList))
         
                                        elif (self.curr_tok[0] in ["NUMBAR Literal","NUMBR Literal","TROOF Literal","Variable Identifier"]):
                                            self.tree.add_child(TreeNode(["<loop>",loopCondition,self.curr_tok[1]]))
                                            self.advance()
                                        elif (self.curr_tok[0] == "String Delimiter"):
                                            self.advance()
                                            self.tree.add_child(TreeNode(["<loop>",loopCondition,("\""+self.curr_tok[1]+"\"")]))
                                            self.advance()
                                            self.advance()
                                        
                                        if (self.curr_tok[0] == "NEWLINE"):
                                            self.advance()

                                            while (1):
                                                if (self.curr_tok[0] == "Loop Delimiter CLOSE"):
                                                    loopList.append(self.curr_tok)
                                                    self.advance()
                                                    if (self.curr_tok[0] == "Loop Identifier"):
                                                        if (loopLabel == self.curr_tok[1]):
                                                            loopList.pop()
                                                            self.advance()
                                                            if (self.curr_tok[0] == "NEWLINE"):
                                                                self.advance()
                                                                break
                                                            else:
                                                                self.error = "ERROR: IM OUTTA YR <label> must be alone in its line"
                                                                return self.error
                                                        else:
                                                            continue
                                                if (self.curr_tok == "END OF TOKENS"):
                                                    self.error = "ERROR: Lacking IM OUTTA YR"
                                                    return self.error
                                                loopList.append(self.curr_tok)
                                                self.advance()
                                            #print(loopList)
                                            loopSyntax = Parser(loopList, TreeNode("<loop content>"))
                                            loopList = []
                                            if (isinstance(loopSyntax.getResult(), str)):
                                                self.error = loopSyntax.getResult()
                                                return self.error
                                            else:
                                                self.tree.children[len(self.tree.children)-1].add_child(loopSyntax.getResult())
                                        else:
                                            self.error = "ERROR: Unexpected end of Loop IM IN YR line: " + str(self.curr_tok )
                                            return self.error
                                    else:
                                        self.error = "ERROR: Problem with expression after TIL/WILE"
                                        return self.error
                                else:
                                    self.error = "ERROR: Unexpected end of Loop IM IN YR line"
                                    return self.error
                            else:
                                self.error = "ERROR: There must be a variable identifier after YR"
                                return self.error
                        else:
                            self.error = "ERROR: There must be a YR after the UPPIN/NERFIN"
                            return self.error
                    else:
                        self.error = "ERROR: There must be an UPPIN/NERFIN after the function identifier/label"
                        return self.error
                else:
                    self.error = "ERROR: There must be an identifier after the IM IN YR"
                    return self.error

            
            cnt -= 1
                    
        #self.tree.print_tree()

# use this to catch Comparison Operation
def getComparison(self, operand_type):
    own_list = ['', '', '']

    own_list[0] = self.curr_tok[1]
    self.advance()

    if (operand_type[0] == "NULL"):
        if (self.curr_tok[0] == "Variable Identifier"):
            # check the type of this variable using third index and then save to operand_type
            # operand_type[0] = "NUMBAR Literal"  # VARIABLES ARE IMPLICITLY TYPECASTED TO NUMBAR ------- MUST CHANGE TO REAL TYPE OF VARIABLE
            pass
        elif ((self.curr_tok[0] == "NUMBAR Literal") or (self.curr_tok[0] == "NUMBR Literal")):
            operand_type[0] = self.curr_tok[0]
        elif (self.curr_tok[1] in comparator):
            pass
        else:
            self.error = "ERROR: (Comparison) Invalid operand type. Must be NUMBAR or NUMBR " + str(self.curr_tok)
            return self.error

    # ========= first operand ==============
    if (self.curr_tok[0] == "Variable Identifier"):         # first operand is a variable 
        own_list[1] = self.curr_tok[1]                          # check if type is same of operand_type. ------ NOT CURRENTLY CHECKING TYPE SO ERROR MIGHT NOT BE CATCHED
        self.advance()
        # print(str(self.curr_tok))
    elif (self.curr_tok[1] in comparator):      # first operand is another BOTH SAEM or DIFFRINT (or SMALLR OF or BIGGR OF)
        own_list[1] = getComparison(self, operand_type)
        if (self.error != "NONE"):
            return self.error
    elif ((self.curr_tok[0] in ["NUMBAR Literal", "NUMBR Literal"]) and ((self.curr_tok[0] == operand_type[0]) or (operand_type[0] == "NULL"))):    # first operand is a literal
        #print("first " + str(self.curr_tok) + " ; " + operand_type[0])
        operand_type[0] = self.curr_tok[0]
        own_list[1] = self.curr_tok[1]
        self.advance()
    else:
        self.error = "ERROR: (Comparison) Operand must be of the same types. (NUMBR or NUMBAR):\n\tCurrent token: " + str(self.curr_tok) + "\n\tPrevious types: " + str(operand_type[0])
        return self.error

    # ========= AN seperator ==============
    if(self.curr_tok[0] == "Operand Separator"): # AN keyword
        self.advance()
    else:
        self.error = "ERROR: (Comparison) Missing AN seperator: " + str(self.curr_tok) + " : " + operand_type[0]
        return self.error

    # ========= second operand ==============
    if (self.curr_tok[0] == "Variable Identifier"):         # second operand is a variable 
        own_list[2] = self.curr_tok[1]                              # -------------------------------- check if type is same of operand_type.
        self.advance()
    elif (self.curr_tok[1] in comparator):       # second operand is another BOTH SAEM or DIFFRINT (or SMALLR OF or BIGGR OF)
        own_list[2] = getComparison(self, operand_type)
        if (self.error != "NONE"):
            return self.error
    elif ((self.curr_tok[0] in ["NUMBAR Literal", "NUMBR Literal"]) and ((self.curr_tok[0] == operand_type[0]) or (operand_type[0] == "NULL"))):    # second operand is a literal
        #print("second " + str(self.curr_tok) + " ; " + operand_type[0])
        operand_type[0] = self.curr_tok[0]
        own_list[2] = self.curr_tok[1]
        self.advance()
    else:
        self.error = "ERROR: (Comparison) Operand must be of the same types. (NUMBR or NUMBAR):\n\tCurrent token: " + str(self.curr_tok) + "\n\tPrevious types: " + str(operand_type[0])
        return self.error

    if (self.error != "NONE"):
        return self.error
    return own_list

# use this to catch Boolean Operation
def generateBooleanStatement(self):
    if (self.curr_tok[1] in boolTwoOperands):
        boolList = solveBooleanStatement_2(self) # 2 operand boolean
    elif (self.curr_tok[1] == "NOT"):
        boolList = solveBooleanStatement_1(self) # 1 operand boolean
    else:
        boolList = solveBooleanStatement(self) # infinite operand boolean

    return boolList

# boolean with 2 operands
def solveBooleanStatement_2(self):
    own_list = ['','','']
    # if(self.curr_tok[1] in boolTwoOperands):
    # boolTokens[0] += 3 # i think nonsense

    own_list[0] = self.curr_tok[1]
    self.advance()
    # ========= first operand ==============
    if((self.curr_tok[0] in literals) or (self.curr_tok[0] == "Variable Identifier")): # first operand is literal
        if(self.curr_tok[0] == "String Delimiter"):
            self.advance()
            own_list[1] = self.curr_tok
            self.advance()
            self.advance()
        else:
            own_list[1] = self.curr_tok
            self.advance()
    elif (self.curr_tok[1] in boolTwoOperands):      # first operand is another 2 operand bool (BOTH OF ...)
        own_list[1] = solveBooleanStatement_2(self)
        if (self.error != "NONE"):
            return self.error
    elif (self.curr_tok[1] == "NOT"):                # first operand is 1 operand bool (NOT)
        own_list[1] = solveBooleanStatement_1(self)
        if (self.error != "NONE"):
            return self.error
    elif (self.curr_tok[1] in boolMoreOperand):      # first operand has infinite operand (ALL OF, ANY OF)
        own_list[1] = solveBooleanStatement(self)  
        if (self.error != "NONE"):
            return self.error
    else:
        self.error = "ERROR: (Bool) Unexpected first operand"
        return self.error

    # ========= AN seperator ==============
    if(self.curr_tok[0] == "Operand Separator"): # AN keyword
        self.advance()
    else:
        self.error = "ERROR: (Bool) Missing AN seperator"
        return self.error

    # ========= second operand ==============
    if((self.curr_tok[0] in literals) or (self.curr_tok[0] == "Variable Identifier")): # second operand is literal
        if(self.curr_tok[0] == "String Delimiter"):
            self.advance()
            own_list[2] = self.curr_tok
            self.advance()
            self.advance()
        else:
            own_list[2] = self.curr_tok
            self.advance()
    elif (self.curr_tok[1] in boolTwoOperands):         # second operand is another 2 operand bool (BOTH OF ...)
        own_list[2] = solveBooleanStatement_2(self)
        if (self.error != "NONE"):
            return self.error
    elif (self.curr_tok[1] == "NOT"):                   # second operand is 1 operand bool (NOT)
        own_list[2] = solveBooleanStatement_1(self)
        if (self.error != "NONE"):
            return self.error
    elif (self.curr_tok[1] in boolMoreOperand):         # second operand has infinite operand (ALL OF, ANY OF)
        own_list[2] = solveBooleanStatement(self)  
        if (self.error != "NONE"):
            return self.error
    else:
        self.error = "ERROR: (Bool) Unexpected second operand"
        return self.error

    if (self.error != "NONE"):
        return self.error
    return own_list        

# boolean with 1 operand
def solveBooleanStatement_1(self):
    own_list = ['', '']

    own_list[0] = self.curr_tok[1]
    self.advance()

    if((self.curr_tok[0] in literals) or (self.curr_tok[0] == "Variable Identifier")): # second operand is literal
        if(self.curr_tok[0] == "String Delimiter"):
            self.advance()
            own_list[1] = self.curr_tok
            self.advance()
            self.advance()
        else:
            own_list[1] = self.curr_tok
            self.advance()
    elif (self.curr_tok[1] in boolTwoOperands): # second operand is another 2 operand bool
        own_list[1] = solveBooleanStatement_2(self)
        if (self.error != "NONE"):
            return self.error
    elif (self.curr_tok[1] == "NOT"): # second operand is 1 operand bool
        own_list[1] = solveBooleanStatement_1(self)
        if (self.error != "NONE"):
            return self.error
    elif (self.curr_tok[1] in boolMoreOperand):   
        own_list[1] = solveBooleanStatement(self)  
        if (self.error != "NONE"):
            return self.error
    else:
        self.error = "ERROR: (Bool-not) Unexpected operand"
        return self.error

    if (self.error != "NONE"):
        return self.error
    return own_list

# boolean with infinite operands
def solveBooleanStatement(self):
    own_list = []

    own_list.append(self.curr_tok[1]) # ANY OF || ALL OF
    self.advance()

    # ========= first operand ==============
    if((self.curr_tok[0] in literals) or (self.curr_tok[0] == "Variable Identifier")): # first operand is literal
        if(self.curr_tok[0] == "String Delimiter"):
            self.advance()
            own_list.append(self.curr_tok)
            self.advance()
            self.advance()
        else:
            own_list.append(self.curr_tok)
            self.advance()
    elif (self.curr_tok[1] in boolTwoOperands): # first operand is another 2 operand bool
        own_list.append(solveBooleanStatement_2(self))
        if (self.error != "NONE"):
            return self.error
    elif (self.curr_tok[1] == "NOT"): # first operand is 1 operand bool
        own_list.append(solveBooleanStatement_1(self))
        if (self.error != "NONE"):
            return self.error
    else:
        self.error = "ERROR: (Bool) Unexpected first operand"
        return self.error

    # ========= AN seperator ==============
    if(self.curr_tok[0] == "Operand Separator"): # AN keyword
        self.advance()
    else:
        self.error = "ERROR: (Bool) Missing AN seperator"
        return self.error

    # ========= second operand ==============
    if((self.curr_tok[0] in literals) or (self.curr_tok[0] == "Variable Identifier")): # second operand is literal
        if(self.curr_tok[0] == "String Delimiter"):
            self.advance()
            own_list.append(self.curr_tok)
            self.advance()
            self.advance()
        else:
            own_list.append(self.curr_tok)
            self.advance()
    elif (self.curr_tok[1] in boolTwoOperands): # second operand is another 2 operand bool
        own_list.append(solveBooleanStatement_2(self))
        if (self.error != "NONE"):
            return self.error
    elif (self.curr_tok[1] == "NOT"): # second operand is 1 operand bool
        own_list.append(solveBooleanStatement_1(self))
        if (self.error != "NONE"):
            return self.error
    else:
        self.error = "ERROR: (Bool) Unexpected second operand"
        return self.error

    while(1):
        if (self.curr_tok[0] == "Parameter Delimiter"):
            self.advance()
            break
        # ========= AN seperator ==============
        if(self.curr_tok[0] == "Operand Separator"): # AN keyword
            self.advance()
        else:
            self.error = "ERROR: (Bool) Missing AN seperator"
            return self.error

        # ========= next operand ==============
        if((self.curr_tok[0] in literals) or (self.curr_tok[0] == "Variable Identifier")): # second operand is literal
            if(self.curr_tok[0] == "String Delimiter"):
                self.advance()
                own_list.append(self.curr_tok)
                self.advance()
                self.advance()
            else:
                own_list.append(self.curr_tok)
                self.advance()
        elif (self.curr_tok[1] in boolTwoOperands): # second operand is another 2 operand bool
            own_list.append(solveBooleanStatement_2(self))
            if (self.error != "NONE"):
                return self.error
        elif (self.curr_tok[1] == "NOT"): # second operand is 1 operand bool
            own_list.append(solveBooleanStatement_1(self))
            if (self.error != "NONE"):
                return self.error
        else:
            self.error = "ERROR: (Bool) Unexpected second operand"
            return self.error

    if (self.error != "NONE"):
        return self.error
    return own_list

# returns value or string error
def checkIfValidMathSyntax(tokens):
    acc = []
    eval = "NO ERRORS"
    curr = 0
    math_operations = ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"]
    sublistTokens = []
    for i in tokens:
        if (i[0] == 'Arithmetic Operation' or i[0] == 'Operand Separator'):
            sublistTokens.append(i[1])
        else:
            sublistTokens.append(random.randint(1,999)) 
    #print(sublistTokens)
    if (len(tokens) < 4):
        eval = "ERROR: Not enough lexemes for an arithmetic expression"
    else:
        while (1):
            print(acc, len(acc))
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
                    eval = "ERROR: Lacking AN and an operand in the arithmetic expression"
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
                        eval = "ERROR: Lacking operand after AN in the arithmetic expression" 
                        break
                    toBeInserted = sublistTokens[curr]
                
                #print("TO BE INSERTED: "+str(toBeInserted))
                acc.append(toBeInserted)
                curr += 1

    if (eval == "NO ERRORS"):
        return tokens
    else:
        return eval

#accumulatedMathTokens = [['Arithmetic Operation', 'SUM OF'], ['Arithmetic Operation', 'BIGGR OF'], ['Arithmetic Operation', 'SUM OF'], ['NUMBR Literal', '4'], ['Operand Separator', 'AN'], ['NUMBR Literal', '2'], ['Operand Separator', 'AN'], ['NUMBR Literal', '2'], ['Operand Separator', 'AN'], ['Arithmetic Operation', 'DIFF OF'], ['NUMBR Literal', '10'], ['Operand Separator', 'AN'], ['NUMBR Literal', '7']]
#print(checkIfValidMathSyntax(accumulatedMathTokens))
tokens = lexical_analyzer.lex_main()
i = 0
if (isinstance(tokens, list)):
    while (i < len(tokens)):
        #print(i,tokens[i])
        i +=1
    syntax = Parser(tokens,1)
    if (isinstance(syntax.getResult(), str)):
        print(syntax.getResult())
    else:
        syntax.getResult().print_tree()
    