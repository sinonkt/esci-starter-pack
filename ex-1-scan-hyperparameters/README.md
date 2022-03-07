# esci-starter-pack

![Alt text](/misc/images/tensorflow.jpeg "AI Workflow")
![Alt text](/misc/images/hyperparameters.png "Hyperparameters tuning")

```nextflow
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
	file "*.txt" into Models
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
```

