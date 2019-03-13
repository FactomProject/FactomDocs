# Application Identity
Not to be confused with Server Identities used within the context of Factomd Consensus. This document describes a generic identity system for use in applications where an Identity is a structured chain that keeps an auditable history of public keys and when they were activated or retired.

## Identity Key Pair

For Factom Application Identities, ed25519 keys are used to sign and verify messages. Rather than simply using raw 32 byte arrays for keys, the following encoding scheme is used: 

Pseudo-code for constructing a private key string:
```
prefix_bytes = [0x03, 0x45, 0xf3, 0xd0, 0xd6]              // gives an "idsec" prefix once in base58 
key_bytes = [32 bytes of raw private key]                  // the actual ed25519 private key seed
checksum = sha256( sha256(prefix_bytes + key_bytes) )[:4]  // 4 byte integrity check on the previous 37 bytes

idsec_key_string = base58( prefix_bytes + key_bytes + checksum )
```

Pseudo-code for constructing a public key string:
```
prefix_bytes = [0x03, 0x45, 0xef, 0x9d, 0xe0]              // gives an "idpub" prefix once in base58 
key_bytes = [32 bytes of raw public key]                   // the actual ed25519 public key
checksum = sha256( sha256(prefix_bytes + key_bytes) )[:4]  // 4 byte integrity check on the previous 37 bytes

idpub_key_string = base58( prefix_bytes + key_bytes + checksum )
```

For the sake of human-readability, all characters must be in Bitcoin's base58 character set, the private key will always begin with "idsec", and the public key will always begin with "idpub". Additionally, the checksum at the end serves to signal that a user has incorrectly typed/copied their key.

Example key pair for the private key of all zeros:
- `idsec19zBQP2RjHg8Cb8xH2XHzhsB1a6ZkB23cbS21NSyH9pDbzhnN6 idpub2Cy86teq57qaxHyqLA8jHwe5JqqCvL1HGH4cKRcwSTbymTTh5n`

Example key pair for the private key of all ones:
- `idsec1ARpkDoUCT9vdZuU3y2QafjAJtCsQYbE2d3JDER8Nm56CWk9ix idpub2op91ghJbRLrukBArtxeLJotFgXhc6E21syu3Ef8V7rCcRY5cc`

## Identity Chain
As mentioned above, an Identity is a chain with a specific structure. The ExtIDs of the first entry contain the tag "IdentityChain", followed by any user specified byte arrays (human-readable or otherwise) that make up the Identity Name. The initial public Identity Keys are contained within a JSON object in the Content field of the same entry, the first key string being highest priority (i.e. a master-key) and last being lowest priority.

First Entry Structure:
- ExtID[0] = "IdentityChain"
- ExtID[1] = *Identity Name 1*
- ...
- ExtID[N] = *Identity Name N*
- Content = {"version": 1, "keys": ["idpub2Cy86teq57qaxHyqLA8jHwe5JqqCvL1HGH4cKRcwSTbymTTh5n", "idpub2op91ghJbRLrukBArtxeLJotFgXhc6E21syu3Ef8V7rCcRY5cc"]}

Where "idpub2Cy8..." is of higher priority than "idpub2op9..."

## Identity Key Replacement
A Key Replacement is performed by creating a structured entry in the Identity's chain. This entry will tell us that from this point on (the block that the entry is in), the old key will be considered invalid and the new key will be considered valid. In order to reconstruct the current set of active keys for an Identity, one would parse through the chain's entries validating and executing these key replacement entries in the order that they appear.

Rules for a Valid Replacement Entry:
- The entry must strictly follow the below External ID format
- Old key must be currently active for the identity of interest
- New key must have never been active for the identity of interest (for any priority level)
- Signer key must be currently active and of the same or higher priority than the old key
- Multiple key replacements included in the same block must be parsed in the exact order that they appear in the block
- A key replacement entry that resides outside of the Identity's chain will not be taken into consideration when determining which keys were valid at a given block height

Entry Structure:
- ExtID[0] = "ReplaceKey"
- ExtID[1] = Old key string
- ExtID[2] = New Key string
- ExtID[3] = bytes of signature( identity chain id + ExtID[1] + ExtID[2] )
- ExtID[4] = Key string used to sign the above

A function to the tune of "GetKeysAtHeight" would be used to parse a given Identity's chain (according to the above rules) in order to determine which keys were recognized as active at a certain point in time (a block height). This can be used to validate that an entry signed by an Identity was constructed using an authorized key pair.
