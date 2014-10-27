Factom
============

Abstract
--------

Factom is an open source project which leverages the irreversible security of the Bitcoin Block Chain ("blockchain").  Multiple user's data is collected by the Factom system and is packaged with other user's data.  The entire set of data is distilled to a single hash which is placed in the blockchain.  The data package is then published on a peer-to-peer network, allowing users to download the entire set of data.

Factom secures the entries by creating a hierarchical system of blocks and hashes culminating into a single hash every ten minutes.  This single hash is placed into the Bitcoin blockchain.  These structures holding and securing the entries are shared on a P2P network, using a BitTorrent like protocol.  The structures are arranged in a hierarchy, allowing for compact proofs.  The arrangement also allows users to download only the data subset they are interested in, and still be able to create proofs on their data, such as proofs of the negative (the hash of this document is not in the ledger).
 
Factom is run on a system of federated servers.  The servers are subject to real time audits, which provide users assurance that the servers are implementing published policies.  This system of audits is referred to as Proof by Audit. 

One objective of the project is to provide a location to house Mastercoin transactions, providing the security of Bitcoin, without bloating Bitcoin.

Introduction
------------

When Satoshi Nakamoto launched the Bitcoin blockchain he revolutionized the way transactions were recorded. There had never before existed a permanent, decentralized, and trustless ledger of records. Developers have rushed to create applications built on top of this ledger. Unfortunately, they run into a few core problems that were part of the original design tradeoffs when the blockchain was launched:

1)	Speed – because of its decentralized nature, the blockchain takes on average 10 minutes to confirm a transaction. Many applications require multiple confirmations for security.  Many applications can’t deliver a practical user experience with this time constraint. 

2)	Cost – the current minimum transaction cost is around 100 Bits (or roughly $0.05). The exchange price of Bitcoins has increased approximately 500% in the last 12 months ending August 2014, and is projected to continue to increase long term. This provides a serious cost barrier to applications that need to manage millions of transactions. (For conversions between USD, BTC, mBTC, and bits, check out this [Bitcoin Price Converter](http://youmeandbtc.com/bitcoin-converter/).)

3)	Bloat – the Bitcoin blockchain currently has a 1 MB block size limit which caps it at 7 transactions per second. Any application that wants to write and store information using the blockchain will add to the traffic. This problem has become politically charged. Should the blockchain be used for non-BTC transactions, or should it stay pure?

Factom is a protocol designed to solve these three core problems. Factom creates a Protocol Stack for Bitcoin 2.0 applications and constructs a simple, standard, effective, and secure foundation for these applications to run faster, cheaper, and bloat-free. 

------------

Bitcoin is disrupting the status quo for online payments.  With Bitcoin, payments can be made worldwide without any centralized party.  The success and elegance of Bitcoin has inspired many others to seek ways of decentralizing more than just payment systems.  Many have observed that the blockchain could enable the trading of commodities, trading of assets, issuing  securities, implementing self enforcing smart contracts, crowd sourced loans, etc.  The set of such extended applications is often referred to as "Bitcoin 2.0".

Factom simplifies how Bitcoin 2.0 applications can be deployed.  Factom does so by providing a few simple operators from which many more complicated designs can be built.  Factom extends Bitcoin beyond the exchange of bitcoins to include the recording and management of arbitrary events, and chains of such events.

Consider what any Bitcoin 2.0 application requires:

* A set of public or private events
* An unforgeable ledger recording and ordering entries
* Support for unambiguous audits of the ledger, ensuring internal consistency
* The ability to determine the state(s) of participants based on the ledger

Factom is designed to both meet and support the implementation of systems that have these requirements.

------------

Factom is a method of decentralized structure for collecting and packaging data.  Bitcoin does this too, but it has a requirement for total consistency over many thousand servers worldwide.  Distributing the world's records to every Bitcoin server presents a substantial bandwidth challenge.

At its heart, Factom is a network of federated servers.  These servers rotate responsibility for different aspects of the system.  No single server is permanently in control of the system, or part of a system.

Factom implements a Protocol Stack for Bitcoin 2.0 Applications.  The layers in this stack are:

1) Time Stamping Layer 

2) Factom Layer

