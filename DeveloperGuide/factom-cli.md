Using factom-cli
===

factom-cli is the command line tool for using Factom. 

By itself, factom-cli may be used to read data from factom.

In conjunction with fctwallet, it may be used to:
- create or import Factoid and Entry Credit Addresses
- create and send Factoid transactions
- create new Factom Entries and Chains
 
This guide will show how to use factom-cli to read existing Chain and Entry data (does not require fctwallet), and to write new Chain and Entry data (does require fctwallet).

For demonstration purposes:
- open one terminal window and run ``factomd``
- open another terminal window and run ``fctwallet``

Reading Factom Data
---

factom-cli may be used to read the latest data from Factom or to get data about specific Chains.

To use factom-cli to get the first Entry in a Chain which, by convention, has a description of the Chain:

	$ factom-cli get firstentry 3e3eb61fb20e71d8211882075d404f5929618a189d23aba8c892b22228aa0d71
	ChainID: 3e3eb61fb20e71d8211882075d404f5929618a189d23aba8c892b22228aa0d71
	ExtID: Universal Declaration of Human Rights
	Content:
	The Universal Declaration of Human Rights (UDHR) is a milestone document in the history of human rights. Drafted by representatives with different legal and cultural backgrounds from all regions of the world, the Declaration was proclaimed by the United Nations General Assembly in Paris on 10 December 1948 General Assembly resolution 217 A (III) (French) (Spanish)  as a common standard of achievements for all peoples and all nations. It sets out, for the first time, fundamental human rights to be universally protected.
	
	source: http://www.unicode.org/udhr

