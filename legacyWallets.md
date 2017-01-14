Factoid Legacy Wallet Guide
==========

### Install Instructions

Factom install directions have been created for M2 [here](installFromSourceDirections.md).

The old wallet (fctwallet and walletapp) will continue to work though. The updated M2 factomd has a new V2 API which provides more feedback, but the older V1 API still is supported. Fctwallet is an API based wallet, but can be interfaced with using factom-cli. The latest version of factom-cli no longer recognizes fctwallet, but the legacy verison was renamed to factom-cli1. This program will control fctwallet. Walletapp can also read the old wallets as well.  The legacy wallets are much slower when operating on M2 factomd compared with M1.


These instructions will install the legacy wallets.



```
# install glide, the package dependency manager
go get -u github.com/Masterminds/glide
# download the code
git clone https://github.com/FactomProject/factom-cli1 $GOPATH/src/github.com/FactomProject/factom-cli1
git clone https://github.com/FactomProject/fctwallet $GOPATH/src/github.com/FactomProject/fctwallet
git clone https://github.com/FactomProject/walletapp $GOPATH/src/github.com/FactomProject/walletapp

# get the dependencies and build each factom program
glide cc
cd $GOPATH/src/github.com/FactomProject/factom-cli1
glide install
go install
cd $GOPATH/src/github.com/FactomProject/fctwallet
glide install
go install
cd $GOPATH/src/github.com/FactomProject/walletapp
glide install
go install
# almost done.  To use walletapp with the GUI webpage, you need to copy the source HTML files to the proper location/

# sudo mkdir -p /usr/share/factom/walletapp/
# sudo cp -r $GOPATH/src/github.com/FactomProject/walletapp/staticfiles/* /usr/share/factom/walletapp/
```

Earlier commands that used factom-cli will now work using the command factom-cli1.



### Legacy Wallet Import Instructions

Most users will just want to port the legacy wallet databases into the new enterprise-wallet or factom-walletd. factom-walletd is much faster and is more robust.  The existing `factoid_wallet_bolt.db` contains the private keys for both fctwallet and walletapp. Both Enterprise and factom-walletd share the new `factom_wallet.db` file. Only Enterprise wallet uses the `factom_wallet_gui.db` file to save metadata about the addresses in `factom_wallet.db`.  The `factoid_blocks.cache` file enables the wallets to restart quickly.

##### factom-walletd

factom-walletd is the API wallet for new updated M2 version of factom. It is accessed through the factom-cli program, as well as a V2 JSON PRC.

One disadvantage of porting wallets from fctwallet to factom-walletd is that the address nicknames will be lost. Factom-walletd does not support address names, and addresses must be used by their public keys.

When a new wallet is made, a new BIP-44 seed is created from randomness.

To import, start factom-walletd with the -i flag and specify the M1 wallet.  This will specify where the M1 wallet is located and to import the addresses from it.  Factom-walletd will exit after it imports the addresses.

```
$ factom-walletd -i ~/.factom/factoid_wallet_bolt.db
Reading from '/home/factom/.factom/m2/factomd.conf'
Cannot open custom config file,
Starting with default settings.
open /home/factom/.factom/m2/factomd.conf: no such file or directory

Warning, factom-walletd API is not password protected. Factoids can be stolen remotely.
Warning, factom-walletd API connection is unencrypted. Password is unprotected over the network.
2017/01/14 15:51:56 Importing version 1 wallet /home/factom/.factom/factoid_wallet_bolt.db into /home/factom/.factom/wallet/factom_wallet.db
Database started from: /home/factom/.factom/wallet/factom_wallet.db
```


- `factom-cli backupwallet` will export the BIP-44 seed as well as the private keys for all addresses held by the wallet.
- `factom-cli exportaddresses` will export the public/private keypairs of all addresses in the wallet.
- `factom-cli importaddress` will import a list of private keys into the wallet.

To save the valuable keys and to review progress, you can import and export keys with the above commands. The most reliable backup method is to copy the `factom_wallet.db` to a safe location and recording the 12 words for newly created addresses.



##### Enterprise Wallet

Here are the import instructions for Enterprise Wallet:
https://docs.factom.com/#run-the-factom-foundation-wallet

Enterprise Wallet automatically imports old wallets if they are in the default location. If they are in a different location, old wallets can be imported with `enterprise-wallet -v1path=~/Desktop/factoid_wallet_bolt.db`

