#! /usr/bin/env python
# model with double the filters for the fashion mnist dataset
import click
from numpy import mean, sum
from numpy import std
from matplotlib import pyplot
from sklearn.model_selection import KFold
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.python.keras.utils.layer_utils import count_params
from tensorflow.keras.optimizers.schedules import ExponentialDecay
import click
from contextlib import redirect_stdout

optimizer_dict = {
	"SGD": SGD,
	"Adam": Adam
}

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    click.echo("Running...")

@cli.command()
@click.option('--k-folds', default=5, help='Number of fold for cross validations')
@click.option('--epochs', default=10, help='Number of epochs.')
@click.option('--batch-size', default=32, help='Batch size')
@click.option('--output', default='validation_results.csv', type=click.File('w'), help='mean,std,total_params') 
@click.option('--output-summary', default='model_summary.txt', type=click.File('w')) 
@click.option('--conv-layer', type=str, default='None', help='Convolution layer architecture str for exmaple, None, conv_32_2x2,maxpooling_2x2 ')
@click.option('--dense-layer', type=str, default='None', help='Dense layer architecture str for example, None, 50, 100x100, 100x50')
@click.option('--conv-activation', type=click.Choice(['elu', 'relu', 'sigmoid', 'swish', 'tanh']), default='relu', help='Activation function for conv layer')
@click.option('--dense-activation', type=click.Choice(['elu', 'relu', 'sigmoid', 'swish', 'tanh']), default='relu', help='Activation function for dense layer')
@click.option('--dropout', type=float, default=0.0, help='fraction of dropout (zero means no dropout')
@click.option('--optimizer', type=click.Choice(['SGD', 'Adam']), default='Adam', help='Optimizer')
@click.option('--learning-rate', default=0.01, help='Learning rate')
@click.option('--decay-steps', default=10000, help='Decay steps')
@click.option('--decay-rate', default=0.9, help='Decay rate')
@click.pass_context
def evaluate(ctx, k_folds, epochs, batch_size, output, output_summary, **kwargs):
    dataX, dataY, __, __ = load_dataset()
    dataX = prep_pixels(dataX)
    # evaluate a model using k-fold cross-validation
    scores, histories = list(), list()
    total_params = 0
    kfold = KFold(k_folds, shuffle=True, random_state=1)
    print(f'k-folds: {k_folds}, epochs: {epochs}, batch_size: {batch_size}')
    print(kwargs)
    for train_ix, test_ix in kfold.split(dataX):
	    model = define_model(**kwargs)
	    trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
	    history = model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, validation_data=(testX, testY), verbose=0)
	    _, acc = model.evaluate(testX, testY, verbose=0)

	    trainable_count= count_params(model.trainable_weights)
	    non_trainable_count= count_params(model.non_trainable_weights)
	    total_params= trainable_count + non_trainable_count
	    print('(parameters=%.3f)> %.3f' % (total_params, acc * 100.0))

	    scores.append(acc)
	    histories.append(history)

    model.summary()
    output.write(f'mean,std,total_params\n')
    output.write(f'{(mean(scores)*100)},{(std(scores)*100)},{total_params}\n')
    output.close()

    with redirect_stdout(output_summary):
        model.summary()

    print(scores)
    print(histories)
    print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(scores)*100, std(scores)*100, len(scores)))


@cli.command()
@click.option('--k-folds', default=5, help='Number of fold for cross validations')
@click.option('--epochs', default=10, help='Number of epochs.')
@click.option('--batch-size', default=32, help='Batch size')
@click.option('--output', default='test_results.csv', type=click.File('w'), help='acc,loss,total_params') 
@click.option('--output-model', default='learned_model') 
@click.option('--conv-layer', type=str, default='None', help='Convolution layer architecture str for exmaple, None, conv_32_2x2,maxpooling_2x2 ')
@click.option('--dense-layer', type=str, default='None', help='Dense layer architecture str for example, None, 50, 100x100, 100x50')
@click.option('--conv-activation', type=click.Choice(['elu', 'relu', 'sigmoid', 'swish', 'tanh']), default='relu', help='Activation function for conv layer')
@click.option('--dense-activation', type=click.Choice(['elu', 'relu', 'sigmoid', 'swish', 'tanh']), default='relu', help='Activation function for dense layer')
@click.option('--dropout', type=float, default=0.0, help='fraction of dropout (zero means no dropout')
@click.option('--optimizer', type=click.Choice(['SGD', 'Adam']), default='Adam', help='Optimizer')
@click.option('--learning-rate', default=0.01, help='Learning rate')
@click.option('--decay-steps', default=10000, help='Decay steps')
@click.option('--decay-rate', default=0.9, help='Decay rate')
@click.pass_context
def train(ctx, k_folds, epochs, batch_size, output, output_model, **kwargs):
	trainX, trainY, testX, testY = load_dataset()
	trainX = prep_pixels(trainX)
	testX = prep_pixels(testX)
	model = define_model(**kwargs)
	history = model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, validation_data=(testX, testY))
	loss, acc = model.evaluate(testX, testY, verbose=2)
	model.summary()
	print(history, loss, acc)
	trainable_count= count_params(model.trainable_weights)
	non_trainable_count= count_params(model.non_trainable_weights)
	total_params= trainable_count + non_trainable_count
	# output.write(f'acc,loss,total_params\n')
	output.write(f'{acc},{loss},{total_params}\n')
	output.close()
	model.save(output_model)

def load_dataset():
	(trainX, trainY), (testX, testY) = fashion_mnist.load_data()
	return trainX.reshape((trainX.shape[0], 28, 28, 1)), to_categorical(trainY), testX.reshape((testX.shape[0], 28, 28, 1)), to_categorical(testY)

def prep_pixels(data):
    return data.astype('float32') / 255.0

# define cnn model
def define_model(conv_layer, dense_layer, conv_activation, dense_activation, dropout, optimizer, learning_rate, decay_steps, decay_rate):
	model = Sequential()
	firstInputLayerShape = {
	   "input_shape": (28, 28, 1)
	}

	# Construct Convolution Layer
	if conv_layer != 'None':
		for sub_layer in conv_layer.split(','):
			layer_type, *rest = sub_layer.split('_')
			if layer_type == 'conv':
				filters, strides = rest
				swidth, sheight = strides.split('x')
				model.add(Conv2D(int(filters), (int(swidth), int(sheight)), padding='same', activation=conv_activation, kernel_initializer='he_uniform', **firstInputLayerShape))
			elif layer_type == 'maxpooling':
				(width, height) = rest[0].split('x')
				model.add(MaxPooling2D((int(width), int(height))))
			firstInputLayerShape = {}
	
	model.add(Flatten(**firstInputLayerShape))

	# Construct Dense Layer
	hasDropout = dropout > 0.0
	if dense_layer != 'None':
		for dense_sub_layer_size in dense_layer.split('x'):
			model.add(Dense(int(dense_sub_layer_size), activation=dense_activation, kernel_initializer='he_uniform'))
			if hasDropout:
				model.add(Dropout(dropout))
			

	model.add(Dense(10, activation='softmax'))
	lr_schedule = ExponentialDecay(
		initial_learning_rate=learning_rate,
		decay_steps=decay_steps,
		decay_rate=decay_rate)
	opt = optimizer_dict[optimizer](lr_schedule)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
	return model


if __name__ == '__main__':
    cli()