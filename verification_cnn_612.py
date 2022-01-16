from sklearn import preprocessing
from numpy import loadtxt
import numpy
from keras.models import load_model
from sklearn.metrics import confusion_matrix
from numpy import savetxt
from imblearn.over_sampling import SMOTE
import tensorflow
from sklearn.model_selection import train_test_split
from numpy import mean

MY_CONST = 60.
MY_CONST_NEG = -60.

def NormalizeData(data):
	print(numpy.amin(data))	
	print(numpy.amax(data))	
	return (data + (MY_CONST)) / (MY_CONST - (MY_CONST_NEG))


#X = loadtxt('d:\\flashes_1_to_12_152_small_mat_hiren_1-gr-7-or.csv', delimiter=',')
#X = loadtxt('d:\\flashes_1_to_12_152_small_mat_swati_1g_7o.csv', delimiter=',')
#X = loadtxt('d:\\Atharva_3g-2o-flashes_1_to_12_152_small_mat_experiment_1.csv', delimiter=',')
#X = loadtxt('d:\\mugdha-1g-4o-flashes_1_to_12_152_small_mat_20220105-151110.csv', delimiter=',')
#X = loadtxt('d:\\ritu_3o-exp2-flashes_1_to_12_152_small_mat.csv', delimiter=',')

X = loadtxt('d:\\table_of_flashes_1_to_12_612_testing.csv', delimiter=',')

mean_of_test = mean(X[:, 0:612])
print(mean_of_test)
input = X[:, 0:612] - mean_of_test
too_high_input = input > MY_CONST
input[too_high_input] = MY_CONST
too_low_input = input < MY_CONST_NEG
input[too_low_input] = MY_CONST_NEG
input = NormalizeData(input)
savetxt('d:\\input-swati-online.csv', input, delimiter=',')

input = input.reshape(len(input), 4, 153)
input = input.transpose(0, 2, 1)

y_real = X[:, -1]

model = load_model('D:\\model_conv1d_reproduce.h5')
y_pred = model.predict_proba(input) 
print(y_pred.shape)

y_max = numpy.argmax(y_pred, axis=1)
matrix = confusion_matrix(y_real, y_max)
print(matrix)
