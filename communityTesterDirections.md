Factom Community Tester Install Guide
==========

Master branch is current as of **July 3, 1AM** Central Time.  If you installed before then, try doing the 'go get' steps again.



### Prepare Operating System

The most testing to date has been done under Linux. To get the best testing experience, it should be done on Linux. That will also help us recreate the bugs you experience better. If you are running Windows or Mac, please install a virtual machine to run Factom. Once we get a more stable system, we will get it working on Windows and Mac. 

Here are some good directions to get a virtual machine installed with Linux. http://www.instructables.com/id/Introduction-38/?ALLSTEPS

The following are assuming you are using the 64 bit version of Ubuntu, or one of its descendant projects like xubuntu or mint.

#### Install the go language and dependencies, then setup GOPATH

In a terminal window, install Git and Mercurial

```
sudo apt-get install git mercurial
```

download latest version of go https://golang.org/dl/  This example uses 64 bit Linux and 1.4.2 is the latest version.
```
sudo tar -C /usr/local -xzf go1.4.2.linux-amd64.tar.gz
```

Put the go binary directory in you path.
Open the file `~/.profile` and add these lines to the bottom.  If they are not exact, then your Linux may not be bootable.
```
export PATH=$PATH:/usr/local/go/bin
```
Now setup GOPATH
In the same `~/.profile` file and add these lines to the bottom.  If they are not exact, then your Linux may not be bootable.
```
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```
**logout and login**.  This is the most straightforward way to run/test these changes.


### Install Factom

Factom is currently developed in two different channels in Github. The bleeding edge is in the development branch, which may not even compile.  The version intended for testing is in the master branch. These directions install the master branch.
```
go get -v -u github.com/FactomProject/FactomCode/factomd
go get -v -u github.com/FactomProject/factoid/fctwallet
go get -v -u github.com/FactomProject/factom-cli
```
copy the config file
```
mkdir ~/.factom
cp ~/go/src/github.com/FactomProject/FactomCode/factomd/factomd.conf ~/.factom/factomd.conf
```

### Run Factom

Factom is run as 3 command line programs for this version. First, there is factomd. It connects to the server and handles connections to the internet. Second there is fctwallet. It handles the complexity of preparing the factoid transactions.  Third is factom-cli. It is currently how users are expected to interact with Factom. Also factom-cli serves as an example of how to make API calls.  Proper API documentation is forthcoming.

Open 3 command line windows. In the first one, run `factomd`. It should show lots of technical outputs showing what it is doing. Leave it running.
![factomd](/images/factomd.png)

In the second command line window, run `fctwallet`. It will have very little output. It will show more output after factom-cli is run though.
![fctwallet](/images/fctwallet.png)

In the third window, the factom-cli program will be run. You should run the trans.sh script to buy Entry Credits, move Factoids, and generally prep to place Entries. 

Run the script `~/go/src/github.com/FactomProject/factom-cli/trans.sh`.
![factom-cli](/images/factom-cli.png)

After the script has been run, you can now create your own Chains:

