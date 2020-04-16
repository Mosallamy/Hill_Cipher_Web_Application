from flask import Flask, render_template, request
import string
import math
import random
from sympy import Matrix
import numpy as np
import ast

app = Flask(__name__)

keys = dict()
errors1 = errors2 = text =  ""
letters = string.ascii_uppercase
keyMatrix = messageVector =cipherMatrix = decryptMatrix = list()

for i in range(len(letters)):
    keys[i] = letters[i]

def isSquare (m): return all (len (row) == len (m) for row in m)
def isInt(x): return any(char.isdigit() for char in x)

def encrypt(message, key,length): 
    global keyMatrix, cipherMatrix, messageVector, text, errors1, letters
    keyMatrix = key
    CipherText = [] 
    numbers = {letters[i]:i for i in range(len(letters))}
    
    messageVector = [[0] for i in range(length)] 
    cipherMatrix = [[0] for i in range(length)] 

    try:
        for i in range(length):
                messageVector[i][0] = numbers[message[i]]
    except:
        errors1 = "Plain text should contain onyl English characters"
        return render_template("index.html",errors1 = errors1)

    for i in range(length): 
                cipherMatrix[i][0] = 0
                for x in range(length):
                    cipherMatrix[i][0] += (keyMatrix[i][x] * messageVector[x][0]) 
                cipherMatrix[i][0] = cipherMatrix[i][0] % 26
  
    for i in range(length): 
        CipherText.append(chr(cipherMatrix[i][0] + 65)) 
  
    text += "".join(CipherText)

def decrypt(message, key, length):
    global text, decryptMatrix, errors2
    
    errors2 = ""
    letters = string.ascii_uppercase

    numbers = {letters[i]:i for i in range(len(letters))}
    letters = {i:letters[i] for i in range(len(letters))}
    try:
        matrix = [numbers[i] for i in message]
        matrix = np.array(matrix)
    except:
        errors2 = "Ciphered text should be in English only."
        return render_template("index.html",errors2 = errors2)
    try:
        inverse = Matrix(key).inv_mod(26)
    except:
        errors2 = "Matrix is not invertible (mod 26)"
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
            global errors1
            errors1 = text = ""
            letters = list(string.ascii_uppercase)
            normal = request.form['normal'].replace(" ","").upper()
            matrix = request.form['matrix1']

            if(len(matrix) <= 1):
                errors1 = "Key must be 2x2 and higher."
                return render_template("index.html",errors1 = errors1) 
            try:
                if(isInt(normal)):
                    raise("Plain text cannot contain integers.")
            except:
                errors1 = "Plain text cannot contain integers."
                return render_template("index.html",errors1 = errors1)
            try:
                x = ast.literal_eval(matrix)
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
                
            try:
                inverse = Matrix(matrix).inv_mod(26)
            except:
                errors1 = "Matrix is not invertible (mod 26)"
                return render_template("index.html",errors1 = errors1)
                
            if(len(matrix) <= 1):
                errors1 = "Key must be 2x2 and higher."
                return render_template("index.html",errors1 = errors1) 

            key = len(matrix)
                
            while(len(normal) % key != 0):
                normal += letters[random.randrange(26)]
                            
            for i in range(int(len(normal)/(key))):
                encrypt(normal[(i*key):(i*key + key)], matrix,key)

            return render_template("index.html",text1=text,matrix1=matrix,errors1=errors1)
        else:
            global errors2
            text = errors2 = ""
            ciphered = request.form['ciphered'].replace(" ","").upper()
            matrix = request.form['matrix2']
            matrix3 = matrix
            key = matrix
        
            try:
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

            for i in range(int(len(ciphered)/(length))):
                decrypt(ciphered[(i*length):(i*length + length)], matrix,length)

            return render_template("index.html",text2=text,matrix2 = decryptMatrix,matrix3 = matrix3,errors2=errors2)
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0")
