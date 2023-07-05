# blockchain-apis-speed-benchmark

The goal of this repository is to compare Blockchain APIs speed vs an Ethereum node in Python.

We use [web3.py](https://pypi.org/project/web3/) for the Python client and [blockchain-apis](https://pypi.org/project/blockchain-apis/) for the Python API client.

## What is tested

During the test, we simulate the selling of every token of a wallet in exchange of Ethereum.

## How to run

You can edit the file "config.yml" by adding your tokens.
You also must edit the .env file in order to put your HTTP_RPC endpoint to interact with the Ethereum Node and Blockchain APIs key

Once you edited, you need to install dependencies:

`pip install -r requirements.txt`

Then you can run the program:

`python main.py`

You will get the time printed in the terminal and results inside of a .csv file
