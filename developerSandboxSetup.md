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

The install directions are located [here](https://www.factom.com/howto/)

Here are the binaries for Windows, Mac, and Linux: https://github.com/FactomProject/distribution

Install the binaries like you would any other for your OS. The install directions walk you through various operating systems.  Do not run them yet, as you will be making your own fresh blockchain instead of using the public one. If you did run factomd before setup, follow the directions below for resetting the blockchain.

Three programs are installed: factomd, fctwallet, and factom-cli.

* Factomd is the main program.  It manages the blockchain, connects to the public network, and enforces the network rules.
* Fctwallet is an application for holding private keys. It builds Factoid transactions and handles crypto related operations to add user data into Factom.
* Factom-cli is a program for users to interface with factomd and fctwallet. Through this they create Chains, Entries, and Factoid transactions.

#### Configure Factomd for Sandbox use


Create a folder in your user home folder. The folder should be called `.factom`. If factomd has been run on your computer before you may need to first rename the database that is already there: `mv ~/.factom/ldb ~/.factom/ldb_old`.

In a terminal Linux and Mac: `mkdir ~/.factom`or Windows: `mkdir %HOMEDRIVE%%HOMEPATH%\.factom`

Save the configuration file [factomd.conf](https://raw.githubusercontent.com/FactomProject/FactomCode/master/factomd/factomd.conf) to your `.factom` directory.

* Open `factomd.conf`
* Change the line `NodeMode` from `FULL` to `SERVER`
  * This will make factomd create a blockchain
* Change `ExchangeRate` to `00000100`
  * This allows you to create many more Entries with Factoids.  It simulates Factoids having a high market value.
* Optionally adjust `DirectoryBlockInSeconds`.  600 gives 10 minute blocks, which is more realistic
  * The default is for 1 minute blocks (60) which is much easier to develop with.  Shorter times have not been tested.

For easier debugging, change the `logLevel` to  `debug`.  This exports pointers to data which is added into factom to the ~/.factom/data/export/ directory.  Adding new entries will add new files to the directory with the specified ChainID.


#### Run Factomd

In a terminal window, run `factomd`. (Windows users have a desktop shortcut)

In a new terminal window, run `fctwallet`. (Windows users have a desktop shortcut)

In a new terminal window, run `factom-cli properties` (Windows users may have to browse to the install location of factom-cli, or it might be in the path)

If you see the various version information from the different programs, it is working.


#### Charge an Entry Credit key

For this example, we will use the ed25519 private key with 32 bytes of zeros.
The private key is: `Es2Rf7iM6PdsqfYCo3D1tnAR65SkLENyWJG1deUzpRMQmbh9F3eG`
The public key is: `EC2DKSYyRcNWf7RS963VFYgMExoHRYLHVeCfQ9PGPmNzwrcmgm2r`

We will also use a Factoid key which has a balance of 300 in the genesis block. It has since been depleted on mainnet, but can be used on sandbox systems.
The private key is: `Fs3E9gV6DXsYzf7Fqx1fVBQPQXV695eP3k5XbmHEZVRLkMdD9qCK`
The public key is: `FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q`

Run these commands from a terminal window:
```
factom-cli importaddress zeros Es2Rf7iM6PdsqfYCo3D1tnAR65SkLENyWJG1deUzpRMQmbh9F3eG
factom-cli importaddress sand Fs3E9gV6DXsYzf7Fqx1fVBQPQXV695eP3k5XbmHEZVRLkMdD9qCK
factom-cli newtransaction trans1
factom-cli addinput trans1 sand 10
factom-cli addecoutput trans1 zeros 10
factom-cli addfee trans1 sand
factom-cli sign trans1
factom-cli transactions
factom-cli submit trans1
```
The above commands bought Entry Credits with 10 Factoids at the exchange rate dictated by the Federated Servers.

Wait 1 minute (the block time), then run:
```
factom-cli balances
```
It should display this:
```
  Factoid Addresses

     sand    FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q           289.999988

  Entry Credit Addresses

    zeros    EC2DKSYyRcNWf7RS963VFYgMExoHRYLHVeCfQ9PGPmNzwrcmgm2r       10000000
```

#### Make Entries into Factom

All Entries in Factom need to be in a Chain. First, make a Chain for your entries to live in.

```
echo "This is the payload of the first Entry in my chain" | factom-cli mkchain -e thisIsAChainName -e moreChainNameHere zeros
```
It makes the chain `23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8`

After a minute, you can now place Entries into this Chain
```
echo "This is the payload of an Entry" | factom-cli put -e newextid -e anotherextid -c 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8 zeros
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

You can get some diagnostic info from the control panel (which incidentally doesn't control anything). Browse to http://localhost:8090/controlpanel

![controlpanel](/images/controlpanel.png)


Also, browse to the .factom/data/export/ directory. It will make new folders when new Chains are created and new files when new Entries are made in a block period.  To enable this feature, change the logLevel field in factomd.conf from info to debug and restart factomd.


Another way is to run
```
factom-cli get chain 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
```
Then with the result it gives
```
factom-cli get eblock <result from above>
```
This gives some data, showing a 32 byte EntryHash
```
factom-cli get entry <EntryHash from above>

factom-cli get entry b77b7aaa1de46303141d633caac0bdc9b8a093555d2061211ffea9f6256a3e45
ChainID: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
ExtID: 74686973497341436861696e4e616d65
ExtID: 6d6f7265436861696e4e616d6548657265
Content:
"This is the payload of the first Entry in my chain"
```


### Setup a Factom Sandbox Server and Client


#### Setup a Factom Remote Server

On a remote machine, setup a Factom server. Both the client and server must be run of different machines.  
Use the same directions as [Install Factom Binaries](https://github.com/FactomProject/FactomDocs/blob/master/developerSandboxSetup.md#setup-a-local-sandbox-factom-server) and [Configure Factomd for Sandbox use](https://github.com/FactomProject/FactomDocs/blob/master/developerSandboxSetup.md#configure-factomd-for-sandbox-use).  Run factomd.  Make sure that port 8108 is open on the server.  Only factomd needs to be running on the remote server.

#### Setup Client to use Sandbox Server

Create a folder in your user home folder. The folder should be called `.factom`. If factomd has been run on your computer before you may need to first rename the database that is already there: `mv ~/.factom/ldb ~/.factom/ldb_old`.  Factomd will panic if it loads blocks with the wrong keys.

In a terminal Linux and Mac: `mkdir ~/.factom`or Windows: `mkdir %HOMEDRIVE%%HOMEPATH%\.factom`

Save the configuration file [factomd.conf](https://raw.githubusercontent.com/FactomProject/FactomCode/master/factomd/factomd.conf) to your `.factom` directory.

* Open `factomd.conf`
* Change the line `ServerPubKey` from `"0426a802617848d4d16d87830fc521f4d136bb2d0c352850919c2679f189613a"` to `"8cee85c62a9e48039d4ac294da97943c2001be1539809ea5f54721f0c5477a0a"`
  * This will make factomd recognize the sandbox public key instead of the official public key.

##### Connect Local Factomd to Sandbox Server

The local machine should be set as a client in the factomd.conf, which is default.

run factomd this way, but use the remote factom server's IP address instead.
```
factomd --connect=123.456.789.100
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

By default, Factom holds all the blockchain, wallet, etc data in the user's home directory in a folder called ".factom". This may be a hidden folder, so make sure to display hidden folders on your OS.

To reset the blockchain, first close factomd and fctwallet.  Delete all the folders and files in .factom except `factomd.conf` and `factoid_wallet_bolt.db`.

When you connect to mainnet again, it will redownload all the data again.
