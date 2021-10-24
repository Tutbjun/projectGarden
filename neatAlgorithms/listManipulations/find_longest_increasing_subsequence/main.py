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
            

def find_LIS(list):
    tree = branch();
    tree.append(list[0])
    tree.depth += 1
    for i,e in enumerate(list):
        for j,f in enumerate(tree):
            if e


def main():
    subject = initList()
    LIS = find_LIS(subject)

if __name__ == "__main__":
    main()