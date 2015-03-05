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

An Entry is the element which carries user data. An Entry Reveal is essentially this data.

An External ID (ExtID) is one or more byte fields which can serve as hints to 3rd party databases.  These are fields which the Entry author felt would make good keys into a database.  They are not required for Factom usage.  The data is not checked for validity, or sanitized.  The only enforcement of these fields is the lengths need to be within bounds.  Also, the character encoding selected must be not reserved.

**(Different from what is implemented)**


| data | Field Name | Description |
| ----------------- | ---------------- | --------------- | 
| **Header** |  | |
| 32 bytes | ChainID | This is the chain which the author wants this entry to go into |
| 1 byte | version | starts at 0.  Higher numbers are currently rejected |
| 2 bytes | Entry Length | Describes how many bytes the Entry uses.  Count starts at the beginning of the Chain ID and ends at the end of the user data.  Big endian. |
| 1 byte | Number of ExtIDs | Can be 0. Max is 255.  This describes the number of individual  |
| **If Number of ExtIDs is > 0** |  | |
| 1 byte | character encoding | 0=UTF-8  All other values are reserved |
| varInt_F | ExtID 0 length | This is the number of the following bytes to be interpreted as an External ID | 
| varaible | Chain Name element data | This is the first External ID |
| varInt_F | Chain Name element X length | There will be as many ExtIDs and length designators as are specified in 'Number of ExtIDs' | 
| varaible | Chain Name element data | This is the Xth External ID |
| **Name Header** |  | This header is only interpreted and enforced if this is the first Entry in a Chain, otherwise the Entry Data field starts here |
| 1 byte | number of Chain Name elements  | This must be 1-255 if creating a new Chain.  These fields must hash to the ChainID specified in this Entry. |
| varInt_F | Chain Name element 0 length | This is the number of the following bytes to be interpreted as a Chain Name element | 
| varaible | Chain Name element 0 data | This is the data to be hashed |
| varInt_F | Chain Name element X length | There will be as many elements and length designators as are specified in 'number of Chain Name elements' | 
| varaible | Chain Name element X data | This is the data to be hashed |
| variable | Entry Data | This is the payload of the Entry.  It is all user specified data. |

Minimum Empty Entry length: 36 bytes

Maximum Payload size: 10KiB - (32 + 1 + 2 + 1) = 10204 bytes

Typical size recording the hash of a file with 200 letters of ExtID metadata: 32+1+2+1+1+1+200+32 = 270 bytes