Get the most recent Entries in a Chain.

	% factom-cli get chainhead d3abab36f0abe172b08df64396e6e4b4129bcaf7b0b3e1b94653414c68249386
	EBlock: 6c4d2b72a6efa6648702b0f6b8f5297d943955fba02d7651facbc296f9011e1c
	BlockSequenceNumber: 14880
	ChainID: d3abab36f0abe172b08df64396e6e4b4129bcaf7b0b3e1b94653414c68249386
	PrevKeyMR: b9a89668b6fa32cf7bb3a67c1b6fc80cbf9d022104bf94628ce338c5c46fcf5a
	Timestamp: 1457041800
	EBEntry {
		Timestamp 1457041860
		EntryHash 29208f81ce849291ab7fae458bd7624dbfb03c3b9f506d7f3e9e45a1339561c8
	}

	% factom-cli get eblock 6c4d2b72a6efa6648702b0f6b8f5297d943955fba02d7651facbc296f9011e1c
	BlockSequenceNumber: 14880
	ChainID: d3abab36f0abe172b08df64396e6e4b4129bcaf7b0b3e1b94653414c68249386
	PrevKeyMR: b9a89668b6fa32cf7bb3a67c1b6fc80cbf9d022104bf94628ce338c5c46fcf5a
	Timestamp: 1457041800
	EBEntry {
		Timestamp 1457041860
		EntryHash 29208f81ce849291ab7fae458bd7624dbfb03c3b9f506d7f3e9e45a1339561c8
	}
	
	% factom-cli get entry 29208f81ce849291ab7fae458bd7624dbfb03c3b9f506d7f3e9e45a1339561c8
	ChainID: d3abab36f0abe172b08df64396e6e4b4129bcaf7b0b3e1b94653414c68249386
	ExtID: ����1Ee+_5P��%�������l1
	                            �!�v����
	s(��Ņ�O                                    ���P�
	Content:
	{"APIMethod":"https://poloniex.com/public?command=returnOrderBook\u0026currencyPair=BTC_DOGE\u0026depth=4","ReturnData":"{\"asks\":[[\"0.00000058\",18923132.45473],[\"0.00000059\",14674610.350392],[\"0.00000060\",3373359.5320179],[\"0.00000061\",5314538.8908938]],\"bids\":[[\"0.00000057\",24850505.374277],[\"0.00000056\",49813613.467365],[\"0.00000055\",12240692.413305],[\"0.00000054\",9643845.2732678]],\"isFrozen\":\"0\"}","Timestamp":1457041801}

Get all of the Entries in a Chain in order.

	% factom-cli get allentries 00511c298668bc5032a64b76f8ede6f119add1a64482c8602966152c0b936c77
	Entry [0] {
	ChainID: 00511c298668bc5032a64b76f8ede6f119add1a64482c8602966152c0b936c77
	ExtID: Factom
	ExtID: Project Gutenberg
	Content:
	Project Gutenberg (http://www.gutenberg.org/) is a volunteer effort to digitize and archive cultural works, to "encourage the creation and distribution of eBooks". It was founded in 1971 by Michael S. Hart and is the oldest digital library. Most of the items in its collection are the full texts of public domain books. The project tries to make these as free as possible, in long-lasting, open formats that can be used on almost any computer.
	
	This chain documents the Project Gutenberg DVD (https://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project) published April 2010. Each entry in this chain represents one of the 29000+ books on the DVD, and contains sha256sum hashes of each of the .zip files associated with the book.
	
	b69644d2ee2fd2a886cec724e8c1b0fe0018ccbc3ccfbfe58d4575555ad31ac3  pgdvd042010.iso
	
	Each entry of hashes will be signed with the Factom.org Project Gutenberg PGP key.
	
	-----BEGIN PGP PUBLIC KEY BLOCK-----
	Version: GnuPG v1
	
	mQENBFYOz0QBCAC1AVabyuMDCJwMqSuetEW1BOt2p21LxKPc0TDBmuzzVgVs/SmI
	oGweWu+NES69zG+nALhH2pueUeedEJK8rAcjLJPUdGvcLa4JmZgHOgxtVFXs3erf
	oqMpCsRyt/FqDWvOzvt0H6Qk3R4FZeQbvGWHbEbi6GJxn/n55S9x2usJF4kTMjfM
	t3X8LGqTTXCay0JZsEGXGADSSWYJihdTdUxM7NH4EfF5cXxsqW/B/6X0B19xtlDw
	VspF+pMHxMXl5s3IKvnK+McSwLIC9Jo6fpJYJlKT0l+5F3EbO9nkOv8SEsS8pcnR
	Q9ie8OvtCD5KNI3sSl/PSTvopGiW6+nIWySNABEBAAG0SUZhY3RvbS5vcmcgKFNp
	Z25pbmcga2V5IGZvciBQcm9qZWN0IEd1dGVuYmVyZyBlbnRyaWVzKSA8aGVsbG9A
	ZmFjdG9tLm9yZz6JAT4EEwECACgFAlYOz0QCGwMFCQWjmoAGCwkIBwMCBhUIAgkK
	CwQWAgMBAh4BAheAAAoJEIuOBXcCsud6nTgH/jr6H3ZM7NcpwlUTe3TcJC6+FsyO
	bJJjvNn1NhItFYSngo1fdcUMbbtaZ54r0uPwiDmATvy57vg+605kU2ih2n7JJv18
	Yd2U4PN8cnmtHsukgpqAdZNvE8tTPQEafFWdhRCgmfp9Ne8E7BfG7KZZETHNVUE0
	U5bLtAsbDRYAy2XyJsUt56r+aFBraPV6IYNbskqM1i4ISrZpQHF+e8e85eY2FmpE
	cZrlUnMWZDD0G7z6P9Fg48iejSiHuU3tL0dt6+GSxcOb741S1LftV8alaYF3ENZX
	rzGpqJiI4oMTgNR3BC2KIYrxeeUprKGc/GrPGCNwZq5Sa+ZdOzw/7JK0kaq5AQ0E
	Vg7PRAEIAL/gCcDHVV06wN7MiEdQJtElf12TEgc5rfcmY8KxGWpIuWFHRcce+YPi
	AJAbPW7FOKsb3m0a1alGZuyQwZRioPRik7vDayiVaYBX4fmwawFo4XdZ0NYpo2sc
	/bshTbMTcXsV580BJiYN42Ks+Qj6F4a4pMNTvOiQhkXaycSQNxWu6CUPcKjfJ/TZ
	5qIL+tBJhj9sHyYNSNdeo0XoQMed6PM6k1Q0yxbQF6fgywT3LrehmMhAXlXfbQc4
	h+NpRz0iMbfhozjfP4byui/TEIl4/0lAN9p9h9ZEEeRZZRodqG/VKcztjeFuf1Qx
	2gweW8CSy2/iQSeUwReLzpkmgmRhNbMAEQEAAYkBJQQYAQIADwUCVg7PRAIbDAUJ
	BaOagAAKCRCLjgV3ArLnej26B/9f4YJyEafETBmg0JVCx7I4EsPEOkNOrMkIKgzB
	wDH3GgaHCkE6OsCSdR249DG2t7RdewoJoViix/sm4eIDunABy7J53pdCz9NmqoZb
	ak0xBrhCmBxYJqK6zzGYkrmVaOyegmHIqbOPlaCGyD3/LMGspQ9tpQm1NqiufGcE
	SLAXbI9T+S35b4bibio8ftbMl8c7ra6g16BJKWsHbc4aBHbcVnfJHYVhXCUmzDTB
	BvUD/4OAtqe061roSyqH7+b9J4SidyVx6fvErS+4DTMwqY21H29dceEGt9atB1mZ
	olnz+u+YezDu9Sn63jT+Z2JhxfOEOaWHsAezrgIk/FGvT7y/
	=3NSj
	-----END PGP PUBLIC KEY BLOCK-----
	
	}
	Entry [1] {
	ChainID: 00511c298668bc5032a64b76f8ede6f119add1a64482c8602966152c0b936c77
	ExtID: Lucius Seneca
	ExtID: Apocolocyntosis
	Content:
	-----BEGIN PGP SIGNED MESSAGE-----
	Hash: SHA1
	
	6e2f37545a37b0cccf9cc0e95b17091f57b5ffd2743113e1720acbd95caf185f  10001.zip
	-----BEGIN PGP SIGNATURE-----
	Version: GnuPG v1
	
	iQEcBAEBAgAGBQJWEqhTAAoJEIuOBXcCsud6M5YH/0G0GrZYF4V0M9yYa2mO3BC+
	1uEG81K3CMSX32SPmi6atyVkodvik+PFkYCPyzmgGk3LLUCD6DTTpJWWC837yotb
	T7cQL/E/U4x1C+8L/MU+YuyhXSru8e/V0ltWnD+sE+BsHg3UbhpfcQ2Zu6zuGlCC
	7+WFGosg8hFNhoQTWpTQiDl9R8ySO7jKF7qWy06DJUaXTJWtBHLAXwdSWNTbnEE7
	Lx5VrQL9NYLOYv85BoY50wbtkAGAUOjgjxIAep14QBAjX8cDU9j0LLTrHH4WBE8R
	HzDeFKpPwTwuvxGnrwImlSximqeY9qQgqIKBgW2CCXtmpMAJuBAmspAo1zX3tR0=
	=u5Lp
	-----END PGP SIGNATURE-----
	
	}
	Entry [2] {
	ChainID: 00511c298668bc5032a64b76f8ede6f119add1a64482c8602966152c0b936c77
	ExtID: William Hope Hodgson
	ExtID: The House on the Borderland
	Content:
	-----BEGIN PGP SIGNED MESSAGE-----
	Hash: SHA1
	
	e8398edab3e9e5785d80ce8629abc851f38408ce588deacde08419a1425aee54  10002_8.zip
	-----BEGIN PGP SIGNATURE-----
	Version: GnuPG v1
	
	iQEcBAEBAgAGBQJWEqhUAAoJEIuOBXcCsud6KJgH/3ct55S6d8QHBPMaaUNMcPth
	PCcPI1UiuzYux7iI4x4hb9znuYir7lgjhqpfOMwppQFESy+HoznJvWYWNiEZNN0o
	meDct/xroLN2Lndw3raStqoHR3tjkjEaZ33yEqwUL0uI1ETYq7D+d6qJpw6AEyqR
	oSSL7RfhVQbxsE9KNxwmKMekkCbi2OtMJdRBbN3FH4QD5eFE2DT8opmELc8e3J8d
	9PrOe5zfmC3NPdqMdf7pCt8NHFZzPqeGzwH3MCL77yadLFaFTf1pCOlF6hPnb8Y1
	7bSDT6A2KKYa+I5iZq+sK2ZCi2Xj7m4R7D5OvoEceBbRu1vNFMjUzRlTTX2wJIU=
	=B4K2
	-----END PGP SIGNATURE-----
	
	}
	#...
	

Creating new Chains and Entries
---

