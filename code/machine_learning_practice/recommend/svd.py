from numpy import  *


def svdMat(mat):
    U,Sigma,VT = linalg.svd(mat)
    print U
    print "###########################"
    print "sigma:",Sigma
    print "###########################"
    print VT
    print "###########################"
    return (U,Sigma,VT)


def recMatFromSvd(svdResult):
    U = svdResult[0]
    Sigma = svdResult[1]
    VT = svdResult[2]
    SigmaNew = mat([[Sigma[0],0,0],[0,Sigma[1],0],[0,0,Sigma[2]]])
    print U[:,:3]*SigmaNew*VT[:3,:]

def loadExData():
    return [[1,1,1,0,0],
            [2,2,2,0,0],
            [1,1,1,0,0],
            [5,5,5,0,0],
            [1,1,0,2,2],
            [0,0,0,3,3],
            [0,0,0,1,1]]

if __name__ == "__main__":
    recMatFromSvd(svdMat(loadExData()))