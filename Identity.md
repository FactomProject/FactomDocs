Identity in Factom
===============

Factom Servers and Users who vote for them must create an identity.  The identity is contained within a set of chains.  This document describes an identity system primarily intended for internal management.  Identity in general is a powerful concept useful for numerous applications, and tying time to it is also very powerful.  For example, it solves problems of authenticity of signed data after private keys are compromised.  Data signed before the compromise can still be relied on.  Old data does not need to be resigned with the new key to maintain authenticity.  Identities from other contexts, like software distribution signing, should use independent identity schemes, but can model them on this design.  Other identity systems probably don't need the chainID mining aspects, since that is primarily to consolidate internal identity chains into future network segments.  Eliminating mining also would allow a deterministic directory structure with the extIDs as folder paths.

An Identity Chain
-----------------

To establish an identity, a user needs to create several private keys, combine the public key hashes into a Chain Name, mine to get an appropriate prefix, then create a new chain with that Chain Name.  Entry Credit keys are then linked to that identity.  The identity then lends support to other identities, then ultimately to a server candidate, which may be a Federated or Audit server.

#### Root Factom Identity

A Factom identity is bootstrapped with a series of keys.  Different logical identity subchains are associated with the root identity to catalog specific functions.  The subchains segregate various types of data, so it does not need to be downloaded if the data is ignorable.

### Human Readable Identity Keys

The first step in creating an identity is to create 4 levels of private keys, with level 1 being the lowest security online key.

The Factom identities are managed by ed25519 digital signatures. The keys can be represented in base58 form with checksums to allow for human interfacing.

Four different private keys are created, each a 32 byte random number.  The 4 different levels are presented to the user with 4 different prefixes, resulting in address that start with sk1, sk2, sk3, and sk4.

The conversion to human readable form is very similar to Entry Credit keys, and only differs by having an extra byte in the prefix.  The prefix is prepended to the private key, then that is hashed with SHA256d, and the first 4 bytes of the SHA256d is appended to the end of the key.  The entire thing is converted to base58.

The prefixes and key ranges are shown here:

The secret part of the identity keys:

| prefix | All Zeros | All Ones |
| ----------------- | ---------------- | --------------- | 
| 4db6c9 | sk11pz4AG9XgB1eNVkbppYAWsgyg7sftDXqBASsagKJqvVRKYodCU | sk13mjEPiBP6rEnC5TWQSY7qUTtnjbKb4QcpEZ7jNDJVvsupCg9DV |
| 4db6e7 | sk229KM7j76STogyvuoDSWn8rvT6bRB1VoSMHgC5KD8W88E26iQM3 | sk2464XMB8ws92poWcho4WjTThNDD8piLgDzMnSE178A8WiU46gJy |
| 4db705 | sk32Tee5C4fCkbjbN4zc4VPkr9vX4xg8n53XQuWZx6xAKm2cAP7gv | sk34QPpJe6WdRpsQwmuBgVM5SvqdggKqcwqAV1kidzwpL9X86sVi9 |
| 4db723 | sk42myw2f2Dy3PnCoEBzgU1NqPPwYWBG4LehY8q4azmpXPqGY6Bqu | sk44ij7G745Picv2Nw6aJTxhSAK4ADpxuDSLcF5DGtmUXnKs6XT1F |


The public part of the identity keys:

| prefix | All Zeros | All Ones |
| ----------------- | ---------------- | --------------- | 
| 3fbeba | id11qFJ7fe26N29hrY3f1gUQC7UYArUg2GEy1rpPp2ExbnJdSj3mN | id13mzUM7fsX3FHXSExEdgRintPena8Ns92c5y4YVvEccAoEttNTG |
| 3fbed8 | id229ab58barepCKHhF3df62BLwxePyoJXr9968tSv4coR7LbtoFL | id246KmJadSHL3L8sQ9dFf3Ln7s5G7dW9QdnDCP38p4GoobsaTCHN |
| 3fbef6 | id32Tut2bZ9cwcEvirSSFdheAaRP7wUvaoTKGKTP5otH13uzjcHTd | id34Qf4G3b13cqNkJZM1sdexmMLVjf8dRgExLRhXmhsw1SQSzthdm |
| 3fbf14 | id42nFAz4WiPEQHYA1dpscKG9otobUz3s54VPYmsihhwCgibnEPW5 | id44izMDWYZoudRMjiYQVcGakaovDCdkhwr8Tf22QbhbD5D934waE |



