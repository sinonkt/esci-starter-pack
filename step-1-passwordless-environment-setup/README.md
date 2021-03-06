# Passwordless Login & e-Science Alias

![Alt text](/misc/images/passwordless-login.gif "Passwordless Login")

3 steps

## #1 Setup Passwordless, generate Public key & Private Key (PKI)

Feels free to skipped this step if you already have Public key & Private Key pair. You could check if there is any existing key pair by following cmd. 

```bash
ls -al ~/.ssh/id_*.pub
```

Generate Key pair.

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@domain.com"
```

Press Enter, Enter for accepting default key's Location and no passphrase for key.

![Alt text](/misc/images/ssh-key-pair-prompt.png "ssh-keygen prompt")
![Alt text](/misc/images/key-pair-generated.png "key-pair generated")

Now we've Private Key locate at `~/.ssh/id_rsa` and Public key at `~/.ssh/id_rsa.pub`.

Notes: We should keep `~/.ssh/id_rsa` secure and backup whenever we reinstall OS or move to other laptop. 

## #2 Setup Passwordless, Copy Public key to e-Sci

Copy Public key to e-Science server via command

```
ssh-copy-id -i ~/.ssh/id_rsa your_account_name@escience0.sc.chula.ac.th
```

Provide password only once.

![Alt text](/misc/images/ssh-copy.gif "ssh-copy prompt")

## #3 Set Alias name for convinient

sudo vim / sudo nano at file `/etc/hosts` and add host ip nickname like following.

```
161.200.116.61 esci
```
![Alt text](/misc/images/etc_hosts.jpg "etc_hosts")

Done!! :))
