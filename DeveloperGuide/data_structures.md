Understanding Factom data structures.
===
User data in the Factom network is organized into Entries and Chains. Entries hold the user data, and Chains associate Entries with one another over time.

* Anyone may write an Entry into any existing Chain
* An Entry must be associated with a Chain
* All Entry Content and External IDs are visible to anyone
* An Entry may contain any binary data up to 10KB
* It is up to the application to interperate the Entry Content and ExtIDs

Entries
---
A Factom Entry is composed of a ChainID, 0 or more External IDs, and the Entry Content. The External IDs and Content are binary data but it is most common to write decoded text into these fields. It is up to the application to interperate the Entries. A Factom application might write any data into the External IDs and Entry Content then parse or interperate the data any way it likes. All Entries to a given Chain in a 10 minute block of time are hashed and collected into an Entry Block for the given Chain. 

Chains
---
Factom Chains are essencialy mini Blockchains for individual applications. Chains may be used by applications to find the Entries they are interested in, to prove that Entries were made, and to prove that certain Entries were never added to the Chain.

Chains consist of a series of Entry Blocks, one for every 10 minute period where new Entries were added to the Chain. When a new Entries are commited and revealed to the Factom network their hashes are added to the Entry Block for the specified Chain. At the end of the 10 minute period all of the new Entry Blocks for all Chains are combined into the Directory Block, then anchored into the Bitcoin Blockchain. If there are no new Entries for a Chain in a given 10 minute period, no new Entry Block is added for the Chain.

A new Chain is created by constructing a First Entry which esablishes the new ChainID. The First Entry is a normal Entry with the added reqirement that its collective External IDs must be unique among all First Entries for all existing Chains. The First Entry Content has no additional restrictions, but by convention it may be used to describe the Chain and post relevent information for how to process the Chain. For example the First Entry may perscribe a format that future Entries' Content must follow to be considered valid by the application, or it may post a public key that all valid Entries in the Chain must be signed by.

More Info
---
For more information on Entries, Chains, Entry Blocks, or internal Factom data structures see the [Factom Witepaper](https://github.com/FactomProject/FactomDocs/blob/master/Factom_Whitepaper.pdf)