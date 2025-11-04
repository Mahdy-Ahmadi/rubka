from random import randint
from ..network import Network, Socket
from ..crypto import Cryption
from ..utils import Utils
from time import sleep


class Methods:

    def __init__(self, sessionData:dict, platform:str, apiVersion:int, proxy:str, timeOut:int, showProgressBar:bool) -> None:
        self.platform = platform.lower()
        if not self.platform in ["android", "web", "rubx", "rubikax", "rubino"]:
            print("The \"{}\" is not a valid platform. Choose these one -> (web, android, rubx)".format(platform))
            exit()
        self.apiVersion = apiVersion
        self.proxy = proxy
        self.timeOut = timeOut
        self.showProgressBar = showProgressBar
        self.sessionData = sessionData
        self.crypto = Cryption(
            auth=sessionData["auth"],
            private_key=sessionData["private_key"]
        ) if sessionData else Cryption(auth=Utils.randomTmpSession())
        self.network = Network(methods=self)
        self.socket = Socket(methods=self)


    def sendCode(self, phoneNumber:str, passKey:str=None, sendInternal:bool=False) -> dict:
        input:dict = {
            "phone_number": f"98{Utils.phoneNumberParse(phoneNumber)}",
            "send_type": "Internal" if sendInternal else "SMS",
        }

        if passKey:
            input["pass_key"] = passKey

        return self.network.request(
            method="sendCode",
            input=input,
            tmpSession=True
        )
    
    def signIn(self, phoneNumber, phoneCodeHash, phoneCode) -> dict:
        publicKey, privateKey = self.crypto.rsaKeyGenrate()

        data = self.network.request(
            method="signIn",
            input={
                "phone_number": f"98{Utils.phoneNumberParse(phoneNumber)}",
                "phone_code_hash": phoneCodeHash,
                "phone_code": phoneCode,
			    "public_key": publicKey
            },
            tmpSession=True
        )
        
        data["private_key"] = privateKey

        return data
    
    def registerDevice(self, deviceModel) -> dict:
        return self.network.request(
            method="registerDevice",
            input={
                "app_version": "WB_4.3.3" if self.platform == "web" else "MA_3.4.3",
                "device_hash": Utils.randomDeviceHash(),
                "device_model": deviceModel,
                "is_multi_account": False,
                "lang_code": "fa",
                "system_version": "Windows 11" if self.platform == "web" else "SDK 28",
                "token": "",
                "token_type": "Web" if self.platform == "web" else "Firebase"
            }
        )
    
    def getChatAllMembers(self, objectGuid:str, searchText:str, startId:str, justGetGuids:bool=False) -> dict:
        chatType:str = Utils.getChatTypeByGuid(objectGuid=objectGuid)

        data = self.network.request(
            method=f"get{chatType}AllMembers",
            input={
                f"{chatType.lower()}_guid": objectGuid,
                "search_text": searchText.replace("@", "") if searchText else searchText,
                "start_id": startId
            }
        )

        if justGetGuids: return [i["member_guid"] for i in data["in_chat_members"]]

        return data