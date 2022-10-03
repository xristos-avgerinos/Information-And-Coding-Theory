import random
import itertools
import numpy as np
import re

#n = int(input("Enter code dimensions(n)")) #give input
n = 7
print("dimensions:",7)
seperator_len = 3 #FINAL
isPadded = False



#pairnw to ginomeno paragontwn toy polyonymoy
def factorization(x):
    x = GF(2)['x'].0
    f= (x**n)+1
    F = f.factor(); F
    return F

#Generate invertible matrix
def generate_invertible_matrix(length):
    A = random_matrix(GF(2),length,length)
    if(not(A.is_invertible())):
        generate_invertible_matrix(length)
    return A


#addpading
def padding(c):
    if(len(c) % seperator_len == 0):
        return c
    else:
        end= (text_to_bits(str(len(c)).zfill(4)))
        if(len(c+end) % seperator_len == 0):
            c = c+end
        else:
            if(len(c+end)%seperator_len == 1):
                middle = 2 #0s to add
            elif(len(c+end)%seperator_len == 2):
                middle = 1
            c = c+ middle*"0" + end
        print(end)
        return c

def text_to_bits(text, encoding='latin-1', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='latin-1', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'




#apothikeyoyme se mia lista ta ginomena toy polyonimoy
F= factorization(n)
Final_Polynomial=str(F).split('*')
print("Polynomial of x^"+str(n)+"+1 : "+str(F))




#creating g(x)
g_x = []
for L in range(0, len(Final_Polynomial)+1):
    for subset in itertools.combinations(Final_Polynomial, L):
        g_x.append(','.join(subset))

#modifying g(x) so first element is 1 and replacing "," with "*"
g_x[0] = g_x[0].replace("", "1")
g_xFinal = []
for j in g_x:
    new_string = j.replace(" , ", "*")
    g_xFinal.append(new_string)
g_x = g_xFinal

#creating h(x)
h_x = g_x[::-1]


print("\n Consequently the  cyclic codes are: ")
for i in range(0,len(g_x)):
    print("C"+str(i+1)+" g(x) = " + g_x[i] + "    |  h(x) = " + h_x[i])
#generating random number (agnooyme to c8 kathos dinei keno matrix gia ayto exoyme -2 anti gia -1 )
random_number1 = random.randint(0,len(g_x)-2)
random_number2 = random.randint(0,len(g_x)-2)

F.<x> = GF(2)[]

#Creating C1,G1
g1 = F((g_x[random_number1]))
print("\nThe first random selected cyclic code is C=",random_number1+1)
C1 = codes.CyclicCode(generator_pol = g1, length = n)
E1 = codes.encoders.CyclicCodeVectorEncoder(C1) #VECTOR OF C1
G1 = C1.generator_matrix()
print(G1,"= G1")



#Creating C2,G2
g2 = F((g_x[random_number2]))
print("\nThe second random selected cyclic code is C=",random_number2+1)
C2 = codes.CyclicCode(generator_pol = g2, length = n)
E2 = codes.encoders.CyclicCodeVectorEncoder(C2)  #VECTOR OF C2
G2 = C2.generator_matrix()
print(G2,"= G2")



    #P Matrix
#Create an Identity Matrix
I = matrix.identity(n)
# Assign identity matrix as array
arrayP = np.array(I)
# Shuffle array
np.random.shuffle(arrayP)
#cast to Sage Matrix
P = matrix(arrayP)
# Display shuffled Matrix
print("\nRandom permutations of the identity matrix(" + str(n) +"x" + str(n) +") :\n",P," = P")



    #S Matrix
S=generate_invertible_matrix(n)
# Display Random invertible matrix
print("\nRandom invertible matrix(" + str(n) +"x" + str(n) +") :\n",S," = S")



    #G'
Gt = G1*P*S
print("\nS*G1*P Matrix :\n",Gt," = G'\n")

#string to binary
msg=input("Give Message: ")
b=text_to_bits(msg)



#create c = msg * G'
VectorGt=(vector(Gt.list()))
c=int(str(b))*VectorGt
#(0,0,1...,1) to 001...1
c=str(c).strip("()").replace(",","").replace(" ","")
print("c =msg x G' ",c)
c= b
startedC=c
previous_lengthC = len(c)
print("length c:",previous_lengthC,"\n")


c=padding(c) #000000101...0101,80



print("padded C is : ",c," with length",len(c))
padded_lengthC = len(c)

print("-"*100)
if (previous_lengthC != padded_lengthC):
    isPadded = True

encodingList = []
encodedList = []


#xwrizw to c se 3ades kai to bazw sthn lista encodingList
for i in range(0,len(c),3):
    encodingList.append(c[i:i+3])




#kwdikopoiw ta stoixeia ths encodingList kai ta bazw sthn encodedList
for i in encodingList:
    m = vector(GF(2),(i))
    encodedmsg=(E2.encode(m))
    encodedList.append(str(encodedmsg))
print("List for encoding ",encodingList,"\n")
print("Encoded List ",encodedList,"\n")


ct=[]
for i in range(len(encodedList)):
    encodedList[i] = re.sub(r'[()]', '', str(encodedList[i]))
    encodedList[i] = str(encodedList[i]).strip("()").replace(",","").replace(" ","")


ct=""
for i in encodedList:
    ct+=i
print("C' without noise: ",ct,"\n")


err=C2.minimum_distance()

#add noise
for i in range(0,err-1):
    rnd= random.randint(0,len(ct)-1)
    if(ct[:rnd]=="1"):
        ct = ct[:rnd]+ "0"+ ct[rnd+1:]
    else:
        ct = ct[:rnd]+ "1"+  ct[rnd+1:]
print("C' with " ,err,"random errors",ct,"\n")



#metatrepoyme to c' se lista ana n-ades(anti tou split)
ct_list=re.findall(n*'.',ct)


#kanoume decode to c'
decoded_ct = ""
for i in ct_list:
    m2 = vector(GF(2),(i))
    y=C2.decode_to_message(m2)
    decoded_ct+=str(y[0:3])

decoded_ct=str(decoded_ct).strip("()").replace(",","").replace(" ","")
decoded_ct=re.sub(r'[()]', '', str(decoded_ct))
print("\ndecoded c': ",decoded_ct ,"\n")

print("IsPadded: ",isPadded)
if isPadded:
    last32 = decoded_ct[-32:]
    Clength = str(text_from_bits(last32))
    print("c 4 last bytes as number ",Clength)
    realMsg = decoded_ct[:int(Clength)]
    print("StartedMsg:",startedC," | Binary -> Text = ",text_from_bits(startedC))
    print("ConcstructedMSG: ",realMsg," Decoded to: ",text_from_bits(realMsg))
else:
    realMsg = decoded_ct
    print("StartedMsg:",startedC," | Binary -> Text = ",text_from_bits(startedC))
    print("ConcstructedMSG: ",realMsg," Decoded to: ",text_from_bits(realMsg))