### Factom Identity Chain Creation

Messages and updates for an identity occur within an identity chain.  There is a single root chain per identity, and the 32 byte ChainID of the identity is how the identity is referenced. A Factom identity is not explicitly tied to any real world human/organizational entity. A real world entity can claim an identity, but it is not necessary. 

An identity is established with the first entry in the chain.  It is updated with entries signed by keys placed in the first entry.  The public keys are placed in the Chain Name, so the initial identity keys largely make up the identity.

There is something akin to mining in the identity creation.  This marginally rate limits identity creation.  It also makes future P2P network segmentation possible based solely on the ChainID.  All the chains related to voting would share the first few bytes and be on the same network segment.  All the ChainIDs related to identity start with 0x888888.

First, 4 random 32 bytes are chosen.  These are the 4 different private keys of the different levels.

| Level | Four Private Keys | Human Readable Equivalent |
| ---- | ----------------- | ----------------- |
| 1 | f84a80f204c8e5e4369a80336919f55885d0b093505d84b80d12f9c08b81cd5e | sk13iLKJfxNQg8vpSmjacEgEQAnXkn7rbjd5ewexc1Un5wVPa7KTk |
| 2 | 2bb967a78b081fafef17818c2a4c2ba8dbefcd89664ff18f6ba926b55e00b601 | sk22UaDys2Mzg2pUCsToo9aKgxubJFnZN5Bc2LXfV59VxMvXXKwXa |
| 3 | 09d51ae7cc0dbc597356ab1ada078457277875c81989c5db0ae6f4bf86ccea5f | sk32Xyo9kmjtNqRUfRd3ZhU56NZd8M1nR61tdBaCLSQRdhUCk4yiM |
| 4 | 72644033bdd70b8fec7aa1fea50b0c5f7dfadb1bce76aa15d9564bf71c62b160 | sk43eMusQuvvChoGNn1VZZwbAH8BtKJSZNC7ZWoz1Vc4Y3greLA45 |

Raw public keys are created from those private keys.  These are treated similar to Factoid RCDs.  The pubkeys are prepended with a byte 0x01 and hashed with SHA256d.

The four keys above would result in these identity keys:

| Level | Four Identity Keys | Human Readable Equivalent |
| ---- | ----------------- | ----------------- |
| 1 | 3f2b77bca02392c95149dc769a78bc758b1037b6a546011b163af0d492b1bcc0 | id12K4tCXKcJJYxJmZ1UY9EuKPvtGVAjo32xySMKNUahbmRcsqFgW |
| 2 | 58190cd60b8a3dd32f3e836e8f1f0b13e9ca1afff16416806c798f8d944c2c72 | id22pNvsaMWf9qxWFrmfQpwFJiKQoWfKmBwVgQtdvqVZuqzGmrFNY |
| 3 | b246833125481636108cedc2961338c1368c41c73e2c6e016e224dfe41f0ac23 | id33pRgpm8ufXNGxtW7n5FgdGP6afXKjU4LfVmgfC8Yaq6LyYq2wA |
| 4 | 12db35739303a13861c14862424e90f116a594eaee25811955423dce33e500b6 | id42vYqBB63eoSz8DHozEwtCaLbEwvBTG9pWgD3D5CCaHWy1gCjF5 |

A Chain Name is constructed with 7 elements. The first element is a binary string 0 signifying the version. The second element is ASCII bytes "Identity Chain".  The third element is the level 1 identity key in binary form. Elements 4-6 are levels 2-4. The 7th element is a nonce which is iterated until the first 3 bytes match 0x888888. The Entry content is not defined, and does not affect the Chain Name. On a 5 year old laptop the search took about 1 minute per core.

