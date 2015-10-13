Factom Data Structures
==========

This document describes the byte level detail of the Factom data structures.

Unless otherwise specified, Data is interpreted as big-endian.  Exceptions include ed25519 R and S values, are standardized as [little endian](https://tools.ietf.org/html/draft-josefsson-eddsa-ed25519-03).

## Building Blocks

This describes the low level minutia for common data structures.

### Chain Name

A Chain Name is a value to uniquely identify a Chain. It can be a random number, a string of text, a public key, or hash of some private directory path.  The choice of Chain Name is left up to the user. The Chain Name can be specified with multiple sequential byte strings.  They are treated as different segments of data instead of concatenated, to differentiate trailing bytes of one segment from leading bytes of the next segment.

The individual segment length are limited by how many bytes can fit in an Entry (approx 10 KiB).  Each Chain Name element must be at least 1 byte long. A Chain Name with no elements is a special case where the ChainID is the hash of a null string `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.


### ChainID

A ChainID is a series of SHA256 hashes of Chain Name segments.  The ChainID is 32 bytes long. The ChainID must be the hash of *something* to only have opaque data in the higher level block structures.

The algorithm hashes each segment of the Chain Name.  Those hashes are concatenated, and are hashed again into a single 32 byte value.

Getting a ChainID from a single segment Chain Name would be equivalent of hashing the Chain Name twice.

ChainID = SHA256( SHA256(Name[0]) | SHA256(Name[1]) | ... | SHA256(Name[X]) )


## User Elements

These data structures are composed by the Users.

### Entry

An Entry is the element which carries user data. An Entry Reveal is essentially this data.

The External IDs are a part of the Entry which have byte sequence lengths that must be known by Factom.  The first Entry in a Factom Chain uses the External IDs to define the Chain Name.  Other Entries can use the External IDs as their application dictates.

To be valid, the External IDs are parsed and the end of the last element must match the defined length for the External IDs as defined in the header.

External IDs (ExtID) are intended to provide any sort of tagging information for Entries that applications may find useful.  Keys to databases are likely to be a common use.  External IDs are simply data to Factom, and are not used in the consensus algorithm after the first Entry.

External IDs and Content is not checked for validity, or sanitized, as it is only viewed as binary data.


| data | Field Name | Description |
| ----------------- | ---------------- | --------------- | 
| **Header** |  | |
| varInt_F | Version | starts at 0.  Higher numbers are currently rejected. Can safely be coded using 1 byte for the first 127 versions. |
| 32 bytes | ChainID | This is the Chain which the author wants this Entry to go into. |
| 2 bytes | ExtIDs Size | Describes how many bytes required for the set of External IDs for this Entry.  Must be less than or equal to the Payload size.  Big endian. |
| **Payload** | | This is the data between the end of the Header and the end of the Content. |
| **External IDs** |  | This section is only interpreted and enforced if the External ID Size is greater than zero. |
| 2 bytes | ExtID element 0 length | This is the number of the following bytes to be interpreted as an External ID element.  Cannot be 0 length. |
| variable | ExtID 0 | This is the data for the first External ID. |
| 2 bytes | ExtID X | Size of the X External ID  |
| variable | ExtID X data | This is the Xth element.  The last byte of the last element must fall on the last byte specified ExtIDs Size in the header. |
| **Content** | | |
| variable | Entry Data | This is the unstructured part of the Entry.  It is all user specified data. |

Minimum empty Entry length: 35 bytes

Minimum empty first Entry with Chain Name of 1 byte: 38 bytes

Maximum Entry size: 10KiB + 35 bytes = 10275 bytes

Typical size recording the hash of a file with 200 letters of ExtID metadata: 1+32+2+2+200+32 = 269 bytes

example size of something similar to an Omni(MSC) transaction, assuming 500 bytes [per transaction](https://blockchain.info/address/1EXoDusjGwvnjZUyKkxZ4UHEf77z6A5S4P):
1+32+2+500 = 535 bytes

Example Entry with a Chain Name of 'test', spaces added for clarity:
As first Entry:
00 954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f4 0006 0004 74657374 5061796c6f616448657265

As regular Entry without ExtID:
00 954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f4 0000 5061796c6f616448657265

As regular Entry with ExtID of 'Hello' in 'test' chain:
00 954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f4 0007 0005 48656c6c6f 5061796c6f616448657265


### Entry Hash

The Entry Hash is a 32 byte identifier unique to specific Entry data.  It is referenced in the Entry Block body as well as in the Entry Commit.  In a desire to maintain long term resistance to [second-preimage attacks](http://en.wikipedia.org/wiki/Preimage_attack) in SHA2, as well as preventing length extension attacks, SHA512 is included in the Entry Hash generation process. For a future attacker to come up with a dishonest piece of data, they would need contend with many extra hashing rounds with a combined SHA512 and SHA256 in series. This operation is in contrast to the SHA256d, which does one hash over the SHA256 of the protected data. To brute force a SHA256d collision, modifying data at the end can only require 128 rounds. Prepending the SHA512 requires finding collision to iterate over the entire Entry more than once per attempt.

Straight SHA256 is used for Merkle roots due to anticipated CPU hardware acceleration, as well as being double-checkable by the serial hash. Entries (unlike blocks) do not have two independent ways of hashing protecting data, so this is why the hashing is more complex.

To calculate the Entry Hash, first the Entry is serialized and passed into a SHA512 function.  The 64 bytes output from the SHA512 function is prepended to the serialized Entry.  The Entry+prependage are then fed through a SHA256 function, and the output of that is the Entry Hash.

Using the above Entry as an example.

00954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f400005061796c6f616448657265
is passed into SHA512 and that gives: 0ba3c58955c69b02aa675d8ff15b505a48335fdc9a06354ba55e4149f77b69835c8c2b7002ca3b09202846d03626bada6b408fa1374f22dc396c64d9a3980ed3

The Entry is appended to the SHA512 result to make 
0ba3c58955c69b02aa675d8ff15b505a48335fdc9a06354ba55e4149f77b69835c8c2b7002ca3b09202846d03626bada6b408fa1374f22dc396c64d9a3980ed300954d5a49fd70d9b8bcdb35d252267829957f7ef7fa6c74f88419bdc5e82209f400005061796c6f616448657265
which is then SHA256 hashed to make an Entry Hash of:
72177d733dcd0492066b79c5f3e417aef7f22909674f7dc351ca13b04742bb91


### Entry Commit

An Entry Commit is a payment for a specific Entry. It deducts a balance held by a specific public key in the amount specified. They are collected into the Entry Credit chain as proof that a balance should be decremented.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- |
| **Header** |  | |
| varInt_F | Version | starts at 0.  Higher numbers are currently rejected.  Can safely be coded using 1 byte for the first 127 versions. |
| 6 bytes | milliTimestamp | This is a timestamp that is user defined.  It is a unique value per payment. This is the number of milliseconds since 1970 epoch. |
| 32 bytes | Entry Hash | This is the SHA512+256 descriptor of the Entry to be paid for. |
| 1 byte | Number of Entry Credits | This is the number of Entry Credits which will be deducted from the balance of the public key. Any values above 10 are invalid. |
| 32 bytes | Pubkey | This is the Entry Credit public key which will have the balance reduced. It is the ed25519 A value. |
| 64 bytes | Signature | This is a signature of this Entry Commit by the pubkey.  Parts ordered R then S. Signature covers from Version through 'Number of Entry Credits' |

The Entry Commit is only valid for 12 hours before and after the milliTimestamp. Since Entry Credits are balance based, replay attacks can reduce balances. Also a user can pay for the same Entry twice, and have two copies in Factom. Since a P2P network is used, the payments would need to be differentiated. The payments would be differentiated by public key and the time specified. This puts a limit of 1000 per second on any individual Entry Credit public key per duplicate Entry. The milliTimestamp also helps the network protect itself.  Adding the time element allows peers to automatically reject payments beyond 12 hours plus or minus. This means they must check for duplicates only over a rolling one day period. 

The number of Entry Credits is based on the Payload size. Cost is 1 EC per partial KiB. Empty Entries cost 1 EC.


### Chain Commit

A Chain Commit is a simultaneous payment for a specific Entry and a payment to allow a new Chain to be created. It deducts a balance held by a specific EC public key in the amount specified. They are collected into the Entry Credit chain as proof that a balance should be decremented.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- |
| varInt_F | Version | starts at 0.  Higher numbers are currently rejected. Can safely be coded using 1 byte for the first 127 versions.|
| 6 bytes | milliTimestamp | This is a timestamp that is user defined.  It is a unique value per payment. This is the number of milliseconds since 1970 epoch. |
| 32 bytes | ChainID Hash | This is a double hash (SHA256d) of the ChainID which the Entry is in. |
| 32 bytes | Commit Weld | SHA256(SHA256(Entry Hash <code>&#124;</code> ChainID)) This is the double hash (SHA256d) of the Entry Hash concatenated with the ChainID. |
| 32 bytes | Entry Hash | This is the SHA512+256 descriptor of the Entry to be the first in the Chain. |
| 1 byte | Number of Entry Credits | This is the number of Entry Credits which will be deducted from the balance of the public key. Any values above 20 or below 11 are invalid. |
| 32 bytes | Pubkey | This is the Entry Credit public key which will have the balance reduced. |
| 64 bytes | Signature | This is a signature of this Chain Commit by the pubkey.  Parts ordered R then S. Signature covers from Version through 'Number of Entry Credits' |

The Federated server will keep track of the Chain Commits based on ChainID Hash. The Federated servers keep track of the Chain Commits they receive.  When the first Entry is received, it will reveal the ChainID.  If the ChainID was a secret, then it now can be compared against all the possible Chain Commits claiming to pay for Entries of a certain ChainID. Once the ChainID is revealed, the ChainID hash and the 'Entry Hash + ChainID' fields can be compared to see if they match and form valid hashes. If they do not match, that Chain Commit is invalid.  If they do match, then the first one to be acknowledged gets accepted as the first Entry.  They maintain exclusivity for 1 hour for each ChainID hash after an acknowledgement.  The commit itself must be within 12 hours +/- of the milliTimestamp.

A prudent user will not broadcast their first Entry until the Federated server acknowledges the Chain Commit.  If they do not wait, a peer on the P2P network can put their Entry as the first one in that Chain.

Chain Commits cost 10 Entry Credits to create the Chain, plus the fee per KiB of the Entry itself.

### Factoid Transaction

Factoid transactions are similar to Bitcoin transactions, but incorporate some [lessons learned](http://www.reddit.com/r/Bitcoin/comments/2jw5pm/im_gavin_andresen_chief_scientist_at_the_bitcoin/clfp3xj) from Bitcoin.
- They are closer to P2SH style addresses, where the value is sent to the hash of a redeem condition, instead of sent to the redeem condition itself. To redeem value, a datastructure containing public keys, etc should be revealed. This is referred to as the **Redeem Condition Datastructure (RCD)**
- Factoids use Ed25519 with Schnorr signatures.  They have [many benefits](https://ripple.com/uncategorized/curves-with-a-twist/0) over the ECDSA signatures used in Bitcoin.
- The signatures are enforced to be [canonical](https://github.com/FactomProject/ed25519/blob/master/ed25519.go#L143).  This will limit malleability by attackers without the private key.
- Scripts are not used.  They may be added later, but are not implemented in the first version. Instead of scripts, there are a limited number of valid RCDs which are interpreted.  This is similar to how Bitcoin only has a handful of standard transactions.  Non-standard transactions are not relayed on the Factom P2P network. In Factom, non-standard transactions are undefined.  Adding new transaction types will cause a hard fork of the Factom network.

Factoids are balanced based and have all the value combined to a single amount.  The address is a hash of a Redeem Condition Datastructure (RCD). The Factoid transaction is denominated in Factoshis, which is 10^-8 Factoids.


| data | Field Name | Description |
| ----------------- | ---------------- | --------------- |
| **Header** | | |
| varInt_F | Version | Version of the transaction type.  Versions other than 2 are not relayed. Can safely be coded using 1 byte for the first 127 versions. |
| 6 bytes | milliTimestamp | Same rules as the Entry Commits. This is a unique value per transaction.  This field is the number of milliseconds since 1970 epoch.  The Factoid transaction is valid for 24 hours before and after this time. |
| 1 byte | Input Count | This is how many Factoid addresses are being spent from in this transaction. |
| 1 byte | Factoid Output Count | This is how many Factoid addresses are being spent to in this transaction. |
| 1 byte | Entry Credit Purchase Count | This is how many Entry Credit addresses are being spent to in this transaction. |
| **Inputs** | | |
| varInt_F | Value | (Input 0) This is how much the Factoshi balance of Input 0 will be decreased by. |
| 32 bytes | Factoid Address | (Input 0) This is an RCD hash which previously had value assigned to it. |
| varInt_F | Value | (Input X) This is how much the Factoshi balance of Input X will be decreased by. |
| 32 bytes | Factoid Address | (Input X) This is an RCD hash which previously had value assigned to it. |
| **Factoid Outputs** | | |
| varInt_F | Value | (Output 0) This is how much the Output 0 Factoshi balance will be increased by. |
| 32 bytes | Factoid Address | (Output 0) This is an RCD hash which will have its balance increased. |
| varInt_F | Value | (Output X) This is how much the Output X Factoshi balance will be increased by. |
| 32 bytes | Factoid Address | (Output X) This is an RCD hash which will have its balance increased. |
| **Entry Credit Purchase** | | |
| varInt_F | Value | (Purchase 0) This many Factoshis worth of ECs will be credited to the Entry Credit public key 0. |
| 32 bytes | EC Pubkey | (Purchase 0) This is Entry Credit public key that will have its balance increased. |
| varInt_F | Value | (Purchase X) This many Factoshis worth of ECs will be credited to the Entry Credit public key X. |
| 32 bytes | EC Pubkey | (Purchase X) This is Entry Credit public key that will have its balance increased. |
| **Redeem Condition Datastructure (RCD) Reveal / Signature Section** | | |
| variable | RCD 0 | First RCD.  It hashes to input 0. The length is dependent on the RCD type, which is in the first byte. There are as many RCDs as there are inputs. |
| variable | Signaure 0 | This is the data needed to satisfy RCD 0. It is a singature for type 1, but might be other types of data for later RCD types.  Its length is dependent on the RCD type. |
| variable | RCD X | Xth RCD.  It hashes to input X. |
| variable | Signaure X | This is the data needed to satisfy RCD X. |

The transaction is protected against replay attacks because the servers do not allow duplicate transactions with the same timestamp if they share the same inputs and outputs.  Changing any of those fields would also break the signature.

The signatures cover the Header, Inputs, Outputs, and Purchases.  The RCD is protected from tampering because the signed inputs specify only one possible RCD.

##### Redeem Condition Datastructure (RCD)

This can be considered equivalent to a Bitcoin redeem script behind a P2SH transaction. The first version will only support single signature addresses.  Type 1 is defined here.  The RCD is hashed twice using SHA256d, to prevent potential length extension attacks. Multisignature RCDs are planned for release soon.

**RCD Type 1**:

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- |
| varInt_F | Type | The RCD type.  This specifies how the datastructure should be interpreted.  Type 1 is the only currently valid type. Can safely be coded using 1 byte for the first 127 types. |
| 32 bytes | Pubkey 0 | The raw ed25519 public key. |


Note: For the token sale, a raw Ed25519 pubkey is included in an OP_RETURN output along with the payment to the sale multisig address.  The the genesis block will contain a transaction which outputs to many 1 of 1 addresses.  There will be an output for each of the Bitcoin payments' specified pubkeys.  The addresses will be derived from the exposed pubkeys. Payments with the same pubkey will have their balances combined.

Some later RCD types will be added.  Output types supporting [atomic cross](https://en.bitcoin.it/wiki/Atomic_cross-chain_trading) chain swaps and [time locking](https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki) outputs are desirable.  Output scripts are also useful and desirable, but can open security holes.  They are not critical for the first release of Factom, so we will implement them later. This would give us the ability to make conditional outputs (IF, AND, OR, etc).  Nesting is also desirable.  This would give multisig within a multisig transaction.  Implementing scripts will give all the intermediate RCD types, so possibly going directly to scripts can bypass a special atomic cross chain swap, etc.

Ed25519 allows for threshold multisig in a [single signature](http://crypto.stackexchange.com/questions/20581/does-ed25519-support-cryptographic-threshold-signatures), but that cryptography will have to come later. This does have the disadvantage against Bitcoin style, multiple individual key checking though. When a signature is made, this method does not show who in the group made the signature.

##### Fees

Fees are the difference between the outputs and the inputs.  The fees are [sacrificed](https://blog.ethereum.org/2014/02/01/on-transaction-fees-and-the-fallacy-of-market-based-solutions/).  They are defined by, but not reclaimed by the Federated servers.  The minimum transaction fees are based on the current exchange rate of Factoids to Entry Credits.  The outputs must be less than the inputs by at least the the fee amount at confirmation time.  The minimum fees are the sum of 3 things that cause load on the system:

1. Transaction data size. -- Factoid transactions are charged the same amount as Entry Credits (EC).  The size fees are 1 EC per KiB with a maximum transaction size of 10 KiB.
2. Number of outputs created -- These are data points which potentially need to be tracked far into the future.  They are more expensive to handle, and require a larger sacrifice.  Outputs cost 10 EC per output. A purchase of Entry Credits also requires the 10 EC sized fee to be valid.
3. Number of signatures checked -- These cause expensive computation on all full nodes.  A fee of 1 EC equivalent must be paid for each signature included.

A minimal transaction buying Entry Credits or sending Factoids to one address from a single sig address would cost the equivalent of 12 Entry Credits.


#### Coinbase Factoid Transaction

The coinbase transaction, like in Bitcoin, is how the servers are paid for their services.  These are new Factoids created by the protocol.  The outputs are allocated in a deterministic fashion based upon the results from the election and which of the Federated servers participated in generating the blocks in the past.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- |
| **Header** | | |
| varInt_F | Version | Determined by Federated Servers, version 2 for now. |
| 6 bytes | milliTimestamp | The time is set as the Directory Block timestamp. |
| 1 byte | Input Count | Always zero. coinbase has no inputs. As such, it has no RCD reveals or signatures. |
| 1 byte | Factoid Output Count | This is how many Factoid addresses are being spent to in this transaction. It is coordinated among the Federated Servers. |
| 1 byte | Entry Credit Purchase Count | Always zero. Federated Servers do not need to buy entry credits in the coinbase. |
| **Factoid Outputs** | | |
| varInt_F | Value | (Output 0) This is how much the Output 0 Factoshi balance will be increased by. |
| 32 bytes | Factoid Address | (Output 0) This is an RCD hash which will have its balance increased. |
| varInt_F | Value | (Output X) This is how much the Output X Factoshi balance will be increased by. |
| 32 bytes | Factoid Address | (Output X) This is an RCD hash which will have its balance increased. |


#### Balance Increase

This datastructure is a pointer to a valid Factoid transaction which purchases Entry Credits. It creates a trigger to increase the Entry Credit balance of a particular EC pubkey. It is derived deterministically from every Factoid output which credits EC keys.

| data | Field Name | Description |
| ----------------- | ---------------- | --------- |
| 32 bytes | EC Public Key | This is the public key which the Factoid transaction has credited. |
| 32 bytes | TXID | This is the transaction ID of the Factoid transaction crediting the above public key. |
| varInt_F | Index | The index in the above Factoid transaction's Purchase field crediting the EC pubkey. |
| varInt_F | NumEC | This is the number of Entry Credits granted to the EC public key based on the current exchange rate in effect. |


### Human Readable Addresses

Factoid and Entry Credit addresses are modeled after Bitcoin addresses.  They have an identifiable prefix and a checksum to prevent typos.  See [base58check](https://en.bitcoin.it/wiki/Base58Check_encoding) encoding.  Instead of Bitcoin's 160 bits, they use 256 bits.  They also use 2 bytes for the version byte instead of Bitcoin's 1 byte.

#### Factoid Address

Factoids are sent to an RCD Hash.  Inside the computer, the RCD hash is represented as a 32 byte number.  The user sees Factoid addresses as a 52 character string starting with FA.

To convert a 32 byte RCD Hash to a Factoid address follow these steps:

1. Concatenate 0x5fb1 and the RCD Hash bytewise
  * `5fb10000000000000000000000000000000000000000000000000000000000000000` using zeros as a substitute RCD Hash
2. Take the SHA256d of the above data.  Append the first 4 bytes of this SHA256d to the end of the above value bytewise.
  * `5fb10000000000000000000000000000000000000000000000000000000000000000d48a8e32`
3. Convert the above value from base 256 to base 58.  Use standard Bitcoin base58 encoding to display the number.
  * `FA1y5ZGuHSLmf2TqNf6hVMkPiNGyQpQDTFJvDLRkKQaoPo4bmbgu`

Factoid addresses will range between `FA1y5ZGuHSLmf2TqNf6hVMkPiNGyQpQDTFJvDLRkKQaoPo4bmbgu` and `FA3upjWMKHmStAHR5ZgKVK4zVHPb8U74L2wzKaaSDQEonHajiLeq` representing all zeros and all ones.

#### Entry Credit Address

Entry Credits are redeemed to an Ed25519 raw public key.  Inside the computer, the pubkey is represented as a 32 byte number.  The user sees Entry Credit addresses as a 52 character string starting with EC.

To convert a 32 byte pubkey to an Entry Credit address follow these steps:

1. Concatenate 592a and the pubkey bytewise
  * `592a0000000000000000000000000000000000000000000000000000000000000000` using zeros as a substitute pubkey
2. Take the SHA256d of the above data.  Append the first 4 bytes of this SHA256d to the end of the above value bytewise.
  * `592a00000000000000000000000000000000000000000000000000000000000000003cf4595f`
3. Convert the above value from base 256 to base 58.  Use standard Bitcoin base58 encoding to display the number.
  * `EC1m9mouvUQeEidmqpUYpYtXg8fvTYi6GNHaKg8KMLbdMBrFfmUa`

Entry Credit addresses will range between `EC1m9mouvUQeEidmqpUYpYtXg8fvTYi6GNHaKg8KMLbdMBrFfmUa` and `EC3htx3MxKqKTrTMYj4ApWD8T3nYBCQw99veRvH1FLFdjgN6GuNK` representing all zeros and all ones.


#### Private Keys

Private keys for Factoids and Entry Credits follow a similar pattern.  They start with Fs and Es, with the s standing for secret.

##### Factoid Private Keys

Single signature private keys are represented in human readable form using the same base58check as the public keys.  The only difference is the prefix bytes.  The Factoid private key prefix is `0x6478`.

Human readable Factoid private keys will range between `Fs1KWJrpLdfucvmYwN2nWrwepLn8ercpMbzXshd1g8zyhKXLVLWj` and `Fs3GFV6GNV6ar4b8eGcQWpGFbFtkNWKfEPdbywmha8ez5p7XMJyk` representing all zeros and all ones.

##### Entry Credit Private Keys

Single signature private keys are represented in human readable form using the same base58check as the public keys.  The only difference is the prefix bytes.  The Entry Credit private key prefix is `0x5db6`.

Human readable Entry Credit private keys will range between `Es2Rf7iM6PdsqfYCo3D1tnAR65SkLENyWJG1deUzpRMQmbh9F3eG` and `Es4NQHwo8F4Z4oMnVwndtjV1rzZN3t5pP5u5jtdgiR1RA6FH4Tmc` representing all zeros and all ones.
 
## Block Elements

These data structures are constructed of mostly User Elements defined by the Federated servers.

### Directory Block

A Directory Block consists of a header and a body. The body is a series of pairs of ChainIDs and Entry Block Merkle Roots.  The Body and BodyMR are derived from iterating the process lists generated by the Federated servers over the last 10 minutes.

| data | Field Name | Description |
| ----------------- | ---------------- | --------- |
| **Header** |  |  |
| varInt_F | Version | Describes the protocol version that this block is made under.  Only valid value is 0. Can safely be coded using 1 byte for the first 127 versions. |
| 4 bytes | NetworkID | This is a magic number identifying the main Factom network.  The value for Directory Blocks is 0xFA92E5A1. |
| 32 bytes | BodyMR | This is the Merkle root of the body data which accompanies this block.  It is calculated with SHA256. |
| 32 bytes | PrevKeyMR | Key Merkle root of previous block.  It is the value which is used as a key into databases holding the Directory Block. It is calculated with SHA256. |
| 32 bytes | PrevFullHash | This is a SHA256 checksum of the previous Directory Block. It is calculated by hashing the serialized block from the beginning of the header through the end of the body. It is included to allow simplified client verification without building a Merkle tree and to doublecheck the previous block if SHA2 is weakened in the future. |
| 4 bytes | Timestamp | This the time when the block is opened.  Blocks start on 10 minute marks based on UTC (ie 12:00, 12:10, 12:20).  The data in this field is POSIX time, counting the number of minutes since epoch in 1970. |
| 4 bytes | DB Height | The Directory Block height is the sequence it appears in the blockchain. Starts at zero. |
| 4 bytes | Block Count | This is the number of Entry Blocks that were updated in this block. It is a count of the ChainID:Key pairs. Inclusive of the special blocks. Big endian. |
| **Body** |  |  |
| 32 bytes | Admin Block ChainID | Indication the next item is the serial hash of the Admin Block. |
| 32 bytes | Admin Block Hash | This is the serial hash of the Admin Block generated during this time period. |
| 32 bytes | Entry Credit Block ChainID | Indication the next item belongs to the Entry Credit Block. |
| 32 bytes | Entry Credit Block HeaderHash | This is the serial hash of the Entry Credit Block Header generated during this time period. |
| 32 bytes | Factoid Block ChainID | Indication the next item belongs to the Factoid Block. |
| 32 bytes | Factoid Block KeyMR | This is the KeyMR of the Factoid Block generated during this time period. |
| 32 bytes | ChainID 0 | This is the ChainID of one Entry Block which was updated during this block time. These ChainID:KeyMR pairs are sorted numerically based on the ChainID.  
| 32 bytes | KeyMR 0 | This is the Key Merkle Root of the Entry Block with ChainID 0 which was created during this Directory Block. |
| 32 bytes | ChainID N | Nth Entry Block ChainID. |
| 32 bytes | KeyMR N | Nth Entry Block KeyMR. |

Note about the Timestamp: This timestamp differs from Bitcoin, as it signifies the opening rather than the closing of a block. All the lower level blocks have minute markers in them, signifying how many full minutes after opening that an Entry was seen. If block creation starts in the middle of a 10 minute window, it will still show being opened a the beginning of the window, but all the Entries will have minute markers indicating they were seen at the correct time.

### Administrative Block

This is a special block which accompanies this Directory Block. It contains the signatures and organizational data needed to validate previous and future Directory Blocks.  A hash of this block is included in the DB body.  It appears there with a pair of the Admin ChainID:SHA256 of the block.

| data | Field Name | Description |
| ----------------- | ---------------- | --------- |
| **Header** |  |  |
| 32 bytes | Admin ChainID | The Admin ChainID is predefined as 0x000000000000000000000000000000000000000000000000000000000000000a. |
| 32 bytes | PrevFullHash | This is the top 256 bits of a SHA512 checksum (SHA512[:256]) of the previous Admin Block. It is calculated by hashing the previous serialized Admin block. It is included to doublecheck the previous block if SHA2 is weakened in the future.  First block has a PrevFullHash of 0. |
| 4 bytes | DB Height | This is the Directory Block height which this Admin Block is located in. Big endian. |
| varInt_F | Header Expansion Size | This is the number bytes taken up by the Header Expansion area. Set at zero for now. |
| Variable | Header Expansion Area | This is a field which can be defined and expanded in the future. It is good for things that can be derived deterministically by all the Federated servers when iterating the process lists. One planned feature to go in this field is a Chain Head Commitment. This would be a Merkle root of ChainIDs with their current heads.  This would allow a peer to demonstrate to a light client that the Chain head being offered is the current chain head as defined by the Federated servers. |
| 4 bytes | Message Count | This is the number of Admin Messages and time delimiters that the body of this block contains.  Big endian. |
| 4 bytes | Body Size | This is the number of bytes the body of this block contains.  Big endian. |
| **Body** |  |  |
| variable | All objects | A series of variable sized objects and timestamps arranged in chronological order.  Each object is prepended with an AdminID byte. Objects in this field (other than the minute number) have been sent over the network and were included in the process list of the Federated Server handling the Admin block for that minute. |


##### AdminID Bytes

Administrative Identifier (AdminID) bytes are single bytes which specify how to interpret the following data. It specifies the type, and the type determines how to interpret subsequent bytes.

| Binary | Name | Data Bytes | Description |
| ----------------- | ---------------- | ------- | --------- |
| 0x00 | Minute Number | 1 byte | The preceding data was acknowledged before the minute specified. 1 byte follows the Minute Number. |
| 0x01 | DB Signature | 128 bytes | The following data is a signature of the preceding Directory Block header. The signature consists of the servers 32 byte identity ChainID, a 32 byte Ed25519 public key in that identity and a 64 byte signature of the previous Directory Block's header. |
| 0x02 | Reveal Matryoshka Hash | 64 bytes | This is the latest M-hash reveal to be considered for determining server priority in subsequent blocks. Following this byte are 32 bytes specifying the identity ChainID and 32 bytes for the M-hash reveal itself. |
| 0x03 | Add/Replace Matryoshka Hash | 64 bytes | This is a command which adds or replaces the current M-hash for the specified identity with this new M-hash. Following this byte are 32 bytes specifying the identity ChainID and 32 bytes for the new M-hash itself. This data is replicated from the server's identity chain. |
| 0x04 | Increase Server Count | 1 byte | The server count is incremented by the amount encoded in a following single byte. |
| 0x05 | Add Federated Server | 32 bytes | The following 32 bytes are the ChainID of the Federated server which is added to the pool. |
| 0x06 | Remove Federated Server | 32 bytes | The following 32 bytes are the ChainID of the Federated server which is removed from the pool. All public keys associated with it are removed as well. |
| 0x07 | Add Federated Server Signing Key | 65 bytes | This adds an Ed25519 public key to the authority set.  First 32 bytes are the server's identity ChainID.  Next byte is the key priority. Next 32 bytes are the public key itself.  If the specified priority for the server already exists, this replaces the old one. |
| 0x08 | Add Federated Server Bitcoin Anchor Key | 66 bytes | This adds a Bitcoin public key hash to the authority set.  First 32 bytes are the server's identity ChainID.  Next byte is the key priority. Next byte is 0=P2PKH 1=P2SH. Next 20 bytes are the HASH160 of ECDSA public key.  If the specified priority for the server already exists, this replaces the old one. |


### Entry Credit Block

An Entry Credit (EC) Block is a datastructure which packages Chain Commits, Entry Commits, and EC balance increases over a 10 minute period. The Entries are ordered in the Entry Block in the order that they were received by each Federated server. All the Federated servers contribute to the building of the EC Block.

The Entry Credit Block consists of a header and a body.  The body is composed of primarily Commits and balance increases with minute markers and server markers distributed throughout the body.

| data | Field Name | Description |
| ----------------- | ---------------- | --------- |
| **Header** |  |  |
| 32 bytes | EC ChainID | The EC ChainID is predefined as 0x000000000000000000000000000000000000000000000000000000000000000c. |
| 32 bytes | BodyHash | This is the SHA256 hash of the serialized body data which accompanies this block. |
| 32 bytes | PrevHeaderHash | This is the key to the previous block. It is a SHA256 hash of the serialized header of the previous block.  This is the value of the previous EC Block's key which was placed in the previous Directory Block.  It is the value which is used as a key into databases holding the EC Block. |
| 32 bytes | PrevFullHash | This is a SHA256 checksum of the entire previous Entry Block. It is calculated by hashing the serialized block from the beginning of the header through the end of the body. It is included to doublecheck the previous block if SHA2 is weakened in the future.  Genesis block has a PrevFullHash of 0. |
| 4 bytes | DB Height | This the Directory Block height which this block is located in. Big endian. |
| varInt_F | Header Expansion Size | This is the number bytes taken up by the Header Expansion area. Set at zero for now. |
| Variable | Header Expansion Area | This is a field which can be defined and expanded in the future. It is good for things that can be derived deterministically by all the Federated servers when iterating the process lists. Two features are planned. One is SegmentsMR, which will allow the Body to be chopped into small pieces for parallel download and validation. Another is Balance Commitment, where there is a Merkle root of pairing each public key to a balance. |
| 8 bytes | Object Count | This is the number of objects this block contains.  Big endian. |
| 8 bytes | Body Size | This is the number of bytes the body of this block contains.  Big endian. |
| **Body** |  |  |
| variable | All objects | A series of variable sized objects arranged in chronological order.  Each object is prepended with an ECID byte. |


##### ECID Bytes

Entry Credit Identifier (ECID) bytes are single bytes which specify how to interpret the following data. It specifies the type, and the type determines how to interpret subsequent bytes.

| Binary | Name | Description |
| ----------------- | ---------------- | --------- |
| 0x00 | Server Index Number | The following data was acknowledged by the server with the specified Index.  This byte is followed by another byte which signifies the server's order. |
| 0x01 | Minute Number | The preceding data was acknowledged before the minute specified. 1 byte follows the Minute Number. |
| 0x02 | Chain Commit | The following data is a Chain Commit. The following 200 bytes are a Chain Commit. |
| 0x03 | Entry Commit | The following data is an Entry Commit. The following 136 bytes are an Entry Commit. |
| 0x04 | Balance Increase | The following data is a balance increase. The following 66 - 82 bytes are a Balance Increase. |


### Factoid Block

Factoid Block is a datastructure which packages Factoid transactions over a 10 minute period. The Factoid transactions are ordered in the Block in the order that they were received by the Federated server.

The Factoid Block consists of a header and a body.  The body is composed of serialized Factoid transactions with minute markers distributed throughout the body. The minute markers consist of a single byte 0x00.  There are 10 of them, each being placed at a minute boundary, and the 10th marker being the last item in the block. Factoid transactions begin with a version number above zero, which is how they can be differentiated from transactions. The minute markers are included in both the body and ledger Merkle roots.

| data | Field Name | Description |
| ----------------- | ---------------- | --------- |
| **Header** |  |  |
| 32 bytes | Factoid ChainID | The Factoid ChainID is predefined as 0x000000000000000000000000000000000000000000000000000000000000000f. |
| 32 bytes | BodyMR | This is the Merkle root of the Factoid transactions which accompany this block.  The leaves of the Merkle tree are the full Factoid transacion, from the version through the last signature, inclusive. Minute markers are also leaves of this tree. It is calculated with SHA256. |
| 32 bytes | PrevKeyMR | Key Merkle root of previous block. This is the value of the Factoid Block's previous Key Merkle root which was placed in the Directory Block.  It is the value which is used as a key into the Directory Block. It is calculated with SHA256. |
| 32 bytes | PrevLedgerKeyMR | This is a data structure which allows proofs of only the value transfers. This approach allows the confirmation and tracking of a transaction while ignoring signatures. A Merkle tree is constructed with the leaves being individual Factoid transactions hashed from the Version through the Entry Credit Purchase section. Neither the RCD reveals nor the signatures are included in this Merkle root.  This allows a future client to prove they recieved all the data documenting value movement, without needing to download signatures or all the public keys needed. The Merkle root of last block's value transfers is hashed with the last block's header hash to make a KeyMR, called PrevLedgerKeyMR. This differs from regular KeyMRs, in that the LedgerMR comes before the previous header hash. First block has a PrevLedgerKeyMR of 0. The minute markers are included in the tree. |
| 8 bytes | EC Exchange Rate | This the number of Factoshis required to purchase 1 Entry Credit, and set the minimum fees. This is the exchange rate currently in force for this block.  The initial value will be about 700000, but will be re-targeted based on the factoid/$ exchange rate.  It is an integer, because it is always expected that ECs will cost more than a single Factoshi.  Big endian. |
| 4 bytes | DB Height | This the Directory Block height which this Factoid Block is located in. Big endian. |
| varInt_F | Header Expansion Size | This is the number bytes taken up by the Header Expansion area. Set at zero for now. |
| Variable | Header Expansion Area | This is a field which can be defined and expanded in the future. It is good for things that can be derived deterministically by all the Federated servers when iterating the process lists. One planned feature is Balance Commitments, with a Merkle root of public keys paired with balances. |
| 4 bytes | Transaction Count | This is the number of Factoid transaction included in this block.  Big endian.  |
| 4 bytes | Body Size | This is the number of bytes the body of this block contains.  Big endian. |
| **Body** |  |  |
| variable | All objects | A series of variable sized objects arranged in chronological order. |


### Entry Block

An Entry Block is a datastructure which packages references to Entries all sharing a ChainID over a 10 minute period. The Entries are ordered in the Entry Block in the order that they were received by the Federated server. The Entry Blocks form a blockchain for a specific ChainID.

The Entry Block consists of a header and a body.  The body is composed of primarily Entry Hashes with 10 one minute markers distributed throughout the body. 

| data | Field Name | Description |
| ----------------- | ---------------- | --------- |
| **Header** |  |  |
| 32 bytes | ChainID | All the Entries in this Entry Block have this ChainID |
| 32 bytes | BodyMR | This is the Merkle root of the body data which accompanies this block.  It is calculated with SHA256. |
| 32 bytes | PrevKeyMR | Key Merkle root of previous block.  This is the value of this ChainID's previous Entry Block Merkle root which was placed in the Directory Block.  It is the value which is used as a key into databases holding the Entry Block. It is calculated with SHA256. |
| 32 bytes | PrevFullHash | This is a SHA256 checksum of the previous Entry Block of this ChainID. It is calculated by hashing the serialized block from the beginning of the header through the end of the body. It is included to doublecheck the previous block if SHA2 is weakened in the future.  First block has a PrevFullHash of 0. |
| 4 bytes | EB Sequence | This is the sequence which this block is in for this ChainID.  This number increments by 1 for every new EB with this chain ID.  First block is height 0. Big endian. |
| 4 bytes | DB Height | This the Directory Block height which this Entry Block is located in. Big endian. |
| 4 bytes | Entry Count | This is the number of Entry Hashes and time delimiters that the body of this block contains.  Big endian. |
| **Body** |  |  |
| 32 bytes | All objects | A series of 32 byte sized objects arranged in chronological order as received by the Federated server for that minute. |

Time delimiters are 32 byte big endian objects between 1 and 10 (inclusive).  They are inserted in into the Entry Block when a new Federated server yields control of the Chain and an Entry has been acknowledged prior to the handoff.  They are not needed if there is not an Entry to include that minute.  Note, there can be duplicate Entries included in an Entry Block.  If an Entry is paid for twice, it is included twice.  The times are organized when the Federated server saw and acknowledged the Entry.

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



### Components

These are some custom datastructures for Factom

#### KeyMR

A Key Merkle Root is a datastructure which allows fast validation of a header and also allows Merkle proofs to be built to the body data elements.

First a Merkle tree is constructed of all the body elements. It is called the BodyMR.  This is very similar to how all Bitcoin transactions can be proven with a Merkle root in the header.

The BodyMR is included in the header, among other things. The serialized header is then hashed.  The hashed header is combined with the BodyMR and hashed. This creates the KeyMR. With only the KeyMR, when a header is produced by a peer, the header can be validated with 2 hashes.

Note: the Factoid's LedgerKeyMR is constructed differently than the other KeyMRs.  It concatenates the LedgerMR first, then the header hash.  This is the opposite of other KeyMRs, which put the header hash first.  The rationale for this is to have different hashes for the Factoid's PrevKeyMR and PrevLedgerKeyMR when there is only a coinbase, which increases the security level to that of other objects in this case.



#### Variable Integers (varInt_F)

Integers can be serialized in blocks in a compact form to save space when stored indefinitely, like in a blockchain.  Factom's varInt_F is modeled after the [Protobuff](https://developers.google.com/protocol-buffers/docs/encoding)'s variable length integer, but is big-endian compared to Protobuff's little endian, and operates on the byte level rather then 4 bytes.

Values 127 and below can be represented in a single byte. Only positive integers are supported. The highest number is 2^64, which takes 10 bytes.

Larger numbers are represented by a sequence of bytes. The sequence length is indicated by the Most Significant Bit of each byte. If the MSB is set to one, then the next byte is considered part of the number. The number itself is held in the lower 7 bits. The LSB of the number is held in the LSB of the last byte.  Bits higher than the 7th are held in earlier bytes. 

This is the algorithm to create the stream:
Convert the value to big endian.
Count the number of bits between the LSB and the most significant 1 bit, inclusive. Divide this number by 7 and take the cieling of the remainder. This is the byte count M.
Create a byte sequence with M bytes.
Take the least significant 7 bits of the number and place them in the Mth byte.  Set the highest bit of the Mth byte to zero.
Take the bits 13 through 7 and add them to the byte M-1. Set the highest bit of byte M-1 to one.
Continue until all the M bytes have been filled with with data.

Here are some examples:

| Base 10 value | Binary Value | varInt_F Serialization|
| ----------------- | ---------------- | --------- |
| 0 | 00000000 | 00000000 |
| 3 | 00000011 | 00000011 |
| 127 | 01111111 | 01111111 |
| 128 | 10000000 | 10000001 00000000 |
| 130 | 10000010 | 10000001 00000010 |
| 2^16 - 1 | 11111111 11111111 | 10000011 11111111 01111111 |
| 2^16  | 00000001 00000000 00000000 | 10000100 10000000 00000000 |
| 2^32 - 1 | 11111111 11111111 11111111 11111111 | 10001111 11111111 11111111 11111111 01111111 |
| 2^32 | 00000001 00000000 00000000 00000000 00000000 | 10010000 10000000 10000000 10000000 00000000 |
| 2^63 - 1 | 01111111 11111111 11111111 11111111 11111111 11111111 11111111 11111111 | 11111111 11111111 11111111 11111111 11111111 11111111 11111111 11111111 01111111 |
| 2^64 - 1 | 11111111 11111111 11111111 11111111 11111111 11111111 11111111 11111111 | 10000001 11111111 11111111 11111111 11111111 11111111 11111111 11111111 11111111 01111111 |
