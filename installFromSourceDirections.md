Community Tester Install Guide for Factom Federation (M2)
==========

This will walk you through setting up the experimental distributed version of Factom.

### Prepare Operating System

The most testing to date has been done under Linux. To get the best testing experience, it should be done on Linux. That will also help us recreate the bugs you experience better. If you are running Windows, please install a virtual machine to run Factom. Installing on Windows has been known to work, but is not covered here.

Here are some good directions to get a virtual machine installed with Linux. http://www.instructables.com/id/Introduction-38/?ALLSTEPS

The following are assuming you are using the 64 bit version of Ubuntu, or one of its descendant projects like xubuntu or mint.

#### Install the go language and dependencies, then setup GOPATH

###### Install Package Managers 

In a terminal window, install Git

On Linux:
```
sudo apt-get install git
```

On Mac:
Steps 1 and 3 should be enough in this tutorial:
https://confluence.atlassian.com/pages/viewpage.action?pageId=269981802

###### Install Golang

Download latest version of go https://golang.org/dl/  This example uses 64 bit Linux and 1.7.4 is the latest version.
```
sudo tar -C /usr/local -xzf go1.7.4.linux-amd64.tar.gz
```

On Mac, installing go this way should work:
http://www.cyberciti.biz/faq/installing-go-programming-language-on-mac-os-x/


###### Setup Paths

Put the go binary directory in you path.  Also add the GOPATH to your profile.
Open the file `~/.profile` and add these lines to the bottom.  If they are not exact, then your Linux may not be bootable.
```
export PATH=$PATH:/usr/local/go/bin

export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```
**logout and login**.  This is the most straightforward way to run/test these changes.  Run `go version` from a terminal to verify the install.


### Install Factom

Currently, the blog post [here](https://factom.com/blog/factom-launches-federated-testnet) has some screenshots of what to expect Factom Federation (M2) to look like.

These steps will get factom installed onto a linux machine. The steps should be similar for mac.

```
# install glide, the package dependency manager
go get -u github.com/Masterminds/glide
# download the code
git clone https://github.com/FactomProject/factomd $GOPATH/src/github.com/FactomProject/factomd
git clone https://github.com/FactomProject/factom-cli $GOPATH/src/github.com/FactomProject/factom-cli
git clone https://github.com/FactomProject/factom-walletd $GOPATH/src/github.com/FactomProject/factom-walletd
git clone https://github.com/FactomProject/enterprise-wallet $GOPATH/src/github.com/FactomProject/enterprise-wallet

# To use the unstable development branch, uncomment these lines
# This is primarily for developers who are updating factom itself
# Leave alone to get the tested, released version.
cd $GOPATH/src/github.com/FactomProject/factomd
# git checkout develop
cd $GOPATH/src/github.com/FactomProject/factom-cli
# git checkout develop
cd $GOPATH/src/github.com/FactomProject/factom-walletd
# git checkout develop
cd $GOPATH/src/github.com/FactomProject/enterprise-wallet
# git checkout develop

# get the dependencies and build each factom program
glide cc
cd $GOPATH/src/github.com/FactomProject/factomd
glide install
go install -ldflags "-X github.com/FactomProject/factomd/engine.Build=`git rev-parse HEAD` -X github.com/FactomProject/factomd/engine.FactomdVersion=`cat VERSION`" -v
cd $GOPATH/src/github.com/FactomProject/factom-cli
glide install
go install -ldflags "-X main.FactomcliVersion=`cat VERSION`" -v
cd $GOPATH/src/github.com/FactomProject/factom-walletd
glide install
go install -ldflags "-X github.com/FactomProject/factom-walletd/vendor/github.com/FactomProject/factom/wallet.WalletVersion=`cat ./vendor/github.com/FactomProject/factom/wallet/VERSION`" -v
cd $GOPATH/src/github.com/FactomProject/enterprise-wallet
glide install
go install -v
cd $GOPATH/src/github.com/FactomProject/factomd

# done.  factomd should be installed
# you can optionally use a config file to run in a non-standard mode
# mkdir -p ~/.factom/m2/
# cp $GOPATH/src/github.com/FactomProject/factomd/factomd.conf ~/.factom/m2/
```


### Starting Factom

Factom takes a while to download the blockchain. It can be expidited by downloading the first 70k blocks via HTTP. Factomd still checks the blockchain on each bootup, so it will check for inconsistencies in the download.

Note: currently factomd uses a lot of drive accesses when running. It is reccomended to hold the blockchain on a solid state drive. Running factomd on a spinning hard drive will be arduously slow. Since factomd currently scans the entire blockchain each time it is started, bootup takes a while (~30 min on an SSD).  You can watch the progress on the [Control Panel](http://localhost:8090/).

Download the blockchain here: https://www.factom.com/assets/site/factom_bootstrap.zip
SHA256: 2d4d256c337cdabc8f75aa71180c72129f807c365c78356471350ac1e0a4faed

Extract the zip file to your home directory. It will create files in the location: ~/.factom/m2/main-database/ldb/MAIN/factoid_level.db/

Compressed the blockchain is currently about 5 GB and uncompressed is over 9 GB.

After factomd boots and downloads the remaining blocks, it likely is not keeping up with minutes. To see if it is, on the control panel click the "More Detailed Node Information" button. Towards the right of the top line there will be a field "-/ 0". If the 0 number does not increase after a minute, then it is not keeping up with minutes.

In most cases factomd will need to be restarted after synching to the latest blockchain.

### Factom Wallets

Most users will want to run either the API wallet factom-walletd or the GUI wallet enterprise-wallet. Directions for those are located here: https://docs.factom.com/wallet#run-the-factom-foundation-wallet

Although the factomd API is backwards compatible, the API extended by the old API wallet, fctwallet, is not supported by factom-walletd. The entire wallet from M1 can be imported into factom-walletd using the -i flag and an empty ~/.factom/wallet directory.

Some users will want to use the old fctwallet with the new factomd. Follow the directions [here](legacyWallets.md) to compile the old programs.


### Testing Factom

You can run a local version of factomd to get greater flexibility by running it like this:

`factomd -network=LOCAL`

This will make a new blockchain without worrying about other's data interfering with your testing.  You can use the key `factom-cli importaddress Fs1KWJrpLdfucvmYwN2nWrwepLn8ercpMbzXshd1g8zyhKXLVLWj` to get local Factoids after starting factom-walletd.

For issues with the software, please post [here](https://github.com/FactomProject/factomd/issues).




