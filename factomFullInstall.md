Factom Central Server Install Guide
==========

Before the node network gets setup. Factom clients will simulate talking to a P2P network by using web services calls to a central server.  For testing, it will be beneficial to developers to have their own central server.


## Prepare Operating System

These directions were prepared on ubuntu 14.04.  Variations have been reported to work on windows, but no guarantees.

Install the go language

```
sudo apt-get install golang git mercurial
```

open the file `~/.profile` and add these lines to the bottom.  if they are not exact, then your ubuntu may not be bootable.

```
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```

**logout and login**.  this is the most straighforward way to run/test these changes.

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

In a second console window, run `btcwallet`

In a 3rd console window, run `btcctl --rpcuser=testuser --rpcpass=SecurePassHere --testnet --wallet createencryptedwallet HardToGuessPW`

change HardToGuessPW to something hard to guess.  It will still be in a config file, so it will not be that secure, though.


### Install GUI

This is not strictly nessicary, but is needed if you want to know where to send testnet BTC and diagnose some issues.  Command line alternatives are listed below.


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

Run `btcd` & `btcwallet` each in seperate terminal windows.

In a 3rd terminal window run `btcgui`

Send testnet bitcoins to an address in gui


### Command Line Alternatives to GUI


You might be able to get by with some command line arguments.  This one outputs an address in your wallet `btcctl --rpcuser=testuser --rpcpass=SecurePassHere --testnet --wallet getnewaddress`.  Save the address it gives you and send testnet bitcoins to it.  You can use `btcctl --rpcuser=testuser --rpcpass=SecurePassHere --testnet --wallet listreceivedbyaccount 0` to see if money has been sent to the wallet.  Also `btcctl --rpcuser=testuser --rpcpass=SecurePassHere --testnet --wallet listtransactions` to see what has happened in the wallet.



# Install Factom Central Server

coming soon.