3) Entry Layer

4) Application Layer

**Time Stamping**

Factom data is time stamped and made irreversible by the Bitcoin network.  User's data is as secure as any other Bitcoin transaction.  A compact proof of existence is possible for any data entered into the Factom system.  The Bitcoin entry is also a key to query a peer-to-peer Distributed Hash Table (DHT, similar to BitTorrent) in order to retrieve all the data which was time stamped.

Data is organized into block structures, and combined via a Merkle trees.  Every 10 minutes, the data set is frozen and submitted to the Bitcoin network.  Since Bitcoin has an unpredictable block time, there may be more or fewer than one Factom time stamp per Bitcoin block.

Bitcoin internal header block times themselves have a fluid idea of time.  They have a 2 hour flexibility from reality [[1](https://en.bitcoin.it/wiki/Block_timestamp)].  Factom will provide its own internal time stamps which conform with standard time systems.  Since Factom places high importance on time stamping, it will be a closely audited part of the system.

The user data ordering will be assigned when received at the server.  A federated server network bounds the assigned server to within a 1 minute time frame; the time between when a Factom block is opened and closed.  The server is not allowed to time stamp its data collection outside of that time frame.  On closing, the federated server network generates consensus and cumulatively time stamp each other's data.

As a general note, the data could have existed long before it was time stamped.  Factom only proves the data did not originate after the time stamp.

The Merkle Root for the Factom block (effectively a time stamp) is entered into the Bitcoin blockchain with a spending transaction.  The spend includes an output with an OP_RETURN.  This method is the least damaging to the Bitcoin network of the various ways to time stamp data [[2](http://bitzuma.com/posts/op-return-and-the-future-of-bitcoin/)].  The first eight bytes of the available 40 following the OP_RETURN code would be a designator tag.  The designator tag indicates the transaction could be a Factom entry.  Other qualifiers are required, but the tag eliminates most of the OP_RETURN entries that would otherwise need to be inspected.

The Merkle Root time stamp will be entered into the Bitcoin blockchain by one of the members in the federation.  The server delegated to time stamp the federation’s collected data creates a small BTC transaction.  The transaction will be broadcast to the Bitcoin network, and be included in a Bitcoin block.  Bitcoin transactions that look like Factom entries, but are not spent from an address known as a Factom server will be ignored.

Bitcoin blocks are generated with a statistical process, as such, their timing cannot be predicted.  This means that the time stamping done for entries within Factom is only roughly bound by the entries inserted into the Bitcoin blockchain, and thus Bitcoin time stamping system.  The real value of inserting these values  into Bitcoin is to prevent anyone from generating false Factom histories in the future.  Due to bad luck of Bitcoin miners, or slow inclusion of Factom transactions, there could easily be an hour or more between when the Factom state is frozen for a particular Factom block and when the Bitcoin transaction that secures that Factom block is mined into a Bitcoin block.


**Factom Layer**

The Factom layer implements proof of existence for an digital artifact.  Any event, document, image, recording, etc. that is defined in a digital representation can be hashed.  That hash can be recorded in the Factom layer.  Because of the vast (currently insurmountable) difficulty and complexity of creating a digital document that will generate a particular hash, the mere recording of such a hash is proof of the digital document’s existence at the time of the recording of the hash.

Factom collects sets of such hashes into a Factom block.  The Factom block is then hashed by computing a Merkle tree, and the Merkle root is recorded into the Bitcoin blockchain.  This allows the most minimum expansion of the blockchain, yet the ledger itself becomes as secure as Bitcoin itself.  Furthermore, since Factom can be maintained more cheaply in terms of resources, the cost of entries into the Factom layer will be much cheaper than transactions in the blockchain.

**Entry Layer**

Bitcoin 2.0 applications will need to record a varied range of information associated with events within their application.   The information associated with an event can be encoded into an Entry and the entry recorded into Factom.  Encoding all that information into the Bitcoin blockchain is unreasonable, yet some applications need information recorded into the ledger rather than holding that information off chain.   Factom allow the application to define the entry structure(s) they require, and manage the structure(s) in Factom Chains. 

**Factom Chains**

Factom Chains are chains of entries that that reflect the events of an application.  These sequences are at the heart of Bitcoin 2.0.  Defining what an event is, and what is required for following events is basic to all event sequences (even outside of Bitcoin 2.0).  Factom Chains document and validate these event sequences to provide an audit trail that can prove an event sequence occurred.  

**Applications**

Applications are possibly distributed applications running on top of Factom to provide additional services.  For example, one might imagine a trading engine that processes transactions very fast, with very accurate time stamping.  Such an application may none the less stream transactions out into Factom chains to document and secure the ledger for the engine.  Such a mechanism could provide real time cryptographic proof of process, of reserves, and of  communications.

Another application may provide an exchange of Bitcoin or even conventional credit cards for Factom tokens.  Using such a "Vending Machine", users could buy entries to be used in Factom without ever owning the Factom Tokens that drive the Factom servers.  And yet such a service is decentralized, in the sense that no application is forced to use a particular "Vending Machine," even if such applications are run by centralized parties.

-----------

Factom Chains
---------------

The first entry beginning a chain will, by convention, provide a hash of a human readable list of rules for the Factom Chain, a url The first event will also provide a hash of a script or an application that can be run to validate entries in the sequence.  The description of the event will provide a link to these rules, scripts, and applications.

An enforced sequence can be specified.  Entries that cannot meet the requirements of the specified enforced sequence will be rejected.  However, entries that might be rejected by the script or the app will still be recorded.  Thus users of such chains will need to run the app or script to validate a chain sequence of this type. The FactomChain servers will not validate using the script or app.

As new public enforced sequences become popular, they can be added to the set of enforced sequences.

*Private enforced sequences*

These sequences are identical to the public enforced sequences, only the readable list of rules, scripts, and applications are only provided as hashes.  Users with access to the rules, scripts and applications can validate them via the first event in such a FactomChain, but the links to them are not provided by the FactomChain.

This is useful for testing, or for documenting and driving private transactions. 
Applications
Using these operators and facilities, Distributed Autonomous Applications (DAPPs) and Distributed Autonomous Organizations (DAOs) can be constructed.  But even everyday sorts of uses can be facilitated as well, like simple movie tickets or arcade tokens.  Factom Chains can support:

* Crowd sourcing loans
* Issuing securities and paying dividends 
* Powerful scripted chains with functionality like Ethereum, Darkcoin, etc.
* Smart Contracts
* Smart Properties
* Event ticketing

#Discussion

Using Bitcoin to prove the existence of a document (really any digital asset, like a tweet, a web page, a spreadsheet, a security video, a photo, etc.) is a concept that is well known.  (See the references at the end of this document).  And some have even suggested that a service could be created to take a list of signatures, compute a merkle root, place that in the Bitcoin blockchain.  This not only provides the same security, but limits the “blockchain pollution” of pushing a hash into the blockchain for every signed document.  There are at least a couple of online websites that provide these services.

Factom provide for simple “proof of existence” entries.  In addition, Factom provide proof of transform.  Factom implement validation scripts that allow for chains of notarized entries.   Factom can be used to implement token systems, asset trading systems, smart contracts, and more.   A federated set of FactomChain servers provide for real time audits, easy transfer from one FactomChain server to another, reduced blockchain pollution, and other benefits.

Bitcoin implements a strict, distributed method for the validation of transactions, where anyone can validate each transaction, and the validity of every input into a transaction can be verified.  Because each transaction is authorized via cryptographic signatures, no transaction can be arbitrarily reversed.  Furthermore, the meaning of each transaction is defined as a validation of the input values (amounts of bitcoin) for each transaction.

The Bitcoin protocol is transactionally complete.  In other words, the creation and distribution of Bitcoins through transactions is completely defined within the Bitcoin protocol.  Transactions (which specify movement of bitcoin) and block discovery (which move bitcoin via mining fees and provide block rewards) are the only inputs into the Bitcoin Protocol, and nothing leaves the Bitcoin Protocol.  In other words, the 21 million Bitcoin that will ultimately exist will always and forever exist within the protocol.  (Well, at least until side chains are implemented, which will provide additional movement of Bitcoin in and out of side chains.)

Many different groups are looking to find ways to leverage the Bitcoin approach for managing other sorts of transactions besides tracking bitcoin balances.  For example, the trading of assets such as houses or cars can be done digitally using Bitcoin.  Even the trading of Commodities such as precious metals, futures, or securities might be done via clever encoding and inserting of information into the Bitcoin blockchain.  

Efforts to expand Bitcoin to cover these kinds of trades include Colored Coins,  Mastercoin, and Counterparty.  Others seek to build their own cryptocurrency with a more flexible protocol that can handle trades beyond currency.  These include Namecoin, Ripple, Etherium, BitShares, NXT, and others.  And of course Open Transactions uses Cryptographic signatures and signed receipts and proof of balance for users (i.e., a user does not need the transaction history to prove their balance, just the last receipt). 

A FactomChain seeks to gain the ability to track assets and implement contracts, while securing the advantage Bitcoin’s security via Bitcoin blockchain.  Instead of inserting transactions into the blockchain (viewed as “blockchain pollution” by many), Factom keeps most information off blockchain.  Furthermore, the FactomChain provides a record keeping system that minimizes the information any actor has to maintain to validate their Factom of interest.  In short,   Factom utilize a combination of mathematical proofs and hashes within the Factom, while inserting the least amount of information into blockchain.  The goal is to create an system of records whose audit trails can prove the interactions of FactomChain users.

A user only needs the artifacts of the FactomChain of interest rather than the full set of Factom maintained by the FactomChain servers.

Of course, the FactomChain can notarize documents, providing proof of their existence at a point in time, and validating their construction (any modification will be detected). In addition, a FactomChain provides a history that proves a series of events occurred. The FactomChain is a series of entries that form a chain of time-stamped events, providing a provable history.  This allows a FactomChain to implement smart contracts and even alternate currencies.  All of which can clear instantly (assuming trust in the FactomChain servers), and within minutes once a Factom entry is secured via the blockchain.

The FactomChains are maintained on a set of federated, independently controlled FactomChain servers.  Factom borrows from the concept of Private Chains, and allows for reactive security by limiting the ability of any FactomChain server to fail to log entries without immediate detection by not only the other FactomChain servers, but by the users themselves.  And like Open Transactions, all links in a chain are secured with cryptographic signatures; there is no opportunity for a FactomChain server to insert a bogus transaction. 

Furthermore, a FactomChain is largely left ignorant of the significance of any transaction.  The management and backing of any FactomChain is left to the users of the service.  The FactomChain is an automated, powerless, and disinterested party to the transformations of a particular FactomChain.

The FactomChain concept is designed to allow many different protocols and rules to be run in parallel within data structures designed and implemented by its users.  At the same time, the integrity of the system is secured with the Bitcoin blockchain.  Factom also limits the amount of “pollution” to the blockchain that would result if the same data and information were encoded into Bitcoin Transactions.  Additionally, the FactomChain seeks to reduce the overhead of a single blockchain for sets of transactions that have little to do with one another.  In other words, while Bitcoin benefits from thousands of computers holding the full blockchain, many applications simply need to be auditable, with far fewer systems holding the entire Factom History.  Thus Factom significantly reduces the resources required to process transactions while providing nearly instant transaction clearing.  Federated FactomChain Servers provide for distributing FactomChain processing, load balancing, real time audits to insure honesty, and redundancy to insure availability.

Initially, FactomChain servers will provide APIs to query information from the FactomChain as needed.  Tools for analyzing the FactomChain and torrents for distributing the FactomChain will also be provided.  As technologies such as MaidSafe and the SAFE Network come online, then FactomChain data can be published there in a way that insures all the Factom Blocks are available going forward, despite the fate of any particular FactomChain Server.

Yet even if the data in FactomChain servers expand to many terabytes in size, the validity of Factom Entries and particular Factom Chains are only going to require a small portion of that data.

#How Factom Works

![Figure 1](images/fig1.png)

*Figure 1: Diagram showing that Factom Blocks are linked together, and the hash of each Factom Block is inserted into the Bitcoin blockchain.*

The proof of existence hashes are held within a series of Factom Blocks.  Every so often, the current Factom block is hashed, and that hash is inserted into the Bitcoin blockchain, as shown by Figure 1.  The periodic hash is all that is inserted into the blockchain.  With the single hash, the Factom Block can be provably unalterable (as it would break the hash recorded in the blockchain).  We are looking at different ways to create a link to this hash from the Factom block. 

A Factom Block is created immediately after the previous Factom Block is slated to have its Hash submitted to the blockchain.  A new Factom Block begins with a Block ID (one greater than the last).

![Figure 2](images/fig2.png)

*Figure 2:  Internal structure of a Factom Block.*

As each Factom Entry is submitted, it is added to the Factom Block, along with a type, and a timestamp.  For a simple proof of existence entry, the type will be 0.  Other types provide indexes and information that link to information held in entries and chains.

#A Simple Factom Entry

Any number of Factom entries can be added to a Factom Block, and remain secured by the Bitcoin blockchain.  This vastly reduces the overhead of Factom functions on the blockchain without significant loss of security for the Factom entries themselves.  We will discuss how the Factom Blocks are published in a later section.  But suffice it to say that anyone holding a copy of a Factom Block can prove its validity by simply providing the Bitcoin Transaction holding the block’s hash.  The block could not possibly have been constructed after the fact (as fitting a block’s contents to produce an existing hash is quite out of the question).  The Bitcoin Transaction holding the Factom Block’s hash + a copy of the Factom Block will fix the existence of a document at a point in time, and prove the document has not been altered.

![Figure 3](images/fig3.png)

*Figure 3: Internal structure of a Factom Entry*

Figure 3 shows a simple Factom Entry.  It is composed of structured data (pretty much whatever data the user wants to provide), a reverse hash (a token system used by Factom to control access) and one or more signatures.  A simple entry does not receive any validity checking by the FactomChain server outside of verifying the signatures, if any are provided.  The user provides the entry, structured data, and the signatures (if desired) for the structured data.  If signatures are provided, but do not validate against the structured data provided, then the entry will be rejected. The FactomChain hashes the entry and signatures, then adds that hash to the Factom block (per figure 2).  The Factom block adds the entry type 1 (simple entry) and the time stamp at the Factom block level.

While a user can use the Structured Data section to implement a range of protocols like tokens, smart contracts, smart properties, etc., Factom provide some generic support for these features.  The support for Factom within FactomChain servers is necessary to make the FactomChain Servers auditable in real time for many common functions by its users, and by other Federated FactomChain Servers.   Federated FactomChain servers provide the redundancy and cross checking required for the security of many applications that may wish to run on top of Factom.


# How to Create a Factom Chain

Factom Chains are chains of Factom Entries. A Factom Chain provides the infrastructure for managing smart contracts, token counts, alternative currencies, etc.  

![Figure 4](images/fig4.png)

*Figure 4: Structure of the first link in a Factom Chain, i.e., a chain of Factom entries*

A Start Link begins a Factom Chain.  It looks just like a simple entry, but is typed as a chain.  (The specification for the types for chains is under discussion.) The Structured Description must include a “VScript” entry.   Many chains could be validated privately.  In other words, the validation rules for the chain can be published (and notarized via the Start Link) and any attempt to fraudulently add links to the chain are invalidated by the rules published by the parties starting the FactomChain.  In fact, a reference implementation of an application that validates a FactomChain should be hashed and secured in the Start Link for a FactomChain. That application in combination with the published rules for the FactomChain, rather than the FactomChain server, would be responsible for validating that FactomChain. 

Still, there is some use in creating an Account FactomChain supported by FactomChain servers, if for no other reason than to allow the group purchase of Factom entries by users of Factom.   Because of the reduced overhead of Factom, these can be made available at rates far cheaper than Bitcoin Transactions.

An Account FactomChain is enforced by the FactomChain Server.  And it serves as an example for creating user-defined chains.  The Start Link for an Account Factom Chain might look like this:

```
NE Type: 	Start Link
Structured Description:	{  
    "vscript" : "<sig> <pubKey> OP_CHECKSIG"
    "val" : 1000 }
Signature:	<sig> 
```


The Validation Script must evaluate to true for any link that would directly follow the Start Link in the FactomChain.  The FactomChain script will implement a subset of the operators defined by Bitcoin, and a few additional operators.  For example, there is no need to implement OP_RETURN, as users can add whatever data they wish to Factom Entries.  Also, the FactomChain will implement a OP_USER.   This operation will return true immediately as far as the FactomChain servers are concerned.  But any following operations will be defined as the user sees fit.  Thus they can provide an application that follows the rules that user cares to implement.  OP_USER is only allowed in a type USER FactomChain.

#Creating Links in a FactomChain

Following the Start Link is a series of Factom Entries of Type Link.

![Figure 5](images/fig5.png)

*Figure 5:  A link in a Factom Chain*

A Factom Link points back to its parent links.  The Validation Script (part of the structured data) must evaluate to true, or the FactomChain service will not add the link to the Factom Block.  A USER FactomChain can possibly accept invalid entries, so it is critical for a FactomChain of type USER to make use of clear FactomChain rules and perhaps a reference application for entry validation in order to ignore invalid entries.

#FactomChain Servers

FactomChain servers are federated under one of the FactomChain servers, the Master Factom server.  They register their Factom Blocks with the Master Factom server, and validate the other Factom servers.  Payments for Factom services are managed with Factom Chains, and accounts are settled by payments that are made periodically.   Payments can be in bitcoin, various alt currencies, or even traditional currencies (though that is less likely).  Half of a payment for Factom services should go to the Factom Server accepting payment, and the other half distributed to all the Factom servers providing auditing services.

Each Factom Server must provide access to their Factom Blocks to the other Factom Servers as well as to their users and customers.  For now, access can be provided via websites and torrents.  In the future, they can be provided by MaidSafe and the SAFE Network. 

#Crowd Funding
Factom will use a token system for paying for entries to be placed into Factom blocks secured by Factom.  Some token is necessary to prevent spamming or attacking the system.  

##Factom Coins (XNC)
Factom Coins will be used for paying to create FactomChain Specifications, start new Factom using those specifications, and adding entries into Factom.  Factom Coins will be tracked in a Factom Chain, and will be generated to provide incentives for running the Federated Factom Chain servers, run independent audits, and other behaviors.  Because Factom Coins are tracked on Factom Chain servers directly, they can be used to automate payments for entries and chains directly.

We plan to fund the development of Factom using their tokens.  While we are building the infrastructure, we will use the Mastercoin Protocol as a temporary representation of the Factom Coins as Master Factom Coins.  Once the launch of Factom Chains is final, the Master Factom Coins will be converted to native Factom Coins. The outline of the distribution of Factom Chains is still being discussed, but a possible structure is as follows:

* Algorithm:  Mastercoin Protocol 
* Block Time: 10 minutes
* Total Coins: 10,000,000 XNC
* Coin Distribution:
 * 10% -- Auditing
 * 10% -- Core Developers
 * 10% -- Crowd Sale Participation
 * 20% -- Third Party Developers
 * 50% -- Federated SErvers

# Disclosures
1. FactomChain coins (XNC) are not a Stock or Equity.  Participation in the crowd sale will not provide you with a "security" or "equity" stake in this 
project. The digital token known as Factom Coins is only useful for creating and using Factom Chains on Factom Chain servers after development is complete. 

#Bibliography

"Bitcoin." / Mailing Lists. Accessed May 27, 2014. http://sourceforge.net/p/bitcoin/mailman/message/32108143/.

"Could the Bitcoin Network Be Used as an Ultrasecure Factom Service?" Computerworld. Accessed May 27, 2014. http://www.computerworld.com/s/article/9239513/Could_the_Bitcoin_network_be_used_as_an_ultrasecure_Factom_service_.

"Proof of Existence." Proof of Existence. Accessed May 27, 2014. http://www.proofofexistence.com/.

"Virtual-Factom." Virtual-Factom. Accessed May 27, 2014. http://virtual-Factom.org/.

[1] "Block timestamp" Accessed Sep 12, 2014. https://en.bitcoin.it/wiki/Block_timestamp

[2] "OP_RETURN and the Future of Bitcoin" Accessed Sep 12, 2014.  http://bitzuma.com/posts/op-return-and-the-future-of-bitcoin/
