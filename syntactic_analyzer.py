import random
import lexical_analyzer

canBeLevelTwo = ["Arithmetic Operation","Output Keyword","Variable Declaration","Code Delimiter CLOSE"]
mathRelatedLex = ["Arithmetic Operation","Operand Separator","NUMBR Literal","NUMBAR Literal","YARN Literal","TROOF Literal","Variable Identifier"]

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
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.error = "NONE"
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
                self.tree.add_child(TreeNode(self.curr_tok))
                self.advance()
                if (self.curr_tok[0] == "NEWLINE"):
                    self.advance()
                else:
                    self.error = "ERROR: There must not be anything after HAI"
                    return self.error
            elif (self.curr_tok[0] == "Variable Declaration"):
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
                            #boolean
                            #comparison
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
                            if (self.curr_tok[0] in mathRelatedLex):
                                mathList.append(self.curr_tok)
                                self.advance()
                            else:
                                break
                        evalMathList = checkIfValidMathSyntax(mathList)
                        if (isinstance(evalMathList, str)):
                            self.error = evalMathList
                            return self.error
                        else:
                            self.tree.children[len(self.tree.children)-1].add_child(TreeNode("<math_arguments>"))
                            child = self.tree.children[len(self.tree.children)-1]
                            child.children[len(child.children)-1].add_child(TreeNode(mathList))
                    #boolean
            #         #comparison
            elif (self.curr_tok[0] == "Input Keyword"):
                print("==========================jhvjhv==")
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
                    self.error = "ERROR: Must have variable identifier to store the input"
                    return self.error
                # pass
                    







            elif (self.curr_tok[0] == "If-Then Delimiter"):
                ifList = []
                ifList.append(self.curr_tok)
                self.advance()
                while (self.curr_tok[0] != "Conditional Delimiter"):
                    if (self.curr_tok == "END OF TOKENS"):
                        self.error = "ERROR: Lacking OIC"
                        return self.error
            cnt -= 1
                    
        #self.tree.print_tree()


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
            sublistTokens.append(random.randint(1,999)) # para san etong randomize? pangcheck?

    if (len(tokens) < 4):
        eval = "ERROR: Not enough lexemes for an arithmetic expression"
    else:
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
        print(i,tokens[i])
        i +=1
    syntax = Parser(tokens)
    if (isinstance(syntax.getResult(), str)):
        print(syntax.getResult())
    else:
        syntax.getResult().print_tree()
    