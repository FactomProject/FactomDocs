# Special Chains

We have a few chains we handle in a special fashion, which must have valid entries to include in these chains.

* Factoid Chain -- chain of all Factoid transactions
* Entry Credit Chain -- chain of all Entry Credit transactions
* System Chain -- Parameters driving Factom
* Software Sale Chain -- Documents the Factoids purchased during the software sale.

## Software Sale Chain

A special chain used to document the Factom software sale.  Validates the genesis block.  Entries will include:

Each entry is the UTC timestamp to start the period, followed by the BTC price.  The next Entry start 
is the end of the previous.  A 0 price marks the end of the sale.  The sale starts on March 31, 2015 at 
10:00 am CDT.  There are 5 one week periods, and the last period last 10 days ending on May 15, 2015 at 10:00 am 
CDT.

The followint entry will be made in the Software Sale Chain

```JSON
{ 
  "1427814000" : 2000,
  "1428418800" : 1900,
  "1429023600" : 1800,
  "1429628400" : 1700,
  "1430233200" : 1600,
  "1431097200" : 1500 ,
  "1431702000" : 0
}
```

A Summary Entry will document the totals for the sale:

```JSON
{
  "Sale Summary" : {
    "total software sale BTC" : "#BTC",
    "total software sale factoids" : "#factoids",
    "total issued to contributors" : "#factoids",
    "total software sold to early purchasers" : "#factoids"
  }
}  
```

The actual distribution will be documented with a list of the purchases and the destination addresses.  Any number of the entries of the following form will document the sales:

```JSON
{
  "factoidSales" : [ 
     [ "<UTC>", "<BTC Trasnaction ID>" , "<Factom Address>", "<Factoid Amount>" ]
     [ "<UTC>", "<BTC Trasnaction ID>" , "<Factom Address>", "<Factoid Amount>" ]
  ]
}
```

Any number of contributor records of the form:

```JSON
{
  "contributors" : [ 
     [ "<Factom Address>", "<Factoid Amount>" ]
  ]
}
```

Any number of early buyer records of the form:

```JSON
{
  "earlyBuyer" : [
      [ "<Factoid Address>", "<Factoid Amount>" ],
      [ "<Factoid Address>", "<Factoid Amount>" ]
   ]
}
```

## Factoid Chain

Contains only valid Factoid Transactions.  The Genesis Block for Factom will do a mass generation of Factoids to all the Factoid Addresses as defined by the crowd sale.  Individuals participating in the presale will have to provide addresses, and people who were initial contributors will need to provide addresses in order to receive their Factoids.  For individuals who have not provided addresses by the time we generate the Genesis Block, the Factom Foundation will create address, and transfer the Factoids once notified of the proper address.


## System Chain

Discussed elsewhere

## Identity Chain

Each Federated Server, or voter, must have an identity chain.  This serves as the user’s identity, defines their public keys, their Entry Credit keys for voting, and more. 

An Identity is defined by a Factom Chain, and a series of Entries holding JSON data.

The first Entry must define the security for the Identity.  The JSON must include:

* Version -- Version of the Identity, if it is to be used with Factom
* Key Type -- What type of key used.  For now we support ECDSA and Ed25519.  More key types may be supported in the future.
* Four keys, by priority.  The higher priority keys can be used to regain control of an identity should an identity be compromised, or make changes to the Identity.


### Example Identity:

“Server” “Factom Server 1”  has a Chain ID of 

e367cebf263e8f2d1d56a38287ccbf051be853eea44333cb8b8c52678ea66b5e

And the first Entry is:

```JSON
{  
   "Key List Type" : "Identity"  ,
   "type" : "Ed25519",
   "1" : "de8634289a978df57c5b07a3423b01e1a1c37263506c43b739d770e6d5924d92",
   "type" : "ECDSA",
   "2" : "5dbfc8221051e0ce6a26e518ba7b0f2d0291e8a1ede150c51695470f2c2a1423",
   "3" : "b90b0c1f73b142faabeb3113bfbf26a8156b0e6d2c5897675a9b9dd1443822e1",
   "4" : "41d21362bd5f2c07a316defa69d19ce41ab0bbd96bd0b0a27792a6ad7d7e44f8"
}
```

The 4th level signature would be the one used to sign additional entries to the Identity.  These additional entries can be used to change the keys, change the security, add a set of Bitcoin addresses, etc.

The Entry to add Bitcoin addresses would look like this:

```JSON
    {
        "Key List Type" : "Bitcoin",
          "1" : "1EYP7NzhfugjKvJH3BQTU7J6cQhCWWVYHx",
          "2" : "19jPEV4sf4sahupcawFD5vZ4Z3811HZB6i",
"3" : "1GTALs4J3tzyknyY2k7DdGDFLTPTKnHYyk",
"4" : "16NZ2R5YrMn1C9n5PcrFB1QrMoFWCmbNim"
   }
```   

Any Identity used to back a server must have a Bitcoin Entry.  The 4th level address is what is used to write entries into Factom, and the higher priority addresses are used to manage situations where the 4th level address has been compromised. 

Other entry types are possible.
