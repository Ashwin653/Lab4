""
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
    This is the function for training a decision tree model
    """
    # implement your code here

    pass



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
    while val is not ")":
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
    if node.returnVal is not null:
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
        EvaNB(predictionLabel,trueLabel, outPerf)
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
