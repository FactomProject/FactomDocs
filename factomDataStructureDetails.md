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

ChainID = SHA256(SHA256(Name[0]) | SHA256(Name[1] | ... | Sha(Name[n])

See code at the go source path github.com/FactomProject/FactomCode/notaryapi/echain.go


## User Elements

These data structures are composed by the Users.

### Entry

An Entry is the element which carries user data. An Entry Reveal is essentially this data.

An External ID (ExtID) is one or more byte fields which can serve as hints to 3rd party databases.  These are fields which the Entry author felt would make good keys into a database.  They are not required for Factom usage.  The data is not checked for validity, or sanitized.  The only enforement of these fields is the lenghts need to be within bounds.  Also, the character encoding selected must be not reserved.

**(Different from what is implemented)**


| data | Field Name | Description |
| ----------------- | ---------------- | --------------- | 
| **Header** |  | |
| 32 bytes | ChainID | This is the chain which the author wants this entry to go into |
| 1 byte | version | starts at 0.  Higher numbers are currently rejected |
| varInt_F | Entry Length | Describes how many bytes the Entry uses.  Count starts at the beginning of the Chain ID and ends at the end of the user data |
| 1 byte | Number of ExtIDs | Can be 0. Max is 255.  This describes the number of individual  |
| **If Number of ExtIDs is > 0** |  | |
| 1 byte | character encoding | 0=UTF-8  All other values are reserved |
| varInt_F | ExtID 0 length | This is the number of the following bytes to be interpreted as an External ID | 
| varaible | Chain Name element data | This is the first External ID |
| varInt_F | Chain Name element n length | There will be as many ExtIDs and length designators as are specified in 'Number of ExtIDs' | 
| varaible | Chain Name element data | This is the Nth External ID |
| **Extra Header** |  | This header is only interpreted and enforced if this is the first Entry in a Chain, otherwise the Entry Data field starts here |
| 1 byte | number of Chain Name elements  | This must be 1-255 if creating a new Chain.  These fields must hash to the ChainID specified in this Entry. |
| varInt_F | Chain Name element 0 length | This is the number of the following bytes to be interpreted as a Chain Name element | 
| varaible | Chain Name element data | This is the data to be hashed |
| varInt_F | Chain Name element n length | There will be as many elements and length designators as are specified in 'number of Chain Name elements' | 
| varaible | Chain Name element data | This is the data to be hashed |
| variable | Entry Data | This is the payload of the Entry.  It is all user specified data. |

Minimum Empty Entry length: 35 bytes
Maximum Payload size: 10KiB - (32 + 1 + 3 + 1) = 10203 bytes

### Entry Commit


## Block Elements

These data structures are constructed of User Elements, etc.


