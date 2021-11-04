"""
 Name: Romeo Garcia, Ashwin Deodhar, Angela You
 Assignment: Lab 4 - Decision Tree
 Course: CS 330
 Semester: Fall 2021
 Instructor: Dr. Cao
 Date: 10/26/21
 Sources consulted: StackOverFlow, Dr.Cao
 
 Known Bugs: Program will run to a max recursion depth, causing itself to crash due to the method WriteNode.
 A similar issue happens in buildtreenode, but it does not cause a crash, rather, it causes a much
 longer running time.
 
 Creativity: N/A

 Instructions: Unfortunately, there is no real way to run this program without it ultimately crashing.
 The formatting we chose is organized, but somewhere there was a fatal mistake made in either
 the readfile, or buildtreenode method that prevents the code from ever fully running.

"""
import sys
import argparse
import math

# This is the Treenode class, which has a parent, an attribute as the value, and then a dictionary
# that contains all children associated to this node. It also has a return value.
class TreeNode:
    # This is used for decision trees #
    def __init__(self, attribute, children={}, returnVal=None):
        self.attribute = attribute
        self.children = children
        self.returnVal = returnVal
    
class DTTrainCL:
    # This is used to allow all the data for the DTTrain method to be changed if needed
    data_dict = {}  # initialize a dictionary for storing data
    attValues = {}  # initialize the dictionary of attribute values
    atts = list()       # initialize atts list
    numAtts = -1    # initialize the numAtts int
    numClasses = -1 # initialize the numClasses int
    def __init__(self):
        self = self
        
class DTPredictCL:
    # This is used to allow all the data for the DTPredict method to be changed if needed
    attArr = list()
    root = TreeNode(None)
    predictions = list()
    def __init__(self):
        self = self



# this is function acts as a log base 2.
def log2(x):
    if(x == 0): return 0
    return math.log(x)/math.log(2)

# utilizes the log2 function to calculate the entropy of the chosen classCount, which is an integer array.
def entropy(classCounts):
    total = 0.0
    for i in classCounts:
      total += i
    
    sum1, i = 0.0, 0
    while (i < len(classCounts)):
        sum1 -= (classCounts[i]/(total + 0.000000001))*log2(classCounts[i]/(total + 0.000000001))
        i += 1
    return sum1


# Uses the entropy method and a partition of data to supply again, the entropy of the
# provided data.
def partitionEntropy(partition):
    totalEnt, total, i = 0, 0, 0
    
    while (i < len(partition)):
        n, j = 0, 0
        while (j < len(partition[0])):
            n += partition[i][j]
            total += partition[i][j]
            j += 1
        totalEnt += n * entropy(partition[i])
        i += 1
    return totalEnt/(total + 0.000000001)


# The Write node method, made instead in python.
def writeNode(outfile, current):
    with open(outfile, "w") as f:
        if(current.returnVal is not None):
            f.write("[" + current.returnVal + "] ")
            return
        f.write(current.attribute + " ( ")
        for key, value in current.children.items():
            f.write(key + " ")
            #print(value)
            writeNode(outfile, value)
        f.write(" ) ")
    
    
# Saves the loaded model to a file.
def saveModel(modelfile, root, dtt):
    try:
        file = open(modelfile, "w")
        i = 0
        while(i < dtt.numAtts-1):
            file.write(dtt.atts[i+1] + " ")
            i += 1
        file.write("\n")
        writeNode(modelfile, root)
        file.close()
    except Exception as e: print(e)

# effectively will read in all the data in the file and parse it into a usable format for the rest of the code.
def readFile(data, dtt):
    try:
        # open the training data file
        file = open(data, "r")
        # read the attributes from the first line of the file
        attline = file.readline()
        dtt.atts = attline.split("|")
        dtt.numAtts = len(dtt.atts)
        
        # this fills the list designated for the values associated with the attributes
        for a in dtt.atts:
            dtt.attValues[a] = list()
            
        # read data into dictionary
        index = 0 # for percent math
        for x in file:
            data = x.split() # parse the data for the use throughout this iteration. (data[0] is our 'dataclass')
            arr = dtt.attValues.get(dtt.atts[0]) # access the list from the first attribute in attvalues
            if(arr.count(data[0]) == 0):
                arr.append(data[0]) # this will modify the other list in attvalues, adding the data for this first attribute
            
            if data[0] not in dtt.data_dict: # modifying the data_dict so that all outcomes of the first attribute are seperated and have their own outcomes.
                dtt.data_dict[data[0]] = list()
                    
            a = dtt.data_dict.get(data[0]) # retrieving the list we made just above
            datapoint = list() # another list for [figure out what this is doing]
            for i in range(dtt.numAtts):
                if(i == 0): # skips the first value as we don't need it here
                    continue
                val = data[i] # retrieve the next value
                datapoint.append(val) # put data point into data map
                arr = dtt.attValues.get(dtt.atts[i])
                if val not in arr:
                    arr.append(val)
            # only add data point to the dictionary 'percent' of the time.
            if(index%100 < 100):
                a.append(datapoint)
            index += 1
        
        dtt.numClasses = len(dtt.data_dict.keys())
    except Exception as e: print(e)

