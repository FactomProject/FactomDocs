Factom Data Structures
==========

This document describes the byte level detail of the Factom data structures.

Unless otherwise specified, Data is interpreted as big-endian.

## Building Blocks

This describes the low level minutia for common data structures.

### Variable Integers (varInt_F)
**(implemented, not verified)**

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

The individual segment length are limited by how many bytes can fit in an Entry (approx 10 KiB).  There must be at least one element in the Chain Name, and each element must be at least 1 byte long.


### ChainID
**(implemented, not verified)**

A ChainID is a series of SHA256 hashes of Chain Name segments.  The ChainID is 32 bytes long. The ChainID must be the hash of *something* to only have opaque data in the higher level block structures.

The algorithm hashes each segment of the Chain Name.  Those hashes are concatenated, and are hashed again into a single 32 byte value.

Getting a ChainID from a single segment Chain Name would be equivalent of hashing the Chain Name twice.

ChainID = SHA256( SHA256(Name[0]) | SHA256(Name[1]) | ... | SHA256(Name[X]) )

See code at the go source path github.com/FactomProject/FactomCode/common/echain.go


## User Elements

These data structures are composed by the Users.

### Entry
**(Different from what is implemented)**

An Entry is the element which carries user data. An Entry Reveal is essentially this data.

The Defined Fields (DF) are a part of the Entry which have byte sequence lengths that must be known by Factom.  The two data types in the DF are Chain Name and External IDs.

If the Entry is the first of a certain ChainID in Factom, the DFs are interpreted as a Chain Name.  If it is not the first Entry, then the DFs are interpreted as External IDs.

To be valid, the DF header is parsed and the end of the last field must match the defined length of the header.

External IDs (ExtID) are intended to serve as keys to databases.  They are not required for Factom usage.  The data content is not checked for validity, or sanitized, as it is only viewed as binary data.


| data | Field Name | Description |
| ----------------- | ---------------- | --------------- | 
| **Header** |  | |
| 1 byte | Version | starts at 0.  Higher numbers are currently rejected. |
| 32 bytes | ChainID | This is the Chain which the author wants this Entry to go into. |
| 2 bytes | DF Header Size | Describes how many bytes the defined header takes.  Must be less than or equal to Paylod Size.  Big endian. |
| 2 bytes | Payload Size | Describes how many bytes the payload of this Entry uses.  Count starts at the beginning of the DF header (if present) and spans through the Content.  Max value can be 10240.  Big endian. |
| **Payload** | | This is the data between the end of the Header and the end of the Content. |
| **Defined Fields Header** |  | This header is only interpreted and enforced if the DF Header Size is greater than zero. |
| 2 bytes | DF element 0 length | This is the number of the following bytes to be interpreted as a Defined Field element.  Cannot be 0 length. | 
| variable | DF element 0 data | This is the data for the first element.  It is an ExtID or Chain Name element. |
| 2 bytes | DF element X length | The DF Header will keep being parsed until it has iterated over the number of bytes specified in DF Header Size. | 
| variable | DF element X data | This is the Xth element.  The last byte of the last element must fall on the last byte specified by DF Header Size. |
| **Content** | | | 
| variable | Entry Data | This is the unstructured part of the Entry.  It is all user specified data. |

Minimum empty Entry length: 37 bytes

Minimum empty First Entry with Chain Name of 1 byte: 40 bytes

Maximum Entry size: 10KiB + 37 bytes = 10277 bytes

Typical size recording the hash of a file with 200 letters of ExtID metadata: 1+32+2+2+2+200+32 = 271 bytes

