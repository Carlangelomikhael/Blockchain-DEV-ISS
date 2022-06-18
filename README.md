![ISS logo](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/static/iss.png)

# Blockchain Development Using Python

## CONTENTS OF THIS FILE

 * Introduction 
 * Requirements
 * Overview
 * Instructions
  
### INTRODUCTION
------------
This project is a simple **Proof Of Work** [(POW)](https://www.investopedia.com/terms/p/proof-work.asp) [Blockchain](https://www.investopedia.com/terms/b/blockchain.asp) ecosystem with its wallet built from scratch with **Python**.
Our main goal is to offer the basic services of a [Cryptocurrency](https://www.investopedia.com/terms/c/cryptocurrency.asp) in a [LAN](https://www.cisco.com/c/en/us/products/switches/what-is-a-lan-local-area-network.html).
This **Blockchain** ecosystem enables users to create wallets, transact with other peers in their LAN and to participate in building the Blockchain by [mining](https://www.investopedia.com/tech/how-does-bitcoin-mining-work/) new Blocks. 

### REQUIREMENTS
------------
* [Python 3](https://www.python.org/downloads/)
* Create a seperate directory on your device that will store all the client or server files.
* Install requirements.txt file:
  * First Step: Place the file in the folder that you created earlier.
  * Second Step: Open your **CMD** and make sure the current **working** directory is the project's folder directory.
  * Third Step: Write ***pip install requirements.txt*** and then press the enter key.
  *Example*: If your project has this path **C:\Users\User\ISSCORE** then:
  ```bash
  C:\Users\User\ISSCORE>pip install requirements.txt
  ```
### OVERVIEW
------------
[classes.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/classes.py) is the main file, it contains all the **Blockchain's** elements as Classes (Block,Transaction,Input,Output) in addition to that it contains the Wallet, ObjectDesc and Database Classes.
* The **Block** Class contains 2 main methods: The **computeHash** function that calculates the hash of the current block instance and the **mine** function that utilizes the former function to reach the target nonce of the block.
* The **Transaction** Class contains 2 main methods: The **computeTxId** function that calculates the transaction id of the current transaction instance and the **calculateFees** function that calculates the fees of the transaction.
* The **Input** and **Output** Classes have no methods, they are stored in the transaction instance and represents the inputs and outputs of the transaction.
* The **Wallet** Class has several methods, the main ones are: The **balance** function that calculates the wallet's balance, the **constructTx** and **constructCoinbaseTx** functions that constructs 2 different types of transactions ( a normal peer-2-peer transaction and a reward transaction for the miner respectively) and the **sign** function that provides a private key signature.
* The **Database** Class is conceived to make it easy for us to insert/remove/update/query objects from our database.
* The **ObjectDesc** Class is stored as an attribute in every class, it provides an object description for every instance. This class enables the use of a single function to insert/remove/update/query any object regardless of it's type.

The [server.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/server.py) file is basically a server that has to be run on a machine, and nodes from the same LAN can connect to it by running the [client.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/client.py) file on their machines.
The client and server exhanges data through TCP sockets, the server will send all the updates made on the database to the node once its connected.

The [KeysGeneration.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/KeysGeneration.py) file contains 2 main functions: The **generate** function that generates the wallet's **Public and Private Keys**, the **pubkeyToAddr** function that transforms a pubkey to a valid **BTC** address.

The [home.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/home.py) contains the **main window** that the node will operate on and the **result window** that displays results based on our research criteria.

The [welcome.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/welcome.py) is the **welcome window** displayed only the first time the node wants to connect.

The [init_database.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/init_database.py) is the file that will create the initial database with all the tables.

### INSTRUCTIONS
------------
#### -> The Server:
* Create a folder that contains the following files:
  * server.py
  * classes.py
  * init_database.py
  * requirements.txt

* Install the requirements.txt file with the steps described in [Requirements](#Requirements)

Now the server is ready, you can *execute* the file on your **IDE**, or open your **CMD** in the directory of the files then type **python server.py** and press `Enter`:

![running console](https://user-images.githubusercontent.com/88195134/174439195-62251362-dfd0-46d0-8a4f-5add2be53055.png)
The **server** is listening as **192.168.56.1** on port **50000**.

#### -> Client Connection:
* Create a folder that contains the following files:
  * client.py
  * classes.py
  * init_database.py
  * requirements.txt
  * home.py
  * welcome.py
  * KeysGeneration.py

* Install the requirements.txt file with the steps described in [Requirements](#Requirements)

* In the case where you are running both **client** and **server** on the **same machine** you are ready to go:
You can *execute* the file on your **IDE**, or open your **CMD** in the directory of the files then type **python welcome.py** and press `Enter`:
The following window will appear, then press OK.

![welcome window](https://user-images.githubusercontent.com/88195134/174439564-d5ccc3e3-4c19-43fb-a4dc-79b7b621b0e2.png)

Then the **home** window will be displayed and you are connected to the server, you can now **transact*, *mine* and *search** for blocks and transactions.

![home window](https://user-images.githubusercontent.com/88195134/174439759-2ae60d37-ef8b-4b40-8d1d-da7a6b748c47.png)

* In the case where the **client** and **server** are on **different hosts** in the same **LAN**, all you have to do is to get the server's **IPv4 Address** and **Port** then set those variables in the **home.py** file: https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/home.py#:~:text=%23%20The%20ip%20address,port%20%3D%2050000 .
