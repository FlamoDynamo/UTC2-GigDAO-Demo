# deploy.py
from algosdk.v2client import algod
from smart_contracts.contract.contract import GigDAOContract
from smart_contracts.contract.nft_contract import NFTMintingContract

def deploy():
    # Sử dụng Algonode.io cho testnet
    algod_address = "https://testnet-api.4160.nodely.dev/"
    algod_token = ""  # Algonode không yêu cầu token
    
    try:
        # Khởi tạo Algod client
        algod_client = algod.AlgodClient(algod_token, algod_address)

        # Kiểm tra kết nối
        status = algod_client.status()
        print(f"Kết nối thành công. Phiên bản node: {status['last-round']}")

        # Lưu ý: Bạn cần cung cấp địa chỉ và private key của người triển khai
        # Thay thế các giá trị dưới đây bằng địa chỉ và private key thực tế
        address = "MV7HWZVFW64CK2A5JCUEXXWORNZRIRQLPPNAUPO4IP4AHMZ7XB6BU2ZSNM"
        private_key = "tree river prefer carry lift together charge priority cloud oxygen model twin hockey citizen deputy baby flip security bullet dry seat concert special about pride"

        print(f"Địa chỉ người triển khai: {address}")

        # Triển khai GigDAO Contract
        gig_dao_contract = GigDAOContract(algod_client)
        gig_dao_app_id = gig_dao_contract.create_gig_dao(address, private_key)
        print(f"GigDAO Contract đã được triển khai với app_id: {gig_dao_app_id}")

        # Triển khai NFT Minting Contract
        nft_minting_contract = NFTMintingContract(algod_client)
        nft_minting_app_id = nft_minting_contract.create_nft_minting_contract(address, private_key)
        print(f"NFT Minting Contract đã được triển khai với app_id: {nft_minting_app_id}")

        print("Tất cả các contract đã được triển khai thành công!")

    except Exception as e:
        print(f"Lỗi khi triển khai: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    deploy()
