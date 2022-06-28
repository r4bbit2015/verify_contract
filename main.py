import json
import time
from settings import *
import requests
def read_file(file_name):
    with open (file_name,'r') as f:
        return f.read()

def verify_contract(contract_code,contract_address,contract_name,contract_version):
    #TestNet默认为True
    if TestNet:
        urls = "https://api-testnet.bscscan.com/api"
    else:
        urls = "https://api.bscscan.com/api"

    headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36",
               'Content-Type': 'application/x-www-form-urlencoded'}
    payloads = {"apikey":API_KEY,
                "module":"contract",
                "action":"verifysourcecode",
               "sourceCode":contract_code,
               "contractaddress":contract_address,
               "codeformat":"solidity-single-file",
               "contractname":contract_name,
               "compilerversion": contract_version,
               "optimizationUsed":0# 0无优化 1优化
               }
    print(f"ContractName:{contract_name}")
    print(f"ContractAddress:{contract_address}")
    print(f"ContractVersion:{contract_version}")
    try:
        res = requests.post(urls,headers=headers,data=payloads).json()
        if res['status'] == "0" :
            print(res["result"])
        else:
            print(f"GUID:{res['result']}")
            return res['result']
    except Exception as e:
        print(e)

def check_verify_status(guid):
    # TestNet默认为True
    if TestNet:
        urls = "https://api-testnet.bscscan.com/api"
    else:
        urls = "https://api.bscscan.com/api"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36",
        'Content-Type': 'application/x-www-form-urlencoded'}
    payloads = {"apikey": API_KEY,
                "module": "contract",
                "action": "checkverifystatus",
                "guid" : guid
                }
    try:
        while True:
            "Contract source code already verified 12"
            "Pending in queue  16"
            "Pass - Verified  15"
            res = requests.post(urls, headers=headers, data=payloads).json()
            lens = len(res['result'])
            if lens == 12:
                print("合约已验证")
                break
            elif lens == 16:
                print("合约正在验证")
            elif lens == 15:
                print("合约验证通过")
                break
            time.sleep(10)
    except Exception as e:
        print(e)

#https://bscscan.com/solcversions
#https://docs.bscscan.com/api-endpoints/contracts#check-source-code-verification-submission-status



def main():
    contract_code = read_file("合约源码.sol")
    contract_address = Web3.toChecksumAddress("部署的合约地址")
    contract_name = "合约名称" #合约名称一定要写准确，否则无法通过
    contract_version = "v0.8.6+commit.11564f7e" #编译版本
    check_verify_status(verify_contract(contract_code,contract_address,contract_name,contract_version))


if __name__ == '__main__':
    main()
