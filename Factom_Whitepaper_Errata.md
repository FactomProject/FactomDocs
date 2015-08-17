Factom Whitepaper Errata
=============


Design Changes
--------
Some minor details about Factom have changed since the Whitepaper was published.


### Block Times

The whitepaper describes Directory Blocks, as being 1 minute long.  They have been changed to be 10 minutes long.  Minute level resolution is maintained in the lower level blocks by adding demarcation structures. Merkle Roots are still placed into Bitcoin every 10 minutes.


### Denial of Chain

The whitepaper describes this attack denying for 10 minutes.  The attack is actually 1 hour long. The time a Chain Commit gives for exclusivity was increased to give time to recover from network errors.
see: https://github.com/FactomProject/WorkItems/issues/368

Changes in the Teachings
--------
Some minor details describing other systems is updated here.

### Bitcoin Headers


The Whitepaper describes the Bitcoin coinbase as being in the header. It is not in the header, but instead is the first thing after the header in a block.
