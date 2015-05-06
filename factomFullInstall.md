Factom Central Server Install Guide
==========

Before the node network gets setup. Factom clients will simulate talking to a P2P network by using web services calls to a central server.  For testing, it will be beneficial to developers to have their own central server.


## Prepare Operating System

These directions were prepared on ubuntu 14.04.  Variations have been reported to work on windows, but no guarantees.

#### Install the go language

It is best to follow the directions here to install golang for for your platform.  http://golang.org/doc/install

Examples for ubuntu are included here for expediency.

##### Install go and dependencies
```
sudo apt-get install git mercurial
```
download latest version of go https://golang.org/dl/  This example uses 64 bit linux and 1.4.1 is the latest version.

```
sudo tar -C /usr/local -xzf go1.4.1.linux-amd64.tar.gz
```

Put the go binary directory in you path.

Open the file `~/.profile` and add these lines to the bottom.  If they are not exact, then your ubuntu may not be bootable.

```
export PATH=$PATH:/usr/local/go/bin
```

note: using `sudo apt-get install golang` will install go version 1.2.1.  Btcd requires go v1.3 or above.  Compiling with v1.2.1 will cause the compiler to use [lots of ram](https://github.com/btcsuite/btcd/issues/277).

##### Setup gopath
Open the file `~/.profile` and add these lines to the bottom.  If they are not exact, then your ubuntu may not be bootable.

```
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```

**logout and login**.  This is the most straightforward way to run/test these changes.

# Install BTC Suite

### Install BTCD
```
go get -v github.com/btcsuite/btcd/...
mkdir $HOME/.btcd/
cp $GOPATH/src/github.com/btcsuite/btcd/sample-btcd.conf $HOME/.btcd/btcd.conf
```

In a text editor open `$HOME/.btcd/btcd.conf`

Uncomment the line `testnet=1`

uncomment rpcuser and rpcpass and set them to:
`rpcuser=testuser`
`rpcpass=SecurePassHere`


In a console window, run `btcd` and wait for it to download the testnet blockchain.  This will take a while, unless you can copy the folder `~/.btcd/data/testnet/` from an already running version of btcd.  Note, copying the levelDB files may cause problems with btcd.  It may be more prudent to merely run `btcd --connect=<localip>` to download the blockchain.


### Install Wallet

```
go get -v github.com/btcsuite/btcwallet/...
mkdir $HOME/.btcwallet/
cp $GOPATH/src/github.com/btcsuite/btcwallet/sample-btcwallet.conf $HOME/.btcwallet/btcwallet.conf
```

In a text editor open `$HOME/.btcwallet/btcwallet.conf`

In the RPC section, uncomment and set:
`username=testuser`
`password=SecurePassHere`

In a second console window, run `btcwallet --create`

Follow the directions to create a wallet.  Give it password which is hard to guess.  One example password is `HardToGuessPW` which will be used as an example later.  It will be in a config file, so it will not be that secure, though.


### Install GUI

This is not strictly necessary, but is needed if you want to know where to send testnet BTC and diagnose some issues.  Command line alternatives are listed below.


```
sudo apt-get install libgtk-3-dev libcairo2-dev libglib2.0-dev libsasl2-dev
go get -v -tags gtk_3_10 github.com/btcsuite/btcgui/...
mkdir $HOME/.btcgui/
cp $GOPATH/src/github.com/btcsuite/btcgui/sample-btcgui.conf $HOME/.btcgui/btcgui.conf
```

open `$HOME/.btcgui/btcgui.conf` in a text editor
In the Authentication section, uncomment and set:
`username=testuser`
`password=SecurePassHere`

Run `btcd` & `btcwallet` each in separate terminal windows.

In a 3rd terminal window run `btcgui`

Send testnet bitcoins to an address in gui


### Command Line Alternatives to GUI


You might be able to get by with some command line arguments.  This one outputs an address in your wallet `btcctl --rpcuser=testuser --rpcpass=SecurePassHere --testnet --wallet getaccountaddress "default"`.  Save the address it gives you and send testnet bitcoins to it.  You can use `btcctl --rpcuser=testuser --rpcpass=SecurePassHere --testnet --wallet listreceivedbyaccount` to see if money has been sent to the wallet.  Also `btcctl --rpcuser=testuser --rpcpass=SecurePassHere --testnet --wallet listtransactions` to see what has happened in the wallet.



# Install Factom Central Server

The central server executable is called `restapi`.  It can be installed with this command:
```
go get -v github.com/FactomProject/FactomCode/restapi
cp $GOPATH/src/github.com/FactomProject/FactomCode/restapi/restapi.conf $HOME/restapi.conf
```

open `$HOME/restapi.conf` in a text editor
Change values on the lines:
`BTCPubAddr` to the address in your wallet with testnet bitcoins
`WalletPassphrase` to `HardToGuessPW` or the password used to encrypt your wallet
`RpcClientPass` to `SecurePassHere` or the RPC password used in the btcd config files


### Use the Installation

With btcd, btcwallet and restapi all running concurrently, you can now run factomclient and factomexplorer.

The API document will walk you through installing those.

https://github.com/FactomProject/FactomDocs/blob/master/FactomAPI.pdf

The default configurations for those should point to localhost and work without further configuration.

```
go get -v github.com/FactomProject/FactomCode/factomclient/...
go get -v github.com/FactomProject/factomexplorer/...
mkdir ~/.factom/client/data
cp -r ~/go/src/github.com/FactomProject/factomexplorer/bundle/data/* ~/.factom/client/data/
# optional to configure clients to not use defaults
cp ~/go/src/github.com/FactomProject/factomexplorer/client.conf ~/
cp ~/go/src/github.com/FactomProject/FactomCode/factomclient/factomclient.conf ~/
```
Run both factomclient and factomexplorer concurrently.

Browse to `http://localhost:8088/v1/buycredit?&to=wallet&value=100` to add entry credits.

Browse to `http://localhost:8087/` and play with adding chains then entries.

If the system gets into a weird mode, you might want to delete the folder `/tmp/ldb9/` and `/tmp/wallet/`

Also, since the factom server state data is held in the temp directory, rebooting will erase changes made to your local installation.
