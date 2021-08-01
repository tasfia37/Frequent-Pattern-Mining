import os
import time

class treeNode:
    def __init__(self, name1, count2, parentNode):
        self.name = name1
        self.count1 = count2
        self.Link = None
        self.parent = parentNode
        self.children = {}


    def __lt__(self, other):
        in1 = self.count1
        in2 = other.count1
        if in1 < in2:
            return True
        else:
            return False

    def inc(self, count2):
        self.count1 += count2

def create_headertable(dataSet):
    headertable = {}
    for trans in dataSet:
        for item in trans:
            if item!='':
                headertable[item] = headertable.get(item, 0) + dataSet[trans]
    return headertable

def prune_step(headertable,minSup,cnt3):
    for k in headertable.copy().keys():
        if headertable[k] < minSup*cnt3:
            del (headertable[k])
    return headertable

def sort_update(headertable,dataSet,freqItemSet):

    retTree = treeNode('Null Set', 1, None)
    for tranSet, count1 in dataSet.items():
        localID = {}
        for item in tranSet:
            if item in freqItemSet:
                localID[item] = headertable[item][0]
        if len(localID) > 0:
            orderedItems = [v[0] for v in sorted(localID.items(),key=lambda p: p, reverse=True)]
            updateTree(orderedItems, retTree, headertable, count1)

    return headertable,freqItemSet,retTree

def createTree(dataSet, minSup,cnt3):
    headertable=create_headertable(dataSet)
    headertable=prune_step(headertable, minSup, cnt3)
    freqItemSet = set(headertable.keys())
    # if no items meet minsup then return None
    if len(freqItemSet) == 0:
        return None, None
    for k in headertable:
        headertable[k] = [headertable[k], None]
    #Sort and update tree if there are new freqitemsets found
    headertable, freqItemSet, retTree=sort_update(headertable,dataSet,freqItemSet)
    return retTree, headertable


def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.Link != None):
        nodeToTest = nodeToTest.Link
    nodeToTest.Link = targetNode
def set_header(headertable,inTree,items):
    if headertable[items[0]][1] == None:
        headertable[items[0]][1] = inTree.children[items[0]]
    else:
        updateHeader(headertable[items[0]][1], inTree.children[items[0]])
    return headertable,inTree


def updateTree(items, inTree, headertable, count1):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count1)
    else:
        inTree.children[items[0]] = treeNode(items[0], count1, inTree)
        headertable,inTree=set_header(headertable,inTree,items)
    if len(items) > 1:
        updateTree(items[1:], inTree.children[items[0]], headertable, count1)

def read_data(file_name):
    data = []
    a = 0
    if not os.path.isfile(file_name):
        print("Not found")
        return None
    cnnt=0
    with open(file_name, 'r') as file:
        for line in file:
            z = []
            for x in line.split(' '):
                if x!='\n':
                    z.append(x)
                    cnnt+=1
            data.append(z)
            a = a + 1
    #print(data)
    print("numb of trans", a)
    print("total items: ",cnnt)
    return data,a


def loadSimpDat(az):
    if az==1:
        simpDat,cnt3 = read_data("mushroom.dat")
        return simpDat,cnt3
    if az == 2:
        simpDat,cnt3 = read_data("groceries.csv")
        return simpDat,cnt3

def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def cal_path(prefixPath,condPats,treeNode):
    if len(prefixPath) > 1:
        condPats[frozenset(prefixPath[1:])] = treeNode.count1
    treeNode = treeNode.Link
    return condPats,treeNode


def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        condPats, treeNode=cal_path(prefixPath,condPats,treeNode)
    return condPats


def mineTree(inTree, headertable, minSup, preFix, freqItemList,cnt3):
    bigL = [v[0] for v in sorted(headertable.items(),key=lambda p: p)]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headertable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup,cnt3)
        #print(myHead)
        if myHead :
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList,cnt3)



print("Enter 1 for dataset mushroom ")
print("Enter 2 for dataset  groceries ")

choice = int(input())
print("Enter minimum support value betweeen 0 to 1: ")
minSupp = input()
minSupp = float(minSupp)
simpleDat,cnt3 = loadSimpDat(choice)
#print(simpleDat)
print(minSupp,"  ",cnt3)
#simpleDat.pop('\n')
retDict = {}
for trans in simpleDat:
    retDict[frozenset(trans)] = 1
import time

# print(initSet)
start_time=time.time()
myFPtree, myHeaderTab = createTree(retDict,minSupp,cnt3)
freqItems = []
if myFPtree is not None:
    mineTree(myFPtree, myHeaderTab, minSupp, set(), freqItems,cnt3)
end_time=time.time()
print(freqItems)
print("Number of freq patterns generated: ",len(freqItems))

max_len=0
for x in freqItems:
    if len(x)>max_len:
        max_len=len(x)


counttt=0
for x in freqItems:
    if len(x)==max_len:
        counttt+=1

print("maximum size: ",max_len)
print("number of maximal itemsets is : ",counttt)
print("Number of freq patterns generated: ",len(freqItems))
print("Total time taken : ", end_time - start_time)
