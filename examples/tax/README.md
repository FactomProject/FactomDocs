### Factom Tax Document Example

This example shows how Factom can be used to deliver documents to an organization.  The organization in this example is the Example Revenue Service (ERS).  The sending of the document is timestamped in the Bitcoin blockchain.  The document remains encrypted, so only the recipient can read it.  The sending of the document can be proven, even though it cannot be read by 3rd parties.  Only the ERS can decrypt the tax returns.

This example assumes that the ERS takes delivery of documents via Factom and is watching their own Factom chain.  

This example was put together with some freely available open source tools, along with the prototype Factom system.  This procedure is awkward, only because it is not yet streamlined for this process.  In a production environment, the software would handle minutia automatically.  To follow the example, you can use a live boot of any popular linux distribution.  This example was done with Xubuntu.



### Send Documents to ERS

This is how you can send encrypted documents to the ERS.  Some examples are already in Factom, but here is how more can be added.

1. Start the linux OS and open a terminal.
2. Download the file `ERS_publickey.txt` from the github repository to the ~/ (home) directory
3. Import the ERS public key with the command `gpg --import ~/ERS_publickey.txt`  The output should be:

```
gpg: /home/xubuntu/.gnupg/trustdb.gpg: trustdb created
gpg: key 579228B9: public key "Example Revenue Service (ERS)" imported
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)
```

4. Encrypt the document to send.  In this example, we are using `Unencrypted_Obama_Tax_Return.txt` from the github repository.  Use this command to encrypt it: `gpg -e -a -r "Example Revenue Service (ERS)" -o ~/Encrypted_Obama_Tax_Return.txt ~/Unencrypted_Obama_Tax_Return.txt`  The output should be: 
```
gpg: 8A138E1B: There is no assurance this key belongs to the named user

pub  1024R/8A138E1B 2015-02-11 Example Revenue Service (ERS)
 Primary key fingerprint: 323A 8A02 5793 2F31 C0BF  4C1F 280D 8A92 5792 28B9
      Subkey fingerprint: A8BE 8143 D3C9 36BC 084A  FB74 E8FA 4C32 8A13 8E1B

It is NOT certain that the key belongs to the person named
in the user ID.  If you *really* know what you are doing,
you may answer the next question with yes.

Use this key anyway? (y/N) y
```
It will create the file `Encrypted_Obama_Tax_Return.txt`, the contents of can be copied and pasted into Factom.

The file will look like this:
```
-----BEGIN PGP MESSAGE-----
Version: GnuPG v1

hIwD6PpMMooTjhsBBACR2g4KMg6k7dzTvg/8xJGa62YW1O3eXKPR05aRuZbJvFyW
70caMU+GgKgfjgzyafJNkc/ZDCbyl0MqZhCfeFOW66cNJ+GrQFwutVvFaZ9aIU2K
... removed for space ...
wrEpwVgJ5wBNeScLkF+LFj3wr5vo9ROBj/kPr9RNoSVB+g9/PV6prYv2Pp9Yjidh
7iYXHMys+wxzG7f7bRT4O3GXM/3gkACVgYwIGHtuVQoW9QD9VVBKXIisIupv7mmF
OIc=
=rvNQ
-----END PGP MESSAGE-----
```

5. Post the document to Factom.
  1. Browse to http://demo.factom.org:8087/ in a web browser
  2. Click the down arrow next to Entries
  3. Select the Chain `13915515269537837/ERS/2015`
  4. In the Data field, paste the text from the `Encrypted_Obama_Tax_Return.txt` file
  5. Click submit
  6. Wait 1-10 minutes for the Factom Directory Block to be created
  7. Wait several minutes longer for the Directory Block to be timestamped in the Bitcoin blockchain

6. Check that the document was included.

In the Chains page, click on the Chain `13915515269537837/ERS/2015`
In each block, there is a list of Entries.  One of the Entries should be the one you created.

