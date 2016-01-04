Identity in Factom
===============

Factom Servers and Users who vote for them must create an identity.  The identity is contained within its own Chain, and updates to itself happen in that Chain.

An Identity Chain
-----------------

To establish an identity, a user needs to create several private keys, combine the public key hashes into a Chain Name, mine to get an apropriate prefix, then create a new chain with that Chain Name.  Entry Credit keys are then linked to that identity.  The identiy then lends support to other identities, then ultimately to a server candidate, which may be a Federated or Audit server.


#### Human Readable Identity Keys

The first step in creating an identity is to create 4 levels of private keys, with level 1 being the lowest security online key.

The Factom identities are managed by ed25519 digital signatures. The keys can be represented in base58 form with checksums to allow for human interfacing.

Four different private keys are created, each a 32 byte random number.  The 4 different levels are presented to the user with 4 different prefixes, resulting in address that start with sk1, sk2, sk3, and sk4.

The conversion is very similar to Entry Credit keys, and only differs by having an extra byte in the prefix.  The prefix is prepended to the private key, then that is hashed with SHA256d, and the first 4 bytes of the SHA256d is appended to the end of the key.  The entire thing is converted to base58.

The prefixes and key ranges are shown here:

| prefix | All Zeros | All Ones |
| ----------------- | ---------------- | --------------- | 
| 4db6c9 | sk11pz4AG9XgB1eNVkbppYAWsgyg7sftDXqBASsagKJqvVRKYodCU | sk13mjEPiBP6rEnC5TWQSY7qUTtnjbKb4QcpEZ7jNDJVvsupCg9DV |
| 4db6e7 | sk229KM7j76STogyvuoDSWn8rvT6bRB1VoSMHgC5KD8W88E26iQM3 | sk2464XMB8ws92poWcho4WjTThNDD8piLgDzMnSE178A8WiU46gJy |
| 4db705 | sk32Tee5C4fCkbjbN4zc4VPkr9vX4xg8n53XQuWZx6xAKm2cAP7gv | sk34QPpJe6WdRpsQwmuBgVM5SvqdggKqcwqAV1kidzwpL9X86sVi9 |
| 4db723 | sk42myw2f2Dy3PnCoEBzgU1NqPPwYWBG4LehY8q4azmpXPqGY6Bqu | sk44ij7G745Picv2Nw6aJTxhSAK4ADpxuDSLcF5DGtmUXnKs6XT1F |







| prefix | All Zeros | All Ones |
| ----------------- | ---------------- | --------------- | 
| 3fbeba | id11qFJ7fe26N29hrY3f1gUQC7UYArUg2GEy1rpPp2ExbnJdSj3mN | id13mzUM7fsX3FHXSExEdgRintPena8Ns92c5y4YVvEccAoEttNTG |
| 3fbed8 | id229ab58barepCKHhF3df62BLwxePyoJXr9968tSv4coR7LbtoFL | id246KmJadSHL3L8sQ9dFf3Ln7s5G7dW9QdnDCP38p4GoobsaTCHN |
| 3fbef6 | id32Tut2bZ9cwcEvirSSFdheAaRP7wUvaoTKGKTP5otH13uzjcHTd | id34Qf4G3b13cqNkJZM1sdexmMLVjf8dRgExLRhXmhsw1SQSzthdm |
| 3fbf14 | id42nFAz4WiPEQHYA1dpscKG9otobUz3s54VPYmsihhwCgibnEPW5 | id44izMDWYZoudRMjiYQVcGakaovDCdkhwr8Tf22QbhbD5D934waE |




