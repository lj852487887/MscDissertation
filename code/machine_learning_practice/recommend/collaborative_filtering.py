from numpy import *
from numpy import  linalg as la
import svd

def eulidSim(inA,inB):
    return 1.0/(1.0 + la.norm(inA - inB))

def pearsSim(inA,inB):
    if len(inA) < 3: return 1.0
    return 0.5+0.5*corrcoef(inA,inB,rowvar=0)[0][1]

def cosSim(inA,inB):
    num = float(inA.T*inB)
    denom = la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)

def standEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[1]
    simTotal = 0.0
    ratSimTotal = 0.0
    for j in range(n):
        userRating = dataMat[user,j]
        if userRating == 0:continue
        overLap = nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]
        if len(overLap)==0:similarity = 0
        else:similarity = simMeas(dataMat[overLap,item],dataMat[overLap,j])

        print "the %d and %d similarity is: %f" % (item,j,similarity)
        simTotal += similarity
        ratSimTotal += simTotal*userRating
    if simTotal==0:return 0
    else: return ratSimTotal/simTotal

def recommend(dataMat,user,N=3,simMeas=cosSim,estMethod=standEst):
    unratedItems = nonzero(dataMat[user,:].A==0)[1]
    if len(unratedItems) == 0: return "you rated everything"
    itemScore = []
    for item in unratedItems:
        estimateScore = estMethod(dataMat,user,simMeas,item)
        itemScore.append((item,estimateScore))
    return sorted(itemScore,key=lambda jj:jj[1],reverse=True)[:N]

if __name__ == "__main__":
    exData =   [[4,4,0,2,2],
                [4,0,0,3,3],
                [4,0,0,1,1],
                [1,1,1,2,0],
                [2,2,2,0,0],
                [1,1,1,0,0],
                [5,5,5,0,0]]
    myMat = mat(exData)
    print recommend(myMat,2)
