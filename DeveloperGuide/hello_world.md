Hello World!
===

The easiest way to create Factom entries and chains programatically is to use the [factom library](http://github.com/FactomProject/factom) for golang. Install and setup the Go environment using the [installation instructions](https://golang.org/doc/install) provided by [golang.org](http://golang.org). Import the [factom package](https://github.com/FactomProject/factom) with ``go get github.com/FactomProject/factom``.

Creating a new Factom Entry
---
In the first example a new Entry is constructed then sent to the Factom network. Notice that the ExtIDs, and Entry Content are ``[]byte`` not ``string``. This allows the Entries to contain binary data. For example an ExtID may be a key or a key signature.

	package main
	
	import (
		"log"
		"time"
		
		"github.com/FactomProject/factom"
	)
	
	func main() {
		e := factom.NewEntry()
		e.ChainID = "5c337e9010600c415d2cd259ed0bf904e35666483277664d869a98189b35ca81"
		e.ExtIDs = append(e.ExtIDs, []byte("hello"))
		e.Content = []byte("Hello Factom!")
		
		if err := factom.CommitEntry(e, "app01"); err != nil {
			log.Fatal(err)
		}
		time.Sleep(10 * time.Second)
		if err := factom.RevealEntry(e); err != nil {
			log.Fatal(err)
		}
	}
	
The easiest way to create Factom applications in golang is to import the factom package by running ``go get github.com/FactomProject/factom``

	import (
		//...		
		"github.com/FactomProject/factom"
	)

Create a new ``factom.Entry`` and fill in the relevent data. We will be adding this Entry to a testing Chain ``5c337e9010600c415d2cd259ed0bf904e35666483277664d869a98189b35ca81``. the first External ID for the Entry will be "hello" and the Entry Content will be "Hello Factom!".

	e := factom.NewEntry()
	e.ChainID = "5c337e9010600c415d2cd259ed0bf904e35666483277664d869a98189b35ca81"
	e.ExtIDs = append(e.ExtIDs, []byte("hello"))
	e.Content = []byte("Hello Factom!")

Once the Entry is ready we send the Commit Message to the Factom network. The Commit is process by fctwallet and signed with the Entry Credit Address specified here.

	if err := factom.CommitEntry(e, "app01"); err != nil {
		log.Fatal(err)
	}

It is not strictly nessesary to wait between the Commit Message and the Reveal, but waiting reduces the chance of errors. When we are ready we reveal the Entry.

	if err := factom.RevealEntry(e); err != nil {
		log.Fatal(err)
	}

If there are no errors, the Entry will be included in the current 10 minute Entry Block for the specified chain. After the end of the current 10 minutes the Entry Block containing the Entry will be hashed and included into the Directory Block which will be anchored into the Bitcoin Blockchain.

Creating a new Factom Chain
---
A new Factom Chain is created by constructing an Entry to be the first Entry of the new Chain, then constructing the Chain from the Entry. The Chain is then commited and revealed to the Factom network.

	package main
	
	import (
		"log"
		"time"
		
		"github.com/FactomProject/factom"
	)
	
	func main() {
		e := factom.NewEntry()
		e.ExtIDs = append(e.ExtIDs, []byte("MyChain"), []byte("12345"))
		e.Content = []byte("Hello Factom!")
		
		c := factom.NewChain(e)
		log.Println("Creating new Chain:", c.ChainID)
		
		if err := factom.CommitChain(c, "app01"); err != nil {
			log.Fatal(err)
		}
		time.Sleep(10 * time.Second)
		if err := factom.RevealChain(c); err != nil {
			log.Fatal(err)
		}
	}

Since a new Chain is being created the Entry may be constructed without the ChainID field. The new ChainID will be computed using the ExtIDs of the Entry. Remember that the ExtIDs of the first Entry of a Chain must be unique among all first Entries (A new Chain cannot be created if a Chain with the same ID already exists). 

	e := factom.NewEntry()
	e.ExtIDs = append(e.ExtIDs, []byte("MyChain"), []byte("12345"))
	e.Content = []byte("Hello Factom!")
	
	c := factom.NewChain(e)
	
The ChainID will be printed to the screen.

	log.Println("Creating new Chain:", c.ChainID)

``Creating new Chain: cfa35f22d4790a3f3121d6cc192da26813ee29cb0f8ad220fbe3563fa9d351d1``
