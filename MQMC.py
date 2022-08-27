def grpPrep(varCount):
    g=list()
    for i in range(varCount+1):
        g.append([])
    return g

def pairing(col,varCount,i=0):
    col.append([])
    col[i+1]=(grpPrep(varCount))
    p=[1,2,4,8,16,32,64,128]
    anyPairing = 0
    for gc in range(varCount):
        if col[i][gc]:
            for termA in col[i][gc]:
                numOf1s = gc
                for termB in col[i][gc+1]:
                    if termA[1]==termB[1]:
                        if (termB[0][0] - termA[0][0])in p:
                            termA[2]=termB[2]=1
                            newTerm = [termA[0]+termB[0] , termA[1]+(termB[0][0] - termA[0][0]),0]
                            newTerm[0].sort()
                            if not newTerm in col[i+1][ numOf1s ]:
                                col[i+1][numOf1s].append(newTerm)
                                anyPairing=1
    if anyPairing:
        pairing(col,varCount,i+1)

def piChart(col,varCount):
    PI_chart_index = list()
    NumberCounter=[0]*2**varCount
    for cl in col: 
        for grp in cl:
            if grp:
                for term in grp:
                    if not term[2]:
                        PI_chart_index.append([col.index(cl),cl.index(grp),grp.index(term)])
                        for minterm in term[0]:
                            NumberCounter[minterm]+=1
    return (PI_chart_index,NumberCounter)

def findEPI(col, PI_chart_index , NumberCounter ,dontCareMint):
    EPI_index=[]
    EPI_dec=[]
    if dontCareMint:
        for i in dontCareMint:
            NumberCounter[i]=0
    for i in range(len(NumberCounter)):
        if NumberCounter[i] == 1:
            EPI_dec.append(i)
    for adr in PI_chart_index:
        if any(True for x in EPI_dec if x in col[adr[0]][adr[1]][adr[2]][0]):
            adr=[adr[0],adr[1],adr[2]]
            EPI_index.append(adr)
            for minterm in col[adr[0]][adr[1]][adr[2]][0]:
                NumberCounter[minterm]=0
    PI_chart_index= [x for x in PI_chart_index if x not in EPI_index ]
    return EPI_index

def reducedPI(col,PI_chart_index,remaningMinterms,EPI_index,step=0):
    success=0
    if len(remaningMinterms)>1:
        satisfyingLen= len(remaningMinterms) - step
    else:
        satisfyingLen = 1    
    for adr in PI_chart_index :
        if not success:
            counter = 0
            incDecOfEPI=[]
            for rm in remaningMinterms:
                if rm in col[adr[0]][adr[1]][adr[2]][0]:
                    incDecOfEPI.append(rm)
                    counter+=1
            if counter == satisfyingLen:
                EPI_index.append(adr)
                PI_chart_index.remove(adr)
                for i in incDecOfEPI:
                    remaningMinterms.remove(i)
    if remaningMinterms :
        if not success:
            reducedPI(col,PI_chart_index,remaningMinterms,EPI_index,step+1)

def digitCombine(x,y):
    counter= 0
    newBit=''
    for index in range(0,len(x)):
        if x[index] == y[index]:
            newBit+=x[index] 
        else:
            newBit+='_'
            counter+=1
    if counter>1:
        return False
    else:
        return newBit

def mintermToBit(mintermsList,varCount):
    bits=list()
    for i in mintermsList:
        b=bin(i).replace("0b", "")
        if varCount > len(b):
            b= '0'*(varCount-len(b)) + b
        bits.append(b)  
    return bits

def combineBits(mintermsList,varCount,s=0):
    if s==0:
        bits = mintermToBit(mintermsList,varCount)
    else:
        bits=mintermsList
    minList=[]
    for b in bits:
        ii=0
        bits.remove(b)
        for r in bits:
            x=digitCombine(b,r)
            if x:
                bits.append(x)
                bits.remove(r)
                ii=1
                break
    if not ii:
        bits.append(b)            
    if len(bits)!=1 :
        combineBits(bits,varCount,1)
    if len(bits)==1:
        return bits   

def cycle(x,varCount,c=''):
    al= list("ABCDEFG")
    p = varCount - len(x)
    if len(x) != 0 :
        if(x[0] == '0'):
            c += al[p]+"'"
        if(x[0] == '1'):
            c += al[p]
    if len(x)>1:
        return cycle(x[1:],varCount,c)
    if len(x)==1:
        return c

def toLiterals(minimizedList,varCount):
    minli=[]
    for term in minimizedList:
        if term[0] == '0'*varCount :
            minli.append("A'B'C'D'E'F'G'"[0:2*varCount])
        else:
            c= list(term[0]) 
            minli.append(cycle(c,varCount))
    print(f"minimized SOP by literals = ", ' + '.join(minli))

def MQMC(minterms , dontCareMint=[],varCount=4):
    col=[[],[]]
    col[0]=(grpPrep(varCount))
    decMinterms= set(list(map(int,minterms.strip().split()))).union(set(dontCareMint))
    for minterm in decMinterms:  
        col[0][bin(minterm).count("1")].append( [ [minterm] , 0 , 0 ] )
    pairing(col,varCount)
    PI_chart_index,NumberCounter = piChart(col,varCount)
    EPI_index = findEPI(col, PI_chart_index , NumberCounter ,dontCareMint)
    remaningMinterms=[]
    nc=0
    for index in NumberCounter: 
        if index:
            remaningMinterms.append(nc)
        nc+=1
    if remaningMinterms:
        reducedPI(col,PI_chart_index,remaningMinterms,EPI_index)  
    minimizedList=[]
    for adr in EPI_index:
        minimizedList.append(combineBits(col[adr[0]][adr[1]][adr[2]][0],varCount))
    toLiterals(minimizedList,varCount)

def main():
    print(f"* Welcome to Modified Quine-McCluskey minimization method program *\n")
    varCount=int(input("\nEnter the number of variables : \n"))
    Minterms= input("\nEnter the minterms : ")
    x=input("\nIs there any Don't care minterms in the function ? (y/n)\t")
    if x=='y':
        dontCareMint=list(map(int,input("\nEnter Don't care terms:").strip().split()))
    else:
        dontCareMint=[]
    MQMC(Minterms , dontCareMint ,varCount)
    c=int(input("\nEnter 1 to start again , 0 to exit the program\n"))
    if c==1:
        main()

main()