`echo "hello" | factom-cli mkchain -e thisisanexternalid jane` makes a new Chain with Chain Name "thisisanexternalid" paid for with the Entry Credit key named jane.  (Sorry the example would have been clearer if the Chain Name wasn't thisisanexternalid.  The ExternalID of the first Entry is interpreted as the Chain Name)  In the Entry's payload is the text string "hello". It returns "Chain: dbe18345132e9f1bd248b7f41da64bd2fad1479452ad509fa8a4b00ca3714fcc" which is the ChainID for the chain name thisisanexternalid. Note, hello = "68 65 6C 6C 6F 0A" and thisisanexternalid = "74 68 69 73 69 73 61 6E 65 78 74 65 72 6E 61 6C 69 64" when the ascii is decoded.

`factom-cli get chain dbe18345132e9f1bd248b7f41da64bd2fad1479452ad509fa8a4b00ca3714fcc` asks for the hash of the latest Entry Block with the ChainID of dbe18345132e9f1bd248b7f41da64bd2fad1479452ad509fa8a4b00ca3714fcc. In this example it returned cbac3993cf69795cb8916197c11d78de625c6ed80f048a1878a104df5312d350.

`factom-cli get eblock cbac3993cf69795cb8916197c11d78de625c6ed80f048a1878a104df5312d350` asks for the Entry Block with a hash of cbac3993cf69795cb8916197c11d78de625c6ed80f048a1878a104df5312d350. It returns: "&{{0 dbe18345132e9f1bd248b7f41da64bd2fad1479452ad509fa8a4b00ca3714fcc 0000000000000000000000000000000000000000000000000000000000000000 0} [{0 ab47e3cd7f1730f24e6f1633501eb73f787a69e75c6f4b501846cc8699716cb9}]}" with dbe... being the ChainID, 000... being the previous Entry Block hash. This value would be used with get eblock again to retrieve the preceeding block. It is 000... in this case because it is the first block in this Chain.  ab47... is the Entry Hash of the Entry in this block. 

`factom-cli get entry ab47e3cd7f1730f24e6f1633501eb73f787a69e75c6f4b501846cc8699716cb9` asks for the Entry learned about querying the Entry Block. It returns "&{dbe18345132e9f1bd248b7f41da64bd2fad1479452ad509fa8a4b00ca3714fcc [746869736973616e65787465726e616c6964] 68656c6c6f0a}"  with dbe... being the ChainID, 746869... being ascii decoding of the Chain Name, and 6865... being ascii decoding of the Entry payload.

`echo "hello2" | factom-cli put -e newextid -e anotherextid -c dbe18345132e9f1bd248b7f41da64bd2fad1479452ad509fa8a4b00ca3714fcc jane` adds another Entry into the Chain dbe... Nothing is returned.


##### More Examples

When we reset the genesis block after a few days, these hashes wont work, but the basic commands still will.

`factom-cli get head` gets a handle to the latest [Directory Block](https://github.com/FactomProject/FactomDocs/blob/master/factomDataStructureDetails.md#directory-block).  It will return a hash like f32af3c2b7e91df83c2eb887c822776e6480bcc2dd04a5ddb1ce28dd57808f59


It will also be anchored in the blockchain too.  [Here](https://www.blocktrail.com/tBTC/tx/13c3d8bf7fded24918e291d8d535c452dde3b64d7f2e027121a1ddf78abe16b4) is the anchor for the above Directory Block.  The op_return value gives 46610000000007faf32af3c2b7e91df83c2eb887c822776e6480bcc2dd04a5ddb1ce28dd57808f59.  The rightmost 32 bytes are the dblock keymr (hash).  the rightmost two bytes are Fa in ASCII.  The bytes 0000000007fa decode to 2042.


`factom-cli get dblock f32af3c2b7e91df83c2eb887c822776e6480bcc2dd04a5ddb1ce28dd57808f59` returns the data contained in the directory block.  It will return something like:
`&{ {abfddf912f66ecda3bbca5d7f72195d48f5cf9a9948346ad5090599b17c133df 0 2042} [{000000000000000000000000000000000000000000000000000000000000000a 39f8e58f86e6fb080ea938acc27129d84cb0518b136e63301f45bfd566191147} {000000000000000000000000000000000000000000000000000000000000000c 5174993458604fc9f036c10fdc421038544cfeac37a060dae1555cd47de8a302} {000000000000000000000000000000000000000000000000000000000000000f 826c33c79bde2a8082edb705fd8dd8e451b1d3dc67e3ad35f5ce5c4569c6b842}]}`

The value abfddf912f66ecda3bbca5d7f72195d48f5cf9a9948346ad5090599b17c133df is the dblock hash of the previous block.  `factom-cli get dblock abfddf912f66ecda3bbca5d7f72195d48f5cf9a9948346ad5090599b17c133df` will get the previous block, which can be repeated all the way to the genesis block.  

The 2042 value is the block height.  There have been 2042 previous dblocks (first one is zero).

The return value also shows 3 sub blocks which are referenced by this dblock.  The 3 pairs that end in 000a, 000c, and 000f are the adminstrative, entry credit, and factoid blocks.  They are not viewable at this time.

When you make a new chain, it tells you the ChainID the Chain Name hashes to. `echo "hello" | factom-cli mkchain -e chainNameGoesHere jane` returns Chain: 13ea4eb2b62c3bc5049746d964a64b4cbbe764a3f62a5fa2ec410542285c638a.  

After a minute, When you run `factom-cli get dblock 7e2e77727019369585e9ac0299110e90393f2edb9b078633467409e73d4027c9` it returns 
`&{ {907a6d004ed5a3b651af1ac80ff993bdebfc27abbb7f85f75e539bf4345a9e3f 0 2166} [{000000000000000000000000000000000000000000000000000000000000000a c8a29586d51b23a56fecbea15843ff65c77b05943c4286a35eb7a6dc751f0e83} {000000000000000000000000000000000000000000000000000000000000000c 775ed96b2868042a4b51986fd5bc2b6fc80581ba4076b461502511ad35e3e481} {000000000000000000000000000000000000000000000000000000000000000f af87dedc714127df084642be7930e4664b0374dddad2bb0d1cef17a4a15a122f} {13ea4eb2b62c3bc5049746d964a64b4cbbe764a3f62a5fa2ec410542285c638a 0d52effcd5d1a0542ce7fdac352ef5242c2827ee9406deae8b5cec60264683d4}]}`

The value 13ea4eb2b6...42285c638a is paired with 0d52eff...60264683d4, which is the keymr of the Entry Block of the 13ea... chainID for that minute (eventually 10 minutes).

#### Notes

demo.factom.org and explorer.factom.org are not connected in with the experimental server this guide operates on. Do not expect to see your entries there.

At the current time, blocks are set to be generated every 1 minute.

the factom-cli operations mkchain and put both wait 10 seconds between commit and reveal operations.

Intra-block acknowledgements are not generated and passed back to the local factomd yet. The local node waits for finished blocks before showing results. Wait 1 minute between a mkchain or put and when reading the data back.

All the clients share a wallet. You will see Factoid transactions that you did not make yourself.

#### If Factom is Crashing

This version of factomd downloads the blockchain from the server. The server is restarted regularly and the blockchain is reset. Local factomd does not work when the blockchain is reset on the server. The way to fix this is to delete the Factom database files from the /tmp/ directory.  These are the files and folders to delete:
```
/tmp/ldb9/
/tmp/store/
/tmp/factoid_bolt.db
/tmp/factoid_wallet_bolt.db
/tmp/factom-d.log
/tmp/ldb9.ver
```




