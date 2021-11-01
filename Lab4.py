"""
 Name: Romeo Garcia, Ashwin Deodhar, Angela You
 Assignment: Lab 4 - Decision Tree
 Course: CS 330
 Semester: Fall 2021
 Instructor: Dr. Cao
 Date: 10/26/21

 Sources consulted: N/A
 Known Bugs: N/A
 Creativity: N/A

 Instructions: After a lot of practice in Python, in this lab, you are going to design the program
 for decision tree and implement it from scrath! Don't be panic, you still have some reference, 
 actually you are going to translate the JAVA code to Python! The format should be similar to Lab 2!

"""
import sys
import argparse
import math
import os

# This is the Treenode class, which has a parent, an attribute as the value, and then a dictionary
# that contains all children associated to this node. It also has a return value.
class TreeNode:
    # This is used for decision trees #
    def __init__(parent, attribute, children={}, returnVal=None):
        parent.attribute = attribute
        parent.children = children
        parent.returnVal = returnVal
    def __str__(parent):
        return str(parent.attribute)

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
        sum1 -= (classCounts[i]/total)*log2(classCounts[i]/total)
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
    return totalEnt/total

   
# readfile is a helper method that will store our data from the provided
# data set and get it ready to use to build the tree.
def readFile(infile, percent, data_dict, attvalues, atts, numAtts, numClasses):
    try:
        # open the training data file
        file = open(infile, "r")
        # read the attributes from the first line of the file
        attline = file.readline()
        atts = attline.split("|")
        numAtts = len(atts)-1
        
        # this fills the list designated for the values associated with the attributes
        for a in atts:
            attvalues[a] = {}
            
        # read data into dictionary
        index = 0 # for percent math
        for x in file:
            data = x.split() # parse the data for the use throughout this iteration. (data[0] is our 'dataclass')
            
            arr = attvalues.get(atts[0]) # access the list from the first attribute in attvalues
            if(arr.count(data[0]) == 0):
                arr.append(data[0]) # this will modify the other list in attvalues, adding the data for this first attribute
            
            if data[0] not in data_dict: # modifying the data_dict so that all outcomes of the first attribute are seperated and have their own outcomes.
                data_dict[data[0]] = {}
                    
            a = data_dict.get(data[0]) # retrieving the list we made just above
            datapoint = list() # another list for [figure out what this is doing]
            for i in range(numAtts):
                if(i == 0): # skips the first value as we don't need it here
                    continue
                val = data[i] # retrieve the next value
                datapoint.append(val) # put data point into data map
                arr = attvalues.get(atts[i])
                if val not in arr:
                    arr.append(val)
            # only add data point to the dictionary 'percent' of the time.
            if(index%100 < percent):
                a.append(datapoint)
            index += 1
        
        numClasses = len(data_dict.keys())
    except :
        print("Error reading file: " + infile)
        sys.exit(0)


# The Write node method, made instead in python.
def writeNode(outfile, current):
    if(current.returnVal != None):
        outfile.print("[" + current.returnVal + "] ")
        return
    outfile.print(current.attribute + " ( ")
    for ch in current.children:
        outfile.print(ch.getKey() + " ")
        writeNode(outfile, ch.getValue())
    outfile.print(" ) ")
    

# Saves the loaded model to a file.
def saveModel(modelfile, numAtts, root, atts):
    try:
        file = open(modelfile, "w")
        i = 0
        while(i < len(numAtts)):
            file.write(atts[i+1] + " ")
        file.write("\n")
        writeNode(file, root)
        file.close()
    except:
        print("Error writing to file ")
        sys.exit(0)


def DTtrain(data, model):
    """
    This is the function for training a decision tree model, or more importantly, DTtrain will be the one
    building the tree, and calling all the helper methods after being given the critical info from the main.
    """
    data_dict = {}  # initialize a dictionary for storing data
    attvalues = {}  # initialize the dictionary of attribute values
    atts = list()       # initialize atts list
    numAtts = -1    # initialize the numAtts int
    numClasses = -1 # initialize the numClasses int
    readFile(data, 100, data_dict, attvalues, atts, numAtts, numClasses)  # read in the data given, and prepare all fields initialize earlier for the build.

    # build the tree here.
    root = TreeNode()
    
    
    # save the model at the end for comparison.
    saveModel(model)



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
  
    readModel(model)
    print("Model read successfully")
    predictFromModel(data)
    print("Predictions complete")
    savePredictions(prediction)
    print("Predictions saved to file: ", prediction)
    
def readModel(model):
    infile = open(model, 'r')
    for line in infile:
        atts = [i for i in line.split()]
    root = readNode(atts)

def readNode(infile):
    #read att for node
    n = infile[0]
    if n[0] == '[': #build return node
        return TreeNode(null, null, n.substring(1, len(n) - 1))
    #build interior node
    node = TreeNode(n, {}, null)
    val = infile[2]

    index = 2
    while val != ")":
        node.children.put(val, readNode(infile))
        index += 1
        val[index]
    return node

   
def predictFromModel(data):
    try:
        s = open(data, 'r')
        data = []
        predictions = []
        for element in s:
            next(s) #skips -1
            for element in attArr:
                data.append(element)
            pred = traceTree(root, data)
            predictions.append(pred)
    except:
        print("test file has error")

      
def traceTree(node, data):
    if node.returnVal != null:
        return node.returnVal
    att = node.attribute
    val = data.get(attArr.index(att))
    t = node.children.get(val)
    return traceTree(t, data)

   
def savePredictions(output):
    try:
        outfile = open(output, 'w')
        for element in predictions:
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
