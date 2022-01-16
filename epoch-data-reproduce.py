import numpy
from keras.models import Sequential, save_model, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.losses import sparse_categorical_crossentropy
from keras.optimizers import SGD
from imblearn.over_sampling import SMOTE
from numpy import savetxt
#import pickle
from sklearn import preprocessing
import time

class MyOVBox(OVBox):
	def __init__(self):
		OVBox.__init__(self)
		self.signalHeader = None
		self.combinedData = numpy.zeros((1, 613))	

	def initialize(self):
		print("initialize")
		self.output[0].append(OVStimulationHeader(self.getCurrentTime(), self.getCurrentTime()))
		print("initialize complete")

	def uninitialize(self):
		# delete the any row containing all zeros (This scenario occurs where we initialize the variable with zeros)
		self.combinedData = numpy.delete(self.combinedData, numpy.where(~self.combinedData.any(axis=1))[0], axis=0)

		# save to csv file
		fileName = time.strftime("%Y%m%d-%H%M%S")	
		savetxt('d:\\table_of_flashes_1_to_12_612_' + fileName + '.csv', self.combinedData, delimiter=',')


	def process(self):

		# Below snippet of code captures all the target data
		for chunkIndex0 in range( len(self.input[0]) ):
			chunk0 = self.input[0].pop()
			if(type(chunk0) == OVSignalHeader):
				self.signalHeader = chunk0                                                
				self.data = numpy.zeros((1, self.signalHeader.dimensionSizes[1]))	  # initializes the self.data variable with zeros
			elif(type(chunk0) == OVSignalBuffer):	
				self.data = numpy.array(chunk0).reshape(1, 612) 
				self.data = numpy.append(self.data[-1, :], 1)				  # Appends with a value of "1" in the excel sheet rows. Stands for "Target" rows
				self.data.reshape(1, 613)			
				self.combinedData = numpy.insert(self.combinedData, 0, self.data, axis=0) # Insert the data at the location 0 .. always
			else:
				chunk0

		# Below snippet of code captures all the non-target data
		for chunkIndex1 in range( len(self.input[1]) ):
			chunk1 = self.input[1].pop()
			if(type(chunk1) == OVSignalHeader):			
				self.signalHeader = chunk1
				self.data1 = numpy.empty((1, self.signalHeader.dimensionSizes[1]))        # initializes the self.data variable with zeros
			elif(type(chunk1) == OVSignalBuffer):				
				self.data1 = numpy.array(chunk1).reshape(1, 612)			  
				self.data1 = numpy.append(self.data1[-1, :], 0)				  # Appends with a value of "0" in the excel sheet rows. Stands for "NonTarget" rows
				self.data1.reshape(1, 613)						
				self.combinedData = numpy.insert(self.combinedData, 0, self.data1, axis=0)# Insert the data at the location 0 .. always
			else:
				chunk1

		for chunkIndex in range( len(self.input[2]) ):
			chunk = self.input[2].pop()
			print("\n")	
			if(type(chunk) == OVStimulationSet):
				for stimIdx in range(len(chunk)):
					self.stim=chunk.pop();
					print(self.stim.identifier)
					if(self.stim.identifier == 32770):
						stimSet = OVStimulationSet(self.getCurrentTime(), self.getCurrentTime())
						stimSet.append(OVStimulation(33287, self.getCurrentTime(), 0.))
						self.output[0].append(stimSet)

		end = self.getCurrentTime()
		self.output[0].append(OVStimulationEnd(end, end))				
															
box = MyOVBox()