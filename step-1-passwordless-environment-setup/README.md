# Passwordless Login & e-Science Alias

![Alt text](/misc/images/passwordless-login.gif "Passwordless Login")

## Setup Passwordless #1 generate Public key & Private Key (PKI)

Feels free to skipped this step if you already have Public key & Private Key pair. You could check if there is any existing key pair by following cmd. 

```bash
ls -al ~/.ssh/id_*.pub
```

Generate Key pair.

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@domain.com"
```

Press Enter to accept default key Location and no passphrase for key

![Alt text](misc/images/ssh-key-pair-prompt.png "ssh-keygen prompt")
![Alt text](misc/images/key-pair-generated.png "key-pair generated")