Chain Name = [00] [4964656E7469747920436861696E] [3f2b77bca02392c95149dc769a78bc758b1037b6a546011b163af0d492b1bcc0] [58190cd60b8a3dd32f3e836e8f1f0b13e9ca1afff16416806c798f8d944c2c72] [b246833125481636108cedc2961338c1368c41c73e2c6e016e224dfe41f0ac23] [12db35739303a13861c14862424e90f116a594eaee25811955423dce33e500b6] [nonce]

After iterating and finding a nonce 0000000000c512c7 we have a chainID 888888d027c59579fc47a6fc6c4a5c0409c7c39bc38a86cb5fc0069978493762



### Factom Identity Registration

In order for Factom to pay attention to any individual identity, the identity must register itself.  The registration should occur after the chain creation to prevent a 12 hour long denial-of-chain attack (detailed elsewhere).  For the registration to take effect, the corresponding identity chain must be created within 144 blocks (normally 24 hours).  Any updates to the identity (such as adding EC keys or updating keys) must occur during or after the block it was registered in.  This prevents events being reinterpreted retroactively.  Most people will only need to link an EC key and lend support in the server election process.

An identity only needs to be registered once, and cannot be unregistered.

The registration message has 5 ExtIDs.  The first ExtID is a binary string 0 signifying the version.  The second ExtID has 24 ASCII bytes "Register Factom Identity".  It is a long string so there is no overlap in message interpretation with other message types.  It also makes it clear that a hash is not being signed, and can be filtered on this string in potential future messages.  The third ExtID is the binary encoded ChainID of the identity.  It will start with 888888.  The 4th ExtID is the preimage to the identity key.  It includes the type prefix  (0x01) and the raw ed25519 pubkey.  The 5th ExtID is the signature of the first, second, and third ExtIDs serialized together.

The entry would consist of only ExtIDs and look like this:

[0 (version)] [Register Factom Identity] [identity ChainID] [identity key preimage] [signature of version through ChainID]

[00] [526567697374657220466163746F6D204964656E74697479] [888888d027c59579fc47a6fc6c4a5c0409c7c39bc38a86cb5fc0069978493762] [0125b0e7fd5e68b4dec40ca0cd2db66be84c02fe6404b696c396e3909079820f61] [764974ae61de0d57507b80da61a809382e699cf0e31be44a5d357bd6c93d12fa6746b29c80f7184bd3c715eb910035d4dac2d8ecb1c4b731692e68631c69a503]

The identity registration chainID is 888888001750ede0eff4b05f0c3f557890b256450cabbb84cada937f9c258327 with a chain name of "Factom Identity Registration Chain" and "44079090249".

#### Server Management Subchain

Messages related to being a Federated, Audit, or Candidate server would live in this subchain.  The root identity chain links to it.  This chain is only needed if the identity wants to be a server.  It adds keys which are used to sign the Bitcoin anchors as well as keys to sign the directory blocks.

### Server Management Subchain Creation

This chain is created after the identity chain is known.  The Chain Name first element is a version, 0.  The second is the ASCII string "Server Management".  The 3rd consists of the root identity chainID.  The 4th is a nonce which makes the first 6 bytes of the chainID match 0x888888.  Since the root identity chainID would be known at this point, the management subchain would be susceptible to a denial-of-chain attack.  To counter this, a random starting value for the nonce can be chosen.  This makes it far less likely that an attacker could predict which subchain you are about to create.

Chain Name = [00] [536572766572204D616E6167656D656E74] [888888d027c59579fc47a6fc6c4a5c0409c7c39bc38a86cb5fc0069978493762] [nonce]

After iterating and finding a nonce 98765432103e2fbb we have a chainID 8888881d59de393d9acc2b89116bc5a2dd0d0377af7a5e04bc7394149a6dbe23

### Server Management Subchain Registration

The Server Management subchain needs to be discoverable.  The identity will place a signed Entry in their root identity chain which points to the subchain.

It is very similar to the Factom identity registration message.

[0 (version)] [Register Server Management] [subchain ChainID] [identity key preimage] [signature of version through ChainID]

