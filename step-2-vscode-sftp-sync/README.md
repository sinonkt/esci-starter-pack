# Setup VSCode and Sftp sync extension

Install VSCode: https://code.visualstudio.com/download


Fixes: [vscode-sftp-sync Fixes](https://stackoverflow.com/questions/67506693/error-no-such-file-sftp-liximomo-extension)


## Set up Sftp sync once for every starting a new project



`{YourProjectDir}/.vscode/sftp.json`
```json
{
    "name": "chics-hpc-workshop-esci",
    "host": "esci",
    "protocol": "sftp",
    "port": 22,
    "username": "kphornsiri",
    "privateKeyPath": "~/.ssh/id_rsa",
    "remotePath": "/work/project/quantum/kphornsiri/chics-hpc-workshop",
    "uploadOnSave": true,
    "ignore": [
        ".vscode",
        ".git",
        "work",
        ".DS_Store",
        "nextflow.log*"
    ]
}
```
