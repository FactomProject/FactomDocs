Using factom-cli
===
factom-cli is the command line interface for interacting with the factom daemon and the factom wallet daemon. factom-cli may be used to write new data into Factom, read data from Factom, and manage Factoids and Entry Credits in the Factom Wallet.

Getting Entry Credits
---
Entry Credits are required to write Chains and Entries into Factom. A testing Address may be used to obtain Entry Credits when running Factom in testing mode, seperate from the true Factom Network.

Once factomd is running in SERVER mode and factom-walletd has been started the testing Address may be imported with its private key.

	$ factom-cli importaddress Fs3E9gV6DXsYzf7Fqx1fVBQPQXV695eP3k5XbmHEZVRLkMdD9qCK
	FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q
	$ factom-cli listaddresses
	FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q 300

It is convinient to assign the Public Address to a Bash variable for future operations.
	$ f1=FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q

A new Entry Credit Address may be created and stored in the wallet. Again, it is convinient to save the Entry Credit Address as a variable for later use.
* create new ec address
	$ factom-cli newecaddress
	EC2jF4CQZNriM8Z78YPMNrZFBEsHGrgdfnUN2gbLBgTJwtneMFbU
	$ e1=EC2jF4CQZNriM8Z78YPMNrZFBEsHGrgdfnUN2gbLBgTJwtneMFbU

Entry Credits are purchased for the new Entry Credit Address using the Factoid Address that was imported before. The Public Factoid Address is used to query the wallet which returns the Private Key to factom-cli to sign the transaction that purchases Entry Credits. Factoids may only be spent with the factom-cli using Factoid Addresses that are stored in the factom-walletd database.

	$ factom-cli buyec $f1 $e1 10000
	TxID: 1b300a370573cf130e82a00bf3924d0c81ee79dac12e477bf0a4c2c44062c79f
	$ factom-cli listaddresses
	FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q 289.988
	EC2jF4CQZNriM8Z78YPMNrZFBEsHGrgdfnUN2gbLBgTJwtneMFbU 10000

Creating Chains and Entries
---
A new Chain can now be created using the newly aquired Entry Credits. The External IDs of the First Entry of a Chain MUST be unique among all existing First Entrys. If Factom is being run in testing mode it is unlilkely that the Chain Name will be taken, but it is good practace to include a random nonce anyway. 

A new Chain is created by Writing a unique First Entry.

	$ echo Hello Factom | factom-cli addchain -e Hello -e $(openssl rand -base64 10) $e1
	Commiting Chain Transaction ID: ae4b5ec092072c54b55a5c06b9662d65a85f5683c5962abbffb7129a488dba29
	ChainID: e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	Entryhash: 3b5d63a87f2435cc017f824cfa370cd6a9064f6721912d6dd990e429128a7ca9

Getting the Chain Head will show the most recent Entry Block belongin to the Chain. If the Entry Block is the first Entry Block in the Chain the Previous Key Merkel Root will be all zeros, otherwise the Previous Key Merkel Root will be the Merkel Root of the Previous Entry Block in the Chain.

	$ factom-cli get chainhead e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	EBlock: e3f876b40bd641f863a88d2c8299a58d6b749f9ea53f70327fef1659673e72e1
	BlockSequenceNumber: 0
	ChainID: e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	PrevKeyMR: 0000000000000000000000000000000000000000000000000000000000000000
	Timestamp: 1472749920
	DBHeight: 111
	EBEntry {
		Timestamp 1472750280
		EntryHash 3b5d63a87f2435cc017f824cfa370cd6a9064f6721912d6dd990e429128a7ca9
	}

More Entries can be added to the Chain once it has been created. Additional Entries into the Chain need not have a unique set of External IDs.

	$ echo Hello again | factom-cli addentry -c e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5 $e1
	Commiting Entry Transaction ID: a2fbbc9e3beb8f7d6274d761df0645d07c8c56de41045e6f8fff1292f380e3bd
	ChainID: e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	Entryhash: d2628343f63c4cdbd0122d0563acf3f2a9331ebf56212476b02930ee863c7691

Reading Factom Chains
---
The factom-cli can retrive the First Entry of any Chain. By convention the First Entry of a Chain may contain usefull information about the Chains purpose, and/or how the Chains Entries are to be interperated or validated.

	$ factom-cli get firstentry e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	ChainID: e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	ExtID: Hello
	ExtID: j4vLmL/jH2bflw==
	Content:
	Hello Factom

The factom-cli may also be used to get all of the Entries in an existing Chain.

	$ factom-cli get allentries e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	Entry [0] {
	ChainID: e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	ExtID: Hello
	ExtID: j4vLmL/jH2bflw==
	Content:
	Hello Factom
	
	}
	Entry [1] {
	ChainID: e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	Content:
	Hello again
	
	}

Specific Entries or Entry Blocks may also be requested using factom-cli

	$ factom-cli get entry 3b5d63a87f2435cc017f824cfa370cd6a9064f6721912d6dd990e429128a7ca9
	ChainID: e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	ExtID: Hello
	ExtID: j4vLmL/jH2bflw==
	Content:
	Hello Factom

	$ factom-cli get eblock e3f876b40bd641f863a88d2c8299a58d6b749f9ea53f70327fef1659673e72e1
	BlockSequenceNumber: 0
	ChainID: e6a766a9bd9a40a708d85b8523ca55a179fa681853f49941c3456296e605c4b5
	PrevKeyMR: 0000000000000000000000000000000000000000000000000000000000000000
	Timestamp: 1472749920
	DBHeight: 111
	EBEntry {
		Timestamp 1472750280
		EntryHash 3b5d63a87f2435cc017f824cfa370cd6a9064f6721912d6dd990e429128a7ca9
	}
