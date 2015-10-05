Factom Community Tester Install Guide
==========

To see how factom is doing, go to http://factomstatus.com/

To examine your local factomd status, point your browser to: http://localhost:8090/controlpanel


### Prepare Operating System

The most testing to date has been done under Linux. To get the best testing experience, it should be done on Linux. That will also help us recreate the bugs you experience better. If you are running Windows, please install a virtual machine to run Factom. On a Mac, the only differences are with installing Hg and Git.  Installing on Windows has been known to work, but is not covered here.

Here are some good directions to get a virtual machine installed with Linux. http://www.instructables.com/id/Introduction-38/?ALLSTEPS

The following are assuming you are using the 64 bit version of Ubuntu, or one of its descendant projects like xubuntu or mint.

#### Install the go language and dependencies, then setup GOPATH

###### Install Package Managers 

In a terminal window, install Git and Mercurial

On Linux:
```
sudo apt-get install git mercurial
```

On Mac:
Steps 1 and 3 should be enough in this tutuorial:
https://confluence.atlassian.com/pages/viewpage.action?pageId=269981802

###### Install Golang

Download latest version of go https://golang.org/dl/  This example uses 64 bit Linux and 1.5.1 is the latest version.
```
sudo tar -C /usr/local -xzf go1.5.1.linux-amd64.tar.gz
```

On Mac, installing go this way should work:
http://www.cyberciti.biz/faq/installing-go-programming-language-on-mac-os-x/


###### Setup Paths

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
go get -v -u github.com/FactomProject/fctwallet
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
If factomd complains about not connecting, make sure your firewall allows connections out to port 8108 (1FAC in hex).


In the second command line window, run `fctwallet`. It will have very little output. It will show more output after factom-cli is run though.
![fctwallet](/images/fctwallet.png)

In the third window, the factom-cli program will be run. You should run the trans.sh script to buy Entry Credits, move Factoids, and generally prep to place Entries. 

Run this script: 
`~/go/src/github.com/FactomProject/factom-cli/setup.sh`.  After the time passes a 10 minute mark (ie 11:39 -> 11:40) run `factom-cli balances` to see if your app EC address has a balance.  This is the number of Entry Credits you can use to place Entries.
![factom-cli](/images/factom-cli.png)

After the script has been run, you can now create your own Chains:

`echo "hello world" | factom-cli mkchain -e thisIsAChainName -e moreChainNameHere app` makes a new Chain with Chain Name "thisIsAChainName" combined with "moreChainNameHere", paid for with the Entry Credit key named app.  In the Entry's payload is the text string "hello world". It returns "Creating Chain: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8" which is the ChainID for the chain name "thisIsAChainName" + "moreChainNameHere".

Wait until a 10 minute window passes on the clock.

`factom-cli get chain 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8` asks for the hash of the latest Entry Block with the ChainID of 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8. In this example it returned 791e3308911d7076ea2d8732f6ba723eaa027a51e76fca42fd9355062e4fe5d5.

`factom-cli get eblock 791e3308911d7076ea2d8732f6ba723eaa027a51e76fca42fd9355062e4fe5d5` asks for the Entry Block with a hash of 791e3308911d7076ea2d8732f6ba723eaa027a51e76fca42fd9355062e4fe5d5. It returns: "BlockSequenceNumber: 0
ChainID: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
PrevKeyMR: 0000000000000000000000000000000000000000000000000000000000000000
TimeStamp: 1439967000
EBEntry {
	TimeStamp 1439967420
	EntryHash 162fbef6320b28281b585f03a7d38e46ea7d9df14c7a7672df189c6fb0620c68
}
" with 2398... being the ChainID, 000... being the previous Entry Block hash. This value would be used with get eblock again to retrieve the preceeding block. It is 000... in this case because it is the first block in this Chain.  162f... is the Entry Hash of the Entry in this block. 

`factom-cli get entry 162fbef6320b28281b585f03a7d38e46ea7d9df14c7a7672df189c6fb0620c68` asks for the Entry learned about querying the Entry Block. It returns "ChainID: 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8
ExtID: 74686973497341436861696e4e616d65
ExtID: 6d6f7265436861696e4e616d6548657265
Content:
68 65 6c 6c 6f 20 77 6f | 72 6c 64 0a              || "hello world\n"
"

`echo "hello2" | factom-cli put -e newextid -e anotherextid -c 23985c922e9cdd5ec09c7f52a7c715bc9e26295778ead5d54e30a0a6215783c8 app` adds another Entry into the Chain 239... It returns "Creating Entry: 7e25ca2e41cd03782aa3337a98f4a261aa2c00b904b7da2e67d96262a2f5a034".  


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

explorer.factom.org shows entries into the system.  It is a good method of diagnosing problems and seeing what the system is doing.

the factom-cli operations mkchain and put both wait 10 seconds between commit and reveal operations.

Intra-block acknowledgements are not generated and passed back to the local factomd yet. The local node waits for finished blocks before showing results. Wait until the 10 minute has passed between a mkchain or put and when reading the data back.


#### If Factom is Crashing

This version of factomd downloads the blockchain from the server. The server is restarted regularly and the blockchain is reset. Local factomd does not work when the blockchain is reset on the server. The way to fix this is to delete the Factom database files from the /tmp/ directory.  Run this code to delete the databases run `~/go/src/github.com/FactomProject/FactomCode/cleandb.sh`

Backup the factoid_wallet_bolt.db in the .factom directory if you made any new Entry Credit or Factoid addresses. It is a good practice to backup this file after creating every address. 





