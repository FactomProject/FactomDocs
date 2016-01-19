Identity in Factom
===============

Factom Servers and Users who vote for them must create an identity.  The identity is contained within its own Chain, and updates to itself happen in that Chain.

An Identity Chain
-----------------

To establish an identity, a user needs to create several private keys, combine the public key hashes into a Chain Name, mine to get an appropriate prefix, then create a new chain with that Chain Name.  Entry Credit keys are then linked to that identity.  The identity then lends support to other identities, then ultimately to a server candidate, which may be a Federated or Audit server.


#### Human Readable Identity Keys

The first step in creating an identity is to create 4 levels of private keys, with level 1 being the lowest security online key.

The Factom identities are managed by ed25519 digital signatures. The keys can be represented in base58 form with checksums to allow for human interfacing.

Four different private keys are created, each a 32 byte random number.  The 4 different levels are presented to the user with 4 different prefixes, resulting in address that start with sk1, sk2, sk3, and sk4.

The conversion is very similar to Entry Credit keys, and only differs by having an extra byte in the prefix.  The prefix is prepended to the private key, then that is hashed with SHA256d, and the first 4 bytes of the SHA256d is appended to the end of the key.  The entire thing is converted to base58.

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



#### Factom Identity Chain Creation

Messages and updates for an identity occur within an identity chain.  There is a single chain per identity, and the 32 byte ChainID of the identity is how the identity is referenced. A Factom identity is not explicitly tied to any real world human/organizational entity. A real world entity can claim an identity, but it is not necessary. 

An identity is established with the first entry in the chain.  It is updated with entries signed with keys placed in the first entry.  The public keys are placed in the Chain Name, so the identity keys largely what makes up the identity.  

There is something akin to mining in the identity creation.  This marginally rate limits identity creation.  It also makes future P2P network segmentation possible based solely on the ChainID.  All the chains related to voting would share the first few bytes and be on the same network segment.  All the ChainIDs related to identity start with 0x888888.

First, 4 random 32 bytes are chosen.  These are the 4 different private keys of the different levels.

| Level | Four Random Keys | Human Readable Equivalent |
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

A Chain Name is constructed with 6 elements. The first element is three ASCII bytes "ID0" with the 0 signifying a version. The second element is the level 1 identity key in hex. Elements 3-5 are levels 2-4. The 6th element is a nonce which is iterated until the first 6 bytes match 0x888888. The Entry content is not defined, and does not affect the Chain Name. On a 5 year old laptop the search took about 1 minute per core.

Chain Name = [494430] [3f2b77bca02392c95149dc769a78bc758b1037b6a546011b163af0d492b1bcc0] [58190cd60b8a3dd32f3e836e8f1f0b13e9ca1afff16416806c798f8d944c2c72] [b246833125481636108cedc2961338c1368c41c73e2c6e016e224dfe41f0ac23] [12db35739303a13861c14862424e90f116a594eaee25811955423dce33e500b6] [nonce]

After iterating and finding a nonce 0000000000502cb9 we have a chainID 888888d00082a172e4f0c8d03a83d327b4197e68bcc36e88eeefb00b6cec7936



#### Factom Identity Registration

In order for Factom to pay attention to any individual identity, the identity must register itself.  The registration should occur after after the chain creation to prevent a 12 hour long denial-of-chain attack (detailed elsewhere).  For the registration to take effect, the chain must be created within 144 blocks (normally 24 hours).  Any updates to the identity (such as adding EC keys or updating keys) must occur during or after the block it was registered in.  This prevents events being reinterpreted retroactively.  Most people will only need to link an EC key and lend support.  

An identity only needs to be registered once, and cannot be unregistered.

The registration message has 5 ExtIDs.  The first ExtID has 4 ASCII bytes "REG0", with 0 signifying the version.  The second ExtID is the binary encoded ChainID of the identity.  It will start with 888888.  The 3rd ExtID is a byte which indicates which level key matches the 4th ExtID.  The 4th ExtID is the preimage to the identity key.  It includes the prefix and the pubkey.  The 5th ExtID is the signature of the first and second ExtIDs concatenated together.




