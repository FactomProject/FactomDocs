Factom Developer Sandbox Setup Guide
==========

This is the Factom equivalent of Testnet3 in bitcoin, but doesn't require finding testnet coins.

Use Factoids with private key `Fs3E9gV6DXsYzf7Fqx1fVBQPQXV695eP3k5XbmHEZVRLkMdD9qCK`


There are three options for running a sandbox.


1. Run only a local sandbox server
  * Minimal setup
  * good for quickly testing APIs
  * Better feedback metrics


2. Run a test server and client
  * Much closer to production experience
  * Needed if multiple clients are used
  * Factom setup needed on two different computers
  
3. Run a Dockerized Factom sandbox
  * Zero setup
  * Good if you are already familiar with Docker
  * Almost the same as running a local sandbox server

### Setup a Local Sandbox Factom Server

#### Install Factom Binaries

Download the appropriate Factom binary package from factom.org

Directions for installing Factom Federation may be found [here](https://docs.factom.com/#install-factom-federation-ff)

Installers for for Windows, Mac, and Linux are hosted at https://github.com/FactomProject/distribution

Install the binaries like you would any other for your OS. The install directions walk you through various operating systems.  Do not run them yet, as you will be making your own fresh blockchain instead of using the public one. If you did run factomd before setup, follow the directions below for resetting the blockchain.

Three programs are installed: factomd, factom-walletd, and factom-cli. You may also wish to install the GUI [Enterprise Wallet](https://docs.factom.com/#enterprise-wallet).

* Factomd is the main program.  It manages the blockchain, connects to the public network, and enforces the network rules.
* factom-walletd is an application for holding private keys. It builds Factoid transactions and handles crypto related operations to add user data into Factom.
* Factom-cli is a program for users to interface with factomd and factom-walletd. It may be used to create Chains, Entries, and Factoid transactions.

#### Configure Factomd for Sandbox use

Create a folder in your user home folder. The folder should be called `.factom`. If factomd has been run on your computer before this folder will already exist and may already contain part of the factom blockchain.

In a terminal Linux and Mac: `mkdir -p ~/.factom/m2`or Windows: `mkdir %HOMEDRIVE%%HOMEPATH%\.factom\m2`

Save the configuration file [factomd.conf](https://raw.githubusercontent.com/FactomProject/factomd/master/factomd.conf) to your `.factom/m2` directory.

* Open `factomd.conf`
* Change the line `Network` from `MAIN` to `LOCAL`
	* This will cause factomd to run on its own local network rather than the factom main network.
* Change the line `NodeMode` from `FULL` to `SERVER`
  * This will make factomd create a blockchain
* Optionally adjust `DirectoryBlockInSeconds`.  600 gives 10 minute blocks, which is more realistic
  * The default is for 6 second blocks which is easier to develop with, but may cuase some strange behavior and errors.

For easier debugging, change the `logLevel` to  `debug`.  This exports pointers to data which is added into factom to the ~/.factom/data/export/ directory.  Adding new entries will add new files to the directory with the specified ChainID.

#### Run Factomd in sandbox mode

In a terminal window, run `factomd -network=CUSTOM -customnet="mycustomnet" -exclusive=true`. (Windows users have a desktop shortcut)

In a new terminal window, run `factom-walletd`. (Windows users have a desktop shortcut)

In a new terminal window, run `factom-cli properties` (Windows users may have to browse to the install location of factom-cli, or it might be in the path)

```
	% factom-cli properties
	CLI Version: 0.2.0.2
	Factomd Version: 0.4.0.2
	Factomd API Version: 2.0
	Wallet Version: 0.2.0.2
	Wallet API Version: 2.0
```

Once factomd is running you can use an internet browser and navigate to [](http://localhost:8090) to view the factomd Control Panel.

#### Charge an Entry Credit key

We use a Factoid key which has a balance of 40000 in the genesis block. It has since been depleted on mainnet, but can be used on sandbox systems.
The private key is: `Fs3E9gV6DXsYzf7Fqx1fVBQPQXV695eP3k5XbmHEZVRLkMdD9qCK`
The public key is: `FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q`

```
% factom-cli importaddress Fs3E9gV6DXsYzf7Fqx1fVBQPQXV695eP3k5XbmHEZVRLkMdD9qCK
FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q
```

We will generate a new Entry Credit address.

```
% factom-cli newecaddress
EC2kMjtY5jB5sLLzFtfzaA2rU92fqdNeiWNWjvtKmYQoG7fXFTmG
```

```
% factom-cli listaddresses
FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q 40000
EC2kMjtY5jB5sLLzFtfzaA2rU92fqdNeiWNWjvtKmYQoG7fXFTmG 0

% fa1=FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q
% ec1=EC2kMjtY5jB5sLLzFtfzaA2rU92fqdNeiWNWjvtKmYQoG7fXFTmG
```

Then purchase Entry Credits using our Factoid address.

```
% factom-cli buyec $fa1 $ec1 10000
TxID: ce18d00316508dd44a02d20bb3d9ee15f909bd9a099dd1b9b4576e2688f8f42a
Status: TransactionACK
% factom-cli balance $ec1
10000
```

#### Make Entries into Factom

All Entries in Factom need to be in a Chain. First, make a Chain for your entries to live in.

```
% echo "This is the payload of the first Entry in my chain" | factom-cli addchain -n thisIsAChainName -n moreChainNameHere $ec1
CommitTxID: e8950db51f6c15e10fdc6cc928cd40a5b9438b775708bdf4cabb266b0c1ffb5a
ChainID: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
Entryhash: e8a838f95c1fe873e0c7faae401cef31d6273644c32aa2324946613a594c0c77
```

It makes the chain `23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8`

Check the status of the Chain.

```
% factom-cli get chainhead 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
EBlock: c18bf1688d20b145d53f6e995ff8dfe91c2d73a422a625eb68c712ccc7988cd2
BlockSequenceNumber: 0
ChainID: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
PrevKeyMR: 0000000000000000000000000000000000000000000000000000000000000000
Timestamp: 1489718700
DBHeight: 130
EBEntry {
	Timestamp 1489718940
	EntryHash e8a838f95c1fe873e0c7faae401cef31d6273644c32aa2324946613a594c0c77
}
```

You can now place Entries into this Chain.

```
% echo "This is the payload of an Entry" | factom-cli addentry -e newextid -e anotherextid -c 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8 $ec1
CommitTxID: 0e6513528212b476297355207d619807f1b6bf2379f707c84cb0066ad2d4a920
ChainID: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
Entryhash: 0a9fee6636ab71466a8716ba3715cc01582174d8ffab9e830e9f4ce4f1ea8890
```

Query your entries in factom.

```
% factom-cli get entry 0a9fee6636ab71466a8716ba3715cc01582174d8ffab9e830e9f4ce4f1ea8890
EntryHash: 0a9fee6636ab71466a8716ba3715cc01582174d8ffab9e830e9f4ce4f1ea8890
ChainID: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
ExtID: newextid
ExtID: anotherextid
Content:
"This is the payload of an Entry"

```

And get information about the chain and its entries

```
% factom-cli get firstentry 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
EntryHash: e8a838f95c1fe873e0c7faae401cef31d6273644c32aa2324946613a594c0c77
ChainID: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
ExtID: thisIsAChainName
ExtID: moreChainNameHere
Content:
"This is the payload of the first Entry in my chain"


% factom-cli get allentries 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
Entry [0] {
EntryHash: e8a838f95c1fe873e0c7faae401cef31d6273644c32aa2324946613a594c0c77
ChainID: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
ExtID: thisIsAChainName
ExtID: moreChainNameHere
Content:
"This is the payload of the first Entry in my chain"

}
Entry [1] {
EntryHash: 0a9fee6636ab71466a8716ba3715cc01582174d8ffab9e830e9f4ce4f1ea8890
ChainID: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
ExtID: newextid
ExtID: anotherextid
Content:
"This is the payload of an Entry"

}
```

#### Make Entries into Factom Programmatically

Now that your EC key has been charged, you no longer need the wallet.  You can run API calls against factomd, as the crypto is simple enough to do when we get to submitting Entries.
[Here](https://github.com/FactomProject/Testing/tree/master/examples/) are some examples for using Factom.

[This](https://github.com/FactomProject/Testing/blob/master/examples/python/writeFactomEntryAPI.py) is a good example python script which commits and reveals Entries to Factom. 

If you have python installed, first install the needed libraries.  On Ubuntu this is enough:
```
sudo apt-get install python-pip
sudo apt-get install python-dev
sudo pip install ed25519
sudo pip install base58
```
Then run the script on the command line with `python writeFactomEntryAPI.py`

Edit some of the values at the top of the python script to make different Entries. Specifically, modify entryContent and externalIDs.  (Note the same Entry can be made multiple times)

#### Evaluating Success

You can get some diagnostic info from the control panel (which incidentally doesn't control anything). Browse to http://localhost:8090

![controlpanel](/images/controlpanel.png)

#### Setup a Factom Remote Server

On a remote machine, setup a Factom server. Both the client and server must be run of different machines.  
Use the same directions as [Install Factom Binaries](https://github.com/FactomProject/FactomDocs/blob/master/developerSandboxSetup.md#setup-a-local-sandbox-factom-server) and [Configure Factomd for Sandbox use](https://github.com/FactomProject/FactomDocs/blob/master/developerSandboxSetup.md#configure-factomd-for-sandbox-use).  Run factomd.  Make sure that port 8110 is open on the server.  Only factomd needs to be running on the remote server.

#### Setup Client to use Sandbox Server

Create a folder in your user home folder. The folder should be called `.factom/m2`.

In a terminal Linux and Mac: `mkdir -p ~/.factom/m2`or Windows: `mkdir -p %HOMEDRIVE%%HOMEPATH%\.factom\m2`

Save the configuration file [factomd.conf](https://raw.githubusercontent.com/FactomProject/factomd/master/factomd.conf) to your `.factom/m2` directory.

* Open `factomd.conf`
* Change the line `ServerPubKey` from `"0426a802617848d4d16d87830fc521f4d136bb2d0c352850919c2679f189613a"` to `"8cee85c62a9e48039d4ac294da97943c2001be1539809ea5f54721f0c5477a0a"`
  * This will make factomd recognize the sandbox public key instead of the official public key.
* Make sure you are using the default NodeMode = FULL for the client node.

##### Connect Local Factomd to Sandbox Server

The local machine should be set as a client in the factomd.conf, which is default.

run factomd this way, but use the remote factom server's IP address.
```
factomd -network=CUSTOM -customnet="mycustomnet" -exclusive=true -peers="serverip:8110" -prefix="notaserver"
```

The rest of the steps with [fctwallet and factom-cli](https://github.com/FactomProject/FactomDocs/blob/master/developerSandboxSetup.md#run-factomd) should work on the local machine.

### Run a Dockerized Factom sandbox

A community member graciously maintains a docker image for a Factom sandbox. 

Just execute
```
docker run -d --name factom-sandbox 31z4/factom-sandbox
```
and you are all set. You can now for example use `factom-cli`:
```
docker exec -it factom-sandbox factom-cli properties
```
See other details [here](https://github.com/31z4/factom-sandbox-docker).


### Resetting the Blockchain

By default, Factom holds all the blockchain, wallet, etc data in the user's home directory in a folder called ".factom/m2/custom-database". This may be a hidden folder, so make sure to display hidden folders on your OS.

To reset the blockchain, first close factomd and factom-walletd.  Delete all the folders and files in ``.factom/m2/custom-database except`` `factomd.conf`
