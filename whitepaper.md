Factom
============

Abstract
--------

Factom separates the promise of the Bitcoin Blockchain from the currency aspects of Bitcoin.  Factom is an open source project which leverages the irreversible security of the Bitcoin Block Chain ("blockchain") to allow users to create their own, personal, provably immutable ledgers. All the users of Factom submit their entries to Factom, where the entries are combined and organized.  The entire set of data is distilled to a single hash every 10 minutes, and that hash is placed in the Bitcoin blockchain.  The data collected by Factom is published both immediately over a peer to peer network of nodes, as well as being downloadable.

Factom provides a mechanism to create audit trails for business processes that do not necessarily monetary transactions.   Using techniques such as provable secrets, Factom can provide for cryptographic audits, while preserving privacy.

Introduction
------------

Factom structures the entries submitted to factom so that a simple proof of existence can be constructed using only the Bitcoin blockchain and a series of hashes.   A hash of any digital artifact is cryptographically unique. (The odds of a collision under sha256 are currently considered vanishingly small)  The proof of existence provided by Factom for an entry leverages this feature of hashes.  To enable such proofs, Factom builds  a level of independence between entries as Factom creates its structures that makes such proofs possible.  The arrangement of Entries allows users to download only the data subset they are interested in, and still be able to create more complex proofs on their data, such as proofs of the negative (the hash of this document is not in the ledger).
 
Factom is run on a system of distributed servers.  The servers implement a consensus mechanism which supports real time audits, and provides users assurance that the servers are implementing the “record all entries” policy required of Factom servers. Other audits ensure the proper construction of state in real time. This system of audits is referred to as Proof by Audit. 

One objective of the Factom project is to provide users the ledgers they need to support their applications.  

Factom can be used to manage transactions.  Omni Wallet can use Factom to document the transfer of value across blockchains.  Protocols like, Counterparty and MasterCoin can use Factom to actually implement and run their protocols.  Factom is an especially good fit for Counterparty and MasterCoin since their protocols run client side already.  And the exchange of tokens representing real time assets can be done on Factom, simulating Colored Coins.

Factom can be used to simply record events.  Tracking the history of art work has a transactional component (i.e. who owns the work, what rights do they have, when do such rights expire, etc.).  But also art is displayed at various shows, appears in various media (movies, T.V. shows,  advertisements, album covers, book references, etc.).  Documenting the stories around art is nearly as important as the art itself.  Factom can be used to create the history.   Similar histories are needed for documenting pedigrees, appearances, awards, owners, etc. for  show horses, dogs, etc.   And there is just the simple logging of mortgage statements, security camera footage, messages, sensor data, etc.   

Factom can hold data directly, or it can hold hashes of such data to allow verification and validation of data held in distributed computer systems.  Archival services can be built upon Maid Safe, StorJ, conventional databases, torrent networks, etc. and the data validated against the chain in Factom. 

Factom can provide support for settlement between systems of record.  Factom aims to appeal to players not yet leveraging the security of the blockchain such as major banks, exchanges, financial institutions, and governmental actors each of whom have “systems of record” which is difficult to reconcile across the many systems of record held by other institutions.  Such organizations would benefit vastly by securing their data to the blockchain, and documenting their business processes on the blockchain in a cryptographically auditable way.

Factom Goals
--------------

When Satoshi Nakamoto launched the Bitcoin blockchain he revolutionized the way transactions were recorded. There had never before existed a permanent, decentralized, and trustless ledger of records. Developers have rushed to create applications built on top of this ledger. Unfortunately, they run into a few core problems that were part of the original design tradeoffs when the blockchain was launched:

1)    Speed – because of the design of the decentralized, proof of work consensus method used by Bitcoin, difficult requirements are adjusted to maintain roughly 10 minute confirmation times.  Then because blocks can be orphaned by blocks with greater proof of work values, some number of confirmations may be required for security.  Many applications can’t deliver a practical user experience with this time constraint.

