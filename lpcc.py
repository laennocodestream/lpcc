#!/usr/bin/python3.9
#laenpythonCCompile


from statistics import mode
import sys
import typing
auto_value = 0
def auto_int(reset:bool = False):
    global auto_value
    if (reset):
        auto_value = 0
    toRet = auto_value
    auto_value += 1
    return toRet

MODE_64_BITS = 1
SP = "RSP" if (MODE_64_BITS) else "ESP"
BP = "RBP" if (MODE_64_BITS) else "EBP"

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
    "==": auto_int(),
    "<": auto_int(),
    "<=": auto_int(),
    ">": auto_int(),
    ">=": auto_int(),
    "muld" : auto_int(),
    "cmpj0" : auto_int(),
    "jmp" : auto_int(),
    "=": auto_int(),#TODO not implemented yet
}

LABELED_OPERATIONS_NAMES = ["cmpj0", "jmp"]

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
    def __init__(self,operande_type:OPERANDES_TYPE, type:str, valeur:str) -> None:
        self.operande_type = operande_type
        self.type = type
        self.valeur = valeur

def movOPToRegister(file:typing.TextIO, regName:str, operand: operande, func):
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
        if (operand.operande_type == OPERANDES_TYPE["local"]):
            out = getRegisterAssocitatedToType(operand.type, regName)
            file.write(f"\tMOV %s, [%s - %i]\n" % (out, BP, func.variablesLocales[operand.valeur].position))
            return 