# this is the method that will help with the recursive process of building the tree.
def buildTreeNode(parent, currFreeAtts, dtt, nodeData, i):
    if(len(nodeData) == 0):
        nodeData = dtt.data_dict
    
    # build the current tree node
    curr = TreeNode(parent)
    
    minEnt = 1 
    minAtt = None
    # calculate the current entropy for each attribute
    for i in range(dtt.numAtts-1): # for each attribute
        att = currFreeAtts[i] # get the attribute
        if att is not None: # if the attribute hasn't already been used in the tree
            vals = dtt.attValues[att] # get the list of possible values for each attribute
            rows, columns = len(vals), dtt.numClasses
            partition = [[0 for x in range(columns)] for y in range(rows)] # store class counts for each outcome
            for j in range(dtt.numClasses): # for each classification
                outcome = dtt.attValues.get(dtt.atts[0])[j]
                # print(outcome)
                l = nodeData.get(outcome)
                for l2 in l:
                    #print(len(l2), i, dtt.numAtts)
                    x = vals.index(l2[i])
                    partition[x][j] += 1
            # calculate entropy
            ent = partitionEntropy(partition)
            #print(att + ent)
            if(ent < minEnt):
                minEnt, minAtt = ent, att
    # if we are at the base of the tree
    if(minAtt is None):
        maxVal = 0
        maxClass = "undefined"
        for j in range(dtt.numClasses): # for each classification
            outcome = dtt.attValues.get(dtt.atts[0])[j]
            if(len(nodeData.get(outcome)) >= maxVal):
                maxVal = len(nodeData.get(outcome))
                maxClass = outcome
        #print(maxClass)
        curr.returnVal = maxClass
        return curr
    # find the best attribute
    curr.attribute = minAtt
    attIndex = currFreeAtts.index(minAtt)
    currFreeAtts[attIndex] = None
    
    # build child nodes
    for v in dtt.attValues.get(minAtt):
        temp_dict = {}
        for j in range(dtt.numClasses):
            outcome = dtt.attValues.get(dtt.atts[0])[j]
            trimList = list()
            l = nodeData.get(outcome)
            for l2 in l:
                if(l2[attIndex] == v):
                    trimList.append(l2)
            temp_dict[outcome] = trimList
        print(v + "---> ")
        #print(i, "----- This is an issue")
        #i += 1
        curr.children[v] = buildTreeNode(curr, currFreeAtts, dtt, temp_dict, i)
    # return the built node
    currFreeAtts[attIndex] = minAtt
    return curr


def DTtrain(data, model):
    """
    This is the function for training a decision tree model, or more importantly, DTtrain will be the one
    building the tree, and calling all the helper methods after being given the critical info from the main.
    """
    # initialize all the values needed for the DTTrain process
    dtt = DTTrainCL()

    # read the file here
    readFile(data, dtt)
    
    # build the tree here.
    root = TreeNode(None)
    currFreeAtts = list()
    i = 0
    while(i < dtt.numAtts-1):
        currFreeAtts.append(dtt.atts[i+1])
        i += 1
        
    i = 0
    nodeData = {}
    root = buildTreeNode(None, currFreeAtts, dtt, nodeData, i)
    
    # save the model at the end for comparison.
    saveModel(model, root, dtt)


def DTpredict(data, model, prediction):
    """
    This is the main function to make predictions on the test dataset. It will load saved model file,
    and also load testing data TestDataNoLabel.txt, and apply the trained model to make predictions.
    You should save your predictions in prediction file, each line would be a label, such as:
    1
    0
    0
    1
    ...
    """
    dtp = DTPredictCL()
    
    readModel(model, dtp)
    print("Model read successfully")
    predictFromModel(data, dtp)
    print("Predictions complete")
    savePredictions(prediction, dtp)
    print("Predictions saved to file: ", prediction)
    
def readModel(model, dtp):
    infile = open(model, 'r')
    for line in infile:
        dtp.attArr = [i for i in line.split()]
    dtp.root = readNode(dtp.attArr)

