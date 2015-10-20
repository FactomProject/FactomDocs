Identity in Factom
===============

Some thoughts about identity tracking in Factom.  Each of the servers must have an identity, and there are many ways of defining identities using Factom.   I am leaning towards a rather simple approach, as follows.

An Identity Chain
-----------------

Information related to the identity can be placed in a Entry Chain.  To establish an Identity, the first component of the chain name must be "Identity".  The next component would be a human readable name, of the user's choice. The next four components would be the public keys that must sign any authorized entry in the Identity, were the first is the higher priority, ordered downward to the last.  

So for example, an identity could be:

- Identity
- Factom Server One
- EC3NK6diqjoH4VmkDsND6zUBSF5A1SvPgiT1Bin37Xu1qy9dvLJJ
- EC1qQtEJqeupmxSLzwKZdWsuhkcLFaPbBSbHM9Ku3nHjsCpqjvbT
- EC315Akp8ayYcqTJWd4xqBn1NJ62yuEdVYg3apzQsT8ywLhEsSfh
- EC315Akp8ayYcqTJWd4xqBn1NJ62yuEdVYg3apzQsT8ywLhEsSfh

Any key can invalidate a key at the same level or lower.  This is done by signing an entry with that key to that effect.  For example, The entry

Replace EC315Akp8ayYcqTJWd4xqBn1NJ62yuEdVYg3apzQsT8ywLhEsSfh with EC2Q2BrHg9R8rt9FRc8553C4FhHtBNafscZU9u4mP1gFaPrVyN89
