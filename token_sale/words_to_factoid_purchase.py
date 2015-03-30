
from binascii import hexlify, unhexlify
from mnemonic import Mnemonic

from bip32utils.BIP32Key import *

import ed25519

#Replace secret words from koinify wallet below
words = "legal winner thank year wave sausage worth useful legal winner thank yellow"

#uncomment print statements below to see interim datapoints

seed = Mnemonic.to_seed(words, '')
#print "seed derived from words: " + hexlify(seed)

rootkey = BIP32Key.fromEntropy(seed, public=False)
#print "BIP32 root key: " + rootkey.ExtendedKey(private=True, encoded=False).encode('hex')

factoidChildKey = rootkey.ChildKey(BIP32_HARDEN+7)
#print "BIP32 root of Factoid chain key: " + factoidChildKey.ExtendedKey(private=True, encoded=False).encode('hex')

last32 = factoidChildKey.ExtendedKey(private=True, encoded=False)[-32:]
#print "Last 32 bytes: " + last32.encode('hex')

signing_key = ed25519.SigningKey(last32)
#print "The private key (ed25519 seed k) is: " + signing_key.to_ascii(encoding="hex")

verifying_key = signing_key.get_verifying_key()
pubkeyHex = verifying_key.to_ascii(encoding="hex")
#print "The public key is: " + pubkeyHex

opheader = "464143544f4d3030" 
opdata = opheader + pubkeyHex

print "data encoded in OP_RETURN is: " + opdata

 