2)    Cost – the current minimum transaction cost is around 10 Bits (or roughly $0.005 USD). The exchange price of Bitcoins has increased approximately 500% in the last 12 months ending August 2014, and is projected to continue to increase long term. This provides a serious cost barrier to applications that need to manage millions of transactions. (For conversions between USD, BTC, mBTC, and bits, check out this [Bitcoin Price Converter](http://youmeandbtc.com/bitcoin-converter/).) In addition with the propagation of [Bitcoin Core 0.10 version “floating fees”](https://bitcoinfoundation.org/2014/07/floating-fees-for-0-10/ ) are likely to increase transaction fees as the number of transactions continues to increase. 

3)    Bloat – the Bitcoin blockchain currently has a 1 MB block size limit which caps it at 7 transactions per second. Any application that wants to write and store information using the blockchain will add to the traffic. This problem has become politically charged as developers seek to use Bitcoin in various ways to (sometimes inefficiently) encode information into the Bitcoin blockchain.

Factom is a protocol designed to address these three core problems. Factom creates a Protocol Stack for Bitcoin 2.0 applications that constructs a simple, standard, effective, and secure foundation for these applications to run faster, cheaper, and bloat-free.

------------

Bitcoin is disrupting the status quo for online payments.  With Bitcoin, payments can be made worldwide without any centralized party.  The success and elegance of Bitcoin has inspired many others to seek ways of decentralizing more than just payment systems.  Many have observed that the blockchain could enable the trading of commodities, trading of assets, issuing  securities, implementing self enforcing smart contracts, crowd sourced loans, etc.  The set of such extended applications is often referred to as "Bitcoin 2.0".

Factom simplifies how Bitcoin 2.0 applications can be deployed.  Factom does so by providing a few simple operators from which many more complicated designs can be built.  Factom extends Bitcoin beyond the exchange of bitcoins to include the recording and management of arbitrary events, and chains of such events.

Consider what any Bitcoin 2.0 application requires:

* A set of public or private events
* An unforgeable ledger recording and ordering entries
* Support for unambiguous audits of the ledger, ensuring internal consistency
* The ability to determine the state(s) of participants based on the ledger

Factom is designed to both meet and support the implementation of systems having these requirements.




Theory of Operation
------------

Factom extends Bitcoin's feature set to record events outside of monetary transfers.  Factom has a very minimal rule set for adding permanent entries.  This is a double edged sword.  Factom allows data to easily be entered into the record.  The drawback is Factom cannot be relied on to ensure validity.  

Factom has a few rules regarding financial compensation for running the network, and some internal consistency rules, but cannot check the validity of statements recorded in the chains used by its users.

Bitcoin only allows transactions to be recorded which correctly move value from a set of inputs to a set of outputs.  Satisfying the script required of the inputs (generally requiring certain signatures) is enough for the system to ensure validity.  This is a validation process which can be automated, so the audit process is easy.  If Factom were used, for instance, to record a deed transfer of real estate, numerous rules exist for the transfer.  A local jurisdiction may have special requirements for property owned by a foreigner.  A cryptographic signature alone is insufficient to fully verify the validity.  Factom is unable to check legitimacy of such a transfer, and so doesn't try.

Bitcoin miners perform two jobs, amongst others.  First, they resolve a double spend.  Seeing two conflicting transactions which spend the same value twice, they decide which one is legitimate.  The second job they perform is auditing.  Since Bitcoin miners only include valid transactions, one that is included in the blockchain can be assumed to be audited.  A light client does not need to know the full history of Bitcoin to see if value they receive has already been spent.  Having miners audit transactions has the disadvantage of making Bitcoin fragile when updating the transaction rules.  A disagreement on auditing among miners would create a chain fork.  If very few miners split away, Bitcoin would hardly notice.  If the split broke away a significant number of miners, it would disrupt the Bitcoin economy.

Factom splits the two jobs: entry ordering/recording and entry auditing/validation.  The Factom servers accept entries, and assemble them into blocks, fixing their order by broadcasting receipts.  After a few minutes, the transaction ordering is fixed by the Bitcoin blockchain.  The auditing is a separate process which can be done either with or without trust.  Auditing is critical, since Factom does not block writing invalid entries to a Factom chain.  

With trust based auditing, a light client would trust a competent auditor or auditors of their choice.  After an entry was entered into the system, an auditor would verify the entry was valid.  Auditors  would submit their own entry signed cryptographically.  The signature would show that the entry passed all the checks the auditor thought were required.  (The audit requirements could in fact be part of a Factom chain as well.)  In the real estate example from earlier, the auditor would double check the transfer conformed to local standards.  They would publicly attest that the transfer was valid.

Trustless auditing would be similar to Bitcoin.  If a system is as easy to audit as Bitcoin, it also could be audited programmatically.  If the rules for transfer were able to be audited by a computer, then an Application could download the relevant data and run the audit itself.  The application would build an awareness of the system state as it downloaded, verified, and decided which entries were valid or not.

Mastercoin has a similar trust model.  Mastercoin transactions are embedded into the Bitcoin blockchain.  Bitcoin miners do not audit them for validity, therefore invalid Mastercoin transactions can be inserted into the blockchain.  The Mastercoin wallet scans through the blockchain and finds potential Mastercoin transactions.  It then checks them for validity, building an interpretation of which addresses own which assets.  It is up to the Mastercoin wallet to do its own auditing.  Software development is a little more forgiving with this arrangement.  If a software bug causes an incompatibility, interpretation can be changed after the fact instead of disrupting ongoing operations.

Bitcoin, Mastercoin, land registries, and many other systems need to solve a fundamental problem: proving a negative.  They prove something has been transferred to one person, and that it hasn't been transfered to someone else first.  Mastercoin solves this problem by limiting the places where Mastercoin transactions can be found.  Mastercoin transactions can only be found in the Bitcoin blockchain.  If a relevant transaction is not found in the blockchain, it is assumed not to exist and the asset hasn't been sent twice (double spent).

Certain land ownership recording systems are similar.  [[1](http://en.wikipedia.org/wiki/Recording_%28real_estate%29)]  Assume a system where land transfer is recorded in a governmental registry and the legal system is setup so that unrecorded transfers are invalid.  If an individual wanted to check if a title is clear, that no one else claims the land, the answer would be in the governmental registry.  They could prove the negative; the land _wasn't_ owned by a 3rd party.  Where registration of title is not required, the governmental registry can only attest to what has been registered.  A private transfer might very well exist that invalidates the understanding of the registry.

In both of the above cases, the negative can be proven because only when transfers exist within a defined space.   A land transfer recorded in a different jurisdiction 1000 miles away would not have a valid prior claim in the above example.  

In Factom, there is a hierarchy of data classification.  This differs from Bitcoin where every entry is potentially a double spend.  The hierarchy allows Applications to have smaller search spaces than if all Factom data were combined together into one ledger.  

If Factom was used to manage land transfers, an application using a chain to record such registries could safely ignore Entries in chains used to maintain security camera logs.

Nick Szabo has written about Property Clubs, which have many overlaps of this system.  Here is a nugget from his paper "Secure Property Titles with Owner Authority"

`While thugs can still take physical property by force, the continued existence of correct ownership records will remain a thorn in the side of usurping claimants.` [[2](http://szabo.best.vwh.net/securetitle.html)]



Factom
------------

At its heart, Factom is a decentralized way to collect, package, and secure data into the Bitcoin blockchain.  Factom accomplishes this with a network of federated servers.  These servers rotate responsibility for different aspects of the system.  No single server is ever in control of the whole system, but only a part of the system.  And no server is permanently in control of a part of the system; the responsibility for any part of Factom cycles over the servers.

Factom implements a Protocol Stack for Bitcoin 2.0 Applications.  The layers in this stack are:

1) Timestamping Layer

2) Factom Layer

3) Entry Block Layer

4) Entries

5) Factom Chains

