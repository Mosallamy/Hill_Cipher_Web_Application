from flask import Flask, render_template, request
import string
import math
import random
from sympy import Matrix
import numpy as np
import ast

app = Flask(__name__)

keys = dict()
letters = string.ascii_uppercase

for i in range(len(letters)):
    keys[i] = letters[i]


text = ""
keyMatrix = list()
messageVector = list()
cipherMatrix = list()
decryptMatrix = list()
'''
def getKeyMatrix(key):
    key = key.split("/")

    for i in range(len(key)):
        key[i] = key[i].replace("(","")
        key[i] = key[i].replace(")","")
        key[i] = key[i].split(",")

    global keyMatrix
    keyMatrix = key
    for i in range(len(key)):
        for j in range(len(key)):
            key[i][j] = int(key[i][j])
'''
def isSquare (m): return all (len (row) == len (m) for row in m)
def isInt(x): return any(char.isdigit() for char in x)

def encrypt(messageVector,length): 
    

    for i in range(length): 
        for j in range(1): 
            cipherMatrix[i][j] = 0
            for x in range(length):
                print(keyMatrix, " i-",i, " x-",x)
                print(keyMatrix[i][x])
                cipherMatrix[i][j] += (keyMatrix[i][x] * 
                                       messageVector[x][j]) 
            cipherMatrix[i][j] = cipherMatrix[i][j] % 26
  
def HillCipher(message, key,length): 
    #getKeyMatrix(key)
    global keyMatrix
    keyMatrix = key
    global cipherMatrix
    global messageVector
    global text
    messageVector = [[0] for i in range(length)] 
    cipherMatrix = [[0] for i in range(length)] 
    
    for i in range(length): 
        messageVector[i][0] = ord(message[i]) % 65
  
    encrypt(messageVector,length) 
  
    CipherText = [] 
    for i in range(length): 
        CipherText.append(chr(cipherMatrix[i][0] + 65)) 
  
    #print("".join(CipherText))
    text += "".join(CipherText)

def decrypt(message, key, length):
    global text
    global decryptMatrix
    errors2 = ""
    letters = string.ascii_uppercase

    numbers = {letters[i]:i for i in range(len(letters))}
    letters = {i:letters[i] for i in range(len(letters))}
    print("Message: ",type(message))
    matrix = [numbers[i] for i in message]
    matrix = np.array(matrix)
    print("*-------* ",key)
    try:
        inverse = Matrix(key).inv_mod(26)
    except:
        errors2 = "Matrix is not invertible (mod 26)"
        print(errors2)
        return render_template("index.html",errors2 = errors2)
    
    decryptMatrix = inverse.tolist()
    mul = inverse.dot(matrix)
    mul = Matrix(mul) % 26
    mul = mul.tolist()
    for i in range(length):
        text += (letters[mul[i][0]])
    
    
    

@app.route("/",methods=["POST","GET"])
def index():
    if request.method == "POST":
        global text
        if "form1" in request.form:
            text = ""
            letters = list(string.ascii_uppercase)
            normal = request.form['normal'].replace(" ","").upper()
            matrix = request.form['matrix1']
            errors1 = ""

            if(len(matrix) <= 1):
                errors1 = "Key must be 2x2 and higher."
                return render_template("index.html",errors1 = errors1) 
            
            try:
                print(normal)
                print("-------** ",isInt(normal))
                if(isInt(normal)):
                    raise("Plain text cannot contain integers.")
            except:
                errors1 = "Plain text cannot contain integers."
                return render_template("index.html",errors1 = errors1)
            
            try:
                x = ast.literal_eval(matrix)
                print(x)
                print(type(x))
                print(isinstance(x,(list)))
                if not isinstance(ast.literal_eval(matrix), (list)):
                    raise("Key matrix format is not correct")
                matrix = ast.literal_eval(matrix)
            except:
                errors1 = "Key matrix format is not correct"
                return render_template("index.html",errors1 = errors1)

            try:
                if(not isSquare(matrix)):
                    raise Matrix("Not suqare")
            except:
                errors1 = "Key matrix is not an NxN square matrix."
                return render_template("index.html",errors1 = errors1)
                
            if(len(matrix) <= 1):
                errors1 = "Key must be 2x2 and higher."
                return render_template("index.html",errors1 = errors1) 

            key = matrix
            #key = len(key.split("/"))
                        
            key = len(matrix)
                
            while(len(normal) % key != 0):
                normal += letters[random.randrange(26)]
                            
            for i in range(int(len(normal)/(key))):
                HillCipher(normal[(i*key):(i*key + key)], matrix,key)

            return render_template("index.html",text1=text,matrix1=matrix)
        else:
            text = ""
            ciphered = request.form['ciphered'].replace(" ","").upper()
            matrix = request.form['matrix2']
            matrix3 = matrix
            key = matrix

            errors2 = ""

            
            try:
                print(ciphered)
                print("-------** ",isInt(normal))
                if(isInt(ciphered)):
                    raise("Plain text cannot contain integers.")
            except:
                errors2 = "Plain text cannot contain integers."
                return render_template("index.html",errors2 = errors2)
            try:
                if not isinstance(ast.literal_eval(matrix), (list)):
                    raise("Key matrix format is not correct")
                matrix = ast.literal_eval(matrix)
            except:
                errors2 = "Key matrix format is not correct"
                return render_template("index.html",errors2 = errors2)

            try:
                if(not isSquare(matrix)):
                    raise Matrix("Not suqare")
            except:
                errors2 = "Key matrix is not an NxN square matrix."
                return render_template("index.html",errors2 = errors2)
            length = len(matrix)
            if(length <= 1):
                            errors2 = "Key must be 2x2 and higher."
                            return render_template("index.html",errors2 = errors2) 
            '''
            matrix = key.split("/")
            
            for i in range(len(matrix)):
                matrix[i] = matrix[i].replace("(","")
                matrix[i] = matrix[i].replace(")","")
                matrix[i] = matrix[i].split(",")
            '''
            
            print("--------- ",ciphered )
            for i in range(int(len(ciphered)/(length))):
                print("@@@@",type(ciphered[(i*length):(i*length + length)]))
                decrypt(ciphered[(i*length):(i*length + length)], matrix,length)
            
            print(text)
            return render_template("index.html",text2=text,matrix2 = decryptMatrix,matrix3 = matrix3)
    return render_template("index.html")
    
#MISSISSIPPIK [[3,25],[24,17]]
if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0")
