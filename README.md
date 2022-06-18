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

The [server.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/server.py) and [client.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/client.py) files are required in order too generate *public* and *private* [**RSA**](https://stuvel.eu/python-rsa-doc/) key pairs (without the keys you **won't** be able to transact) and it allows *registered* nodes to participate in the **mining** process.
The server.py file is basically a server that has to be run on a machine, and nodes from the same LAN can connect to it by running the client.py file on their machines.

### INSTRUCTIONS
------------
#### -> The Flask App:
After installing all the files, you can run the [app.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/app.py) file and it will launch the flask app server on a random IP on port 5000. If you're on Pycharm's IDE your running console will look like this:

![running console](https://user-images.githubusercontent.com/88195134/143781704-52e153ca-4b1b-4c47-95e3-bdfe4cfcbac9.png)
You can click on **http://<i></i>192.168.0.111:5000/** or you can open your web browser and insert it in the search tab and the home page will pop up:

![Home page](https://user-images.githubusercontent.com/88195134/143782155-24f006d6-5e51-4312-bd1d-5fbd2308da0e.png)
Now anyone on your **LAN** can access this page and interact (signup/login/transact...) by typing **http://<i></i>192.168.0.111:5000/** in their web browser.

#### -> The Server:
* Open your **CMD** and type ipconfig/all then enter:

![CMD](https://user-images.githubusercontent.com/88195134/143783432-1ed1ae32-36d3-4588-962e-32724da0295c.png)           
If you are connected on *Wifi* check for the **Wireless LAN adapter Wi-Fi** section and find your **IPv4 Address**, in the example above it's **192.168.0.111**. 
* Open the [server.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/server.py) file and replace the `SERVER_HOST` variable in line *10* with your **IPv4 Address**.
* Open the [client.py](https://github.com/Carlangelomikhael/Blockchain-Dev-Iss/blob/main/client.py) file and replace the `host` variable in line *56* with your **IPv4 Address**.

Now the server is ready, you can *execute* the file on your **IDE**, or open your **CMD** in the directory of the files then type **python server.py** and press `Enter`:

![running console](https://user-images.githubusercontent.com/88195134/143784939-34ba3a87-2c05-433e-90bc-ebde26a9a064.png)
The **server** is listening as **192.168.0.111** on port **5001**.

#### -> Client Connection:
Open your **CMD** in the directory of the files then type **python server.py node_id password** and press `Enter`:

![CMD](https://user-images.githubusercontent.com/88195134/143785802-90ca3b81-10ca-40ec-a54e-ae24af2442b4.png)
You have 3 choices : you can set your **Public Key** and **Private Key**  ,**Mine** new blocks and **Close** the connection to the server.     
**NB:** If you chose a service that is not **available** at the moment you'll get a message then you'll be able to remake a new choice. However if the service is available, upon completion the **connection to the server will end** and you have to reconnect if you need another service.


