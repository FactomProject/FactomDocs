Understanding Factom Data Structures.
===

User data in the Factom network is organized into Entries and Chains. Entries hold the user data, and Chains associate Entries with one another over time.

* Anyone may write an Entry into any existing Chain
* An Entry must be associated with a Chain
* All Entry Content and External IDs are visible to anyone
* An Entry may contain any binary data up to 10KB
* It is up to the application to interperate the Entry Content and External IDs

Entries
---
A Factom Entry is composed of:
- A ChainID,
- 0 or more External IDs, and 
- Entry Content. 

The External IDs and Content are binary data but it is most common to write decoded text into these fields. It is up to the application to interpret the Entries. A Factom application may write any data into the External IDs and Entry Content and parse or interpret the data any way it likes. All Entries of a given Chain in a 10 minute block of time are hashed and bundled into an Entry Block for the given Chain. 

Chains
---
Factom Chains are essentially mini Blockchains for individual applications. Chains may be used by applications to: 
- find the Entries they are interested in, 
- prove that Entries were made, and 
- prove that certain Entries were never added to the Chain.

![chain-structure] (https://github.com/FactomProject/FactomDocs/blob/master/images/chain-structure.png)

Chains consist of a series of Entry Blocks, one for every 10 minute period where new Entries were added to the Chain. When a new Entry is commited and revealed to the Factom network, its hash is added to the Entry Block for the specified Chain. At the end of the 10 minute period all of the new Entry Blocks for all Chains are combined into one Directory Block, which is then anchored into the Bitcoin and Ethereum Blockchains. If there are no new Entries for a Chain in a given 10 minute period, no new Entry Block is added for the Chain.

A new Chain is created by constructing a First Entry which establishes the new ChainID. The first Entry is a normal Entry with the added reqirement that its collective External IDs must be unique among all first Entries for all existing Chains. The first Entry Content has no additional restrictions, but by convention it may be used to describe the Chain and post relevant information on processing the Chain. For example the first Entry may prescribe a format that future Entries' Content must follow to be considered valid by the application, or it may post a public key by which all valid Entries in the Chain must be signed.

More Info
---
For more information on Entries, Chains, Entry Blocks, and internal Factom data structures, see the [Factom Whitepaper](https://github.com/FactomProject/FactomDocs/blob/master/Factom_Whitepaper.pdf)
