from flask import Flask, render_template, request
from sympy import Matrix
import numpy as np
import string
import math
import random
import ast

app = Flask(__name__)

errors1 = errors2 = text =  ""
decryptMatrix = CipherText = list()

letters = string.ascii_uppercase
numbers = {i:letters[i] for i in range(len(letters))}
letters = {letters[i]:i for i in range(len(letters))}

def isSquare (m): return all (len (row) == len (m) for row in m)

def isInt(x): return any(char.isdigit() for char in x)

def English(text):
    global letters
    try:
        [letters[text[i]] for i in range(len(text))]
        return 1
    except:
        return 0

def Python(matrix):
    try:
        if not isinstance(ast.literal_eval(matrix), (list)):
            raise ("Key matrix format is not correct")
        return 1
    except:
        return 0

def encrypt(message, key,length): 
    global text, errors1, letters, CipherText
    messageVector = [[0] for i in range(length)]
    cipherMatrix = [[0] for i in range(length)]
    CipherText = []
    for i in range(length):
        messageVector[i][0] = letters[message[i]]
    for i in range(length): 
        cipherMatrix[i][0] = 0
        for x in range(length):
            cipherMatrix[i][0] += (key[i][x] * messageVector[x][0])
        cipherMatrix[i][0] = cipherMatrix[i][0] % 26
    for i in range(length): 
        CipherText.append(chr(cipherMatrix[i][0] + 65))
    text += "".join(CipherText)

def decrypt(message, key, length):
    global text, decryptMatrix, errors2,letters, numbers
    matrix = [letters[i] for i in message]
    matrix = np.array(matrix)

    try:
        inverse = Matrix(key).inv_mod(26)
    except:
        return render_template("index.html",errors2 = "Matrix is not invertible (mod 26)")
    decryptMatrix = inverse.tolist()
    mul = inverse.dot(matrix)
    mul = Matrix(mul) % 26
    mul = mul.tolist()
    for i in range(length):
        text += (numbers[mul[i][0]])

@app.route("/",methods=["POST","GET"])
def index():
    if request.method == "POST":
        global text, errors1, errors2, letters
        if "form1" in request.form:
            text = ""
            errors1 = ""
            numbers = list(string.ascii_uppercase)
            plain_text = request.form['normal'].replace(" ","").upper()
            matrix = request.form['matrix1']

            if isInt(plain_text):
                return render_template("index.html",errors1 = "Plain text cannot contain integers.")
            if not English(plain_text):
                return render_template("index.html", errors1="Plain text should be english only.")
            if not Python(matrix):
                return render_template("index.html", errors1="Key matrix format is not correct")
            matrix = ast.literal_eval(matrix)
            if not isSquare(matrix):
                return render_template("index.html",errors1 = "Key matrix is not an NxN square matrix.")
            length = len(matrix)
            if length <= 1:
                return render_template("index.html", errors1="Key must be 2x2 and higher.")
            try:
                inverse = Matrix(matrix).inv_mod(26)
            except:
                return render_template("index.html",errors1 = "Matrix is not invertible (mod 26)")
            while(len(plain_text) % length != 0):
                plain_text += numbers[random.randrange(26)]
            for i in range(int(len(plain_text)/(length))):
                encrypt(plain_text[(i*length):(i*length + length)], matrix,length)
            return render_template("index.html",text1=text,matrix1=matrix,errors1=errors1)
        else:
            text = ""
            errors2 = ""
            ciphered_text = request.form['ciphered'].replace(" ","").upper()
            matrix = request.form['matrix2']
            matrix3 = matrix

            if isInt(ciphered_text):
                return render_template("index.html", errors2="Plain text cannot contain integers.")
            if not English(ciphered_text):
                return render_template("index.html", errors2="Plain text should be english only.")
            if not Python(matrix):
                return render_template("index.html", errors2="Key matrix format is not correct")
            matrix = ast.literal_eval(matrix)
            if not isSquare(matrix):
                return render_template("index.html", errors2="Key matrix is not an NxN square matrix.")
            length = len(matrix)
            if length <= 1:
                return render_template("index.html",errors2 = "Key must be 2x2 and higher.")
            for i in range(int(len(ciphered_text)/(length))):
                decrypt(ciphered_text[(i*length):(i*length + length)], matrix,length)

            return render_template("index.html",text2=text,matrix2 = decryptMatrix,matrix3 = matrix3,errors2=errors2)
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0")
