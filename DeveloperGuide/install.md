Installing Factom
===
The fastest way to install Factom is to use the Factom installation package provided by [factom.org](http://factom.org). The package contains binaries for factomd, factom-walletd, and factom-cli.

Download the factom [installer package](http://factom.org/downloads/factom.deb) for Debian GNU/Linux.

	$ wget http://factom.org/downloads/factom.deb

Run the Factom Installer. The binaries have been built for 32 bit systems to ensure compatability with older hardware, so on 64 bit systems you must add the ``--force-architecture`` option when installing.

	$ sudo dpkg --force-architecture -i factom.deb

Check that the packages have been installed into their correct locations.

	$ which factomd
	/usr/bin/factomd
	
	$ which fctwallet
	/usr/bin/fctwallet
	
	$ which factom-cli
	/usr/bin/factom-cli

Once the Factom Binaries have been installed successfully, run ``$ factomd`` and let it sync with the Factom network. This may take some time if it is the first time running factomd on a new machine.

You are now running a factom client on your machine!

Installing on a Mac
---
TODO
