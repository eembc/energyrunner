from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Reshape, Dense, Activation, Flatten, BatchNormalization

#define model
def toyadmos_autoencoder_eembc():
  # Input parameters (see ToyADMOS paper)
  numDenseUnits = 128
  numLatentUnits = 8
  input_height = 5
  input_width = 128
  input_chan = 1

  # Input layer
  input_img = Input(shape=[input_height, input_width, input_chan])
  
  # Flatten input image
  x = Flatten()(input_img)

  # First encoder layer
  x = Dense(numDenseUnits)(x)
  x = BatchNormalization()(x)
  x = Activation('relu')(x) 
  
  # Second encoder layer
  x = Dense(numDenseUnits)(x)
  x = BatchNormalization()(x)
  x = Activation('relu')(x) 
  
  # Third encoder layer
  x = Dense(numDenseUnits)(x)
  x = BatchNormalization()(x)
  x = Activation('relu')(x) 
  
  # Fourth encoder layer
  x = Dense(numDenseUnits)(x)
  x = BatchNormalization()(x)
  x = Activation('relu')(x) 
  
  # Latent layer
  x = Dense(numLatentUnits)(x)
  x = BatchNormalization()(x)
  x = Activation('relu')(x) 

  # First decoder layer
  x = Dense(numDenseUnits)(x)
  x = BatchNormalization()(x)
  x = Activation('relu')(x) 

  # Second decoder layer
  x = Dense(numDenseUnits)(x)
  x = BatchNormalization()(x)
  x = Activation('relu')(x) 

  # Third decoder layer
  x = Dense(numDenseUnits)(x)
  x = BatchNormalization()(x)
  x = Activation('relu')(x) 

  # Fourth decoder layer
  x = Dense(numDenseUnits)(x)
  x = BatchNormalization()(x)
  x = Activation('relu')(x) 

  # Output layer
  x = Dense(input_height*input_width*input_chan)(x)
  decoded = Reshape((input_height,input_width,input_chan))(x)

  # Build model
  autoencoder = Model(input_img, decoded)
  return autoencoder
