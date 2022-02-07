#!/usr/bin/python3.9
#laenpythonCCompile


import sys
import typing
import compileOperations
auto_value = 0
def auto_int(reset:bool = False):
    global auto_value
    if (reset):
        auto_value = 0
    toRet = auto_value
    auto_value += 1
    return toRet

MODE_64_BITS = (sys.maxsize  > 2**32)
BITS = 64 if (MODE_64_BITS) else 32
TYPES_SIZE = {
    "char" : 1,
    "short" : 2,
    "short int" : 2,
    "int" : 4,
    "long" : 4 if (not MODE_64_BITS) else 8,
    "long long": 8,
    "ptr" : 4 if (not MODE_64_BITS) else 8
}


OPERANDES_TYPE = {
    "immediate": auto_int(True),
    "local": auto_int(),
    "global": auto_int(),
    "label" : auto_int(),
    "result" : auto_int()
}

OPERATIONS = {
    "+": auto_int(True),
    "-": auto_int(),
    "/": auto_int(),
    "%": auto_int(),
    "*": auto_int(),
    "muld" : auto_int(),
    "=": auto_int(),
}

def getRegisterAssocitatedToType(type: str, regName: str) -> str:
    toRet = ""
    if type == "ptr":
        #TODO refactor this
        toRet += "["
    size = TYPES_SIZE[type]
    if (size == 1):
        toRet += regName + "l"
    if (size == 2):
        toRet += regName + "x"
    if (size == 4):
        toRet += "e" + regName + "x"
    if (size == 8):
        toRet += "r" + regName + "x"
    if type == "ptr":
        #TODO refactor this
        toRet += "]"
    return toRet


class operande:
    def __init__(self,operande_type:OPERANDES_TYPE, type:str, valeur:int) -> None:
        self.operande_type = operande_type
        self.type = type
        self.valeur = valeur

def movOPToRegister(file:typing.TextIO, regName:str, operand: operande):
    if (operand.operande_type == OPERANDES_TYPE["result"] and regName == "a"):
        return #il n'y a rien a faire
    else:
        if (operand.operande_type == OPERANDES_TYPE["result"]):
            a = getRegisterAssocitatedToType(operand.type, "a")
            out = getRegisterAssocitatedToType(operand.type, regName)
            file.write("\tMOV " + out + ", " + a + "\n")
            return 
        if (operand.operande_type == OPERANDES_TYPE["immediate"]):
            out = getRegisterAssocitatedToType(operand.type, regName)
            file.write("\tMOV " + out + ", " + str(operand.valeur) + "\n")
            return 

def compileAdd(operandes, file, params):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    movOPToRegister(file, "a", operandes[0])
    movOPToRegister(file, "b", operandes[1])
    file.write("\tADD " + a + ", " + b + "\n")
def compileSub(operandes, file, params):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    movOPToRegister(file, "a", operandes[0])
    movOPToRegister(file, "b", operandes[1])
    file.write("\tSUB " + a + ", " + b + "\n")
def compileMul(operandes, file, params):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0])
    movOPToRegister(file, "b", operandes[1])
    file.write("\tMOV " + d + ", 0\n")
    file.write("\tMUL " + b + "\n")

def compileMulD(operandes, file, params):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0])
    movOPToRegister(file, "b", operandes[1])
    file.write("\tMOV " + d + ", 0\n")
    file.write("\tMUL " + b + "\n")
    file.write("\tMOV " + a + ", " + d + "\n")

def compileDiv(operandes, file, params):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0])
    movOPToRegister(file, "b", operandes[1])
    file.write("\tMOV " + d + ", 0\n")
    file.write("\tDIV " + b + "\n")
def compileMod(operandes, file, params):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0])
    movOPToRegister(file, "b", operandes[1])
    file.write("\tMOV " + d + ", 0\n")
    file.write("\tDIV " + b + "\n")
    file.write("\tMOV " + a + ", " + d + "\n")

class operation:
    def __init__(self, operandes : list([operande]), operation : OPERATIONS) -> None:
        self.operandes = operandes
        self.operation = operation
    def compile(self, file:typing.TextIO, params : list([str]) = None ):
        #code de retours toujours dans le registre A
        if (self.operation == OPERATIONS["+"]):
            compileAdd(self.operandes, file, params)
        if (self.operation == OPERATIONS["-"]):
            compileSub(self.operandes, file, params)
        if (self.operation == OPERATIONS["*"]):
            compileMul(self.operandes, file, params)
        if (self.operation == OPERATIONS["muld"]):
            compileMulD(self.operandes, file, params)
        if (self.operation == OPERATIONS["/"]):
            compileDiv(self.operandes, file, params)
        if (self.operation == OPERATIONS["%"]):
            compileMod(self.operandes, file, params)
        pass
class label:
    def __init__(self, name) -> None:
        pass
    def compile(self, file:typing.TextIO, params : list([str]) = None ):
        pass
class function:
    def __init__(self, name:str, codeOrLabel, parametres = None, variablesLocales = None ) -> None:
        self.name = name
        self.codeOrLabel = codeOrLabel
        self.parametres = parametres
        self.variablesLocales = variablesLocales
    def compile(self, file:typing.TextIO, params : list([str])):
        file.write(self.name + ":\n")
        file.write("PUSH RBP\n") # TO REFACTOR
        file.write("MOV RBP,RSP\n") # TO REFACTOR
        for cl in self.codeOrLabel:
            cl.compile(file, params)
        file.write("POP RBP\n") # TO REFACTOR
        file.write("RET\n") # TO REFACTOR
class program:
    def __init__(self, functions: list([function]), ) -> None:
        self.functions = functions
    def compile(self, path:str, params : list([str]) = None):
        with open(path, "w") as file:
            file.write("[BITS " + str(BITS) + "]\n" )
            file.write("section .text\n")
            for func in self.functions:
                file.write("global " + func.name + "\n")
                if (func.name == "main"):
                    file.write("global _start\n")
            for func in self.functions:
                if (func.name == "main"):
                    file.write("_start: \n")
                    file.write("\tcall main\n")
                    # carefull to return codee, TODO
                    assert  False, "not supported yes"
                func.compile(file, params)

def getProgramFromFile(path):
    toRet = []
    with open(path, "r") as operationToDo:
        for line in operationToDo:
            line = line.split(" ")
            toRet.append(operation([
            operande(OPERANDES_TYPE["immediate"],"int", line[0]),
            operande(OPERANDES_TYPE["immediate"],"int", line[1]),
        ], OPERATIONS[line[2]]))
        for i in range(int((len(line) - 3) / 2 )):
            toRet.append(operation([
            operande(OPERANDES_TYPE["result"], "int", 0),
            operande(OPERANDES_TYPE["immediate"],"int", line[i * 2 + 3 ]),
        ], OPERATIONS[line[i * 2 + 4 ]]))
    return toRet
"""
additionCode.append(operation([
            operande(OPERANDES_TYPE["immediate"],"short", 10),
            operande(OPERANDES_TYPE["immediate"],"short", 20),
        ], OPERATIONS["+"]))
"""

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("usage : " + sys.argv[0] + " in out")
    else:
        additionCode = getProgramFromFile("calc")
        functions = []
        functions.append(function("addition", additionCode))
        p = program(functions)
        
        p.compile(sys.argv[2])