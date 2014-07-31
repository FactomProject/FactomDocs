Compaction and distribution layer.  

A Compaction Service Provider (CSP) is an entity which accumulates data fingerprints (hashes) from its customers.  It assembles its customers' data, and gives it a timestamp.  The CSP periodically bundles all it's customer's data and makes it available on a Bittorrent like network.  Then it publishes the fingerprint on the bitcoin network, permanently timestamping the data. 

The CSP is in a privileged position, sitting between the customer and the bitcoin blockchain.  They have the ability to exclude, delay, or reorder the customer's timestamped entries.  An auditing system operating at a higher level will help prevent the CSP from misbehaving.  

The CSP collects data from its customers and creates a Data Structure Block (DSB), which consists of the most recent customer hashes and timestamps.  The DSB itself is hashed to create the Data Structure Hash (DSH).  The CSP signs the DSH to prove authorship.  A header is created which consists of the DSH and a signature of the DSH.  The header and DSB together create the Notary Block (NB).  The NB is hashed to create a Distributed Hash Table Index (DHTI).  The DHTI is 32 bytes in size.  Bitcoin allows for 40 bytes of prunable data to be added in a OP_RETURN message in the blockchain.  The 8 most significant bytes are arranged as a magic number specific to the CSP.  That magic number should be unique to an individual CSP.  

A limited subset of the CSP's customers will want to store their own copy of the Notary Block.  This will ensure that in the future, they can present their artifact, the NB containing a fingerprint of the artifact, and a reference to the bitcoin blockchain.  All 3 of these pieces are needed to show the artifact existed at or before some time in the past.  The bitcoin blockchain can be expected to remain available for the foreseeable future.  The customer would keep their artifact, since it is important to them.  The middle part of the proof, the NB, was originally hosted by the CSP, but their continued existence and hosting cannot be guaranteed.  To be prudent, the customer would want to save copies of the NB along with their artifact.  A system organized like a Bittorrent DTH would allow for availability far into the future.  Even if the CSP were to disappear, it would take only one customer hosting data they are already retaining to preserve it.  A Bittorrent style distribution system will also allow customers to participate in the initial data propagation, or allowing the CSP to easily distribute distribution servers geographically.




Attacks: 

An attacker could flood the bitcoin blockchain with OP_RETURN messages impersonating the CSP.  The attacker could create a large dataset and present it on the DHT network.  They would then create an OP_RETURN message containing their bloated dataset, with the magic number of a legitimate CSP.  3rd parties wanting to preserve the CSP's uncompacted data would see the CSP's magic number and find it in the DHT network.  They would then start downloading the header associated with that block.  Before downloading the bulk of the data, the 3rd parties would download and check the signature in the header.  If the signature does not match the CSP's, that entry will be ignored.

This attack could further be mitigated by following the value flow through the bitcoin blockchain.  The CSP would need to have some bitcoin value in order to pay fees and embed data.  The CSP could always publish their DHTI by spending from the same public address.  If the magic number came from a different public address, it could be treated with suspicion.





Audit Layer:

The Compaction Service Provider (CSP) has the power to exclude, delay, or reorder the customer's data.  The customer would want some mechanism to keep the CSP from misbehaving in any one of those ways.  The customer could select a Compaction Service Auditor (CSA) who would watch the outputs of the CSP.  The two would be separate rivalrous entities.  The CSA would make sure the CSP follows through with publishing the customer's data.  If the CSP did not include the customer's data when they claimed they would, the CSA would be entitled to restitution from the CSP.

The customer, based on their risk preference, can select from various levels of auditing.

level 1: No Auditing

The customer sends their artifact fingerprint to their CSP of choice.  Minimal acknowledgement would be given to the customer from the CSP.  The customer would rely on the CSP's history to ensure their data gets timestamped.

level 2: Self Auditing

After submission to the CSP, the customer watches for the CSP to embed a Notary Block (NB) into the bitcoin blockchain.  The customer finds the NB on the DHT network and downloads it.  The customer verifies that their artifact fingerprint exists in the NB and that the timestamp is correct.

level 3: Customer holds receipt

When the customer submits a hash to the CSP, they would request the CSP provide a recipt.  The receipt would consist of the customer's fingerprint, a timestamp, and the NB serial number the CSP is expecting to place it in.  The CSP will sign the receipt and send it to the customer.  If the customer finds later that their artifact fingerprint is not in the blockchain, then the customer may be entitled to restitution.  

level 4: Customer delivers receipt to CSA

The customer receives the same receipt as above, but forwards it onto a CSA.  The CSA will watch the chosen CSP's outputs to ensure that the customer's data gets entered into the CSPs block.  If the CSP neglects to add the customer's CSA to the block, then the CSA would be entitled to restitution.

level 5: Customer tests CSA

This operation would allow the customer to work in conjunction with the CSP to trigger an audit failure alarm at the CSA.  The customer would pay above the normal transaction cost to the CSP.  The CSP would create a timestamp receipt, but intentionally leave it out of the NB.  The customer would deliver the receipt to the CSA, without letting them know they were being tested.  If they alert the customer and demand restitution from the CSP, the CSP will show proof that it was only a test and payments will be settled.  If the CSA does not alert the customer of the audit failure, then the customer knows the CSA is not performing it's job.




Attacks:
Collusion
In the level where the customer tests the auditor, there is a chance of collusion.  If the CSP and CSA are colluding, the CSA could be alerted of an audit test.  The CSA would be able to forgo auditing until the CSP alerted them to a test in progress.

Pattern recognition
The CSA can neglect auditing unless they see a particular pattern.  For example take a customer that regularly sends one receipt per minute to be audited.  Occasionally the customer sends a test receipt which will not be included in the NB.  The times when the customer sends two recipts in one minute instead of the usual one receipt, a test is probably in progress.  
