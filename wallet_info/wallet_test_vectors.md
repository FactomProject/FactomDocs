Factom BIP44 derivations
==========

Note: the 12 words from the koinify token sale used a different, incompatible address derivation. The koinify derivation is located [here](https://github.com/FactomProject/FactomDocs/tree/master/wallet_info/token_sale).  **Don't use your Koinify words as a BIP44 wallet.**


There are two coin types in the Factom system: Factoids and Entry Credits (ECs). There is a coin type for each:

See the slip-44 [source](https://github.com/satoshilabs/slips/blob/master/slip-0044.md).

index | hexa       | coin
------|------------|-----------------------------------
  131 | 0x80000083 | [Factom Factoids](https://github.com/FactomProject)
  132 | 0x80000084 | [Factom Entry Credits](https://github.com/FactomProject)


A Factoid test vector generator is located [here](https://github.com/FactomProject/FactomDocs/tree/master/wallet_info/bip44_test.py).
To run this program the same libraries as [this](https://github.com/FactomProject/FactomDocs/tree/master/wallet_info/token_sale/README.md) are needed, plus the base58 python library.

The test vectors for the Factoid BIP44 wallets are:
```
factom bip44 seed: yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow
factoid bip32 extended key xprvA22bpQKA9av7gEKdskwxbBNaMso6XpmW7sXi5LGgKnGCMe82BYW68tcNXtn4ZiLHDYJ2HpRvknV7zdDSgBXtPo4dRwG8XCcU55akAcarx3G
private key hex 0: 36422e9560f56e0ead53a83b33aec9571d379291b5e292b88dec641a98ef05d8
private key hex 1: d595251fcf8c5893476e35284f90b809fb6c2ff6f3e19dcf04f7a76af7644720
human readable private key 0: Fs1jQGc9GJjyWNroLPq7x6LbYQHveyjWNPXSqAvCEKpETNoTU5dP
human readable private key 1: Fs2wZzM2iBn4HEbhwEUZjLfcbTo5Rf6ChRNjNJWDiyWmy9zkPQNP
human readable address 0: FA22de5NSG2FA2HmMaD4h8qSAZAJyztmmnwgLPghCQKoSekwYYct
human readable address 1: FA3heCmxKCk1tCCfiAMDmX8Ctg6XTQjRRaJrF5Jagc9rbo7wqQLV
```


Factoids' public keys are hashed like P2SH addresses in Bitcoin.  See description [here](https://github.com/FactomProject/FactomDocs/blob/master/factomDataStructureDetails.md#factoid-transaction).

Entry Credits use raw ed25519 keys as a public key, so the public address derivation is [different](https://github.com/FactomProject/FactomDocs/blob/master/factomDataStructureDetails.md#entry-credit-address).


