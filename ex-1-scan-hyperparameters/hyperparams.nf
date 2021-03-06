
def ConvLayers = Channel.from(['None', 'conv_32_3x3,maxpooling_2x2', 'conv_32_3x3,maxpooling_2x2,conv_32_3x3,maxpooling_2x2' ])
def DenseLayers = Channel.from(['None', '50', '100', '100x100'])
def ConvActivations = Channel.from(['elu', 'relu', 'swish'])
def DenseActivations = Channel.from(['elu', 'relu', 'swish'])
def Dropouts = Channel.from([0.0, 0.1, 0.2])
def InitialLearningRates = Channel.from([0.1, 0.01])

process Evaluate {

    tag { "${conv_layer}(${conv_activation})|${dense_layer}(${dense_activation})|dropout_${dropout}|${learning_rate}" }

	publishDir "results/oak/${conv_layer}_${conv_activation}_${dense_layer}_${dense_activation}_dropout_${dropout}_${learning_rate}", mode: 'copy'

	maxForks 5

	executor 'slurm'

	clusterOptions '--qos=cu_hpc --gpus=1'

	queue 'cpugpu'

    conda '/work/home/kphornsiri/miniconda3/envs/test'

    input:
    val conv_layer from ConvLayers
    each dense_layer from DenseLayers
    each conv_activation from ConvActivations
    each dense_activation from DenseActivations
    each dropout from Dropouts
    each learning_rate from InitialLearningRates

	output:
	file "model_summary.txt" into Models
	file "validation_results.csv" into MetricsResults
    
    script:
    """
    fmnist.py evaluate \\
        --conv-layer ${conv_layer} \\
        --dense-layer ${dense_layer} \\
        --conv-activation ${conv_activation} \\
        --dense-activation ${dense_activation} \\
        --dropout ${dropout} \\
        --learning-rate ${learning_rate}
    """
}

// def decay_steps = [10000]
// def decay_rates = [0.9]
// def optimizers = ['Adam']

// def HyperParameters = Channel.fromList(conv_layers)
//     .spread(dense_layers)
//     .spread(conv_activations)
//     .spread(dense_activations)
//     .spread(dropouts)
//     .spread(initial_learning_rates)
    // .spread(optimizers)
    // .spread(decay_steps)
    // .spread(decay_rates)
    // .count()
    // .view()