6) Applications

**Timestamping**

![timestamping](images/Whitepaper---Factom---Proof-of-Existance-Layer.png)

Factom data is timestamped and made irreversible by the Bitcoin network.  User's data is as secure as any other Bitcoin transaction.  A compact proof of existence is possible for any data entered into the Factom system.  The Bitcoin entry is also a key to query a peer-to-peer Distributed Hash Table (DHT, similar to BitTorrent) in order to retrieve all the data which was timestamped.

Data is organized into block structures, and combined via a Merkle trees.  Every 10 minutes, the data set is frozen and submitted to the Bitcoin network.  Since Bitcoin has an unpredictable block time, there may be more or fewer than one Factom timestamp per Bitcoin block.

Bitcoin internal header block times themselves have a fluid idea of time.  They have a 2 hour flexibility from reality [[3](https://en.bitcoin.it/wiki/Block_timestamp)].  Factom will provide its own internal timestamps which conform with standard time systems.  Since Factom places high importance on timestamping, it will be a closely audited part of the system.

The user data ordering will be assigned when received at the server.  Factom organizes the submitted entries into blocks.  The block time for Factom is a minute.  On closing, the federated server network generates consensus and and the entries that are part of that block are timestamped to that minute.   

As a general note, the data could have existed long before it was timestamped.  An application running on top of Factom could provide finer and more accurate timestamping services prior to entries being recorded in Factom.  The Factom timestamp only proves the data did not originate after the Factom timestamp.

The Merkle Root for the Factom block is entered into the Bitcoin blockchain with a spending transaction.  The spend includes an output with an OP_RETURN.   We refer to this as “staking” the Factom blocks to the Bitcoin blockchain.  This method is the least damaging to the Bitcoin network of the various ways to timestamp data [[4](http://bitzuma.com/posts/op-return-and-the-future-of-bitcoin/)].  The first eight bytes of the available 40 in the stake will be a tag (“FB”) and a block height.  The designator tag indicates the transaction could be a Factom entry.  Other qualifiers are required, but the tag and Factom block height eliminates most of the OP_RETURN entries that would otherwise need to be inspected.  

The block height in the OP_RETURN helps to fix the order in those cases where the Bitcoin blockchain records the stakes out of order.

The Merkle Root timestamp will be entered into the Bitcoin blockchain by one of the members in the federation.  The server delegated to timestamp the federation’s collected data creates a small BTC transaction.  The transaction will be broadcast to the Bitcoin network, and be included in a Bitcoin block.  Bitcoin transactions that look like Factom entries, but are not spent from an address known as a Factom server would either be junk, or an attempt to fork Factom.  Most users/applications will ignore such entries.

Bitcoin blocks are generated with a statistical process, as such, their timing cannot be predicted.  This means that the stakes are only roughly bound by the entries inserted into the Bitcoin blockchain, and thus the Bitcoin timestamping system.  The real value of staking Factom to Bitcoin is to prevent anyone from generating false Factom histories.  Due to bad luck of Bitcoin miners, or slow inclusion of Factom transactions, there could easily be as much as an hour from when the Factom state is frozen for a particular 10 minute period and when the Bitcoin transaction that secures that Factom block is mined into a Bitcoin block.


**Factom Layer**

![Factom Layer](images/Whitepaper---Factom-Layer-Diagram.png)

The Factom layer is the first level of hierarchy in the Factom system.  It defines which Entry Chain IDs have been updated during the time period covered by a Factom Block.  It mainly consists of entries pairing a Chain ID and the Merkle root of the Entry Block containing data for that Chain ID.

If an Application only has the Factom Blocks, it can find Entry Blocks it is interested in without downloading every Entry Block.  An individual application would only be interested in a small subset of Chain IDs being tracked by Factom.  This greatly limits the amount of bandwidth an individual client would need to use Factom as a system of record.  For example, an Application monitoring real estate transfers could safely ignore video camera security logs.

Factom servers collect Merkle roots of Entry Blocks and package them into a Factom block.  The Factom block is then hashed by computing a Merkle tree, and the Merkle root is recorded into the Bitcoin blockchain.  This allows the most minimum expansion of the blockchain, yet the ledger itself becomes as secure as Bitcoin itself.

**Entry Block Layer**

![Entry Block Layer](images/Whitepaper---Entries-Blocks-written-as-Factom-Blocks.png)

Entry Blocks are the second level of hierarchy in the system.  Individual Applications will pay attention to various Chain IDs.  Entry Blocks are the place where an Application looking for transactions can expand its search from a Chain ID to discover all possibly relevant entries.  

There is one entry block for each updated Chain ID per Factom block.  The Entry Blocks contain hashes of individual Entries.  The hashes of Entries both prove the existence of the data and give a key to find the Entries in the DHT network.  

The Entry Blocks encompass the full extent of possible entries related to a Chain ID.  If an Entry is not entered into a Entry Block, it can be assumed not to exist.  This allows an Application to prove a negative, as described in the Theory of Operation.  

The Entry Block intentionally does not contain the Entries themselves.  This allows the Entry Blocks to be much smaller, than if all the data was grouped together.  Separating the Entries from the Entry Blocks will also allow auditing auditors to be easier.  An auditor can post Entries in a separate chain which approves or rejects Entries in a common chain.  The audit can add reasons for rejection in Entry.  If an Application trusts the auditor, they can cross reference that the auditor has approved or rejected every entry, without knowing what the entry is.  The Application would then only attempt to download the Entries which passed the audit.  Multiple auditors could reference the same Entries, and the Entries would only exist once on the DHT.  Some entries are expected to be larger than the mere 32 bytes a hash takes up.  Lists of things to ignore do not have to have the full object being ignored for an Application to know to ignore it.

An Entry detailing the specifics of a land transfer would be entered into a chain where land transfers of that type are expected to be found.  One or more auditors would then reference the hashes of land transfer in their own chains, adding cryptographic signatures indicating a pass or fail.  The land transfer document would only need to be stored once, and it would be referenced by multiple different chains.  

**Entries**

![Entries](images/Whitepaper---Hashes-and-Data-are-Written-to-Entry-Blocks.png)

Entries are user generated pieces of data collected by the Factom servers.  They can be either public or private Entries.  A private Entry would be a hash of a document.  This would be basic proof of existence.  Something could be timestamped and later proven it existed before a certain time.

The interesting Entry would be a public ones.  There is lots of flexibility in the data that is accepted.  It can short like a hash of a document, photo, etc.  It could also be larger, but not too large, since fees limit the size of the data accepted.  This is similar to Bitcoin.  Extremely large 100kB+ transactions are possible, but would need to pay an exorbitant transaction fee.  This size, while gigantic in Bitcoin, would be moderately sized for Factom.  Since every Bitcoin full node needs the entire blockchain to fully validate, it needs to stay small.  In Factom, only the highest level Factom Blocks are required by everyone.  If someone is not specifically interested in a Chain's data, they would not download it.

Take a simple example of an uneditable Twitter style system.  A celebrity would craft an Entry as a piece of text.  They would then sign it with a private key to show it came from them.  Followers of the celebrity would find which Factom Chain they publish in and would monitor it for updates.  Any new signed entries would be recognized by follower's Application software as a tweet.  Others could tweet at the celebrity by adding entries to their Factom Chain.

One example with a more pressing need is another home for Mastercoin.  In addition to the blockchain, Mastercoin transactions could be placed in a special Mastercoin designated Factom Chain.  Software like Omni wallet would scan both the Bitcoin blockchain as well as the specific Factom Chain.  A User could enter a Mastercoin transactions in the Factom Chain indicating that some asset should be transferred.  It would have the same long term unalterable security of Bitcoin with faster confidence of confirmation and the entry itself would be cheaper.  If the worst happened to Factom, Mastercoin transactions would still be valid on the raw blockchain.

**Factom Chains**

Factom Chains are sequences of Entries that reflect the events relevant to an Application.  These sequences are at the heart of Bitcoin 2.0.  Factom Chains document these event sequences and provide an audit trail recording an event sequence occurred.  With the addition of cryptographic signatures, those events would be proof they originated from a known source.

Factom Chains are logical interpretations of data placed inside Factom Blocks and Entry Blocks.  The Factom Blocks indicate which Chains are updated, and the Entry Blocks indicate which Entries have been added to the Chain.  This is somewhat analogous to how Bitcoin full clients maintain a local idea of the UTxO (Unspent Transaction Output) set.  The UTxO set is not in the blockchain itself, but is interpreted by the full client. 

**Applications**

Application is a generic term for user side software which reads from or writes to the Factom system.  It could be software with a human interface, or could be completely automated.  The Application is interested in the data organized by the Factom Chains it needs.  

Applications are possibly distributed applications running on top of Factom to provide additional services.  For example, one might imagine a trading engine that processes transactions very fast, with very accurate timestamping.  Such an application may none the less stream transactions out into Factom chains to document and secure the ledger for the engine.  Such a mechanism could provide real time cryptographic proof of process, of reserves, and of  communications.

Another application may provide an exchange of Bitcoin or even conventional credit cards for Factom tokens.  Using such a "Vending Machine", users could buy entries to be used in Factom without ever owning the Factom Tokens that drive the Factom servers.  And yet such a service is decentralized, in the sense that no application is forced to use a particular "Vending Machine," even if such applications are run by centralized parties.

-----------

Factom Chains
---------------

**Naming Chains**

Factom groups all Entries under a ChainID.  The ChainID is computed from a Chain Name.  The ChainID is a hash of the Chain Name.  The Chain Name is a byte array arbitrarily long in length.  See figure **How to compute a ChainID**.  Since the conversion from Chain Name to ChainID is a hash operation, it is a simple operation.  Deriving a Chain Name from a ChainID is not simple, so a lookup table would be needed.

The Chain Name is fairly arbitrary.  It could be a random number, a string of text, or a public key.  An individual Application could derive meaning from different Chain Names.

One possible convention would be to use human readable text for the Chain Name.  This would allow for the structuring of Factom Chains in a logical hierarchy, even though Factom Chains are not hierarchical by nature.  Users can even use the same naming conventions, but by making simple modifications, ensure that there are no accidental intersections between their chains and other chains.  Consider the following path:


* MyFavoriteApp/bin

Where the slash is a convention separating ASCII strings “MyFavoriteApp” and “bin”.  These two strings must be converted to bytes, and there are many options for doing so.  The strings could be encoded in UTF-16, UTF-32, ASCII, or EPCIDIC.  Each of those would result in entirely different ChainIDs for the same string.  Furthermore, the application could utilize a nonce (an arbitrary number) as the first byte array in their naming convention. (i.e. the byte arrays would be the nonce, followed by “MyFavoriteApp” then “bin”.   The use of a nonce, or a GUID of some sort, allows for instance specific chain addressing that is none the less provable within a specified convention.

**Chain Validation**
Factom doesn’t validate entries; entries are instead validated client side by users and applications.  As long as an application understands and knows the rules a chain should follow, then the existence of invalid entries doesn’t cause unreasonable disruption.  Entries in a chain that do not follow the rules can be disregarded by the Application. 

Users can use any set of rules for their chains, and any convention to communicate their rules to the users of their chains.  The first entry in a chain can hold a set of rules, a hash of an audit program, etc.   These rules then can be understood by applications running against Factom to ignore invalid entries client side.

An enforced sequence can be specified.  Entries that cannot meet the requirements of the specified enforced sequence will be rejected.  However, entries that might be rejected by the script or the app will still be recorded.  Thus users of such chains will need to run the app or script to validate a chain sequence of this type. The Factom servers will not validate using the script or app.

Factom’s client side validation (in combination with user defined chains) provides a number of advantages for applications written on top of Factom.  

1) Applications can put into Factom whatever entries makes sense for their application.  So a list of hashes to validate a list of account statements can be recorded as easily as exchanges of an asset.

2) Execution of rules is far more efficient, since the only systems running those rules are those systems that care about those rules.   Factom allows a chain to define its rules in whatever language the designers choose, to run on whatever platform they choose, and use any external data.   None of these decisions on the part of one application has any impact on another application.

3) Factom Servers have little knowledge about the entries being recorded.  This makes Factom’s role in recording entries very simple, and very easy to audit;  hiding bad behavior on the part of the Factom servers is very difficult to do.

4) Recording speeds can be very fast, since the number of checks made by the Factom Servers are very few.  

5) Proofs against any particular chain in Factom do not require knowledge of any other chains. Users then only need the sections of Factom they are using, and can ignore the rest.


