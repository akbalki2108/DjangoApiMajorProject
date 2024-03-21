# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from web3 import Web3
# from web3 import Web3, EthereumTesterProvider



# from appapi.models import ToggleSettings
# ToggleSettings.objects.create()




# import os
# from dotenv import load_dotenv
# project_folder = os.path.expanduser('/home/aditya2108/DjangoApiMajorProject')
# load_dotenv(os.path.join(project_folder, '.env'))
# # load_dotenv()
# contract_address = os.environ.get('CONTRACT_ADDRESS')
# mywallet = os.environ.get('MY_WALLET')
# myprivatekey = os.environ.get('PRIVATE_KEY')
# print(contract_address)

# blockchain_url = 'https://sepolia.infura.io/v3/ab071685741847ff8ab969312efc0cfe'

# contract_abi =[
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "_date",
# 				"type": "uint256"
# 			},
# 			{
# 				"internalType": "uint256",
# 				"name": "_numCandidates",
# 				"type": "uint256"
# 			},
# 			{
# 				"internalType": "uint256[]",
# 				"name": "_candidateIds",
# 				"type": "uint256[]"
# 			},
# 			{
# 				"internalType": "string[]",
# 				"name": "_partyNames",
# 				"type": "string[]"
# 			},
# 			{
# 				"internalType": "uint256",
# 				"name": "_numMachines",
# 				"type": "uint256"
# 			},
# 			{
# 				"internalType": "uint256[]",
# 				"name": "_machineIds",
# 				"type": "uint256[]"
# 			}
# 		],
# 		"name": "startElection",
# 		"outputs": [],
# 		"stateMutability": "nonpayable",
# 		"type": "function"
# 	},
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "_date",
# 				"type": "uint256"
# 			},
# 			{
# 				"internalType": "uint256",
# 				"name": "_machineId",
# 				"type": "uint256"
# 			},
# 			{
# 				"internalType": "uint256",
# 				"name": "_candidateId",
# 				"type": "uint256"
# 			}
# 		],
# 		"name": "vote",
# 		"outputs": [],
# 		"stateMutability": "nonpayable",
# 		"type": "function"
# 	},
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "",
# 				"type": "uint256"
# 			}
# 		],
# 		"name": "elections",
# 		"outputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "date",
# 				"type": "uint256"
# 			},
# 			{
# 				"internalType": "uint256",
# 				"name": "numCandidates",
# 				"type": "uint256"
# 			},
# 			{
# 				"internalType": "uint256",
# 				"name": "numMachines",
# 				"type": "uint256"
# 			}
# 		],
# 		"stateMutability": "view",
# 		"type": "function"
# 	},
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "_date",
# 				"type": "uint256"
# 			}
# 		],
# 		"name": "getAllCandidates",
# 		"outputs": [
# 			{
# 				"internalType": "uint256[]",
# 				"name": "",
# 				"type": "uint256[]"
# 			},
# 			{
# 				"internalType": "string[]",
# 				"name": "",
# 				"type": "string[]"
# 			},
# 			{
# 				"internalType": "uint256[]",
# 				"name": "",
# 				"type": "uint256[]"
# 			}
# 		],
# 		"stateMutability": "view",
# 		"type": "function"
# 	},
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "_date",
# 				"type": "uint256"
# 			}
# 		],
# 		"name": "getAllMachines",
# 		"outputs": [
# 			{
# 				"internalType": "uint256[]",
# 				"name": "",
# 				"type": "uint256[]"
# 			},
# 			{
# 				"internalType": "uint256[]",
# 				"name": "",
# 				"type": "uint256[]"
# 			},
# 			{
# 				"internalType": "string[]",
# 				"name": "",
# 				"type": "string[]"
# 			}
# 		],
# 		"stateMutability": "view",
# 		"type": "function"
# 	},
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "_date",
# 				"type": "uint256"
# 			}
# 		],
# 		"name": "getTotalCandidates",
# 		"outputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "",
# 				"type": "uint256"
# 			}
# 		],
# 		"stateMutability": "view",
# 		"type": "function"
# 	},
# 	{
# 		"inputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "_date",
# 				"type": "uint256"
# 			}
# 		],
# 		"name": "getTotalMachines",
# 		"outputs": [
# 			{
# 				"internalType": "uint256",
# 				"name": "",
# 				"type": "uint256"
# 			}
# 		],
# 		"stateMutability": "view",
# 		"type": "function"
# 	}
# ]



# from dotenv import load_dotenv
# load_dotenv()


# w3 = Web3(Web3.HTTPProvider(blockchain_url))
# print(w3.is_connected())

# pk = os.environ.get('PRIVATE_KEY')
# mywallet = os.environ.get('MY_WALLET')
# contract_address = os.environ.get('CONTRACT_ADDRESS')

# print("Private Key:", pk)
# print("My Wallet:", mywallet)
# print("Contract Address:", contract_address)


# chain_id = w3.eth.chain_id
# print(chain_id)

# wallet = w3.to_checksum_address(mywallet)

# balance_wei = w3.eth.get_balance(wallet)
# balance_ether = w3.from_wei(balance_wei, 'ether')

# print(balance_ether)
# print(balance_wei)

# #create instance
# contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)

# date = 1648876800
# # date_uint256 = date.to_uint256(date)

# total_supply = contract_instance.functions.getTotalMachines(date).call()
# print(total_supply)


 

# from datetime import date
# import time

# # Get today's date
# today = date.today()
# unix_timestamp = int(time.mktime(today.timetuple()))
# # print(today)
# print(unix_timestamp)


# # Example parameters
# _date = unix_timestamp
# _num_candidates = 4
# _candidate_ids = [1, 2, 3, 4]
# _party_names = ["Party A", "Party B", "Party C", "Party D"]
# _num_machines = 3
# _machine_ids = [101, 102, 103]


# txn_params = {
# 	'to': contract_instance.address,  # Replace with the contract address
# 	'from': mywallet,  # Replace with your wallet address
# 	'gas': 3000000,  # Adjust gas limit as necessary
# 	'nonce': w3.eth.get_transaction_count(mywallet),
# 	'data': contract_instance.encodeABI('startElection', [_date, _num_candidates, _candidate_ids, _party_names, _num_machines, _machine_ids]),
# 	'maxFeePerGas': w3.to_wei(250, 'gwei'),
# 	'maxPriorityFeePerGas': w3.to_wei(2, 'gwei'),
#     'chainId': chain_id,
# }

# signed_txn = w3.eth.account.sign_transaction(txn_params, private_key=pk)

# # Send the transaction
# tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# print(tx_hash)

# # Wait for the transaction receipt
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# print("Transaction successful:", tx_receipt)