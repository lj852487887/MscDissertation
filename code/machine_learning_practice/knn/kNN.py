from numpy import *
import  operator
import matplotlib
import matplotlib.pyplot as plt


def createDataset():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def kNNClassif(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = argsort(distances)
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def fileToMatrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normedDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normedDataSet = dataSet - tile(minVals,(m,1))
    normedDataSet = normedDataSet/tile(ranges,(m,1))
    return normedDataSet,ranges,minVals

def datingClassTest():
    sampleRatio = 0.1
    datingDataMat,datingLabels = fileToMatrix("datingTestSet2.txt")
    normMat,ranges,minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVec = int(m*sampleRatio)
    errorCount = 0.0
    for i in range(numTestVec):
        classifierResult = kNNClassif(normMat[i,:],normMat[numTestVec:m,:],datingLabels[numTestVec:m],3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult,datingLabels[i])
        if(classifierResult != datingLabels[i]): errorCount+=1.0
    print "the total error rate is %f" % (errorCount/float(numTestVec))

def plotDataSet():
    datingDataMat,datingLabels = fileToMatrix('datingTestSet2.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(datingLabels),15.0*array(datingLabels))
    plt.show()

def classifyPerson():
    resultList = ['not at all','in small doess','in large doess']
    percentTats = float(raw_input("percentage of time spent playing games?"))
    ffMiles = float(raw_input("flier miles earned per year?"))
    iceCream = float(raw_input("ice cream comsumed per year?"))
    datingDataMat,datingLabels = fileToMatrix("datingTestSet2.txt")
    normMat,ranges,minVals = autoNorm(datingDataMat)
    inArr = array([percentTats,ffMiles,iceCream])
    classifierResult = kNNClassif((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "you will probably like this person: ",resultList[classifierResult]


if __name__ == '__main__':
    #plotDataSet()
    #datingClassTest()
    classifyPerson()