*Applications*

Factom enables the Distributed Autonomous Applications (DAPPs) and Distributed Autonomous Organizations (DAOs) to implement distributed ledgers.  These ledgers allow distributed applications to maintain an understanding of the past.  But even everyday sorts of uses can be facilitated as well, like simple movie tickets or arcade tokens.  Factom Chains can support:

* Crowd sourcing loans
* Issuing securities and paying dividends
* Powerful scripted chains with functionality like Ethereum, Monero, Darkcoin, etc.
* Smart Contracts
* Smart Properties
* Event ticketing

#Discussion

Using Bitcoin to prove the existence of a document (really any digital asset, like a tweet, a web page, a spreadsheet, a security video, a photo, etc.) is a concept that is well known.  (See the references at the end of this document).  And some have even suggested that a service could be created to take a list of signatures, compute a Merkle root, place that in the Bitcoin blockchain.  This not only provides the same security for the user wishing to prove a document’s existence, but limits the “blockchain pollution” of pushing a hash into the blockchain for every signed document.  There are at least a couple of online websites that provide these services.

Factom provide for simple “proof of existence” entries.  In addition, Factom provides proof of transformation, i.e. a progression of entries in a Factom Chain.  While clients are responsible for the actual validation of the entries in a chain, Factom enables the unambiguous validation by applications solely by faithfully recording the entries.   

