Factoid API
===========

This document does a quick summary of the API for Factoids and the Factoid wallet.   At this point in time
the wallet is a commandline driven program, intended to demonstrate the API more than to be a viable 
commerical wallet solution.

The first step is to install the factom client and factom wallet helpers.  See the [How To](http://factom.org/howto) 
guides for setting up in your environment.  You will need to run factomd and fctwallet.  Note that from time to 
time over the next few months you will need to update factomd to continue to communicate 
with the network.  Watch our[technical blog](http://blog.factom.org/) for notifications and updates.

The two APIs that are of interest are implemented by factomd and fctwallet.  The first, **factomd**, is the client
program that actually participates in the Factom Network.  The second, **fctwallet**, provides common wallet
functions, and it maintains the address book where private keys are kept.  A third program, **walletapp**, provides
for cold wallets, the generation of offline transactions, and the submission of offline transactions to 
the factom network.

The factom client **factomd** provides a RESTful interface found at http://localhost:8088 by default.  None of the calls to 
factomd present any security issues, so factomd does not have to be colocated with programs creating and
submitting transactions.

The factom wallet **fctwallet** provides a RESTful interface found at http://localhost:8089 by default.  Calls to 
fctwallet allow for the creation of transactions against factoid addresses held in its wallet.  Access to the 
API then must be kept secure.

The factom wallet **walletapp** is an alternative that only supports factoid functions.  It communicates only 
with factomd.  The *walletapp* supports cold storage, construction of offline transactions, and the submission
of offline transaction to the factom network.  We will soon be releasing a GUI that will run on top of the
*walletapp* that will provide support for general factoid users.

The factom commandline wallet **factom-cli** is a wallet that supports factoid transactions, as well as 
general access to the Factom protocol. *factom-cli* uses the interfaces to *factomd* and *fctwallet* to 
implement its functionality.  The main purpose of this program is to demonstrate the use of the factom
APIs.  It can also be used to script transction processes against Factom.

factomd
-------

This is a summery of the factomd API as pertains to trading Factoids.  We will add detail on other calls as we go forward.

+ Post **http://localhost:8088/v1/commit-chain/?**

  Commits a chain.  The first step towards creating a new chain.
  
+ Post **http://localhost:8088/v1/reveal-chain/?**

  Reveal the first entry in a chain.  Required to complete the construction of a new chain.
  
+ Post **http://localhost:8088/v1/commit-entry/?**

  Commits an entry.  The first step in writing an entry to a chain.
  
+ Post **http://localhost:8088/v1/reveal-entry/?**

  Reveal a new entry.  Required to complete the writing of an entry into a chain.
  
+ Post **http://localhost:8088/v1/factoid-submit/?**

  Submit transaction.  Requires the encoded transaction as part of the call.  For example, creating a transaction that sends 10 factoids from xxx to yyy might be encoded as:
  ```
  http://localhost:8088/v1/factoid-submit/httpp02015023e2886901010083ddb4b3006302ac3d
  a1a1e5eac31af88cdbb886f34470cc0415d1968d8637814cfac482f283dceb940025edb8b25808b6e6d
  48ad5ba67d0843eaf962c40f63c9b4df91b8fe7364ae872014b776d236585f2ed658ec9d24a4a65e08e
  f6074573f570b8b25a9d424b1d955d2caaa4d2cfe30eb8217844f8b28b8a47ce6dc3e5eecd03f30954c
  a3f0b64a63e0687f667bc3300bb33a0638953d442db2cd6fb4d27045318ec09463542c66305
  ```
  That seems like a pretty complex construction of data.  Most users will use fctwallet to construct this call.
  
+ Get **http://localhost:8088/v1/directory-block-head/?**

  Returns the hash of the directory block head.  No parameters are needed. Returns a JSON string of the form:
  ```
  {"KeyMR":"f7eb0456b30b1a4b50867a5307532e92ddee7279ffc955ce1284cd142f94d642"}
  ```
+ Get **http://localhost:8088/v1/get-raw-data/([^/]+)**
  
  Returns the block assoicated with the given hash.  
  ```
  http://localhost:8088/v1/get-raw-data/f7eb0456b30b1a4b50867a5307532e92ddee7279ffc955ce1284cd142f94d642
  ```
  returns:
  ```
  {"Data":"00fa92e5a291592f5f78c547560edceb8bc5ef142f20e9689fcd587557a2f3d18406d6e5ece9eacaa1c31d1371af60d6a9d5ea65654d1ff5698f7fb181d0ae4bc8582c093186dd2a14e83bbf53bb7cab230b1d0e2cefbb0d93d16c09c39ea13e338d0a8c0a016f279a000010c100000004000000000000000000000000000000000000000000000000000000000000000a98f7817976ed8ff9aa306834d98c145d7c0334d7057f89dd2f035df1b37946ae000000000000000000000000000000000000000000000000000000000000000c9432448e6c7f56450804b42ed9c1653182efb6f48a5d8da2c22d1789e7dbff44000000000000000000000000000000000000000000000000000000000000000fb642daa292af42dda109bc87cddd31647da6fef9f3f25129c3740ef4d72761a0df3ade9eec4b08d5379cc64270c30ea7315d8a8a1a69efe2b98a60ecdd69e604789b0103e5f8358d7f8402264837986a2b29ac59be8a796dbbe75eecf6a853d9"}
  ```
  This data can be unmarshalled into the directory block struct used by Factom.

+ Get **http://localhost:8088/v1/directory-block-by-keymr/([^/]+)**

  Returns the directory block assoicated with the given hash.  
  ```
  http://localhost:8088/v1/directory-block-by-keymr/f7eb0456b30b1a4b50867a5307532e92ddee7279ffc955ce1284cd142f94d642
  ```
  returns:
  ```
  {"Header":{
     "PrevBlockKeyMR":"e9eacaa1c31d1371af60d6a9d5ea65654d1ff5698f7fb181d0ae4bc8582c0931",
     "SequenceNumber":4289,
     "Timestamp":1443711000},
     "EntryBlockList":[
        {"ChainID":"000000000000000000000000000000000000000000000000000000000000000a",
         "KeyMR":"98f7817976ed8ff9aa306834d98c145d7c0334d7057f89dd2f035df1b37946ae"},
        {"ChainID":"000000000000000000000000000000000000000000000000000000000000000c",
         "KeyMR":"9432448e6c7f56450804b42ed9c1653182efb6f48a5d8da2c22d1789e7dbff44"},
        {"ChainID":"000000000000000000000000000000000000000000000000000000000000000f",
         "KeyMR":"b642daa292af42dda109bc87cddd31647da6fef9f3f25129c3740ef4d72761a0"},
        {"ChainID":"df3ade9eec4b08d5379cc64270c30ea7315d8a8a1a69efe2b98a60ecdd69e604",
         "KeyMR":"789b0103e5f8358d7f8402264837986a2b29ac59be8a796dbbe75eecf6a853d9"}
    ]
  }
  ```
  This call returns the data held in a Directory Block digested into a JSON structure.

+ Get **http://localhost:8088/v1/entry-block-by-keymr/([^/]+)**

  Returns an Entry Block structure. The call:
  ```
  http://localhost:8088/v1/entry-block-by-keymr/789b0103e5f8358d7f8402264837986a2b29ac59be8a796dbbe75eecf6a853d9
  ```
  Returns 
  ```
  {
    "Header":{
      "BlockSequenceNumber":2479,
      "ChainID":"df3ade9eec4b08d5379cc64270c30ea7315d8a8a1a69efe2b98a60ecdd69e604",
      "PrevKeyMR":"63833701a61a846ebe8d38a1c6ede6bf5d5516990c34372c7f7936812ec09bde",
      "Timestamp":1443711000
    },
    "EntryList":[
        { "EntryHash":"c8f4936962836cda0d8bf712653d97f8d8b5cbe675e495b6dfab6b2395c8b80a",
          "Timestamp":1443711360
        }
    ]
  }
```
This is the structure of an Entry block, broken out into JSON.

+ Get http://localhost:8088/v1/entry-by-hash/([^/]+)", handleEntry)

  Returns an Entry broken out into JSON.  The following call:
  ```
  http://localhost:8088/v1/entry-by-hash/c8f4936962836cda0d8bf712653d97f8d8b5cbe675e495b6dfab6b2395c8b80a
  ```
  Returns:
  ```
  {"ChainID":"df3ade9eec4b08d5379cc64270c30ea7315d8a8a1a69efe2b98a60ecdd69e604",
  "Content":"7b22416e63686f725265636f7264566572223a312c224442486569676874223a343238382c224b65794d52223a2265396561636161316333316431333731616636306436613964356561363536353464316666353639386637666231383164306165346263383538326330393331222c225265636f7264486569676874223a343238382c22426974636f696e223a7b2241646472657373223a22314b3253586741706d6f39755a6f79616876736253616e705657627a5a5756564d46222c2254584944223a2263323363623932303764356266643863376539656565303438316338333563663463373665626132363565393832656330623032353964636666323536636134222c22426c6f636b486569676874223a3337373031312c22426c6f636b48617368223a2230303030303030303030303030303030303466396138653735343065383135316336373231653131646264343166633936663931653432313661373161356334222c224f6666736574223a3835317d7d6234643966633530343564653635313532353664623337316463633138636266653761616537383664326262336565633466316334373966636132393762373266363330633261313439366436653737653139633631626165663030326233396133633064656534636439323963396335393836326331366639646136353033","ExtIDs":null}
  ```
  Returns a particiular Entry's construction broken out into JSON.
  
+ Get **http://localhost:8088/v1/chain-head/([^/]+)**

  Returns the KeyMR of the first Entry in an Entry Chain.  The call:
  ```
  http://localhost:8088/v1/chain-head/df3ade9eec4b08d5379cc64270c30ea7315d8a8a1a69efe2b98a60ecdd69e604
  ```
  Returns
  ```
  {"ChainHead":"bfd814a3b9a4356e04c816fe4ce1a53198953ab321912d60dacba766950e5591"}
  ```

+ Get **http://localhost:8088/v1/entry-credit-balance/([^/]+)**

  Returns the balance at the given Entry Credit address.  For example, the call:
  ```
  http://localhost:8088/v1/entry-credit-balance/748be8327d20fee4365e6b5a3dca7df1e59da47e9ebd99129ba84d58d4d0726b
  ```
  Might return (depending on the balance at that address at the time):
  ```
  {"Response":"4000","Success":true}
  ```
  This would indicate that the decoded Entry Credit address (EC2eUoDPupuQXm5gxs1sCBCv3bbZBCYFDTjaFQ6iRaAKfyXNqjEJ) decodes to the hex: 748be8327d20fee4365e6b5a3dca7df1e59da47e9ebd99129ba84d58d4d0726b and has a balance of 4000 entry credits.
  
+ Get **http://localhost:8088/v1/factoid-balance/([^/]+)**

  Returns the Factoid balance at the given address.  For example, the call:
  ```
  http://localhost:8088/v1/factoid-balance/f6e117ea838cb652e9cfc3b29552d5887800a7ba614df0bd8c13e171eddc5897
  ```
  Returns:
  ```
  {"Response":"1210268000","Success":true}
  ```
  Note that, like Bitcoin, Factoids use fixed point to indicate parts of a coin.  so 12.10268000 represents 12.10268 factoids.
  
+ Get **http://localhost:8088/v1/factoid-get-fee/**
  
  Returns the current exchange rate for Entry Credits.  So the call:
  ```
  http://localhost:8088/v1/factoid-get-fee/
  ```
  might return
  ```
  {"Fee":100000}
  ```
  indicating that .001 Factoids will purchase 1 Entry Credit.   
  
+ Get **http://localhost:8088/v1/properties/",handleProperties)

  Returns the version numbers of various components of Factom.  For example at the time of writing, the call:
  ```
  http://localhost:8088/v1/properties/
  ```
  Returns:
  ```
  {
    "Protocol_Version":1005,
    "Factomd_Version":3002,
    "Fctwallet_Version":0
  }
  ```
