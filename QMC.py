def decimalToBinary(n,varCount):
    t = bin(n).replace("0b", "")
    if len(t)<varCount:
        t= '0'*(varCount - len(t)) + t
    return t

def grpPrep(varCount):
    g=list()
    for i in range(varCount+1):
        g.append([])
    return g

def digitCombine(x,y,varCount,c):
    counter= 0
    newBit=''
    w=list(c)
    for index in range(0,varCount):
        if x[index] == y[index]:
            newBit+=x[index] 
        else:
            newBit+='_'
            w+=[index]
            counter+=1
    if counter>1:
        return False
    else:
        return [newBit,w]

def checkDup(grp,newTerm):
    for term in grp:
        if term[0]==newTerm:
            return 0
    return 1

def pairing(col,varCount,i=0):
    col.append([])
    col[i+1]=(grpPrep(varCount))
    anyPairing = 0
    for gc in range(varCount):
        if col[i][gc]:
            for termA in col[i][gc]:
                for termB in col[i][gc+1]:
                    if termA[3]==termB[3]:
                        newTermAndXpos = digitCombine(termA[0],termB[0],varCount,termA[3] )
                        if newTermAndXpos:
                            termA[2]=termB[2]=1
                            if checkDup(col[i+1][newTermAndXpos[0].count("1")],newTermAndXpos[0]):
                                incDec=termA[1]+termB[1]
                                incDec.sort()
                                col[i+1][newTermAndXpos[0].count("1")].append([newTermAndXpos[0],incDec,0,newTermAndXpos[1]])
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
                        for incDec in term[1]:
                            NumberCounter[incDec]+=1
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
    for cl in col:
        for grp in cl:
            if grp:
                for term in grp:
                    if not term[2]:
                        if any(True for x in EPI_dec if x in term[1]):
                            adr=[col.index(cl),cl.index(grp), grp.index(term)]
                            EPI_index.append(adr)
                            PI_chart_index.remove(adr)
                            for incDec in term[1]:
                                NumberCounter[incDec]=0
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
                if rm in col[adr[0]][adr[1]][adr[2]][1]:
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

def toLiterals(col,EPI_index,varCount):
    minli=[]
    li=[]
    for adr in EPI_index:
        li.append(col[adr[0]][adr[1]][adr[2]][0])
    for term in li:
        if term == '0'*varCount :
            minli.append("A'B'C'D'E'F'G'"[0:2*varCount])
        else:
            c= list(term) 
            minli.append(cycle(c,varCount))
    print(f"minimized SOP by literals = ", ' + '.join(minli))

def QMC(minterms , dontCareMint=[],varCount=4):
    col=[[],[]]
    col[0]=(grpPrep(varCount))
    decMinterms= set(list(map(int,minterms.strip().split()))).union(set(dontCareMint))
    for minterm in decMinterms:  
        col[0][bin(minterm).count("1")].append([decimalToBinary(minterm,varCount),[minterm], 0,[]])        
    pairing(col,varCount)
    PI_chart_index , NumberCounter=piChart(col,varCount)
    EPI_index = findEPI(col, PI_chart_index , NumberCounter ,dontCareMint)
    remaningMinterms=[]
    nc=0
    for index in NumberCounter: 
        if index:
            remaningMinterms.append(nc)
        nc+=1
    if remaningMinterms:
        reducedPI(col,PI_chart_index,remaningMinterms,EPI_index)
    toLiterals(col,EPI_index,varCount)

def main():
    print(f"* Welcome to Quine-McCluskey minimization method program *\n")
    varCount=int(input("\nEnter the number of variables : \n"))
    Minterms= input("\nEnter the minterms : ")
    x=input("\nIs there any Don't care minterms in the function ? (y/n)\t")
    if x=='y':
        dontCareMint=list(map(int,input("\nEnter Don't care terms:").strip().split()))
    else:
        dontCareMint=[]
    QMC(Minterms , dontCareMint ,varCount)
    c=int(input("\nEnter 1 to start again , 0 to exit the program\n"))
    if c==1:
        main()

main()