[00] [526567697374657220536572766572204D616E6167656D656E74] [8888881d59de393d9acc2b89116bc5a2dd0d0377af7a5e04bc7394149a6dbe23] [0125b0e7fd5e68b4dec40ca0cd2db66be84c02fe6404b696c396e3909079820f61] [fcb3b9dd3cc9f09b61a07e859d13a569d481508f0d5e672f9412080255ee398428fb2c488e0c3d291218f573612badf84efa63439bbcdd3ca265a31074107e04]

This message is then placed into the root identity chain.  Only one server management subchain is allowed.  In the case of multiple messages, the valid one is the first message that also has a Chain which exists.  For example, if there are two messages registering Chain B and A in that order, but Chain A is created first, then Chain A is considered the valid one.  The chain must be created within 144 blocks (normally 24 hours) of being registered.

### Add New Block Signing Key

The Factom blockchain is signed with a key by each server.  This key signs the Directory blocks, and those signatures are held in the Admin blocks.  They are associated with the identity, but do not sign things other than the blocks.  The public key is added to the Admin block by the Federated servers as part of the server promotion process.  Before promotion, the key needs to be published to the server management subchain.  Keys are not removed, but new keys replace older keys.  To prevent replay attacks, a timestamp is included.  To be valid, the key update must be the latest one seen.  It also needs to be included in the blockchain between 12 hours +- of the message timestamp.  (note: backup block signing key authorizations can be presigned offline in advance.  Only 365 pre-prepared, signed messages would need to be held ready for broadcast to cover a year.)  If a higher level key signs a New Block Signing Key message, no new messages will be allowed by lower level keys until the lower level keys are replaced in the root identity chain.

The message is a Factom Entry with several extIDs holding the various parts.  The first part is a version binary string 0.  The second is the ASCII string "New Block Signing Key".  The third is the root identity ChainID.  Forth is the new public key being asserted.  5th is the timestamp with an 8 byte epoch time.  Next is the identity key preimage.  7th is the signature of the serialized version, text, chainID, new key, and the timestamp.

[0 (version)] [New Block Signing Key] [identity ChainID] [new key] [timestamp] [identity key preimage] [signature of version through timestamp]

[00] [4E657720426C6F636B205369676E696E67204B6579] [888888d027c59579fc47a6fc6c4a5c0409c7c39bc38a86cb5fc0069978493762] [8473745873ec04073ecf005b0d2b6cfe2f05f88f025e0c0a83a40d1de696a9cb] [00000000495EAA80] [0125b0e7fd5e68b4dec40ca0cd2db66be84c02fe6404b696c396e3909079820f61] [0bb2cab2904a014bd915b276c350821620edb432ddfbceed3896e87e591a412712b7db6d8dad1a8313138ea919bbc9b7a1bd4ffe1d84d558b8a78ef7746f480d]


### Add New Bitcoin Key

Factom uses the Bitcoin blockchain as a sibyl resistant communication channel, as well as a method to detect alterations to history.  The bitcoin keys are published in the identity's server management subchain.  When the server is promoted, or when a new key is added, the new Bitcoin key is published in the Admin block.  If a Federated server publishes an update to its chain, the Federated servers place it in the next Admin block. Factom doesn't use this in M2 or on the launch of M3, although these are present in the blockchain.

Like the identity keys, there are multiple levels of authority for the Bitcoin keys.  This allows servers to have an out of band backup signaling method when Bitcoin keys are stolen.  Anchors placed by higher level keys will alert clients that the lower level Bitcoin key(s) are considered compromised, and not to trust anchors from lower level keys.

Multiple levels of bitcoin keys are specified, but only 1 level is need initially.  The max is 4.  The same rules for timing and priority level apply to this message as apply to the New Block Signing message.

Bitcoin keys can either be P2PKH or P2SH.  The address type byte is set as follows:  0=P2PKH 1=P2SH.

The message is an entry with multiple extIDs.  It has a version, a text string saying "New Bitcoin Key".  It specifies the root identity chainID.  Next is a byte signifying the bitcoin key level.  It is 0 origin indexed, so with only 1 key it would be 0x00.  The next extID specifies what type of Bitcoin key is used, P2PKH or P2SH.  Next is the 20 byte Bitcoin key.  Seventh is a timestamp, which prevents replay attacks.  Eighth is the identity key preimage.  Last is the signature of the serialized version through the timestamp.

