Factom Data Structures
==========

This document describes the byte level detail of the Factom data structures.

Unless otherwise specified, Data is interpreted as big-endian.

## Building Blocks

This describes the low level minutia for common data structures.

### Variable Integers (varInt_F)
**(not yet implemented)**

This is modeled after the Bitcoin's variable length integer, but is big-endian compared to Bitcoin's little endian.
https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer

The first byte is the the value represented, or if above 252, indicates how many bytes the integer takes. 
This allows small values to economize on space, but doesn't limit the amount to 255.  Only positive integers can be represented with varInt_F.

| Value of 1st byte | Structure Length | Max Value |
| ----------------- | ---------------- | --------- |
| <0xFD | 1 byte | 0xFC |
| 0xFD | 3 byte | 0xFFFF |
| 0xFE | 5 byte | 0xFFFFFFFF |
| 0xFF | 9 byte | 0xFFFFFFFFFFFFFFFF |


### Chain Name
**(implemented)**

A Chain Name is a value to uniquely identify a Chain. It can be a random number, a string of text, a public key, or hash of some private directory path.  The choice of Chain Name is left up to the user. The Chain Name can be specified with multiple sequential byte strings.  They are treated as different segments of data instead of concatenated, to differentiate trailing bytes of one segment from leading bytes of the next segment.

There can be a maximum of 255 segments in a Chain Name.  The individual segment length are limited by how many bytes can fit in an Entry (approx 10 KiB).


### ChainID
**(implemented, not verified)**

A ChainID is a series of SHA256 hashes of Chain Name segments.  The ChainID is 32 bytes long. The ChainID must be the hash of *something* to only have opaque data in the higher level block structures.

The algorithm hashes each segment of the Chain Name.  Those hashes are concatenated, and are hashed again into a single 32 byte value.

Getting a ChainID from a single segment Chain Name would be equivalent of hashing the Chain Name twice.

ChainID = SHA256( SHA256(Name[0]) | SHA256(Name[1]) | ... | SHA256(Name[X]) )

See code at the go source path github.com/FactomProject/FactomCode/notaryapi/echain.go


## User Elements

These data structures are composed by the Users.

### Entry
**(Different from what is implemented)**

An Entry is the element which carries user data. An Entry Reveal is essentially this data.

An External ID (ExtID) is one or more byte fields which can serve as hints to 3rd party databases.  These are fields which the Entry author felt would make good keys into a database.  They are not required for Factom usage.  The data is not checked for validity, or sanitized.  There is no enforcement of this data and is only interpreted when forming a key for a database.  When a database interprets the data at this point, the only validity check is that when parsed, the ExtID data cannot be more than the Payload.


| data | Field Name | Description |
| ----------------- | ---------------- | --------------- | 
| **Header** |  | |
| 1 byte | version | starts at 0.  Higher numbers are currently rejected |
| 32 bytes | ChainID | This is the chain which the author wants this entry to go into |
| 2 bytes | Entry Length | Describes how many bytes this Entry uses.  Count starts at the beginning of the version and ends at the end of the Payload.  Big endian. |
| **Name Header** |  | This header is only interpreted and enforced if this is the first Entry in a Chain, otherwise the Payload field starts here |
| 1 byte | number of Chain Name elements  | This must be 1-255 if creating a new Chain.  These fields must hash to the ChainID specified in this Entry. |
| 2 bytes | Chain Name element 0 length | This is the number of the following bytes to be interpreted as a Chain Name element.  Cannot be 0 length. | 
| varaible | Chain Name element 0 data | This is the data to be hashed |
| 2 bytes | Chain Name element X length | There will be as many elements and length designators as are specified in 'number of Chain Name elements' | 
| varaible | Chain Name element X data | This is the data to be hashed |
| **Payload** | | This is the data between the end of the enforced header and the end of data defined by Entry Length | 
| **External Identifiers** | | This optional data is intended as suggested keys for searching for this Entry in an external database.  |
| 1 byte | Number of ExtIDs | Can be 0. Max is 255.  This describes the number of individual ExtIDs to parse. |
| 1 byte | ExtID 0 encoding | 0=Unprintable/binary 1=UTF-8  2=UTF-16 |
| 2 bytes | ExtID 0 length | This is the number of the following bytes to be interpreted as an External ID | 
| varaible | ExtID 0 data | This is the first External ID |
| 1 byte | ExtID X encoding | 0=Unprintable/binary 1=UTF-8  2=UTF-16 |
| 2 bytes | ExtID X length | This is the number of the following bytes to be interpreted as an External ID | 
| varaible | ExtID X data | This is the Nth External ID |
| **Content** | | This is all user defined content | 
| variable | Entry Data | This is the payload of the Entry.  It is all user specified data. |

