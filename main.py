###############################################
##### PART ONE : CONVERT HEX TO INSTR CODE ####
###############################################

#Read in file
print ('Reading in asm file (prog.asm) into a list of strings...\n')
f = open('ex.asm')
hexLines = f.readlines()
f.close()

#Define arrays (r is for registers)
binaryArray = [0] * len(hexLines)
r = [0] * 32
pc = [0] * len(hexLines)
instrCode = [0] * len(hexLines)
labels = [0] * len(hexLines)


#Define dictionary
addresses = {}

#Define variables
decimal = instr = rs = rt = rd = imm = newPC = ''
k = 0
userInput = 's'
rtype = '$'

#Define functions
def printInfo(index):
  rtype = '$'
  print('\nregister values: ')
  print(r)
  print('\nData Memory values: ')
  print(addresses)
  print(' ')
  #Print instruction code
  #addi, ori, andi, sw, lw, beq, bne
  splitInstr = instrCode[k].split(' ')
  if splitInstr[0] == 'addi' or splitInstr[0] == 'ori' or splitInstr[0] == 'andi' or splitInstr[0] == 'beq' or splitInstr[0] == 'bne':
    
    rtype = '' 
    print('PC: ' + pc[index] + '\nInstruction: ' + splitInstr[0] + ' $' + splitInstr[1] + ', $' + splitInstr[2] + ', ' + rtype + splitInstr[3])

  elif splitInstr[0] == 'sw' or splitInstr[0] == 'lw':
    rtype = ''
    print('PC: ' + pc[index] + '\nInstruction: ' + splitInstr[0] + ' $' + splitInstr[1] + ', ' + splitInstr[3] + '($' + splitInstr[2] + ')')


def binaryToDec(binary):
  #Converts decimal equivalent signed to unsigned
  if(binary[0] == "1"):
    indexStop = ''
    for i in range(15, 0, -1):
      if(binary[i] == "1"):
        indexStop = i
        break

    binList = list(binary)
      
    for i in range(0,indexStop):
      if(binary[i] == "1"):
        binList[i] = "0"
      else:
        binList[i] = "1"

    signed = ''.join(binList)
    decimal = str(-int(signed, 2))

  #Convert decimal equivalent if unsigned
  else:
    decimal = str(int(binary, 2))
    
  return decimal

def rtype(instr, rs, rt, shift, rd, i):
  #Figure out decimal equivalent of arguments
  rs = binaryToDec(rs)
  rt = binaryToDec(rt)
  rd = binaryToDec(rd)
  
  #Figure out what the instruction is
  if(instr == '100000'):
    instr = 'add'
  elif(instr == '100010'):
    instr = 'sub'
  elif(instr == '000010'):
    instr = 'srl'
  elif(instr == '101010'):
    instr = 'slt'
  elif(instr == '100100'):
    instr = 'and'
  elif(instr == '100110'):
    instr = 'xor'
  else:
    print('THIS IS NOT A VALID R TYPE INSTR')

  #Construct full instruction code and save in array
  instrCode[i] = instr + ' ' + str(rd) + ' ' + str(rs) + ' ' + str(rt)

def itype(instr, rs, rt, imm, i):
  #Figure out decimal equivalent of arguments
  rs = binaryToDec(rs)
  rt = binaryToDec(rt)
  imm = binaryToDec(imm)

  
  
  #Figure out what the instruction is
  if(instr == '001000'):
    instr = 'addi'
  elif(instr == '001101'):
    instr = 'ori'
  elif(instr == '001100'):
    instr = 'andi'
  elif(instr == '101011'):
    instr = 'sw'
    imm = hex(int(imm)).replace('0x','')
  elif(instr == '100011'):
    instr = 'lw'
    imm = hex(int(imm)).replace('0x','')
  elif(instr == '000100'):
    instr = 'beq'
  elif(instr == '000101'):
    instr = 'bne'
#  elif(instr == '111111'):
#    instr = 'adl'
  else:
    print('THIS IS NOT A VALID I TYPE INSTR')

  #Construct full instruction code and save in array

  instrCode[i] = instr + ' ' + str(rt) + ' ' + str(rs) + ' ' + str(imm)
  
#Get rid of line breaks
for i in range(len(hexLines)):
  hexLines[i] = hexLines[i].replace("\n", "")

#Computes PC for each line
for i in range(len(hexLines)):
  if(hexLines[i].find(':') < 0) and (i != 0):
    pc[i] = pc[i-1] + 4
  else:
    pc[i] = pc[i-1]

