
from binascii import hexlify, unhexlify
from mnemonic import Mnemonic

from bip32utils.BIP32Key import *

import ed25519
import base58, hashlib

#Replace secret words from koinify wallet below
words = "yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow"

#uncomment print statements below to see interim datapoints

seed = Mnemonic.to_seed(words, '')
#print "seed derived from words: " + hexlify(seed)

rootkey = BIP32Key.fromEntropy(seed, public=False)
#print "BIP32 root key: " + rootkey.ExtendedKey(private=True, encoded=False).encode('hex')

BIP44subkey = rootkey.ChildKey(BIP32_HARDEN+44)

factoidCoinType = BIP44subkey.ChildKey(BIP32_HARDEN+131)

accountZero = factoidCoinType.ChildKey(BIP32_HARDEN)

externalFacingKeys = accountZero.ChildKey(0)

bip32ExtendedKey = externalFacingKeys.ExtendedKey(private=True, encoded=True)

print "factom bip44 seed: " + words

print "factoid bip32 extended key " + bip32ExtendedKey

privkey0 = externalFacingKeys.ChildKey(0).PrivateKey()
privkey1 = externalFacingKeys.ChildKey(1).PrivateKey()

print "private key hex 0: " + privkey0.encode('hex')
print "private key hex 1: " + privkey1.encode('hex')

privkey0prefixed = "6478" + privkey0.encode('hex')
digest = hashlib.sha256(hashlib.sha256(privkey0prefixed.decode("hex")).digest()).digest()
print "human readable private key 0: " + base58.b58encode(privkey0prefixed.decode("hex") + digest[:4])

privkey1prefixed = "6478" + privkey1.encode('hex')
digest = hashlib.sha256(hashlib.sha256(privkey1prefixed.decode("hex")).digest()).digest()
print "human readable private key 1: " + base58.b58encode(privkey1prefixed.decode("hex") + digest[:4])


privint0 = ed25519.SigningKey(privkey0)
privint1 = ed25519.SigningKey(privkey1)
pubint0 = privint0.get_verifying_key()
pubint1 = privint1.get_verifying_key()

rawpubkey0 = pubint0.to_ascii(encoding="hex")
rawpubkey1 = pubint1.to_ascii(encoding="hex")

rcd0 = "01" + rawpubkey0
rcd1 = "01" + rawpubkey1

rcdhash0 = hashlib.sha256(hashlib.sha256(rcd0.decode("hex")).digest()).digest().encode("hex")
rcdhash1 = hashlib.sha256(hashlib.sha256(rcd1.decode("hex")).digest()).digest().encode("hex")

pub0prefixed = "5fb1" + rcdhash0
digest = hashlib.sha256(hashlib.sha256(pub0prefixed.decode("hex")).digest()).digest()
print "human readable address 0: " + base58.b58encode(pub0prefixed.decode("hex") + digest[:4])

pub1prefixed = "5fb1" + rcdhash1
digest = hashlib.sha256(hashlib.sha256(pub1prefixed.decode("hex")).digest()).digest()
print "human readable address 1: " + base58.b58encode(pub1prefixed.decode("hex") + digest[:4])
# ^ note this is base58 encode, not base58check encode.  base58check adds extra checksum data which we have added manually already.



'''
Results of execution

factom bip44 seed: yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow
factoid bip32 extended key xprvA22bpQKA9av7gEKdskwxbBNaMso6XpmW7sXi5LGgKnGCMe82BYW68tcNXtn4ZiLHDYJ2HpRvknV7zdDSgBXtPo4dRwG8XCcU55akAcarx3G
private key hex 0: 36422e9560f56e0ead53a83b33aec9571d379291b5e292b88dec641a98ef05d8
private key hex 1: d595251fcf8c5893476e35284f90b809fb6c2ff6f3e19dcf04f7a76af7644720
human readable private key 0: Fs1jQGc9GJjyWNroLPq7x6LbYQHveyjWNPXSqAvCEKpETNoTU5dP
human readable private key 1: Fs2wZzM2iBn4HEbhwEUZjLfcbTo5Rf6ChRNjNJWDiyWmy9zkPQNP
human readable address 0: FA22de5NSG2FA2HmMaD4h8qSAZAJyztmmnwgLPghCQKoSekwYYct
human readable address 1: FA3heCmxKCk1tCCfiAMDmX8Ctg6XTQjRRaJrF5Jagc9rbo7wqQLV


'''

