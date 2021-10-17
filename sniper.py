import json

from web3 import Web3


class Mempool:
    connection = "https://bsc-dataseed1.defibit.io/"
    contract_address = ""

    def __init__(self, connection: str = connection, contract_address: str = contract_address, abi: dict = {}):
        self.connection = Web3(Web3.HTTPProvider(connection))
        self.contract_address = contract_address
        self.address_checksum = Web3.toChecksumAddress(self.contract_address)
        self.contract = self.connection.eth.contract(address=self.address_checksum, abi=abi)

    def __pool_data(self):
        pending_pool = self.connection.geth.txpool.content()['pending']
        pool_json = Web3.toJSON(pending_pool)
        return pool_json

    def explore(self):
        pool_data = json.loads(self.__pool_data())
        filtered_results = [list(pool.items())[0][1]
                            for pool in pool_data.values()
                            if self.contract_address in list(pool.items())[0][1]['to']]

        return filtered_results

    def filter_method(self, method_id: str):
        pool_data = json.loads(self.__pool_data())
        pool_info = [(list(pool.items())[0][1]['hash'],
                      self.contract.decode_function_input(list(pool.items())[0][1]['input'])[1])
                     for pool in pool_data.values()
                     if self.contract_address in list(pool.items())[0][1]['to'] and
                     method_id in list(pool.items())[0][1]['input']]
        return pool_info