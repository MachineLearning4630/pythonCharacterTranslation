import random
import numpy as np
import math
import csv
import sys

#rate the data is trained at
rate=.0000001

#sigmoid activation function
def sigmoid(x):
    return 1/(1 + math.exp(-x));
#Function to encode data
def encode(data,length):
    encoded = np.matrix(np.zeros([20,1]))
    for word in range(0,length):
        for node in range(0,20):
            data[301,word]=encoded[node,0]
            encoded[node,0]=np.dot(encoder[node],data[:,[word]])
    return encoded;
#Function to decode data
def decode(encoding,length):
    decode_t = np.matrix(np.zeros([20,1]))
    decoded = np.matrix(np.zeros([20,length]))
    for word in range(0,length):
        for node in range(0,20):
            encoding[21]=decode_t[node,0]
            decode_t[node,0]=np.dot(decoder[node],encoding)
            decoded[:,[word]]=decode_t;
    return decoded;
#Function to output a single vector with an output node
def output(decoding):
    out=np.dot(outw,decoding)
    return out;

#Function to train the layers
def train():
    for j in range (0,100):
        for i in range (0,100):
            #initialize gradient matrices
            encoder_gradient = np.matrix(np.zeros([20,302]))
            decoder_gradient = np.matrix(np.zeros([20,22]))
            output_gradient= np.matrix(np.zeros([1,22]))
            word=np.matrix(np.ones([302,1]))
            for dat in range (0,300):
                word[dat,0]=englishVectorFromCSV[i,dat]
            #encoder layer
            encoded = np.matrix(np.zeros([20,1]))
            for node in range(0,20):
                word[301,0]=0;
                encoded[node,0]=np.dot(encoder[node],word)
            encoded_e = np.matrix(np.ones([22,1]))
            for o in range(0,20):
                encoded_e[o,0]=encoded[o,0]
            #decoder layer
            decoded = np.matrix(np.zeros([20,1]))
            for node in range(0,20):
                encoded_e[21,0]=0;
                decoded[node,0]=np.dot(decoder[node],encoded_e)
            decoded_e = np.matrix(np.ones([22,1]))
            for o in range(0,20):
                decoded_e[o,0]=decoded[o,0]
            #output layer
            output=np.dot(outw,decoded_e)
            #output gradient
            out_error=output[0,0]-i*100
            decoded_e=out_error*decoded_e;
            for c in range(0,22):
                output_gradient[0,c]=output_gradient[0,c]+decoded_e[c,0]
            #decoder gradient
            encoded_e=encoded_e*out_error
            for c in range(0,22):
                for r in range(0,20):
                    decoder_gradient[r,c]=decoder_gradient[r,c]+encoded_e[c,0]*outw[r]
            #encoder gradient
            weight_track = np.matrix(np.ones([20,1]))
            for c in range(0,20):
                for r in range(0,20):
                    weight_track[r,0]=weight_track[r,0]+decoder[r,c]*outw[r]
            word=word*out_error
            for c in range(0,302):
                for r in range(0,20):
                    encoder_gradient[r,c]=encoder_gradient[r,c]+word[c,0]*weight_track[r,0]
            #just in case
            #np.savetxt("encoder.csv",encoder, delimiter=",")
            #np.savetxt("decoder.csv",decoder, delimiter=",")
            #np.savetxt("output.csv",outw, delimiter=",")
            #Adjusts weights based on gradients
            for c in range(0,302):
                for r in range(0,20):
                    encoder[r,c]=encoder[r,c]-encoder_gradient[r,c]*rate
            for c in range(0,22):
                for r in range(0,20):
                     decoder[r,c]=decoder[r,c]-decoder_gradient[r,c]*rate
            for c in range(0,22):
                outw[c]=outw[c]-output_gradient[0,c]*rate
            if (j%5==0)&(i%99==0):
                print(output)
    return 1;

#import encoder weights
with open('encoder.csv') as f:
    encoder=np.loadtxt(f, delimiter=',')
f.close()
#import decoder weights
with open('decoder.csv') as f:
    decoder=np.loadtxt(f, delimiter=',')
f.close()
#import output weights
with open('output.csv') as f:
    outw=np.loadtxt(f, delimiter=',')
f.close()



#encoder = np.matrix(np.ones([20,302]))
#for i in range(0,20):
#    for j in range(0,302):
#        encoder[i,j] = random.random()
#        encoder[i,j] = random.random()

#decoder = np.matrix(np.ones([20,22]))
#for i in range(0,20):
#    for j in range(0,22):
#        decoder[i,j] = random.random()
#        decoder[i,j] = random.random()
        
#outw = np.matrix(np.ones([1,22]))
#for i in range(0,22):
#   outw[0,i] = random.random()
        
#runs the networks and functions
#encoded=encode(data,length)
#encoding = np.matrix(np.ones([22,1]))
#for i in range(0,20):
    #encoding[i,0]=encoded[i,0]
#print(encoding)
#decoding=decode(encoding,length)
#decodinge = np.matrix(np.ones([22,1]))
#for i in range(0,20):
    #decodinge[i,0]=decoding[i,0]
#print(decoding)
#out=output(decodinge);
#print(out)

def initialize_csv_vector():
    global englishVectorFromCSV
    englishVectorFromCSV = np.loadtxt(open("englishVectors.csv", "rb"), delimiter=",")

def getEnglishWords():
    words = []
    with open("english.txt") as f:
        for line in f:
            words.append(line.rstrip('\n'))

    return words
def getSpanishWords():
    words = []
    with open("spanish.txt") as f:
        for line in f:
            words.append(line.rstrip('\n'))

    return words

def getCSVVector(index):
    return englishVectorFromCSV[index]
def main(argv):

    #initialize_model()
    initialize_csv_vector()
    engWords = getEnglishWords()
    spanWords = getSpanishWords()
    #trained=train();
    #if trained==1:
            #print("trained! \n")
    print("Type sentence please \n")
    bu=0
    while(bu==0):
        inputSentence = sys.stdin.readline().rstrip('\n')

        inputWords = inputSentence.lower().split(" ")

        builtString = ""
        for word in inputWords:
            try:
                indexOfWord = engWords.index(word)
            except ValueError:
                builtString += word + " "
                continue
            importedVector = getCSVVector(indexOfWord)
            length=1;
            word=np.matrix(np.ones([302,1]))
            for dat in range (0,300):
                word[dat,0]=importedVector[dat]
            encoded=encode(word,length)
            encoding = np.matrix(np.ones([22,1]))
            for i in range(0,20):
                encoding[i,0]=encoded[i,0]
            #print(encoding)
            decoding=decode(encoding,length)
            decodinge = np.matrix(np.ones([22,1]))
            for i in range(0,20):
                decodinge[i,0]=decoding[i,0]
            #print(decoding)
            out=output(decodinge)/100;
            out=int(round(out[0,0]));
            if out>99:
                out=99
            if out<0:
                out=0
            print(out+1)
            builtString += spanWords[out] + " "

        print(builtString)
if __name__ == "__main__":
    main(sys.argv[1:])
    
#saves the weights
np.savetxt("encoder.csv",encoder, delimiter=",")
np.savetxt("decoder.csv",decoder, delimiter=",")
np.savetxt("output.csv",outw, delimiter=",")