Minimum empty Entry length: 35 bytes

Minimum empty First Entry with Chain Name of 1 byte: 39 bytes

Maximum Payload size: 10KiB - (1 + 32 + 2) = 10205 bytes

Typical size recording the hash of a file with 200 letters of ExtID metadata: 1+32+2+1+1+2+200+32 = 271 bytes

example size of something similar to an Omni(MSC) transaction, assuming 500 bytes [per transaction](https://blockchain.info/address/1EXoDusjGwvnjZUyKkxZ4UHEf77z6A5S4P):
1+32+2+500 = 535 bytes

Example Entry with a ChainID of 'test', spaces added for clarity:
As first Entry:
00 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 0040 01 0004 74657374 01 01 0007 4b657948657265 5061796c6f616448657265

As regular Entry:
00 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 0039 01 01 0007 4b657948657265 5061796c6f616448657265


### Entry Hash

The Entry Hash is a 32 byte identifier unique to a specific Entry.  It is referenced in the Entry Block body as well as in the Entry Commit.  In a desire to maintain long term resistance to [first-preimage attacks](http://en.wikipedia.org/wiki/Preimage_attack) in SHA256, so SHA3-256 is included in the process to generate an Entry Hash. For a future attacker to come up with a dishonest piece of data, they would need to take advantage of weaknesses in both SHA256 and SHA3.  SHA256 is used for merkle roots due to anticipated CPU hardware acceleration.

To calculate the Entry Hash, first the Entry is serialized and passed into a SHA3-256 function.  The 32 bytes output from the SHA3 function is appended to the serialized Entry.  The Entry+appendage are then fed through a SHA256 function, and the output of that is the Entry Hash.

Using the above Entry as an example.

009f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a080039010100074b6579486572655061796c6f616448657265 is passed into SHA3-256 and that gives: bdb7b6b6b349b9cc0ce353b4181b77cb23ea1d2a26dcd90bd701ae6e8dbc673c 

This is then appended to make 
009f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a080039010100074b6579486572655061796c6f616448657265bdb7b6b6b349b9cc0ce353b4181b77cb23ea1d2a26dcd90bd701ae6e8dbc673c
which is then SHA256 hashed to make an Entry Hash of:
66e1b94b528e54405426a103b62c9e8897ee84ce3af8e0ef0c96651a0853e151


### Entry Commit

An Entry Commit is a payment for a specific Entry. It deducts a balance held by a specific public key in the amount specified. They are collected into the Entry Credit chain as proof that a balance should be decremented.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- | 
| **Header** |  | |
| 1 byte | version | starts at 0.  Higher numbers are currently rejected |
| 6 bytes | milliTimestamp | This is a timestamp that is user defined.  It is a unique value per payment. |
| 32 bytes | Entry Hash | This is the SHA2&3 descriptor of the Entry to be paid for. |
| 1 byte | Number of Entry Credits | This is the number of Entry Credits which will be deducted from the balance of the public key. Any values above 10 are invalid. |
| 64 bytes | Signature | This is a signature of the data from the version through the Number of Entry Credits.  Parts ordered R then S. |
| 32 bytes | Pubkey | This is the Entry Credit public key which will have the balance reduced. |

The Entry Commit is only valid for 24 hours before and after the milliTimestamp. Since Entry Credits are balance based instead of transaction based like Factoids, replay attacks can reduce balances. Also a user can pay for the same Entry twice, and have two copies in Factom. Since a P2P network is used, the payments would need to be differentiated. The payments would be differentiated by public key and the time specified. This puts a limit of 1000 per second on any individual Entry Credit public key. The milliTimestamp also helps the network protect itself.  Adding the time element allows peers to automatically reject payments beyond a day plus or minus. This means they must check for duplicates only over a rolling two day period. 

### Factoid Transaction

Factoid transactions are similar to Bitcoin transactions, but incorporate some [lessons learned](http://www.reddit.com/r/Bitcoin/comments/2jw5pm/im_gavin_andresen_chief_scientist_at_the_bitcoin/clfp3xj) from Bitcoin.
- They are closer to P2SH style addresses, where the value is sent to the hash of a redeem condition, instead of sent to the redeem condition itself. To redeem value, a datastructure containing public keys, etc should be revealed. This is referred to as the **Redeem Condition Datastructure (RCD)**
- Factoids use Ed25519 with Schnorr signatures.  They have [many benefits](https://ripple.com/uncategorized/curves-with-a-twist/0) over the ECDSA signatures used in Bitcoin.
- Txid does not cover the signature field.  This will limit damaging malleability by attackers without the private key.
- Scripts are not used.  They may be added later, but are not implemented in the first version. Instead of scripts, there are a limited number of valid RCDs which are interpreted.  This is similar to how Bitcoin only has a handful of standard transactions.  Non-standard transactions are not relayed on the Factom P2P network. In Factom, non-standard transactions are undefined.  Adding new transaction types will cause a hard fork of the Factom network.


The transaction ID (txid) is a SHA256 hash of the data from the header through the inputs.  The RCD reveal and signatures are not part of the txid.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- | 
| **Header** | | |
| 1 byte | Version | Version of the transaction type.  Versions above 0 are not relayed. |
| 5 bytes | lockTime | same rules as Bitcoin.  less than 500 million defines the minimum block height this tx can be included in or be rebroadcast.  Greater or equal to 500 million is minimum Unix epoch time.  Big endian, so first byte is zero for the next 100 years or so. To disable timelock, set to all zeros. |
| **Outputs** | | |
| varInt_F | Factoid Output Count | This is the quantity of redeemable (Factoid) outputs created.  |
| varInt_F | value | (Output 0) The quantity of Factoshis (Factoids * 10^-8) reassigned. |
| 32 bytes | RCD Hash | (Output 0) The hash (SHA256) of the Redeem Condition Datastructure (RCD), which must be revealed then satisfied to later use the value as an input |
| varInt_F | value | (Output X) The quantity of Factoshis reassigned. |
| 32 bytes | RCD Hash | (Output X) The hash of the RCD |
| varInt_F | Entry Credit Purchase Count | This is the quantity of non-redeemable (Entry Credits) outputs created.  |
| varInt_F | value | (Purchase 0) The quantity of Factoshis to be turned into ECs. |
| 32 bytes | EC Pubkey | (Purchase 0) The Ed25519 raw public key which is the Entry Credit pubkey.  |
| varInt_F | value | (Purchase X) The quantity of Factoshis to be turned into ECs. |
| 32 bytes | EC Pubkey | (Purchase X) The Ed25519 raw EC public key. |
| **Inputs** | | |
| varInt_F | Input Count | This is the quantity of previous transaction outputs spent.  |
| 32 bytes | txid | (Input 0) This is the previous transaction identifier which is being spent. |
| varInt_F | output index | (Input 0) This is the index of the specified txid which is being spent. |
| 1 byte | sighash type | (Input 0) Define how the transaction can be reconfigured without resigning. |
| 32 bytes | txid | (Input X) This is the previous transaction identifier which is being spent. |
| varInt_F | output index | (Input X) This is the index of the specified txid which is being spent. |
| 1 byte | sighash type | (Input X) Define how the transaction can be reconfigured without resigning. |
| **Redeem Condition Datastructure (RCD) Reveal** | | |
| varInt_F | RCD Count | The number of different hashes which which are presented as inputs. RCD Count can be lower than Input Count, but not higher. If duplicate input RCD hashes are used, then those inputs need to be ordered so that identical addresses are sequential. |
| varInt_F | RCD 0 length | This is how many bytes the first RCD takes |
| variable | RCD 0 | First RCD.  It hashes to input 0.  It may also hash to input 1, 2, 3, etc. Each RCD is checked against an input address, until the next input address is different.  No two identical RCDs can follow each other.  This allows a tx to be created which spends many inputs to the same address, but only needs to reveal the RCD once. |
| varInt_F | RCD X length | This is how many bytes the Xth RCD takes |
| variable | RCD X | The next RCD is checked against the next different address in the inputs list.|
| **Signatures** | | |
| variable | Signature bitfield | (Input 0) This is a set of bytes which form a bitfield. The number of bytes is determined by the N value in the RCD. |
| 64 bytes | Signature | (Input 0, 1st specified pubkey) signature covering the sighash data specified in input 0.  First is R then S|
| 64 bytes | Signature | (Input 0, Yth specified pubkey) signature covering the sighash data specified in input 0 |
| variable | Signature bitfield | (Input X) The bitfield which cover the Xth input. |
| 64 bytes | Signature | (Input X, 1st specified pubkey) signature covering the sighash data specified in input 0 |
| 64 bytes | Signature | (Input X, Yth specified pubkey) signature covering the sighash data specified in input 0 |


##### Redeem Condition Datastructure (RCD)

This can be considered equivalent to a Bitcoin redeem script behind a P2SH transaction. The first version will only support multisignature addresses.  Type 0 is defined here.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- | 
| **Header** | | |
| 1 byte | Version | Version of the RCD type.  Versions above 0 are not relayed unless it is preceded by a federated server's confirmation.  |
| 1 byte | type | This specifies how the datastructure should be interpreted.  It sets expectations for the signature field. Type 0 is M of N multisignature. No other types are supported at this point. |
| varInt_F | N | The number of pubkeys specified.  |
| 32 bytes | Pubkey 0 | the first pubkey in the datastructure |
| 32 bytes | Pubkey X | There are N total pubkeys |
| varInt_F | M | The minimum number of signatures which are required for validity.  Must be <=N. |

##### Signature bitfield

This set of bytes indicates which M of the N signatures are present.  The number of bits set to 1 specifies the number of signatures.  The position of the bits specify which subset the M signatures are provided.  The number of bytes is determined by N in the RCD.  The number of bytes is ceiling(N/8).  A 1 in the most significant bit of the first byte signifies the presence of a signature from the first pubkey in the RCD.  The most significant bit of the second byte is for the 9th pubkey.  Finding the number of signatures to parse is done by counting the number of bits set.

For example, a 3 of 10 multisig might have a bitfield like this: 00101000 01000000.  The third, 5th and 10th keys have signatures provided.

##### Sighash Type

This field is modeled after Bitcoin's [OP_CHECKSIG](https://en.bitcoin.it/wiki/OP_CHECKSIG).  It allows the signer of this input to specify how the transaction can be reconfigured without resigning.  For the initial release of Factoids, only Sighash_All is supported.  The value must be set to 0x00 for version 0 of the transaction.

The signature covers Header, Outputs, and Inputs.  The RCD is protected from tampering because the signed inputs specify only one possible RCD.


Note: For the token sale, a raw Ed25519 pubkey is included in an OP_RETURN output along with the payment to the sale multisig address.  The the genesis block will contain a transaction which outputs to many 1 of 1 addresses.  There will be an output for each of the Bitcoin payments' specified pubkeys.  The addresses will be derived from the exposed pubkeys. 

Some later RCD types will be added.  Output types supporting [atomic cross](https://en.bitcoin.it/wiki/Atomic_cross-chain_trading) chain swaps and [time locking](https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki) outputs are desirable.  Output scripts are also useful and desirable, but can open security holes.  They are not critical for the first release of Factom, so we will implement them later. This would give us the ability to make conditional outputs (IF, AND, OR, etc).  Nesting is also desirable but undefined in this version.  This would give multisig within a multisig transaction.  Implementing scripts will give all the intermediate RCD types, so possibly going directly to scripts can bypass a special atomic cross chain swap, etc.

Ed25519 allows for threshold multisig in a single signature, but that cryptography will have to come later.  For now, multisig is based on multiple independent pubkeys and multiple signatures.

Fees are the difference between the outputs and the inputs.  The fees are [sacrificed](https://blog.ethereum.org/2014/02/01/on-transaction-fees-and-the-fallacy-of-market-based-solutions/).  They are defined by, but not reclaimed by the Federated servers.  The minimum transaction fees are based on the current exchange rate of Factoids to Entry Credits.  The outputs must be less than the inputs by at least the the fee amount at confirmation time.  The fees the sum of 3 things that cause load on the system:
1. Transaction data size. -- Factoid transactions are charged the same amount as Entry Credits (EC).  The size fees are 1 EC per KiB with a maximum transaction size of 10 KiB.
2. Number of outputs created -- These are data points which potentially need to be tracked far into the future.  They are more expensive to handle, and require a larger sacrifice.  Outputs cost 10 EC per output. A purchase of Entry Credits also requires the 10 EC fee to be valid.
3. Number of signatures checked -- These cause expensive computation on all full nodes.  A fee of 1 EC equivalent must be paid for each signature included.

A minimal transaction with 2 inputs and 2 outputs spending single sig outputs would cost the equivalent of 23 Entry Credits.


## Block Elements

These data structures are constructed of User Elements, etc.

### Directory Block

A Directory Block consists of a header and a body. The body is a series of pairs of ChainIDs and Merkle Roots.
