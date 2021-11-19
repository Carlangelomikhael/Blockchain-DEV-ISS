![ISS logo](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/static/iss.png)

# Blockchain Development Using Python

## CONTENTS OF THIS FILE

 * Introduction 
 * Requirements
 * Overview
  
### INTRODUCTION
------------
This project is a simple **Proof Of Work** [(POW)](https://www.investopedia.com/terms/p/proof-work.asp) [Blockchain](https://www.investopedia.com/terms/b/blockchain.asp) ecosystem built from scratch with **Python**.
Our main goal is to offer the basic services of a [Cryptocurrency](https://www.investopedia.com/terms/c/cryptocurrency.asp) in a [LAN](https://www.cisco.com/c/en/us/products/switches/what-is-a-lan-local-area-network.html).
This **Blockchain** ecosystem enables users to create accounts, transact with other peers in their LAN and to participate in building the Blockchain by [mining](https://www.investopedia.com/tech/how-does-bitcoin-mining-work/) new Blocks. 

### REQUIREMENTS
------------
* [Python 3](https://www.python.org/downloads/)
* Install requirements.txt file:
  * First Step: Open your **CMD** and make sure the **working** directory is the project's folder directory.
  * Second Step: Write ***pip install requirements.txt*** and the enter.
  *Example*: If your project has this path **C:\Users\User\Blockchain** then:
  ```bash
  C:\Users\User\Blockchain>pip install requirements.txt
  ```
### OVERVIEW
------------
[app.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/app.py) is the main file, it contains all the **Blockchain's** elements (Blocks,Nodes,Transactions) and implements the *majority* of the functionalities we need 
like the interface (made with [Flask](https://flask.palletsprojects.com/en/2.0.x/)) that **nodes** visit to signup or login to their **wallet** that enables them to transact, check the Blocks already mined and the unconfirmed transactions.

The [server.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/server.py) and [client.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/client.py) files are required in order too generate *public* and *private* [**RSA**](https://stuvel.eu/python-rsa-doc/) key pairs (without the keys you **won't** be able to transact) and it allows *registered* nodes to participate in the **mining** process.
The server.py file is basically a server that has to be run on a machine, and nodes from the same LAN can connect to it by running the client.py file on their machines.
