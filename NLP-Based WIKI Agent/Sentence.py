class Sentence:
    def __init__(self, textArray=[]):
        self.textArray = textArray
        self.parseTree()

    def setRootNode(self,rootNode):
        self.root_node = rootNode

    def setup(self):
        stack1 = []
        stack2 = []
        i = 0
        for t in self.textArray:
            if t=="(":
                node = Node(self.textArray[i+1])
                stack1.append(node)
            elif t==")":
                node = stack1.pop()
                if self.textArray[i-1] not in ")":
                    node.value = self.textArray[i-1]
                else:
                    for n in stack2:
                        nd = stack2.pop()
                        node.addChild(nd)
                stack2.append(node)
            i+=1
        self.setRootNode(stack2.pop())

    def parseTree(self):
        stack1 = []
        stack2 = []
        i = 0
        rootNode = Node("ROOT")
        for t in self.textArray:
            if t == "(":
                node = Node(self.textArray[i + 1])
                stack1.append(node)
            elif t == ")":
                node = stack1.pop()
                rootNode = node
                if self.textArray[i - 1] not in ")":
                    node.value = self.textArray[i - 1]
                if stack1:
                    stack1[-1].addChild(node)

            i += 1
        self.setRootNode(rootNode)

    def traverseDFS(self):
        self.DFS(self.root_node)

    def DFS(self,node):
        print node.name
        if node.children:
            for n in node.children:
                self.DFS(n)



        # rn = False
        # sp= False
        # name=""
        # val=""
        # v=False
        # for c in self.text:
        #     if c in ["(",")"]:
        #         rn = True
        #     elif c in ["\\"]:
        #         sp = True
        #         rn= False
        #     elif c in [" "]:
        #         if rn:
        #             v= True
        #         rn = False;
        #         sp = False
        #     else:
        #         if rn:
        #             name+=c
        #         elif v:
        #             val+=c



class Node:
    def __init__(self, name="", value=""):
        self.name = name
        self.value = value
        self.children = []
        self.text = ""

    def addChild(self, node):
        self.children.append(node)

    def __str__(self):
        return self.name
    def get_text(self):
        no = Node(self.name, self.value)
        no.children = self.children
        self.DFS(no)
        t = self.text
        self.text = ""
        return t

    def DFS(self, node):
        if node.children:
            for n in node.children:
                self.DFS(n)
        else:
            self.text += node.value+" "