example size of something similar to an Omni(MSC) transaction, assuming 500 bytes [per transaction](https://blockchain.info/address/1EXoDusjGwvnjZUyKkxZ4UHEf77z6A5S4P):
1+32+2+2+500 = 537 bytes

Example Entry with a Chain Name of 'test', spaces added for clarity:
As first Entry:
00 954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f4 0006 0011 0004 74657374 5061796c6f616448657265

As regular Entry without ExtID:
00 954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f4 0000 000b 5061796c6f616448657265

As regular Entry with ExtID of 'Hello' in 'test' chain:
00 954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f4 0007 0012 0005 48656c6c6f 5061796c6f616448657265


### Entry Hash
**(Different from what is implemented)**

The Entry Hash is a 32 byte identifier unique to a specific Entry.  It is referenced in the Entry Block body as well as in the Entry Commit.  In a desire to maintain long term resistance to [second-preimage attacks](http://en.wikipedia.org/wiki/Preimage_attack) in SHA256, SHA3-256 is included in the process to generate an Entry Hash. For a future attacker to come up with a dishonest piece of data, they would need to take advantage of weaknesses in both SHA256 and SHA3.  SHA256 is used for Merkle roots due to anticipated CPU hardware acceleration.

To calculate the Entry Hash, first the Entry is serialized and passed into a SHA3-256 function.  The 32 bytes output from the SHA3 function is appended to the serialized Entry.  The Entry+appendage are then fed through a SHA256 function, and the output of that is the Entry Hash.

Using the above Entry as an example.

00954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f40000000b5061796c6f616448657265 is passed into SHA3-256 and that gives: 1587d15c3a9157016e6284e949665184af402b8f605e1d8b2c75411a3d1f6e6c 

This is then appended to make 
00954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f40000000b5061796c6f6164486572651587d15c3a9157016e6284e949665184af402b8f605e1d8b2c75411a3d1f6e6c
which is then SHA256 hashed to make an Entry Hash of:
3a34ac57249d8321891b5bc04c42eb20dcaf5ddf5516bd9496a1c68c14947979


### Entry Commit

An Entry Commit is a payment for a specific Entry. It deducts a balance held by a specific public key in the amount specified. They are collected into the Entry Credit chain as proof that a balance should be decremented.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- |
| **Header** |  | |
| 1 byte | Version | starts at 0.  Higher numbers are currently rejected |
| 6 bytes | milliTimestamp | This is a timestamp that is user defined.  It is a unique value per payment. |
| 32 bytes | Entry Hash | This is the SHA2&3 descriptor of the Entry to be paid for. |
| 1 byte | Number of Entry Credits | This is the number of Entry Credits which will be deducted from the balance of the public key. Any values above 10 are invalid. |
| 64 bytes | Signature | This is a signature of the data from the version through the Number of Entry Credits.  Parts ordered R then S. Signature covers from Version through 'Number of Entry Credits' |
| 32 bytes | Pubkey | This is the Entry Credit public key which will have the balance reduced. |

The Entry Commit is only valid for 24 hours before and after the milliTimestamp. Since Entry Credits are balance based instead of transaction based like Factoids, replay attacks can reduce balances. Also a user can pay for the same Entry twice, and have two copies in Factom. Since a P2P network is used, the payments would need to be differentiated. The payments would be differentiated by public key and the time specified. This puts a limit of 1000 per second on any individual Entry Credit public key per duplicate Entry. The milliTimestamp also helps the network protect itself.  Adding the time element allows peers to automatically reject payments beyond a day plus or minus. This means they must check for duplicates only over a rolling two day period. 

The number of Entry Credits is based on the Payload size. Cost is 1 EC per KiB. Empty Entries cost 1 KiB.


### Chain Commit

A Chain Commit is a simultaneous payment for a specific Entry and a payment to allow a new Chain to be created. It deducts a balance held by a specific public key in the amount specified. They are collected into the Entry Credit chain as proof that a balance should be decremented.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- |
| 1 byte | Version | starts at 0.  Higher numbers are currently rejected |
| 6 bytes | milliTimestamp | This is a timestamp that is user defined.  It is a unique value per payment. |
| 32 bytes | ChainID Hash | This is a double hash (SHA256d) of the ChainID which the Entry is in. |
| 32 bytes | Entry Hash + ChainID | This is the double hash (SHA256d) of the Entry Hash concatenated with the ChainID. |
| 32 bytes | Entry Hash | This is the SHA2&3 descriptor of the Entry to be the first in the Chain. |
| 1 byte | Number of Entry Credits | This is the number of Entry Credits which will be deducted from the balance of the public key. Any values above 20 or below 11 are invalid. |
| 64 bytes | Signature | This is a signature of the data from the version through the Number of Entry Credits.  Parts ordered R then S. Signature covers from Version through 'Number of Entry Credits' |
| 32 bytes | Pubkey | This is the Entry Credit public key which will have the balance reduced. |

The Federated server will keep track of the Chain Commits based on ChainID Hash. The Federated servers keep track of the Chain Commits they receive.  When the first Entry is received, it will reveal the ChainID.  If the ChainID was a secret, then it now can be compared against all the possible Chain Commits claiming to pay for Entries of a certain ChainID. Once the ChainID is revealed, the ChainID hash and the 'Entry Hash + ChainID' fields can be compared to see if they match and form valid hashes. If they do not match, that Chain Commit is invalid.  If they do match, then the first one to be acknowledged gets accepted as the first Entry.  They maintain exclusivity for 1 hour for each ChainID hash after an acknowledgement.  The commit itself must be within 24 hours +/- of the milliTimestamp.

A prudent user will not broadcast their First Entry until the Federated server acknowledges the Chain Commit.  If they do not wait, a peer on the P2P network can put their Entry as the first one in that Chain.

Chain Commits cost 10 Entry Credits to create the Chain, plus the fee per KiB of the Entry itself.

### Factoid Transaction

Factoid transactions are similar to Bitcoin transactions, but incorporate some [lessons learned](http://www.reddit.com/r/Bitcoin/comments/2jw5pm/im_gavin_andresen_chief_scientist_at_the_bitcoin/clfp3xj) from Bitcoin.
- They are closer to P2SH style addresses, where the value is sent to the hash of a redeem condition, instead of sent to the redeem condition itself. To redeem value, a datastructure containing public keys, etc should be revealed. This is referred to as the **Redeem Condition Datastructure (RCD)**
- Factoids use Ed25519 with Schnorr signatures.  They have [many benefits](https://ripple.com/uncategorized/curves-with-a-twist/0) over the ECDSA signatures used in Bitcoin.
- TXID does not cover the signature field.  This will limit damaging malleability by attackers without the private key.
- Scripts are not used.  They may be added later, but are not implemented in the first version. Instead of scripts, there are a limited number of valid RCDs which are interpreted.  This is similar to how Bitcoin only has a handful of standard transactions.  Non-standard transactions are not relayed on the Factom P2P network. In Factom, non-standard transactions are undefined.  Adding new transaction types will cause a hard fork of the Factom network.


The transaction ID (TXID) is a double SHA256 (SHA256d) hash of the data from the header through the inputs.  The RCD reveal and signatures are not part of the TXID. A double SHA256 is a SHA256 hash of the SHA256 hash of the covered data.  Stops length extension attacks.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- |
| **Header** | | |
| 1 byte | Version | Version of the transaction type.  Versions above 0 are not relayed. |
| 5 bytes | lockTime | same rules as Bitcoin.  less than 500 million defines the minimum block height this tx can be included in or be rebroadcast.  Greater or equal to 500 million is minimum Unix epoch time with 1 second resolution.  Big endian, so first byte is zero for the next 100 years or so. To disable timelock, set to all zeros. |
| **Outputs** | | |
| varInt_F | Factoid Output Count | This is the quantity of redeemable (Factoid) outputs created.  Maximum allowable number is 16,000. |
| varInt_F | value | (Output 0) The quantity of Factoshis (Factoids * 10^-8) reassigned. |
| 32 bytes | RCD Hash | (Output 0) The double hash (SHA256d) of the Redeem Condition Datastructure (RCD), which must be revealed then satisfied to later use the value as an input |
| varInt_F | value | (Output X) The quantity of Factoshis reassigned. |
| 32 bytes | RCD Hash | (Output X) The double hash of the RCD |
| varInt_F | Entry Credit Purchase Count | This is the quantity of non-redeemable (Entry Credits) outputs created.   Maximum allowable number is 16,000. |
| varInt_F | value | (Purchase 0) The quantity of Factoshis to be turned into ECs. |
| 32 bytes | EC Pubkey | (Purchase 0) The Ed25519 raw public key which is the Entry Credit pubkey.  |
| varInt_F | value | (Purchase X) The quantity of Factoshis to be turned into ECs. |
| 32 bytes | EC Pubkey | (Purchase X) The Ed25519 raw EC public key. |
| **Inputs** | | |
| varInt_F | Input Count | This is the quantity of previous transaction outputs spent.   Maximum allowable number is 16,000. |
| 32 bytes | TXID | (Input 0) This is the previous transaction identifier which is being spent. |
| varInt_F | output index | (Input 0) This is the index of the specified TXID which is being spent. |
| 1 byte | sighash type | (Input 0) Define how the transaction can be reconfigured without resigning. |
| 32 bytes | TXID | (Input X) This is the previous transaction identifier which is being spent. |
| varInt_F | output index | (Input X) This is the index of the specified TXID which is being spent. |
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

This can be considered equivalent to a Bitcoin redeem script behind a P2SH transaction. The first version will only support multisignature addresses.  Type 0 is defined here.  The RCD is hashed twice using SHA256d, to prevent potential length extension attacks.

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

Fees are the difference between the outputs and the inputs.  The fees are [sacrificed](https://blog.ethereum.org/2014/02/01/on-transaction-fees-and-the-fallacy-of-market-based-solutions/).  They are defined by, but not reclaimed by the Federated servers.  The minimum transaction fees are based on the current exchange rate of Factoids to Entry Credits.  The outputs must be less than the inputs by at least the the fee amount at confirmation time.  The minimum fees are the sum of 3 things that cause load on the system:
1. Transaction data size. -- Factoid transactions are charged the same amount as Entry Credits (EC).  The size fees are 1 EC per KiB with a maximum transaction size of 10 KiB.
2. Number of outputs created -- These are data points which potentially need to be tracked far into the future.  They are more expensive to handle, and require a larger sacrifice.  Outputs cost 10 EC per output. A purchase of Entry Credits also requires the 10 EC sized fee to be valid.
3. Number of signatures checked -- These cause expensive computation on all full nodes.  A fee of 1 EC equivalent must be paid for each signature included.

A minimal transaction with 2 inputs and 2 outputs spending single sig outputs would cost the equivalent of 23 Entry Credits.


#### Coinbase Factoid Transaction

The coinbase transaction, like in Bitcoin, is how the servers are paid for their services.  These are new Factoids created by the protocol.  The outputs are allocated in a deterministic fashion based upon the results from the election and which of the Federated servers participated in generating the blocks in the past.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- |
| **Header** | | |
| 1 byte | Version | Version 0 only. |
| 5 bytes | lockTime | disabled, all zeros. |
| **Outputs** | | |
| varInt_F | Factoid Output Count | This is the quantity of redeemable (Factoid) outputs created.  Maximum allowable number is 16,000. |
| varInt_F | value | (Output 0) The quantity of Factoshis (Factoids * 10^-8) assigned. |
| 32 bytes | RCD Hash | (Output 0) The double hash (SHA256d) of the Redeem Condition Datastructure (RCD), which must be revealed then satisfied to later use the value as an input |
| varInt_F | value | (Output X) The quantity of Factoshis assigned. |
| 32 bytes | RCD Hash | (Output X) The double hash of the RCD |
| varInt_F | Entry Credit Purchase Count | Must be zero for the coinbase. |
| **Inputs** | | |
| varInt_F | Input Count | This is the quantity of previous transaction outputs spent.   Must be 1. |
| 32 bytes | Coinbase ID | Coinbase identifier is a placeholder for the previous TXID.  This field must be all zeros for the coinbase. |
| varInt_F | Factoid Block Height | This is a changing seed so that the TXID for this transaction changes even if the outputs do not. |
| 1 byte | sighash placeholder | Must be set to 0 for coinbase. |


### Balance Increase

This datastructure is a pointer to a valid Factoid transaction which purchases Entry Credits. It creates a trigger to increase the Entry Credit balance of a particular EC pubkey. It is derived deterministically from every Factoid output which credits EC keys.

| data | Field Name | Description |
| ----------------- | ---------------- | --------- |
| 32 bytes | EC Public Key | This is the public key which the Factoid transaction has credited. |
| 32 bytes | TXID | This is the transaction ID of the Factoid transaction crediting the above public key. |
| varInt_F | Index | The index in the above Factoid transaction crediting the EC pubkey. |
| varInt_F | NumEC | This is the number of Entry Credits granted to the EC public key based on the current exchange rate in effect. |



## Block Elements

These data structures are constructed of mostly User Elements defined by the Federated servers.

### Directory Block

A Directory Block consists of a header and a body. The body is a series of pairs of ChainIDs and Entry Block Merkle Roots.

| data | Field Name | Description |
| ----------------- | ---------------- | --------- |
| **Header** |  |  |
| 1 byte | Version | Describes the protocol version that this block is made under.  Only valid value is 0. |
| 4 bytes | NetworkID | This is a magic number identifying the main Factom network.  The value for Directory Blocks is 0xFA92E5A1. |
| 32 bytes | BodyMR | This is the Merkle root of the body data which accompanies this block.  It is calculated with SHA256. |
| 32 bytes | PrevKeyMR | Key Merkle root of previous block.  It is the value which is used as a key into databases holding the Directory Block. It is calculated with SHA256. |
| 32 bytes | PrevHash3 | This is a SHA3-256 checksum of the previous Directory Block. It is calculated by hashing the serialized block from the beginning of the header through the end of the body. It is included to doublecheck the previous block if SHA2 is weakened in the future. |
| 4 bytes | DB Height | This the current Directory Block height.  Big endian. |
| 4 bytes | Height Skip Count |  |
| | **signatures, extra data, header size...** |
| 4 bytes | Block Count | This is the number of Entry Blocks that were updated in this block. It is a count of the ChainID:KeyMR pairs.  Big endian. |
| **Body** |  |  |
| 32 bytes | ChainID 0 | This is the ChainID of one Entry Block which was updated during this block time. These ChainID:KeyMR pairs are sorted numerically based on the ChainID.  |
| 32 bytes | KeyMR 0 | This is the Key Merkle root of the Entry Block with ChainID 0 which was created during this Directory Block. |
| 32 bytes | ChainID X | Nth Entry Block ChainID. |
| 32 bytes | KeyMR X | Nth Entry Block KeyMR. |

### Entry Block

An Entry Block is a datastructure which packages references to Entries all sharing a ChainID over a 10 minute period. The Entries are ordered in the Entry Block in the order that they were received by the Federated server. The Entry Blocks form a blockchain for a specific ChainID.

The Entry Block consists of a header and a body.  The body is composed of primarily Entry Hashes with 10 one minute markers distributed throughout the body. 

| data | Field Name | Description |
| ----------------- | ---------------- | --------- |
| **Header** |  |  |
| 32 bytes | ChainID | All the Entries in this Entry Block have this ChainID |
| 32 bytes | BodyMR | This is the Merkle root of the body data which accompanies this block.  It is calculated with SHA256. |
| 32 bytes | PrevKeyMR | Key Merkle root of previous block.  This is the value of this ChainID's previous Entry Block Merkle root which was placed in the Directory Block.  It is the value which is used as a key into databases holding the Entry Block. It is calculated with SHA256. |
| 32 bytes | PrevHash3 | This is a SHA3-256 checksum of the previous Entry Block of this ChainID. It is calculated by hashing the serialized block from the beginning of the header through the end of the body. It is included to doublecheck the previous block if SHA2 is weakened in the future.  First block has a PrevHash3 of 0. |
| 4 bytes | EB Height | This is the sequence which this block is in for this ChainID.  First block is height 0. Big endian. |
| 4 bytes | DB Height | This the Directory Block height which this Entry Block is located in. Big endian. |
| 4 bytes | Entry Count | This is the number of Entry Hashes and time delimiters that the body of this block contains.  Big endian. |
| **Body** |  |  |
| 32 bytes | All objects | A series of 32 byte sized objects arranged in chronological order. |

Time delimiters are 32 byte big endian objects between 1 and 10 (inclusive).  They are inserted in into the Entry Block when a new Federated server yields control of the Chain and an Entry has been acknowledged already.  They are not needed if there is not an Entry to include that minute.  Note, there can be duplicate Entries included in an Entry Block.  If an Entry is paid for twice, it is included twice.  The times are organized when the Federated server saw and acknowledged the Entry.

**Body With 1 Entry at 0:10 into block**
```
520E404C6565F5B204E46BA2972220820192F1B11648DFE128F9BD1D2D147D43
0000000000000000000000000000000000000000000000000000000000000001
```

**Body With 1 Entry at 1:10 into block**
```
520E404C6565F5B204E46BA2972220820192F1B11648DFE128F9BD1D2D147D43
0000000000000000000000000000000000000000000000000000000000000002
```

**Body With 1 Entry at 5:50 into block**
```
520E404C6565F5B204E46BA2972220820192F1B11648DFE128F9BD1D2D147D43
0000000000000000000000000000000000000000000000000000000000000006
```

**Body With 1 Entry at 9:50 into block**
```
520E404C6565F5B204E46BA2972220820192F1B11648DFE128F9BD1D2D147D43
000000000000000000000000000000000000000000000000000000000000000A
```

**Body With 2 Entries: 2:20 and 5:30 into block**
```
520E404C6565F5B204E46BA2972220820192F1B11648DFE128F9BD1D2D147D43
0000000000000000000000000000000000000000000000000000000000000003
69379F5B2047A98AC9EC1726F49AB4E7854C958F070A1CFB222F40A0F49A9BB3
0000000000000000000000000000000000000000000000000000000000000006
```

**Body With 3 Entries: 2:20, 2:40 and 5:30 into block**
```
520E404C6565F5B204E46BA2972220820192F1B11648DFE128F9BD1D2D147D43
69379F5B2047A98AC9EC1726F49AB4E7854C958F070A1CFB222F40A0F49A9BB3
0000000000000000000000000000000000000000000000000000000000000003
D03E315186BFBEBF030E9CBCDA99000A45A536ECF1583D792338FB44D9FB0041
0000000000000000000000000000000000000000000000000000000000000006
```

**Body With 8 Entries: 0:05, 3:40, 3:59, 4:00, 4:01, 4:30, 5:30, 9:59 into block with a duplicate**
```
520E404C6565F5B204E46BA2972220820192F1B11648DFE128F9BD1D2D147D43
0000000000000000000000000000000000000000000000000000000000000001
69379F5B2047A98AC9EC1726F49AB4E7854C958F070A1CFB222F40A0F49A9BB3
D03E315186BFBEBF030E9CBCDA99000A45A536ECF1583D792338FB44D9FB0041
0000000000000000000000000000000000000000000000000000000000000004
6E24E241C65E0623BD705CD968EFDBE1C1A5C1D44F11CDA45F23DA24E29DB0E5
EEBF7804DA84E4F8E9330982808225649751EE5CC6CA20281DBE6983FE8E435F
2F1972E07F61DAEC1002647CE5B3CE4D1B031D7D989E761252D6F248C2675D5B
0000000000000000000000000000000000000000000000000000000000000005
3F84CCE967052E85C3CF2D671C2433DC4899226BB99A67D6BFE4AEB9E938B7CC
0000000000000000000000000000000000000000000000000000000000000006
3F84CCE967052E85C3CF2D671C2433DC4899226BB99A67D6BFE4AEB9E938B7CC
000000000000000000000000000000000000000000000000000000000000000A
```


### Entry Credit Block

An Entry Credit (EC) Block is a datastructure which packages Chain Commits, Entry Commits, and EC balance increases over a 10 minute period. The Entries are ordered in the Entry Block in the order that they were received by each Federated server. All the Federated servers contribute to the building of the EC Block.

The Entry Credit Block consists of a header and a body.  The body is composed of primarily Commits and balance increases with minute markers and server markers distributed throughout the body.

| data | Field Name | Description |
| ----------------- | ---------------- | --------- |
| **Header** |  |  |
| 32 bytes | EC ChainID | The EC ChainID is predefined as 0x000000000000000000000000000000000000000000000000000000000000000c. |
| 32 bytes | BodyHash | This is the SHA256 hash of the serialized body data which accompanies this block. |
| 32 bytes | PrevKeyMR | Key Merkle root of previous block.  This is the value of the previous EC Block's key which was placed in the previous Directory Block.  It is the value which is used as a key into databases holding the EC Block. It is calculated with SHA256. |
| 32 bytes | PrevHash3 | This is a SHA3-256 checksum of the previous Entry Block of this ChainID. It is calculated by hashing the serialized block from the beginning of the header through the end of the body. It is included to doublecheck the previous block if SHA2 is weakened in the future.  Genesis block has a PrevHash3 of 0. |
| 4 bytes | DB Height | This the Directory Block height which this block is located in. Big endian. |
| 32 bytes | SegmentsMR | Later when the DHT is implemented, this field will allow for the body to be chopped into many pieces for parallel download.  Currently it is set to all zeros. |
| 32 bytes | Balance Commitment | This will be a Merkle root committing to the current balances of each public key.  Currently set to all zeros. |
| 8 bytes | Body Size | This is the number bytes the body of this block contains.  Big endian. |
| **Body** |  |  |
| variable | All objects | A series of variable sized objects arranged in chronological order.  Each object is prepended with an ECID byte. |


##### ECID Bytes

Entry Credit Identifier (ECID) bytes are single bytes which specify how to interpret the following data. It specifies the type, and the type determines how long the data is.

| Binary | Name | Description |
| ----------------- | ---------------- | --------- |
| 0x00 | Server Index Number | The following data was acknowledged by the server with the specified Index.  This byte is followed by another byte which signifies the server's order. |
| 0x01 | Minute Number | The preceding data was acknowledged before the minute specified. 1 byte follows the Minute Number. |
| 0x02 | Chain Commit | The following data is a Chain Commit. The following 200 bytes are a Chain Commit. |
| 0x03 | Entry Commit | The following data is an Entry Commit. The following 136 bytes are an Entry Commit. |
| 0x04 | Balance Increase | The following data is a balance increase. The following 66 - 82 bytes are a Balance Increase. |


### Components

These are some custom datastructures for Factom

#### KeyMR

A Key Merkle Root is a datastructure which allows fast validation of a header and also allows Merkle proofs to be built to the body data elements.

First a Merkle tree is constructed of all the body elements. It is called the BodyMR.  This is very similar to how all Bitcoin transactions can be proven with a Merkle root in the header.

The BodyMR is included in the header, among other things. The serialized header is then hashed.  The hashed header is combined with the BodyMR and hashed. This creates the KeyMR. With only the KeyMR, when a header is produced by a peer, the header can be validated with 2 hashes.

For the EC block, KeyMR is a hash of the header concatenated with the BodyHash.  The EC block does not have a Merkle root of the body data, but the KeyMR still can prove the header.