When the ERS want to see if any returns have been sent in, they will open their chain.  They will then download each Entry and decrypt each one.  



### How the ERS Reads the Tax Returns

The ERS would follow a similar procedure for reading the tax returns.  Since they are the only ones with the private key, they are the only ones who can read the returns.

1. Start the linux OS and open a terminal.
2. Download the file `ERS_privatekey.txt` from the github repository to the ~/ (home) directory
3. Import the ERS public key with the command `gpg --allow-secret-key-import --import ~/ERS_privatekey.txt`
4. Open a web browser and go to http://demo.factom.org:8087/
5. Browse to the Chain `13915515269537837/ERS/2015`
6. Find Entries which contain a message that starts with `-----BEGIN PGP MESSAGE-----`
7. Copy the text between BEGIN and END, including the BEGIN and END lines.
8. Paste the text into a text file and save it as `Encrypted_Tax_Return.txt` in the ~/ (home) directory
9. Run the command `gpg -d -o Unencrypted_Tax_Return.txt Encrypted_Tax_Return.txt`.  The output should be:
```
gpg: encrypted with 1024-bit RSA key, ID 8A138E1B, created 2015-02-11
      "Example Revenue Service (ERS)"
```
10. The file `~/Unencrypted_Tax_Return.txt` will contain the tax return only visible to the ERS


### ERS Receipts

Since there is still a some question that the ERS got your return, or that something might have gotten jumbled during transit, a receipt would be nice.

The public key that the ERS has issued can also be used to sign receipts, so that shortly after sending a tax return in, the submitter can be sure that the document was received.

When the ERS scans and can correctly decrypt the message, they can sign an acknowledgement.  The receipts are posted in 13915515269537837/ERS/2015/Receipts.

###### The ERS Creates Receipts

The ERS would find a new tax return in Factom and save the Entry Hash.  This is unique to the data that was submitted.  In the Obama example, the Entry Hash is `ad8d6e1ef4cc10d6478b2d9eb01a50f7e4b62a207865769702b1a96f4784c21b`
The ERS would run this command to create the receipt. 
`echo ad8d6e1ef4cc10d6478b2d9eb01a50f7e4b62a207865769702b1a96f4784c21b | gpg --clearsign`  which would output:
```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

ad8d6e1ef4cc10d6478b2d9eb01a50f7e4b62a207865769702b1a96f4784c21b
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1

iJwEAQECAAYFAlTdLiAACgkQKA2KkleSKLl1bgQAjZQphX45OV74vpssCm085aEn
bSPYYR6EO2mfxsMXIZz1nRx6cPXCESpFkmuSiBsXpY9ipE7jsw0DCAYmBshmaqU/
90xV/3f6v8eH/mgrJUZpqQ3dwWliTIfHetV+N1ANeCkkKm0pwswuoS8qenVb1R9P
pEIhDLijjZnuYqeGrGs=
=g/CF
-----END PGP SIGNATURE-----
```

The ERS could then post this in Factom.


###### The Submitter Validates Receipts

The submitter would know their Entry Hash, since they posted it themselves. They would review the 13915515269537837/ERS/2015/Receipts chain for an Entry that signs their Entry Hash.

Once they get message above, they would verify that it was actually signed by the ERS, and not a prankster.

First, they would save the data to a file.  In this example we will use `Receipt.txt`.  

They would then run this command:  `gpg --verify Receipt.txt` which will give the output:
```
gpg: Signature made Thu 12 Feb 2015 04:50:08 PM CST using RSA key ID 579228B9
gpg: Good signature from "Example Revenue Service (ERS)"
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 323A 8A02 5793 2F31 C0BF  4C1F 280D 8A92 5792 28B9
```

This shows that the ERS has seen your Entry.  If the convention is that they only sign it if they can read it, then you can be assured their computer received it and can decrypt it.  This would be a high tech equivalent to registered mail.