def compileAdd(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write("\tADD " + a + ", " + b + "\n")

def compileSub(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write("\tSUB " + a + ", " + b + "\n")

def compileMul(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write("\tMOV " + d + ", 0\n")
    file.write("\tMUL " + b + "\n")

def compileMulD(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write("\tMOV " + d + ", 0\n")
    file.write("\tMUL " + b + "\n")
    file.write("\tMOV " + a + ", " + d + "\n")

def compileDiv(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write("\tMOV " + d + ", 0\n")
    file.write("\tDIV " + b + "\n")

def compileMod(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write("\tMOV " + d + ", 0\n")
    file.write("\tDIV " + b + "\n")
    file.write("\tMOV " + a + ", " + d + "\n")

def compileAffect(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    movOPToRegister(file, "a", operandes[0], func)
    
    if (operandes[1].operande_type == OPERANDES_TYPE["local"]):
        position = func.variablesLocales[operandes[1].valeur].position
        file.write(f"\tMOV [%s - %i], %s\n" % (BP, position, a))

def compileJumpIf0(operandes:list([operande]), file, params, func):
    if (operandes[1].operande_type == OPERANDES_TYPE["label"]):
        a = getRegisterAssocitatedToType(operandes[0].type, "a")
        movOPToRegister(file, "a", operandes[0], func)
        file.write(f"\tCMP %s, 0\n"% a)
        file.write(f"\tJE .%s\n"% operandes[1].valeur)
    else:
        print("error while compiling, expecting a label")

def compileJmp(operandes:list([operande]), file, params, func):
    if (operandes[0].operande_type == OPERANDES_TYPE["label"]):
        file.write(f"\tJMP .%s\n"% operandes[0].valeur)
    else:
        print("error while compiling, expecting a label")

def compileCMPEqual(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write(f"\tXOR %s, %s\n" % (d,d))
    file.write("\tCMP " + a + ", " + b + "\n")
    file.write("\tSETE " + "DL" +  "\n")
    file.write(f"\tMOV %s, %s\n" % (a,d))

def compileCMPGreater(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write(f"\tXOR %s, %s\n" % (d,d))
    file.write("\tCMP " + a + ", " + b + "\n")
    file.write("\tSETG " + "DL" +  "\n")
    file.write(f"\tMOV %s, %s\n" % (a,d))    

def compileCMPGreaterEqual(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write(f"\tXOR %s, %s\n" % (d,d))
    file.write("\tCMP " + a + ", " + b + "\n")
    file.write("\tSETGE " + "DL" +  "\n")
    file.write(f"\tMOV %s, %s\n" % (a,d))

def compileCMPLower(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write(f"\tXOR %s, %s\n" % (d,d))
    file.write("\tCMP " + a + ", " + b + "\n")
    file.write("\tSETL " + "DL" +  "\n")
    file.write(f"\tMOV %s, %s\n" % (a,d))

def compileCMPLowerEqual(operandes, file, params, func):
    a = getRegisterAssocitatedToType(operandes[0].type, "a")
    b = getRegisterAssocitatedToType(operandes[1].type, "b")
    d = getRegisterAssocitatedToType(operandes[1].type, "d")
    movOPToRegister(file, "a", operandes[0], func)
    movOPToRegister(file, "b", operandes[1], func)
    file.write(f"\tXOR %s, %s\n" % (d,d))
    file.write("\tCMP " + a + ", " + b + "\n")
    file.write("\tSETLE " + "DL" +  "\n")
    file.write(f"\tMOV %s, %s\n" % (a,d))

class operation:
    def __init__(self, operandes : list([operande]), operation : OPERATIONS) -> None:
        self.operandes = operandes
        self.operation = operation
    def compile(self, file:typing.TextIO, func,  params : list([str]) = None ):
        #code de retours toujours dans le registre A
        if (self.operation == OPERATIONS["+"]):
            compileAdd(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["-"]):
            compileSub(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["*"]):
            compileMul(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["muld"]):
            compileMulD(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["/"]):
            compileDiv(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["%"]):
            compileMod(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["cmpj0"]):
            compileJumpIf0(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["jmp"]):
            compileJmp(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["=="]):
            compileCMPEqual(self.operandes, file, params, func)
        if (self.operation == OPERATIONS[">"]):
            compileCMPGreater(self.operandes, file, params, func)
        if (self.operation == OPERATIONS[">="]):
            compileCMPGreaterEqual(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["<"]):
            compileCMPLower(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["<="]):
            compileCMPLowerEqual(self.operandes, file, params, func)
        if (self.operation == OPERATIONS["="]):
            compileAffect(self.operandes, file, params, func)
        pass

class variable:
    def __init__(self, type, name, position = None) -> None:
        self.type = type
        self.name = name
        self.position = position
    def __repr__(self) -> str:
        return self.type + " " + self.name + " " + str(self.position)

class label:
    def __init__(self, name: str) -> None:
        self.name : str = name
    def compile(self,  file:typing.TextIO, func, params : list([str]) = None ):
        file.write("." + self.name + ":\n")

class function:
    def __init__(self, name:str, codeOrLabel, parametres = None, variablesLocales = None ) -> None:
        self.name = name
        self.codeOrLabel = codeOrLabel
        self.parametres = parametres
        self.variablesLocales = {}
        currentVal = 0
        for variableLocale in variablesLocales:
            currentVal += TYPES_SIZE[variableLocale.type]
            self.variablesLocales[variableLocale.name] = variable(variableLocale.type, variableLocale.name, currentVal)
        #print(self.variablesLocales)
        self.variablesLocalesAddress = {}

    def compile(self, file:typing.TextIO, params : list([str])):
        file.write(self.name + ":\n")
        file.write(f"PUSH %s\n" % BP) # TO REFACTOR
        file.write(f"MOV %s,%s\n" % (BP, SP)) # TO REFACTOR
        for cl in self.codeOrLabel:
            cl.compile(file, self, params)
        file.write(f"POP %s\n" % BP) # TO REFACTOR
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

def parse_operand(toParse:str, operation: str) -> str:
    if (toParse.isnumeric()):
        return operande(OPERANDES_TYPE["immediate"],"int", toParse)
    if (operation in LABELED_OPERATIONS_NAMES):
        return operande(OPERANDES_TYPE["label"],"int", toParse)
    return operande(OPERANDES_TYPE["local"],"int", toParse)

def getProgramFromFile(path):
    functions = []
    functionCode = []
    lines = []
    variableLocales = []
    functionName = ""
    with open(path, "r") as operationToDo:
        lines = [l for l in operationToDo]
    inFunction = False
    for i in range(len(lines)):
        line = lines[i].strip().split(" ")
        if (inFunction):
            if (line[0] == "}"):
                inFunction = False
                functions.append(function(functionName, functionCode,variablesLocales=variableLocales))
                continue
            if (not line[0].isnumeric() and len(line) <= 2):
                if (len(line) == 1):
                    functionCode.append(label(line[0]))
                else:
                    try:
                        if (line[0] in TYPES_SIZE.keys()):
                            variableLocales.append(variable(line[0], line[1]))
                        else:
                            functionCode.append(operation([operande(OPERANDES_TYPE["label"],"int", line[0])], OPERATIONS[line[1]]))
                    except KeyError:
                        print(line, line[0] in TYPES_SIZE.keys())
            else:
                functionCode.append(operation([
                    parse_operand(line[0], line[2]),
                    parse_operand(line[1], line[2])
                ], OPERATIONS[line[2]]))
                for i in range(int((len(line) - 3) / 2 )):
                    operandArray = [
                        operande(OPERANDES_TYPE["result"], "int", 0),
                    ]
                    opToParse = line[i * 2 + 3 ]
                    operandArray.append(parse_operand(opToParse, line[i * 2 + 4 ]))
                    functionCode.append(operation(operandArray, OPERATIONS[line[i * 2 + 4 ]]))
        else:
            if (len(line) >= 2):
                #print(line)
                functionCode = []
                variableLocales = []
                inFunction = True
                functionName = line[1].split("(")[0]
    return program(functions)
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
        p = getProgramFromFile("calc")
        p.compile(sys.argv[2])