def readNode(atts):
    # read att for node
    n = atts[0]
    if n[0] == '[': # build return node
        return TreeNode(None, None, n.substring(1, len(n) - 1))
    # build interior node
    node = TreeNode(n, {}, None)
    val = atts[2]

    index = 2
    while val != ")":
        node.children.put(val, readNode(atts))
        index += 1
        val[index]
    return node

   
def predictFromModel(data, dtp):
    try:
        s = open(data, 'r')
        data = []
        dtp.predictions = []
        for element in s:
            next(s) #skips -1
            for element in dtp.attArr:
                data.append(element)
            pred = traceTree(dtp.root, data, dtp)
            dtp.predictions.append(pred)
    except:
        print("test file has error")

      
def traceTree(node, data, dtp):
    if node.returnVal != None:
        return node.returnVal
    att = node.attribute
    val = data.get(dtp.attArr.index(att))
    t = node.children.get(val)
    return traceTree(t, data)

   
def savePredictions(output, dtp):
    try:
        outfile = open(output, 'w')
        for element in dtp.predictions:
            outfile.write(element)
        outfile.close()
    except:
        print("error writing to file")


def EvaDT(predictionLabel, realLabel, output):
    """
    This is the main function. You should compare line by line,
     and calculate how many predictions are correct, how many predictions are not correct. The output could be:
    In total, there are ??? predictions. ??? are correct, and ??? are not correct.
    """
    correct,incorrect, length = 0,0,0
    with open(predictionLabel,'r') as file1, open(realLabel, 'r') as file2:
        pred = [line for line in file1]
        real = [line for line in file2]
        length = len(pred)
        for i in range(length):
            if pred.pop(0) == real.pop(0):
                correct += 1
            else:
                incorrect += 1
    Rate = correct/length

    result = "In total, there are "+str(length)+" predictions. "+str(correct)+" are correct and "+ str(incorrect) + " are incorrect. The percentage is "+str(Rate)
    with open(output, "w") as fh:
        fh.write(result)
       
       
def main():
    options = parser.parse_args()
    mode = options.mode       # first get the mode
    print("mode is " + mode)
    if mode == "T":
        """
        The training mode
        """
        inputFile = options.input
        outModel = options.output
        if inputFile == '' or outModel == '':
            showHelper()
        DTtrain(inputFile, outModel)
    elif mode == "P":
        """
        The prediction mode
        """
        inputFile = options.input
        modelPath = options.modelPath
        outPrediction = options.output
        if inputFile == '' or modelPath == '' or outPrediction == '':
            showHelper()
        DTpredict(inputFile,modelPath,outPrediction)
    elif mode == "E":
        """
        The evaluating mode
        """
        predictionLabel = options.input
        trueLabel = options.trueLabel
        outPerf = options.output
        if predictionLabel == '' or trueLabel == '' or outPerf == '':
            showHelper()
        EvaDT(predictionLabel,trueLabel, outPerf)
    pass

def showHelper():
    parser.print_help(sys.stderr)
    print("Please provide input augument. Here are examples:")
    print("python " + sys.argv[0] + " --mode T --input TrainingData.txt --output DTModel.txt")
    print("python " + sys.argv[0] + " --mode P --input TestDataNoLabel.txt --modelPath DTModel.txt --output TestDataLabelPrediction.txt")
    print("python " + sys.argv[0] + " --mode E --input TestDataLabelPrediction.txt --trueLabel LabelForTest.txt --output Performance.txt")
    sys.exit(0)


if __name__ == "__main__":
    #------------------------arguments------------------------------#
    #Shows help to the users                                        #
    #---------------------------------------------------------------#
    parser = argparse.ArgumentParser()
    parser._optionals.title = "Arguments"
    parser.add_argument('--mode', dest='mode',
    default = '',    # default empty!
    help = 'Mode: T for training, and P for making predictions, and E for evaluating the machine learning model')
    parser.add_argument('--input', dest='input',
    default = '',    # default empty!
    help = 'The input file. For T mode, this is the training data, for P mode, this is the test data without label, for E mode, this is the predicted labels')
    parser.add_argument('--output', dest='output',
    default = '',    # default empty!
    help = 'The output file. For T mode, this is the model path, for P mode, this is the prediction result, for E mode, this is the final result of evaluation')
    parser.add_argument('--modelPath', dest='modelPath',
    default = '',    # default empty!
    help = 'The path of the machine learning model ')
    parser.add_argument('--trueLabel', dest='trueLabel',
    default = '',    # default empty!
    help = 'The path of the correct label ')
    if len(sys.argv)<3:
        showHelper()
    main()
