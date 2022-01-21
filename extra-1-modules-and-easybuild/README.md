# Local Modules & EasyBuild

for installing any scientific software without root permission.

(Most of low-level dependecies / software was compiled on our target architecture for better performance)

# Modules command on e-Science
***you could use `module` and `ml` interchangebly.


Show available module

```
module av
```

Show current loaded modules
```
module list
```

Unloaded current modules

```
module purge
```

Search for module `cuda` (case insensitive search)
```
module spider cuda
```

load 2 `CUDA` modules

```
module load CUDA/11.4.1 cuDNN/8.2.2.26-CUDA-11.4.1
```


# Configure Local Module on e-Sci

by added this snipped into `~/.bashrc`

```
######################### local modules #########################
function mu_local(){
    export NBT_MODULES=/work/home/$(whoami)
    export EASYBUILD_PREFIX=${NBT_MODULES}/.local/easybuild
    export EASYBUILD_MODULES_TOOL=Lmod
    export LOCAL_MODULES=${EASYBUILD_PREFIX}/modules/all
    module use $LOCAL_MODULES
}
mu_local
######################### local modules #########################
```

![Alt text](/misc/images/local_modules.jpg "Local Modules")

# use EasyBuild

```
ml load EasyBuild
```

then we looking for the name of sofware we wish to install and pick easyconfig file (like recipe for building each software) at https://github.com/easybuilders/easybuild-easyconfigs)

for instance, [easconfigs/j/Julia](https://github.com/easybuilders/easybuild-easyconfigs/tree/develop/easybuild/easyconfigs/j/Julia)

then software build process is just one line like following.

```
eb Julia-1.7.1-linux-x86_64.eb --robot
```

if there is any problem, Don't hesitate to ping me :)) 
