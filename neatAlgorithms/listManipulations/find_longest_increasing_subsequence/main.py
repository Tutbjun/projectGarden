import random as rand
import numpy as np

listLength = 10

def initList():
    floatList = []
    for i in range(listLength):
        floatList.append(rand.random())
    return floatList

class branch(list):
    depth = 0;
    def get_tipIndecies(self):
        try:
            return [e.getTipIndecies() for e in self]
        except TypeError:
            return list(range(len(self)))
    def get_multiDimIndex(self,index):
        for i in index:
            vals = []
            try:
                vals.append(self[i])
            except TypeError:
                vals.append(self[i].get_multiDimIndex(i))
    def append_multiDimIndexVal():
        return
    def add_branch():
        return

            

def find_LIS(list):
    tree = branch();
    tree.append(list[0])
    tree.depth += 1
    for i,e in enumerate(list):
        indexs = tree.get_tipIndecies()
        for j,f in enumerate(tree.get_multiDimIndex(indexs)):
            if e > f:
                tree.append_multiDimIndexVal(j,indexs,e)
            elif e < f:
                tree.add_branch(j,indexs,e)
        if i % 10 == 0:
            tree.cleanup_LIS()

        


def main():
    raise NotImplementedError
    subject = initList()
    LIS = find_LIS(subject)

if __name__ == "__main__":
    main()