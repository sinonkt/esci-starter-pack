# Setup VSCode and Sftp sync extension

for Convenient file transfering back and forth to esci on a daily basis.

Install VSCode: https://code.visualstudio.com/download

Fixes: [vscode-sftp-sync Fixes](https://stackoverflow.com/questions/67506693/error-no-such-file-sftp-liximomo-extension)


## Set up Sftp sync once everytime we start a new project.

Install SFTP sync extension

![Alt text](/misc/images/sftp_sync_extension.jpg "Sftp Extension")


Activate Command Pallete, `SFTP: Config` to initialize sftp config file.

![Alt text](/misc/images/sftp_command_palette.jpg "Activate SFTP command Palette")

then we fill our remote destination details looks something like following. 

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

then we should be able to `SFTP: Local to Remote` to transfer all files in our laptop's current project directory to `/work/project/quantum/kphornsiri/chics-hpc-workshop` on e-Sci

when we have results on e-Science and want to transfer back `SFTP: Remote to Local`

Besides manual transfer to/from e-Sci, the term `sync` came from everytime we edit file and `save` in vscode it will automatically upload for us (`uploadOnSave`)

