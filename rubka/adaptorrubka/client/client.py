from ..methods import Methods

class Client(object):

    def __init__(
        self,
        session:str=None,
        auth:str=None,
        private:str=None,
        platform:str="web",
        api_version:int=6,
        proxy:str=None,
        time_out:int=10,
        show_progress_bar:bool=True
    ) -> None:
        
        self.session = session
        self.platform = platform
        self.apiVersion = api_version
        self.proxy = proxy
        self.timeOut = time_out
        
        if(session):
            from ..sessions import Sessions
            self.sessions = Sessions(self)

            if(self.sessions.cheackSessionExists()):
                self.sessionData = self.sessions.loadSessionData()
            else:
                self.sessionData = self.sessions.createSession()
        else:
            from ..utils import Utils
            self.sessionData = {
                "auth": auth,
                "private_key": Utils.privateParse(private=private)
            }

        self.methods = Methods(
            sessionData=self.sessionData,
            platform=platform,
            apiVersion=api_version,
            proxy=proxy,
            timeOut=time_out,
            showProgressBar=show_progress_bar
        )

    def send_code(self, phone_number:str, pass_key:str=None) -> dict:
        return self.methods.sendCode(phoneNumber=phone_number, passKey=pass_key)
    
    def sign_in(self, phone_number:str, phone_code_hash:str, phone_code:str) -> dict:
        return self.methods.signIn(phoneNumber=phone_number, phoneCodeHash=phone_code_hash, phoneCode=phone_code)
    
    def register_device(self, device_model:str) -> dict:
        return self.methods.registerDevice(deviceModel=device_model)
    
    def logout(self) -> dict:
        return self.methods.logout()
    
    def get_all_members(self, object_guid:str, search_text:str=None, start_id:str=None, just_get_guids:bool=False) -> dict:
        return self.methods.getChatAllMembers(objectGuid=object_guid, searchText=search_text, startId=start_id, justGetGuids=just_get_guids)