example size of something similar to an Omni(MSC) transaction, assuming 500 bytes [per transaction](https://blockchain.info/address/1EXoDusjGwvnjZUyKkxZ4UHEf77z6A5S4P):
32+1+2+1+500 = 536 bytes


### Entry Commit


### Factoid Transaction

Factoid transactions are similar to Bitcoin transactions, but incorporate some [lessons learned](http://www.reddit.com/r/Bitcoin/comments/2jw5pm/im_gavin_andresen_chief_scientist_at_the_bitcoin/clfp3xj) from Bitcoin.
- They are closer to P2SH style addresses, where the value is sent to the hash of a redeem condition, instead of sent to the redeem condition itself. To redeem value, a datastructure containing public keys, etc should be revealed. This is referred to as the **Redeem Condition Datastructure (RCD)**
- Factoids use Ed25519 with Schnorr signatures.  They have [many benefits](https://ripple.com/uncategorized/curves-with-a-twist/0) over the ECDSA signatures used in Bitcoin.
- Txid does not cover the signature field.  This will limit damaging malleability by attackers without the private key.
- Scripts are not used.  They may be added later, but are not implemented in the first version. Instead of scripts, there are a limited number of valid RCDs which are interpreted.  This is similar to how Bitcoin only has a handful of standard transactions.  Non-standard transactions are valid in blocks, but are not relayed on the P2P network. In Factom, non-standard transactions are undefined.


The transaction ID (txid) is a hash of the data from the header through the inputs.  The RCD reveal and signatures are not part of the txid.

| data | Field Name | Description |
| ----------------- | ---------------- | --------------- | 
| **Header** | | |
| 1 byte | Version | Version of the transaction type.  Versions above 0 are not relayed unless it is preceded by a federated server's confirmation.  |
| 5 bytes | lockTime | same rules as Bitcoin.  less than 500 million defines the minimum block height this tx can be included in or be rebroadcast.  Greater or equal to 500 million is minimum Unix epoch time.  Big endian, so first byte is zero for the next 100 years or so. To disable timelock, set to all zeros. |
| **Outputs** | | |
| varInt_F | Factoid Output Count | This is the quantity of redeemable (Factoid) outputs created.  |
| varInt_F | value | (Output 0) The quantity of Factoids * 10^-8 reassigned. |
| 32 bytes | RCD Hash | (Output 0) The hash of the Redeem Condition Datastructure (RCD), which must be revealed then satisfied to later use the value as an input |
| varInt_F | value | (Output X) The quantity of Factoids * 10^-8 reassigned. |
| 32 bytes | RCD Hash | (Output X) The hash of the RCD |
| varInt_F | Entry Credit Purchase Count | This is the quantity of non-redeemable (Entry Credits) outputs created.  |
| varInt_F | value | (Purchase 0) The quantity of Factoids * 10^-8 to be turned into ECs. |
| 32 bytes | EC Pubkey | (Purchase 0) The Ed25519 raw public key which is the Entry Credit pubkey.  |
| varInt_F | value | (Purchase X) The quantity of Factoids * 10^-8 to be turned into ECs. |
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
| variable | RCD | The next RCD is checked against the next different address in the inputs list.|
| **Signatures** | | |
| variable | Signature bitfield | (Input 0) This is a set of bytes which form a bitfield. The number of bytes is determined by the N value in the RCD. |
| 64 bytes | Signature | (Input 0, 1st specified pubkey) signature covering the sighash data specified in input 0 |
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

Factom note: these will be expanded and better defined soon.

This field is modeled after Bitcoin's [OP_CHECKSIG](https://en.bitcoin.it/wiki/OP_CHECKSIG).  It allows the signer of this input to specify how the transaction can be reconfigured without resigning.  Not using the strictest type allows for transaction malleability.  This field defines the parts of the transaction that the signature is signing.  There are 4 types.
- Sighash all - Inputs and outputs cannot be changed without breaking the signature.  Signature covers Header, Outputs, and Inputs.
- Sighash single - The input signature is valid if the output at the same index number is included.  Signature signs the header, output, and input fields as if the desired output were the only one present.
- Sighash anyonecanpay - signature covers the Header, all outputs, and the input field as if it were the only input.
- Sighash none - Any outputs can be respecified to spend the value in any divisions to any address(es) without breaking the signature.

The upper bits are reserved and should be set to zero.


Note: For the crowdsale, the raw Ed25519 pubkey in an OP_RETURN is used.  The the genesis block will contain a transaction which outputs to many 1 of 1 addresses.  There will be an output for each of the Bitcoin payments' specified pubkeys.  The addresses will be derived from the exposed pubkeys. 

Some later RCD types will be added.  Output types supporting [atomic cross](https://en.bitcoin.it/wiki/Atomic_cross-chain_trading) chain swaps and [time locking](https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki) outputs are desirable.  Output scripts are also useful and desirable, but can open security holes.  They are not critical for the first release of Factom, so we will implement them later. This would give us the ability to make conditional outputs (IF, AND, OR, etc).  Nesting is also desirable but undefined in this version.  This would give multisig within a multisig transaction.

Ed25519 allows for threshold multisig in a single signature, but that cryptography will have to come later.  For now, multisig is based on multiple independent pubkeys and multiple signatures.

Fees are the difference between the outputs and the inputs.  The fees are sacrificed.  They are not reclaimed by the federated servers.  The fees are only partially defined, but will at minimum cost as much as the per-KiB price of an entry.  The number of signature checks will also factor into the cost.


## Block Elements

These data structures are constructed of User Elements, etc.