Factom can be used by its users to implement token systems, asset trading systems, smart contracts, and more.   

**How Factom differs from Bitcoin**

Factom is very different from Bitcoin, and in fact very different from any altcoin.

Cryptocurrencies like Bitcoin implement a strict, distributed method for the validation of transactions, where anyone can validate each transaction, and the validity of every input into a transaction can be verified.  Because each transaction is authorized via cryptographic signatures, no transaction can be forged.  Each transaction can be checked for validity by verifying signatures of each transaction, and the miners hold each other accountable for only including valid transactions.

The Bitcoin protocol is transactionally complete.  In other words, the creation and distribution of Bitcoins through transactions is completely defined within the Bitcoin protocol.  Transactions (which specify movement of bitcoin) and block discovery (which move bitcoin via mining fees and provide block rewards) are the only inputs into the Bitcoin Protocol, and nothing leaves the Bitcoin Protocol. In other words, the 21 million Bitcoin that will ultimately exist will always and forever exist within the protocol.  (Well, at least until side chains are implemented, which will provide additional movement of Bitcoin value in and out of side chains.)

Many different groups are looking to find ways to leverage the Bitcoin approach for managing other sorts of transactions besides tracking bitcoin balances.  For example, the trading of assets such as houses or cars can be done digitally using Bitcoin extensions.  Even the trading of commodities such as precious metals, futures, or securities might be done via clever encoding and inserting of information into the Bitcoin blockchain.  

