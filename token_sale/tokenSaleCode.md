Factom Token Sale Address Derivation
==========

The token sale will cause Bitcoins to be sent from the purchaser to the Factom multisignature address.  The Koinify wallet will attach the desired Factoid public key to the payment with an OP_RETURN statement. The Factoid genesis block will credit these public keys.

Perform this procedure only with small value Koinify wallets, because mistakes can compromise all the assets held in Koinify. Do not use the wallet for high values in the future either.

This is intended only for cryptocurrency experts to audit the Factoid purchase mechanism.  Do not use this procedure if you are not a cryptocurrency expert.

## Setup Environment

To protect all Koinify asset's private keys, the secret words should not be entered until the computer is offline.

- Remove Hard drive, and other permanent storage devices
- Boot to a CD version of linux. This example uses xubuntu 14.04.
- Connect to the internet
- in terminal run `sudo apt-get install python-setuptools`
- Download [python-mnemonic](https://github.com/trezor/python-mnemonic/archive/master.zip)
- unzip and run `sudo python setup.py install` in terminal for python-mnemonic
- Download [bip32utils](https://github.com/jmcorgan/bip32utils/archive/master.zip)
- unzip and run `sudo python setup.py install` in terminal for bip32utils
- Download [ecdsa](https://pypi.python.org/packages/source/e/ecdsa/ecdsa-0.13.tar.gz#md5=1f60eda9cb5c46722856db41a3ae6670)
- unzip and run `sudo python setup.py install` in terminal for ecdsa
- Download [ec25519](https://pypi.python.org/packages/source/e/ed25519/ed25519-1.3.tar.gz#md5=3e025286669b71158e7811e665952b56)
- in terminal run `sudo apt-get install python-dev`
- unzip and run `sudo python setup.py install` in terminal for ed25519

- Download [words_to_factoid_purchase.py](https://github.com/FactomProject/FactomDocs/raw/master/token_sale/words_to_factoid_purchase.py)
- in terminal run `python words_to_factoid_purchase.py`.  If working it should output `data encoded in OP_RETURN is: 464143544f4d303023f0e67ac88d0e39d6f3a894570efee943cd1c326f1d866647151194a8e01e21`

## Run the test

- **Disable internet**
- open `words_to_factoid_purchase.py` in a text editor
- replace the example words with the ones written down during the Koinify wallet creation
- run with `python words_to_factoid_purchase.py`
- The data displayed should be the data which appears after the OP_RETURN in the Bitcoin Blockchain

