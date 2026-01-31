from os.path import exists
from json import loads, dumps

class Sessions:

    def __init__(self, client:object) -> None:
        self.client = client

    def cheackSessionExists(self):
        return exists(f"{self.client.session}.rubka")
    
    def loadSessionData(self):
        return loads(open(f"{self.client.session}.rubka", encoding="UTF-8").read())
        
    def createSession(self):
        from ..methods import Methods
        methods:object = Methods(
            sessionData={},
            platform=self.client.platform,
            apiVersion=6,
            proxy=self.client.proxy,
            timeOut=self.client.timeOut,
            showProgressBar=True
        )

        while True:
            phoneNumber:str = input("\nphone number :\t")
            try:
                sendCodeData:dict = methods.sendCode(phoneNumber=phoneNumber)
            except:
                print("The phone number is invalid! Please try again.")
                continue

            if sendCodeData['status'] == 'SendPassKey':
                while True:
                    passKey:str = input(f'\npass key [{sendCodeData["hint_pass_key"]}]  : ')
                    sendCodeData:dict = methods.sendCode(phoneNumber=phoneNumber, passKey=passKey)
                    
                    if sendCodeData['status'] == 'InvalidPassKey':
                        print(f'\nThe pass key({sendCodeData["hint_pass_key"]})try again.')
                        continue
                    break
            
            while True:
                phoneCode:str = input("\ncode : ").strip()
                signInData:dict = methods.signIn(phoneNumber=phoneNumber, phoneCodeHash=sendCodeData['phone_code_hash'], phoneCode=phoneCode)
                if signInData['status'] != 'OK':
                    print("The code is invalid! Please try again.")
                    continue
                break
            
            from ..crypto import Cryption

            sessionData = {
                'auth': Cryption.decryptRsaOaep(signInData["private_key"], signInData['auth']),
                'private_key': signInData["private_key"],
                'user': signInData['user'],
            }

            open(f"{self.client.session}.rubka", "w", encoding="UTF-8").write(dumps(sessionData, indent=4))

            Methods(
                sessionData=sessionData,
                platform=self.client.platform,
                apiVersion=6,
                proxy=self.client.proxy,
                timeOut=self.client.timeOut,
                showProgressBar=True
            ).registerDevice(deviceModel=f"rubka-Api-{self.client.session}")
            print(f"\nSign successful")

            return sessionData