Efforts to expand Bitcoin to cover these kinds of trades include Colored Coins,  Mastercoin, and Counterparty.  Some developers choose to build their own cryptocurrency with a more flexible protocol that can handle trades beyond currency.  These include Namecoin, Ripple, Etherium, BitShares, NXT, and others.  Open Transactions uses Cryptographic signatures and signed receipts and proof of balance for users (i.e., a user does not need the transaction history to prove their balance, just the last receipt).

The great advantage to an independent platform over trying to build upon Bitcoin is found in flexibility.  The Bitcoin protocol isn’t designed to allow recording of arbitrary entries or data, so the “bookkeeping” necessary to non-Bitcoin type transactions isn’t necessarily supported by Bitcoin.  Furthermore, Bitcoin’s Proof of Work (PoW) based consensus method is not a “one size fits all” solution, given that some transactions must resolve much faster than 10 minutes.  Ripple and Open Transactions vastly speed up confirmation times by changing the consensus method.  

An Application built upon Factom seeks to gain the ability to track assets and implement contracts, while gaining the advantage Bitcoin’s security.  Instead of inserting transactions into the blockchain (viewed as “blockchain pollution” by many), Factom records its entries within its own structures.  At the base level, Factom records what chains have had entries added to Factom within the Factom block time.  Scanning these records, applications can pick out the chains they are interested in.  Factom records each chain independently, so applications can then pull the chain data they need.  

Periodically Factom inserts a hash of the Factom state into the Bitcoin blockchain, staking Factom to Bitcoin. The “stake” is a Merkle root of the data collected by Factom since the stake.  The stakes are set with a predictable set of Bitcoin addresses, so forking of Factom is obvious via a review of the Bitcoin blockchain.  Furthermore, once Factom is staked to Bitcoin, modifications of the Factom ledger are not possible without causing a failure to validate, i.e. breaking the stakes.

Factom is organized in a way that minimizes connections between user chains.  A chain in Factom can be validated without any of the information held in other, unrelated chains.  This minimizes the information a Factom user has to maintain to validate the chains they are interested in.  A Factom node can communicate small data sets to users, utilize a combination of mathematical proofs and hashes within the Factom, and the stakes in Bitcoin to prove validity of that data set.  

A user only needs the artifacts in the Factom Chain of interest rather than the full set of data ever entered into the system.

*Factom Federated Servers*

Factom will be run on a set of federated servers.   The servers will be elected by the users of Factom, and will be rewarded based on the strength of their support.   Users will log their report by tying their entry keys to a server.  Doing so will provide returns from the server.  The function used to compute the ranking of the servers will be a function of the following:

Factom allows for reactive security.  A Factom server cannot fail to log entries without immediate detection other Factom servers and by the users themselves.  Since only one of the Factom servers is puts the Merkle root in the Bitcoin blockchain, the servers need to cooperate. 

Factom servers by default are ignorant of the significance of any entry into Factom.  The management and regulation of a Factom Chain is left to the users of that chain.  Factom is an automated, disinterested party to the transformations of a particular Chain.  

Initially, Factom servers will provide APIs to query information from the Factom servers as needed.  Tools for analyzing the Factom and torrents for distributing the Factom ledger will also be provided.  As technologies such as MaidSafe and the SAFE Network come online, then Factom data can be published there in a way that insures all the Factom structures are available going forward.

Even if the cumulative data in Factom servers expand to many terabytes in size, the Distributed Hash Table allows for segmentation of interested parties.  Parties intersed in Mastercoin could provide additional DHT servers giving high availability to those Entry Blocks and Entries.  This is similar to Bittorrent, where popular files are massively shared, even without financial incentive.

#How Factom Works

