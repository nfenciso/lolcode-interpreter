import random
import lexical_analyzer

canBeLevelTwo = ["Arithmetic Operation","Output Keyword","Variable Declaration","Code Delimeter CLOSE"]
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
        x = self.startParse()
        if (isinstance(x, str)):
            print(self.error)
    
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
        if (self.curr_tok[0] == "Code Delimeter OPEN"):
            self.tree = TreeNode("<program>")
            self.tree.add_child(TreeNode("Code Delimeter OPEN"))
            levelTwoIdx = self.lookAhead()
            self.goBackToSpecificIdx(1)
            self.parse(levelTwoIdx)
            if (self.error != "NONE"):
                return self.error

        else:
            self.error = "ERROR: Must begin the program with HAI"
            return self.error

    def lookAhead(self):
        levelTwoIdx = []
        while (1):
            self.advance()
            if (self.tok_idx == len(self.tokens)): 
                break
            
            #print(self.tok_idx,self.curr_tok)
            if (self.curr_tok[0] in canBeLevelTwo):
                levelTwoIdx.append(self.tok_idx)

                if (self.curr_tok[0] == "Arithmetic Operation"):
                    while (self.curr_tok[0] in mathRelatedLex):
                        #print("x",self.tok_idx,self.curr_tok)
                        self.advance()
                    levelTwoIdx.append(self.tok_idx)
                    #print("xx",self.tok_idx,self.curr_tok)
                if (self.curr_tok[0] == "Output Keyword"):
                    for j in range(0,self.curr_tok[2]):
                        self.advance()     
        return levelTwoIdx

    def parse(self, levelTwoIdx):
        nodeContent = []
        finishedNode = True
        #print(levelTwoIdx)
        while (1):
            
            if (self.tok_idx in levelTwoIdx):
                #print(self.tok_idx)
                #print(levelTwoIdx)
                if (self.curr_tok[0] == "Variable Declaration"):
                    nodeContent.append(self.curr_tok)
                    self.advance()
                    if (self.curr_tok[0] == "Variable Identifier"):
                        nodeContent.append(self.curr_tok)
                        self.advance()
                    else:
                        self.error = "ERROR: There must be a Variable Identifier after I HAS A"
                        return self.error
                    
                    #print("x",self.tok_idx)
                    #print(levelTwoIdx)
                    if (self.tok_idx in levelTwoIdx):
                        self.tree.add_child(TreeNode(nodeContent))
                        nodeContent = []
                        continue
                    if (self.curr_tok[0] == "Variable Assignment"):
                        nodeContent.append(self.curr_tok)
                        self.advance()
                        if (self.tok_idx in levelTwoIdx):
                            finishedNode = False
                            continue
                    elif (self.tok_idx not in levelTwoIdx):
                        self.error = "ERROR: Wrong syntax in I HAS A line"
                        return self.error
                elif (self.curr_tok[0] == "Code Delimeter CLOSE"):
                    self.tree.add_child(TreeNode("Code Delimeter CLOSE"))
                    self.advance()
                elif (self.curr_tok[0] == "Arithmetic Operation"):
                    mathList = []
                    while (self.curr_tok[0] in mathRelatedLex):
                        mathList.append(self.curr_tok)
                        self.advance()
                    evalMathList = checkIfValidMathSyntax(mathList)
                    if (isinstance(evalMathList, int)):
                        if (not finishedNode):
                            nodeContent.append("<arithmeticExpression>")
                            self.tree.add_child(TreeNode(nodeContent))
                            self.tree.children[len(self.tree.children)-1].add_child(TreeNode(mathList))
                            nodeContent = []
                        else:
                            nodeContent = evalMathList
                            self.tree.add_child(TreeNode(nodeContent))
                            nodeContent = []
                        continue
                    else:
                        self.error = evalMathList
                        return self.error
                elif (self.curr_tok[0] == "Output Keyword"):
                    visibleNumLex = self.curr_tok[2]
                    nodeContent = []
                    nodeContent.append(self.curr_tok)
                    nodeContent.append("<arguments>")
                    self.tree.add_child(TreeNode(nodeContent))
                    nodeContent = []
                    self.advance()
                    for j in range(0, visibleNumLex):
                        self.tree.children[len(self.tree.children)-1].add_child(TreeNode(self.curr_tok))
                        self.advance()
                    continue
            
            if (self.curr_tok == "END OF TOKENS"):
                break
   
            self.advance()
        self.tree.print_tree()



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
        #print(acc, "curr:", curr)
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

#accumulatedMathTokens = [['Arithmetic Operation', 'SUM OF'], ['Arithmetic Operation', 'BIGGR OF'], ['Arithmetic Operation', 'SUM OF'], ['NUMBR Literal', '4'], ['Operand Separator', 'AN'], ['NUMBR Literal', '2'], ['Operand Separator', 'AN'], ['NUMBR Literal', '2'], ['Operand Separator', 'AN'], ['Arithmetic Operation', 'DIFF OF'], ['NUMBR Literal', '10'], ['Operand Separator', 'AN'], ['NUMBR Literal', '7']]
#print(checkIfValidMathSyntax(accumulatedMathTokens))
tokens = lexical_analyzer.lex_main()
i = 0
while (i < len(tokens)):
    print(i,tokens[i])
    i +=1
syntax = Parser(tokens)