[0 (version)] [New Bitcoin Key] [identity ChainID] [Bitcoin key level] [type byte] [new key] [timestamp] [identity key preimage] [signature of version through timestamp]

[00] [4e657720426974636f696e204b6579] [888888d027c59579fc47a6fc6c4a5c0409c7c39bc38a86cb5fc0069978493762] [00] [00] [c5b7fd920dce5f61934e792c7e6fcc829aff533d] [00000000495EAA80] [0125b0e7fd5e68b4dec40ca0cd2db66be84c02fe6404b696c396e3909079820f61] [379d64dd36ba724539ce19adb05b9a6a98cc3e3171785553e2985f5542a3ce3bf470ef78a884eee2ba75c9f2cfa64f21d3ace4dc981daeb3c00352dbb19a1e0c]



### Add New Matryoshka Hash

Factom gets a set of randomness from a series of revealed SHA256 hash preimages.  To enforce these to be hash preimages, the last hash in a long hash chain is published.  A server will reveal sequential preimages, which are called Matryoshka hashes or M-hashes.  This message publishes the outermost hash, which is placed in the Admin block when the server is promoted. Factom doesn't use this in M2 or on the launch of M3, although these are present in the blockchain.

The new M-hash message has the same timing and priority level rules at the block signing key message.

It starts with the version and the text "New Matryoshka Hash".  Next is the root identity chainID.  Forth is the outermost M-hash.  Fifth is a timestamp.  Sixth is the root identity key preimage.  Last is the signature of the version through the timestamp.

[0 (version)] [New Matryoshka Hash] [identity ChainID] [new SHA256 M-hash] [timestamp] [identity key preimage] [signature of version through timestamp]

[00] [4e6577204d617472796f73686b612048617368] [888888d027c59579fc47a6fc6c4a5c0409c7c39bc38a86cb5fc0069978493762] [bf1e78e5755851242a2ebf703e8bf6aca1af9dbae09ebc495cd2da220e5d370f] [00000000495EAA80] [0125b0e7fd5e68b4dec40ca0cd2db66be84c02fe6404b696c396e3909079820f61] [b1bc034cf75d4ebf7c4025a6b6b15c8f11a4384dcb043160711f19da9f4efb1315d84811b2247bb703732c2116b464781daf5efe75efd4adc641fee220ec660c]










### For Voting in Milestone3

## Link Entry Credit Key to Identity

Factom identities exist largely to organize and direct votes (Entry Credit purchases) to elect particular Federated servers.  The users can publish messages in their identity chain to switch votes from one server to another.  The Entry Credits the user buys can be linked to an identity. The votes garnered can be delegated multiple times until they are eventually come to rest at a Candidate server's identity.

To begin the vote collecting process, the EC keys need to be linked to an identity.  EC keys can only ever be linked to one identity, and subsequent link messages are ignored.  If there are multiple conflicting link messages but are in different minutes, the earlier message takes precedence.  Since the system has 1 minute resolution, if there are multiple conflicting registrations in the same minute, the one with the lower ChainID takes precedence.  Lower by example means chain 1234xxxx...xxxx takes precedence over FEDCxxxx...xxxx.

The link message would consist of 5 extIDs.  The first is the version, with a single byte of 0.  The second is 21 bytes of ASCII text "Link Entry Credit Key". The third is the identity ChainID.  The 4th is the Entry Credit public key doing the signing, which should be linked to the specified identity.  The 5th is the signature of the first, second, and third ExtIDs serialized together.

[0 (version)] [Link Entry Credit Key] [identity ChainID] [Entry Credit public key] [signature of version through ChainID]

[00] [526567697374657220466163746F6D204964656E74697479] [888888d00082a172e4f0c8d03a83d327b4197e68bcc36e88eeefb00b6cec7936] [01] [0125b0e7fd5e68b4dec40ca0cd2db66be84c02fe6404b696c396e3909079820f61] [aab1cbbd72c8b7db32f45cb89e511793f8d47e0551665679a25ef8444248e045f858701351e0cc17aeb74e4f6aa425ee71663d3a4ca6abfe6fac88d66e0c2c01]

This message must be added to the identity chain specified in order to be counted.