#Convert pc values to hex
for i in range(len(pc)):
  pc[i] = hex(pc[i])
  #If pc values are equal, line must be a label, keep track of labels with 'label' array
  if pc[i] == pc[i-1]:
    labels[i] = 1
    instrCode[i] = hexLines[i]

#Convert hex to binary
for i in range(len(hexLines)):
  #If line is not a label, convert to binary
  if(hexLines[i].find(':') < 0):
    binaryArray[i] = format(int(hexLines[i], 16), "032b")
    

#Figure out if it's an itype or rtype
for i in range(len(hexLines)):
  index = str(binaryArray[i])
  #R-Type [000000][5(rs)][5(rt)][5(rd)][5(sh)][6(func)]
  if (index[:6] == '000000'):
    rs = index[6:11]
    rt = index[11:16]
    rd = index[16:21]
    shift = index[21:26]
    instr = index[26:32]

    rtype(instr, rs, rt, shift, rd, i)

  elif(labels[i] == 1):
    #Deviate compiling of lines that are labels
    pass

  else:
    #I-Type [6(op)][5(rs)][5(rt)][16]
    instr = index[0:6]
    rs = index[6:11]
    rt = index[11:16]
    imm = index[16:32]

    itype(instr, rs, rt, imm, i)


#OUTPUT FOR TESTING PART ONE
#for i in range(len(hex)):
  #if binaryArray != '0':
    #print('Line ' + str(i) + ' is ' + binaryArray[i])
#print(hex)
#print(instrCode)

###############################################
##### PART TWO : MAKE INSTR CODE FUNCTION #####
###############################################

#Define userInput
userInput = input('enter s for step mode, or n for nonstop mode\n')
#Loop through and make code functional    
while (k < (len(instrCode))):

  #If line is not a label, find if i or r type
  if(hexLines[k].find(':') < 0):

    printInfo(k)
  
    splitCode = (instrCode[k]).split(' ')
  
    instr = splitCode[0]
    argOne = int(splitCode[1])
    argTwo = int(splitCode[2])
    argThree = int(splitCode[3])
  
    #Handling R-Type instructions
    if splitCode[0] == 'add':
      r[argOne] = r[argTwo] + r[argThree]
    elif splitCode[0] == 'sub':
      r[argOne] = r[argTwo] - r[argThree]
    elif splitCode[0] == 'srl':
      r[argOne] = r[argTwo] // (2^argThree)
    elif splitCode[0] == 'slt':
      if argTwo < argThree:
        argOne = 1
      else:
        argOne = 0
    elif splitCode[0] == 'and':
      r[argOne] = r[argTwo] & r[argThree]
    elif splitCode[0] == 'xor':
      r[argOne] = r[argTwo] ^ r[argThree]
  
    #Handling I-Type instructions
    elif splitCode[0] == 'addi':
      r[argOne] = r[argTwo] + argThree
    elif splitCode[0] == 'ori':
      r[argOne] = r[argTwo] + argThree
    elif splitCode[0] == 'andi':
      r[argOne] = r[argTwo] & argThree
    elif splitCode[0] == 'sw':
      hexValue = hex(argThree + r[argTwo])
      addresses[hexValue] = r[argOne]
    elif splitCode[0] == 'lw':
      hexValue = hex(argThree + r[argTwo])
      if hexValue not in addresses:
        addresses[hexValue] = 0
        
      r[argOne] = addresses[hexValue]
    elif splitCode[0] == 'beq':
      if (r[argOne]) == (r[argTwo]):
        newPC = int(pc[k].replace('0x',''), 16) + 4 + argThree * 4
        
        for j in range(len(pc)):
          if pc[j] == hex(newPC):
            k = j
          else:
            pass
    elif splitCode[0] == 'bne': 
      if (r[argOne]) != (r[argTwo]):
        newPC = int(pc[k].replace('0x',''), 16) + argThree * 4
        
        for j in range(len(pc)):
          if pc[j] == hex(newPC):
            k = j
          else:
            pass
#    elif splitCode[0] == 'adl':
#      r[argOne] = argThree 
#      r[argTwo] = argThree 
  
    else:
      print('This is not a usable instruction')

  if(userInput == 's'):
    #printInfo(k)
    userInput = input('Enter s for step mode, or n for nonstop mode\n')
  k+=1

print('\n------------------------------------\n')
print('FINAL VALUES:\n')
print('\nRegister Values ($0-$31):')
print(r)
print('\nIf applicable, here is the information that is stored in the data memory: ')
print(addresses)
  #Supported instructions:
  #R-Type: add, sub, srl, slt, and, xor
  #I-Type: addi, ori, andi, sw, lw, beq, bne
