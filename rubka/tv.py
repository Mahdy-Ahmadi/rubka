import asyncio
import random
from typing import Optional, Dict, Any

import httpx

class TV:
    BASE_URL_TEMPLATE = "https://rbvod{}.iranlms.ir/"
    META_URL = "https://tv.rubika.ir/meta.json"
    
    DEFAULT_HEADERS = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'fa',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://tv.rubika.ir',
        'referer': 'https://tv.rubika.ir/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    def __init__(
        self,
        auth: str,
        proxy: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
        - auth: توکن احراز هویت حساب کاربری
        - proxy: پراکسی برای ارسال درخواست‌ها (اختیاری)
        - headers: هدرهای سفارشی برای ارسال درخواست‌ها (اختیاری)
        # نکته:
        https://vod.rubika.ir/ 
        """
        self.auth = auth
        self.headers = headers if headers is not None else self.DEFAULT_HEADERS
        self._version: Optional[str] = None
        self.client = httpx.AsyncClient(
            headers=self.headers,
            proxies=proxy,
            timeout=15.0,
            http2=True
        )

    async def _get_version(self) -> str:
        if self._version is None:
            try:
                response = await self.client.get(self.META_URL)
                response.raise_for_status()
                self._version = response.json()['version']
            except httpx.RequestError:
                self._version = "3.2.3"
        return self._version

    def _get_request_url(self) -> str:
        return self.BASE_URL_TEMPLATE.format(random.randint(1, 4))

    async def _request_post(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "auth": self.auth,
            "api_version": "1",
            "client": {
                "app_name": "Main",
                "app_version": await self._get_version(),
                "package": "tv.rubika.ir",
                "platform": "TVWeb",
                "lang_code": "fa"
            },
            "data": data,
            "method": method
        }
        
        try:
            response = await self.client.post(self._get_request_url(), json=payload)
            response.raise_for_status()  
            response_data = response.json()
            
            if 'data' in response_data:
                return response_data['data']
            elif 'status_det' in response_data:
                return {'status_detail': response_data['status_det']}
            raise ValueError("پاسخ نامعتبر از سرور دریافت شد.")
        
        except httpx.RequestError as e:
            
            raise ConnectionError(f"خطا در ارتباط با سرور: {e}") from e

    
    

    async def get_list_items(self, list_id: str, type: str = "Media", start_id: str = "0"):
        return await self._request_post("getListItems", {"list_id": list_id, "type": type, "start_id": start_id})

    async def get_media_by_id(self, media_id: str,track_id:str=None):
        return await self._request_post("getMedia", {"media_id": media_id,"track_id":track_id})

    async def get_custom_menu_items(self):
        return await self._request_post("getCustomMenuItems", {})
    
    async def get_wish_list(self, start_id: Optional[str] = None):
        return await self._request_post("getWishList", {"start_id": start_id})
    
    async def get_Property_Types(self):
        return await self._request_post("getPropertyTypes", {})
    
    async def get_Listing(self, listing_id: Optional[str] = "home"):
        return await self._request_post("getListing", {"listing_id": listing_id})
    
    async def get_me(self):
        return await self._request_post("getAccountInfo", {})

    async def search_video(self, text: str, start_id: Optional[str] = None):
        return await self._request_post("search", {'search_text': text, 'start_id': start_id})

    async def _action_on_media(self, action: str, media_id: str):
        
        return await self._request_post('actionOnMedia', {'action': action, 'media_id': media_id})

    async def like_media(self, media_id: str):
        return await self._action_on_media("Like", media_id)

    async def un_like_media(self, media_id: str):
        return await self._action_on_media("Dislike", media_id)

    async def add_wish_media(self, media_id: str):
        return await self._action_on_media("AddWishList", media_id)

    async def get_cast_medias(self, cast_id: str, start_id: str = "0"):
        return await self._request_post("getCastMedias", {'cast_id': cast_id, 'start_id': start_id})

    async def get_cast_info(self, cast_id: str):
        return await self._request_post("getCastDetails", {'cast_id': cast_id})
    async def get_Season_Episodes(self, season_id: str,series_id:str):
        return await self._request_post("getSeasonEpisodes", {'season_id': season_id,"series_id":series_id})
    async def get_Related(self, media_id: str,start_id:str="0"):
        return await self._request_post("getRelated", {'media_id': media_id,"start_id":start_id})

    
    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()