nextflow.enable.dsl=2

process Test {

	input:
	val x
	each y

	output:
	val z
	val a

	script:
	z = x * y
	a = z + 1
	"""
	sleep 3
	echo "${z}"
	"""
}

process Stage2_1 {

	input:
	val z

	script:
	"""
	sleep 3
	echo "${z}"
	"""
}

process Stage2_2 {
	input:
	val a

	script:
	"""
	sleep 3
	echo "${a}"
	"""
}

workflow {
	xs = Channel.from(1..10)
	ys = Channel.from(1..5)
	(zs, as) = Test(xs, ys)
	Stage2_1(zs)
	Stage2_2(as)
}

















// // def values = [1..10]
// def square = { x ->
// 	return x * x
// }

// def isEven = { x -> x%2 == 0}
// def values = 1..10

// def xs = Channel.from(1..10)
// 	.map(square)
// 	.filter(isEven)

// def ys = values
// 		.collect(square)
// 		.findAll(isEven)

// def ysChannel = Channel.from(ys)

// process Test {
    
//     executor 'slurm'
    
//     cpus 1

//     queue 'cpu'

//     clusterOptions "--qos cu_hpc"

//     publishDir "results/${x}_$y", mode: "copy"
    
//     input:
//     val x from xs
//     each y from ys

//     output:
//     set file("*_results.txt"), file(".command.*") into MyResults

//     script:
// 	z = x * y
//     """
//     echo "${z}" >> ${z}_results.txt
//     """
// }
