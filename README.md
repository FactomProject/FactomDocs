Factom
=============

Overview
--------

Factom is a extension to the Bitcoin blockchain that solves the three core problems of all Bitcoin 2.0 applications: Speed, Cost, and Bloat.

The Bitcoin blockchain is a trustless, permanent system of record for Bitcoin transactions, secured by 10,000+ nodes across the world. Factom is a simple way to extend this technology to support Bitcoin 2.0, or applications that need such a system of record, but whose transactions do not primarily involve Bitcoin.  These applications often encode their information into Bitcoin transactions, which may be slower, more expensive, and add many transactions to the Bitcoin blockchain that are not actually Bitcoin transactions (something many call "blockchain bloat"). 

Instead of writing every transaction directly to the blockchain, Factom allows Bitcoin 2.0 applications to write unlimited numbers of entries to many distinct Factom chains.  These entries are organized into hierarchical sets of blocks. These blocks are then used to compute a single hash every 10 minutes, which is stored in the Bitcoin blockchain. This design allows applications to write transactions faster, at much a lower cost, and with nearly no blockchain bloat. 

At the most basic level, Factom provides "Proof of Existence."  Any digital artifact can be reduced to a hash, a relatively small 32 byte number, that proves an artifact's existence.  Adding that hash to the Bitcoin blockchain proves the existence of that artifact at a known point in time.  Factom extends this idea.  Each Factom subsystem in the group provides a "Proof of Process."  Proof of each step in a process can be entered into a "Factom chain" of provable events.  One obvious sort of Factom chain is a log.  A security camera can log a stream of signatures, proving video was taken at a point in time, and that the video has not be altered.  A Coin is also a process, one proving that coins existed and were exchanged.  The steps in processing a title for Real Estate is a process, and one where a clear timeline of process can be very helpful.  

Factom Chains are constructed from entries crafted to support a wide range of applications.  An entry can be used to prove data existed at a point in time.  And other Factom Chains and demonstrate their reaction to such data.  In other words, a Factom chain is a sequence of entries that define some progression of state, and the data that drove that progression.  Each Factom chain has its own rules, and entries in these Chains are constrained by those rules.  

The architecture for Factom allows for the easy construction of tokens or coins, securities, smart contracts, etc.
