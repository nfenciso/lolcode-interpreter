import random

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
#print(checkIfValidMathSyntax(accumulatedMathTokens))