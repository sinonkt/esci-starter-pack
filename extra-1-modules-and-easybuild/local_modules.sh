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