Factom collects Entries submitted from users and sorts them into Entry Blocks, based on the Entries specified ChainID.  Entries are hashed, and the Entry Blocks are a list of those hashes.  Once per minute, the entries that arrived are sorted, and added to a Factom Block.  The chain of Factom Blocks becomes a micro chain (a blockchain designed to be very small) that can be used to discover entry blocks, and from the entry blocks discover particular entries.  There is one entry block per ChainID per Factom Block. 

Every 10 minutes Factom is staked to the Bitcoin Blockchain.  The stake is a hash (a Merkle root) created from the 10 blocks created over that 10 minutes, and the stake is inserted into Bitcoin via Bitcoin’s OP_RETURN feature. This can be seen in Figure 1.  The periodic stake is all that is inserted into the blockchain.  With the single stake, the Factom Block becomes provably unalterable (as altering Factom’s ledger would break the stake to the Bitcoin blockchain).  

A Factom Block is created immediately after the previous Factom Block is slated to staked to the Bitcoin blockchain.  

As each Factom Entry is submitted, it is added to the Entry Block for that the entry’s ChainID. At the end of a minute, the Factom Block is created with a timestamp, a block height, and the Merkle Roots of each of the Entry Blocks created during that minute, sorted by ChainID. 

#A Simple Factom Entry

Any number of Factom entries can be added to a Factom Block, and remain secured by the Bitcoin blockchain.  This vastly reduces the overhead of Factom functions on the blockchain without significant loss of security for the Factom entries themselves.  A Factom server can provide proofs for the validity of a Factom Entry and a Factom block that are relatively small, and which do not require the application to trust the Factom server, nor replicate Factom’s data structures.  

An entry can be added to any chain in Factom by simply submitting the entry with signed with a key where the public key has some entry credit.

# Factom’s dual token 

Factom separates the rights to put entries into Factom from the Factom Token used to purchase those rights.  

The Factom Token is implemented in much the same way Bitcoin is implemented, allowing for multisig security, multiple inputs, multiple outputs, etc.  The Factom Tokens run on the Factom Token chain.  This chain is handled uniquely in Factom, in that entries in this chain must be valid Factom Token transactions, or the Factom Servers will reject the entries.  This is to prevent a spam attack on this chain, and to keep the processing of Factom Tokens as efficient as possible.

A Factom token is needed because the purchase of entries in Factom must be part of the protocol if we are going to completely decentralize Factom.  Furthermore, if each entry had to be individually purchased, the overhead of tracking the Factom Token payments for transaction fees would be very expensive in terms of the size of these transactions, as well as expensive computationally.   We also anticipate devices that need the right to write entries into Factom that shouldn’t have to bother with wallet software to do so.

The conversion of a Factom Token to entries will be done via a special purchase transaction on the Factom Token Chain.  This purchase transaction will include:

* An Output directing a Factom Token amount to be converted
* The public key that is to receive the entry rights

Any change will be directed to the address that held the Factom Token.

The conversion rate (Factom Token to Factom Entries) will be determined by an Oracle which maintains the conversion rate of Factom Tokens to Factom Entries at a cost 1/10 to 1/100 the cost of a Bitcoin Transaction.  When we have recruited enough exchanges to post exchange rates and volumes into Factom, we will establish a decentralized computation of the exchange rate.  The standard for publishing exchange information will be determined, and a user voting pool developed for determining which exchanges should be included in the computation.

The Entry chain(s) will then receive a Entry Right Purchase entry.  That entry will look like:

* Public Key
* Number of entries purchased

Then there will be two types of entry transactions:

* Create a Chain
* Create an Entry

## Create a chain

We preserve the first entry of every chain to the user that first creates the chain.  However, there are many ways to try and attack this purchase and deny the user this right. Through a clever set of revealed secrets, we can insure that the user that purchases the first entry can determine the contents of the first entry in the chain.

The call to submit a new chain requires a payment of 10 entries + 1 entry per 1,024 bytes.   This is to reduce spamming popular namespaces.  This submit to setup the creation of a chain includes three parameters:

* The Hash of the ChainID
* The Hash of (the ChainID + the Entry Hash)
* The Entry Hash

These three hashes are placed in an entry in the Entries chain.  

Now that the submit has been accepted, the commit can occur, and the ChainID is revealed.  For the commit to be valid, the commit must supply the name that hashes to produce the ChainID.  And the entry must hash to produce the Entry Hash.  And lastly, the concatenation of the ChainID with the Entry Hash must match the result in the submit.

If any of these conditions isn’t met, the chain isn’t created.

Because the ChainID is hashed, the ChainID is unknown.  Likewise, the hash of the ChainID concatenated with the Entry Hash does not reveal the ChainID.  And the Entry Hash doesn’t reveal the ChainID (even while the Entry must contain the ChainID).

An attacker can front run the submit, but to harm the user creating a chain, it must produce an entry that the user doesn’t want.  But because the attacker doesn’t have the ChainID, the attacker cannot produce the hash of (the ChainID + the Attacker’s Entry).  So the attacker is forced to wait for the attempt to commit.  But the user doesn’t have to commit until the acceptance is seen, assuring the user the submit has been recorded. 

Now the attacker can’t front run the submit, but the attacker can front run the commit.  So when the user submits the commit of the actual entry with the revealed chain name (and thus ChainID), the attacker can now form a valid submit and have it recorded, and then attempt a commit against their submit.

But here is the problem:  *The Attack is Obvious*.  Because when the attacker provides the ChainID in their commit, the earlier recorded submit can be validated, which invalidates the attacker’s.  So the attackers commit can be immediately rejected.

So the first user to successfully record a submit for a chain will get the first entry recorded.

For common namespaces, the attack remains where the attackers precompute userful names within the namespace.  Then when those names are about to be allocated, the attacker can successfully front run, because they can know the ChainID.  The suggestion we have is to include a nonce in the the namespace to prevent the dictionary attack.  In this case, the first entry of the name becomes a simple number, which selects a name space, and the second byte array of the name becomes the effective domain for the application.  

In Factom, the flexibility of defining the namespace makes efforts to hog the namespace ineffective.
 

# How to Create a Factom Chain

Factom Chains are chains of Factom Entries. A Factom Chain provides the infrastructure for managing smart contracts, token counts, alternative currencies, etc.  Factom chains are really just simply lists of entries, so they can just as easily be used to document any number of business processes, provide notices to users, pass messages, and other more mundane purposes.  The nature of the immutable record, user defined and control of the processing of Factom chains, and the privacy afforded individuals watching these lists and using lists to communicate is very powerful.

Chains are named, but nearly all references to a chain are done via a hash of the name referred to as a ChainID.  The design of names in Factom provide total flexibility on the part of the users in how namespaces are defined and used.  

Names are defined by a list of byte arrays.  Because they are byte arrays, the user can choose the encoding.  Names coded in ASCII will hash to different ChainIDs than the same names coded in UTF-16, UTF-32, or EPCIDIC.  And there are many more encodings still.  In fact, each byte array could be simple numbers.  But to create a ChainID, each array is hashed, then the hashes are hashed together.  The hashing of a set of byte arrays will not yield the same result as hashing the byte arrays concatenated together.  ChainIDs are placed in the entry blocks.  




#Attacks on Factom

**Denial of Service**

Since Factom is an open system, any user can put entries into almost any chain.  For example ASCII Art or other invalid data can be placed in the Mastercoin Chain.  Bitcoin has a similar phenomenon.  http://www.righto.com/2014/02/ascii-bernanke-wikileaks-photographs.html  In order for Mastercoin to reject those transactions, they would first need to download and process them.  A large number of bogus entries could slow down processing of Mastercoin transactions.  This threat is mitigated by an attacker needing to spend money to carry it out.  This is similar to Adam Back’s Hashcash solution to email spam. http://www.hashcash.org/  

Another mitigation technique would be audits.  Multiple auditors could maintain their own chains of entries which they believe are valid Entries, or conversely which Entries to ignore.  The auditors could watch each other as well.  If any auditor made a bad decision, it would be easily verifiable and the record of it would be permanent.  Applications could decide to either power through the Denial of Service data or trust auditors telling them to ignore it.

**Man in the Middle**

There is a convention where the first Entry in a Chain can carry more significance than later entries.  An attacker with a privileged position in the network can front run the original submitter by intercepting and getting an attack Entry to the server prior to the authentic request.  This could be done with merely a faster connection to the relevant Factom Server.  Factom turns this attack from a permanent loss by the originator to a mere delay of claiming the chain.  This is done with a system similar to Namecoin [[5](http://dot-bit.org/HowToRegisterAndConfigureBitDomains)].  The hash of the Entry combined with the desired ChainID is recorded in the payment processing section of Factom.  The Factom servers will reserve the hidden ChainID for a period of time, only letting the first paid Entry be the first Chain Entry.  An attacker can front run the payment, but since they do not know the unrevealed ChainID, they cannot form a valid Entry from the information they have.

#Bibliography

"Bitcoin." / Mailing Lists. Accessed May 27, 2014. http://sourceforge.net/p/bitcoin/mailman/message/32108143/.

"Could the Bitcoin Network Be Used as an Ultrasecure Notary Service?" Computerworld. Accessed May 27, 2014. http://www.computerworld.com/s/article/9239513/Could_the_Bitcoin_network_be_used_as_an_ultrasecure_Notary_service_.

"Proof of Existence." Proof of Existence. Accessed May 27, 2014. http://www.proofofexistence.com/.

"Virtual-Factom." Virtual-Factom. Accessed May 27, 2014. http://virtual-Factom.org/.

[1] "Recording (real estate)" Accessed Oct 29, 2014. http://en.wikipedia.org/wiki/Recording_%28real_estate%29

[2] "Secure Property Titles with Owner Authority" Accessed Oct 29, 2014.  http://szabo.best.vwh.net/securetitle.html

[3] "Block timestamp" Accessed Sep 12, 2014. https://en.bitcoin.it/wiki/Block_timestamp

[4] "OP_RETURN and the Future of Bitcoin" Accessed Sep 12, 2014.  http://bitzuma.com/posts/op-return-and-the-future-of-bitcoin/

[5] “HowToRegisterAndConfigureBitDomains” Accessed Nov 4, 2014. http://dot-bit.org/HowToRegisterAndConfigureBitDomains
