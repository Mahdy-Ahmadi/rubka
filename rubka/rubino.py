import urllib3
import json
from typing import Any, Dict
from tempfile import NamedTemporaryFile
from os import system, chmod, remove
from base64 import b64encode
from io import BytesIO
class confing():
    headers= {
        "User-Agent": "okhttp/3.12.1",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json; charset=UTF-8"
        }
    server = {
            "rubino": "https://rubino17.iranlms.ir",
            "messenger": "https://messengerg2c137.iranlms.ir"
        }
    android = {
        "app_name": "Main",
        "app_version": "3.7.3",
        "lang_code": "fa",
        "package": "app.rbmain.a",
        "platform": "Android",
        "store": "Myket",
        "temp_code": "34"
    }
    th=b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xdb\x00C\x01\t\t\t\x0c\x0b\x0c\x18\r\r\x182!\x1c!22222222222222222222222222222222222222222222222222\xff\xc0\x00\x11\x08\x00\x80\x00\x80\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xc4\x00\x1f\x01\x00\x03\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\x00\x01\x02w\x00\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13"2\x81\x08\x14B\x91\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1\x17\x18\x19\x1a&\'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xf0\'\x8c\xa6\x18\x1c\xabt5>\x9e\x86k\xe8\x93 |\xc0\x9c\xfbT+)\xd8c<\xafQ\xecj\xc6\x9a\xfe]\xd1\x93h;T\x9akp\x13S\xc7\xf6\x8c\xf8\xe7\r\xda\xa2\x8eL\xa0\x89\x80\xda\x1bwJI\xa4\xf3fg\xc67\x1c\x9agL\x9a:\x81n\x04YfuF\xfe\x1c\n\x80\x83\xb7\x90s\x9c`Q\x03\x98g\rS]\xc2\x11\x84\x8ar\xaf\xcf\xd0\xd3\x11T\xe74\xe0\x0e\xe0\xb8\xe5\x88\xc6i>R\xbc\xf0i\xf0\x96i\x90.\t\xc8\x14\x86i\xdd\\5\xb5\xb1\x89H\x1c\xf0\x0fZ\xcd\x8ap\x8d\x9d\xb8\x1d\xea\xe6\xa2w\x91\x91\xf7{\x8a\xa3\x1c~c\x0c\x0e;\xd3{\x89\x1a-2\xc3\xa61S\xf3\xb9\xaa0\x1d\xeeT\x9e\x0e(\xbb\x93t\x9b\x00\xc2\xafj\x859=y\xa1\xbd@\xbblM\x9c\xd2N\xc3;Q\x82\x9cq\xb8\xf0*\x91#\x1bGO\\U\xbb\x99\x8f\xd9#\xb7\x07\xa3\x17n:z\x7fZ\xa5I\x8c\xb5-\xb1Xcq\xf7H\xc9&\xab\x10GPjq.\xf8\x94;\x12Tm\x03\xda\x9f9\xcc#\x07\xa9\xe9@\x15*\xfd\x8a\x01\x04\xf26p\x17\x19\xaa>\x95\xa5o\xb5t\x99Y\xb3\x96\x93h\xe7\x8a\x10\x99C\xe5$\x03\x90=ibe\x0c\xd9\x19\xe0\xe2\x92A\x83\x9e9\xedH\x83,=;\xd00l\x9c6z\xd5\xe5\xc5\xcd\x81P~h\xf2qRi\xfa-\xe6\xa9pm\xac\xe12:\x8f1\xdc\xb0T\x89?\xbc\xecxQ\xeeMtvz~\x9f\xa5\xa3%\xac\x03Z\x9d@\xf3\xae&c\x05\x8c\x07\xeaH/\xf8\x95\x07\xd0\xd3\x11\xc6A\x0c\x93\xc8#\x867\x96C\xd1QK\x1f\xc8WI\xa6\xf8C_\xdd\xe6\xff\x00b_\x92G\xc9\xba\xd9\x87\xf3\x15\xa1>\xb0\xeb\t\x88\xebR\xf99\xff\x00\x8fm\x16\x01m\x0f\xd0\xb6\x14\xb7\xe2\xa7\xebT\xae\xf5-&\xddAm*y\xd8\x9e\x1ak\xd6\xcf\xfe:\xa2\x84\x82\xe5]c\xc3\xba\xf5\x94"K\xdd\x16\xfe\xdd\x00\xcbH\xf6\xec\x14{\x13\x8cV,\x12yA\x8ex#\x15\xd2\x8doO\x80-\xc4v\xba\x9d\xa3\x1e\x15\xac\xf5&R?\xef\xa54\xf95\x0b-P$f\xfe\x1b\xb2\xee\x07\x97\xaa\xdb\x88\xa4\x1f\xf6\xdd\x0f\xea\xc4\x0fj\x1e\xe0r\x04\x92I=M[\xd34\xe9u+\xa1\x14c\n9v\xec\xa2\xba\x91\xe0\x83s\x7f\x1cPG=\xb4\xc7\r\xf6;\xa2\x0f\x98=b\x95~Y\x07\xe4}3I\xa9\xcdk\xa0A=\x84Q\xbcw\x92\xe5]1\x8d\x83\x1d\xfb\x83\xedB\x8fV\r\xf49\x89<\xb9.\xe4\xf2\xc7\xeeA\xda\xb9=\x87CT\xd8\x8d\xc7\x1d*h\xd7\xf7L\xdb\xbbt\x07\xadAI\x8c|N#\x90\x16\x1b\x97\xa1\x1e\xb5bF\x8eW\x05S`\x03\xa7Z\xabR#g\xe5n\xe7\xad\x08\x08\xfd\xea\xfc\xd8\x87M\x823\x82X\x97\xfc\xea\xac\x11y\xd3$c\xa3\x1a\x9a\xfe@\xd3y`}\xc1\xb7\xad\x02+u\xeaz\n\xd1\xd1\xf4\xd3\xaaj\x1eP\x99-m\xe3S,\xf72\x02V\x18\xc7V#\xa9\xea\x00\x1d\xc9\x03\xbdf\xe7\x8c\x01\xd6\xba\xfb\x8b(\xf4\xb8\x1bL\x9ds\x05\x92\xa5\xc6\xab\xb5\xb6\x99f?r\xdf?\xec\xe7\x07\xdfy\xec(\x195\xce\xa3b\x9aP\x89\xa2\x9a\xdfC\x07u\xad\x82\x9d\xb3j.\t\x1el\xec:/^\x9c\x0e\x8b\xdd\xab\x9e\xd5\xf5{\x9dU\xe1\x8eGX\xe0\x851\x1c\x11\x8d\xb1\xc7\xdf\xe5_\xeb\xc9=\xc9\xaa\xd7\xf7\xf2\xea\x13=\xc4\xc5|\xc7a\xf2\xa8\xc2\xaa\x81\x80\xaa;\x00\x00\x00zT\n\xad)b\xa0\x96\xcfjb/i\xf3-\xb9\x91$\\\x92\xb9P}j\xbd\xdc\xedrw\xb1\x1d;WS\xe1\xef\x00j\xda\x9c\x1f\xda\x17\x05l\xec\xd4\xed\xf3e\x1dI\x1d\x87z\xe8\xafm|1\xe1+;h\x8a\x89.wnw\x99\x033\x83\xe8;t\xae\xda8)\xd4W\x93\xe5\x8fvsO\x13\x08\xcb\x96:\xbf#\xceYC\xd8\x9eFTg\x19\xa8l-\xbe\xd3r\xa9\xd4u#\xd6\xbd\x82\xff\x00\xc3\xfe\x17\xf1O\x86\xad\xe5\xd2\xa4\xb6\x8a\xf4\x00\xa7g\xca\xd9>\xab\xdf\x15\x81w\xf0\xefX\xf0\xf3$\xc6\x06\x9e\xd88\x06h\x97\xa0\xf7\x1d\xaaj\xe1%\x0bIj\x85O\x15\t{\xafG\xd9\x89k\xa9\xa7\x86\xf4&\xdf\x1f\x9do!\xe2\xdeC\x80O\xb7\xf7O\xb8\xfdk"\xfako\x122\x1b\x9b\xbf6F\xc2\xda\xdf\xcf\x85\x91Oh.\x0f\xe8\xb2\x7fN\x16\x97\x8c/L\x971Z\x0c\x01\x10\xc9\xfa\xd6&\x9bs\xf6[\xa0\x1d<\xc8%\x1b&\x88\x9cy\x89\x9eF{\x1e\xe0\xf6 W4\xde\xb6:b\xb4\xb8O\x1c\x96fKy\xe0x\xa6G*U\xc7\xdd#\x82\r@\x90\xf9\x99\xc3\xa0>\xed\x8a\xe95\xcbcyb\n\xb9\x96\xe2\xca0\xdef1\xf6\x8bl\xedG#\xfb\xcb\xc2\x9fl\x7ft\xd70\x08\xc7Nj\x18\xd0\xa3(\xff\x000\xce\x0f<\xd4\xcb\t\xba\x93\x11\xa6\x18\x8e\x14T*\xb9\x19\xed@vC\xc3\x1f\xc0\xe2\x81\x93X\xb6\xcb\xc8\x9b\xd0\xd4w\x00-\xcc\x98\xe7\xe64\x80\x15\x90m\xedH\xe5\x8f^\xbc\x9c\xfa\xd0\x06\xbf\x86\x12$\xd5\x8d\xfd\xc2\x86\x87O\x89\xae\xd9OFe\xfb\x8b\xf8\xb9A\xf4&\xa7\xd7\xcb\xd9\xd9\xd9XK!\x92\xeat\x17\xf7\x8cO-$\xa3(\x0f\xd1\x08?Wjn\x8d\x0f\x9b\xa1\xde\xc2\x84y\xd7\x97v\xd6\xab\xeb\xb4\x96c\xfa\xaaS\xfcK|\xb3x\x9bT\x9e5\x0e\xe6\xe1\x91\x18\x8e\x11T\xedP>\x8a\x00\xa1!\x190\xd8K$\xb1\xa1\x003\x90\x02\xf7\xe6\xbdW\xc3\xde\x0e\xb5\xd1\xe4[\xdb\xe3\x0c0C\x83%\xd4\xe4c\x91\x92\x15{\x9ez\xfdk\x85\xf0?\x95s\xe3\xed\x15o>x^\xed\x03\x03\xc8<\xd7\xa0|l\xbb\x91uK-&\xd9H\x85\x10\xbb\x05\xfe\'\xff\x00\xf5W~\x16p\xa7\tT\xe5\xbb\xe9\xe4qb\x1c\xa5R4\x93\xb2f\x7f\x8d\xfe$Gz\x91iz\x0co\x05\xac*G\x9ez\xbf\xa9\x03\xb5y\xbb\xc8\xf3j\n\xf3;\xca\xc4\xe7$\xee$\xf5\xad\xed\x0f\xc33j\xba\xd4\x16l\xf88\xdf.?\x85G_\xc6\xbd\x03Q\xd4\xfc-\xe1U\xb7\xb5\x86\x14I@\xde\x02\xc4\x1eB\xd8\xc1\xdcO\xadTi\xcf\x10\xb9\xaaJ\xd1B\xe6\x85\x0f\xdd\xd3\x8d\xd9\xe5P\xea76\xba\x94W\x11;D\xc8\xd9\x1bx\xcf\xf8\xd7\xbe\xf8\x17\xe2D3\xe9\xdb5\xff\x00\xdd\xc9\xff\x00?\x18\xca\x91\xee;V\x1e\x91m\xe1\xcf\x1fG\x046\xe8\x0c\xb1\xa9S\x13\xae\xd9\x10z\xe7\xff\x00\xd7X>6\xd1\x7f\xe1\n\x8d\xec\xe4m\xd1\xb8\x02&\xe7\xe6\x07\xaf\xe5SR\x9f\xb2^\xec\xae\x98\xb9\xa1]\xf2\xca6\x922<{i\xa7\xeb\xda\xb6\xa1\xach\xc4\x11\xe6\x12\xea\xa3\nTq\x90\x05p\x11\xa1,\xbc\x9f\\\x8e\xd5\xd2\xf8Y\xae\xae>\xdf\x04\x12\x10\x85C:\x91\x9c\x8c\xf6\xf7\xe7\xf5\xac\xf9-\xcd\xb5\xfc\xf0\x18\xd9Hr\x9f\xee\x8c\xf7\xad1\x94\xa9\xca\x8d<D\x15\xb9\xae\x9a\xf4\xeamE\xb8\xb7M\xbb\xd8}\xb6\xa4\xc2X\xe7h\x04\xb0\xd9\xb7\xef\x13\xfb\xd0\xbf\xca\xea}\x89?\x81j\xcf\xd5t\xf6\xd2\xf5K\x8b6m\xc2\'\xf9[\xfb\xeayV\xfcA\x07\xf1\xa5|\x0b\xc7C\x80\xad\x19S\x93\xb7\xb7\x19\xfc@5w]o\xb4Y\xe8\xf7\x85p\xf2\xd9\x08\xdc\xff\x00x\xc6\xed\x18?\xf7\xca\xaf\xe5^c:Q\x8e\x1c\xa9\x18\xc7\x14\xf9\x14\xee\xdd\xc1\x1c\x13P\xd3\xd1\x88$v#\x14\x0cyu\'p8c\xf9S\xa1\x88\xdc2\xc6:\x8e\xa7\xd0TQ\xc6\xd28D\x19&\xad\xbd\xca\xdbB`\x83\x96?}\xfb\x93@\x1bZD\xb0Ecn\x14\x12#\xd6-\xd9\x9b\xdb\r\xfe\x06\xb1\xf5\x88\x9a\xdf]\xd4 b~K\x99\x14\x8f\xa3\x11S\xe9e\xa5\xd2uh\x14\x90\xe8\x91\xdd \xf5(\xd8?\x92\xc8\xc7\xf0\xab~)\x8f\x7f\x88f\xbf\x8d?w|\x89z\x98\xe9\xfb\xc0\x19\x87\xe0\xdb\x87\xe1@\x86\xf847\xfc%\xdaS\x01\xf7n\x15\xb2G@9\xaf`\xf8\xcf\x046Z\x95\x8e\xa1\x8c\x89bo\x9b\xdcW\x9b\xf825\x8b\xc5zU\xc9P\xd0\xb3\xf4\x03\xaeF\x08\xf65\xe8\xdf\x1e\x83I\xe1\xbd\x0e\xe9A\xd9\xbd\xa3\'\xae\x0e\x01\xfe\x86\xba\xe1uG\xef\xfd?\xc8\xe2\xa8\xd3\xc4G\xd0\xe1\xfe\x1c\xea\xa8\x9a\xfd\xe4\xb2\xaf.\xa0\x0ey\x03=\xab\x9e\xf1\\r\xff\x00n\xdd\xb4\xe0\xf9\x86BW\xfd\xd3\xd3\xf4\xac\x9d\'R\x97K\xd4\x12\xea>q\xc3)\xfe!\xdcW\xa8i\x9a\xa7\x84\xbcK\x02A\xaa\xf9I \x18F\x91\xf62\xfbdu\x15\xd3K\x92\xbe\x19SN\xd2O\xef\n\x97\xa3U\xd4\xb5\xd32~\x11[\xdeM\xf1\x06\xd6KM\xc1\x13&_M\x98\xe6\xba\xbf\x8f\xb3\x99/4\xd8Ur\xb1D\xe5\x89\xf58\xfe\x95\xdei\x13\xf87\xc0\xfe\x1fi\xedd\xb6\x8cl\xdc\xe6&\xdf#\xff\x00Z\xf3\xff\x00\x1aK\x17\x8c|?6\xb1opV%bT\xba\xf5\xc8?.;t\x1d}\xea)\xe1\xe5Q8Gu\xfef>\xda\xf5cQ\xab#\x82\xf8uo-\xd6\xaf2G\x8c\xe1X\xe7\xbe\x0eqU\xb5\x99DZ\xe5\xf4d6\xc5\x9d\xc3(9\xef\xd6\xbb\x1f\x05\xe9\xd6\x9e\x15\xd2o5\x9b\xb62\xcac\xf9\x15\x7f\x88\xf6\x03\xf1\xae\x12\xe2\xe9\xb5\x1dV\xee\xe9\xd5\x10\xc8\xe5\xce:\x0c\x9e\xd5\xa6)J\x9d\nt\'\xba\xbf\xe6oI\xf3\xd6\x9c\xd6\xc6K\xba=\xce\xf6\x1f\xbb$\x90\x07_l\xd6\x96\xa6\x08\xf0\xb6\x82X\x93\x93q\x8e:.\xf1\xfdsYj\nK#\x03\x90\x01\x19\xfa\xf1Z\x9a\xec\tgk\xa3\xda\x07fu\xb2Y\xa5\x04\xfd\xd6\x91\x8b\x80=>R\x87\xf1\xaf)\x9d\x86 \xf7\xe9N\xff\x00V\xd9\x18>\x86\x9b\x8c\xfd*M\xad\xb3\x9e\x84\xf0)\x0c\x93w\xd9\xd3bcy\xe5\x9b\xfaT\x1dNM)\\\xb6I\xc0<\x8ay\xe7h\xc0\x18\x19\xfa\xd3\x02\xfe\x89w\x1e\x99\xa9\xdb\xddN\x9b\xe0$\xa4\xc8:\xbcL6\xb8\xfa\xed\'\x15\xd2_\xd9\xbc\x1a=\xc6\x9f\xf2\xc9y\xa29x\xe4\x03"{9\x0e\xe0\xea;\x80X7\xd2S\xe9\\s\x15\xdf\xbdr\x14\x1a\xea\xb4MJ\xea\xfd-\x85\xb1_\xed\x9d1X[\x06]\xc2\xea\xdc\xe7t\x0c?\x88\x80[\x03\xba\x96^\xc2\x9a\x13*\xf8b\xe2g\xb9)\x13`\xc6\xdepo\xee\x9e\xf5\xe8^/\xf8\x83a\xaf\xdaX\xe8\xda\x8c>\\\x91\xfc\xf2\xbe2\x8cq\x81\xf4\xef\\\xb6\x85c\x08{\x9dV\xc1q\xa7\xc9\x84hI\xdc\xd6\xaeO\xdcoo\xee\xb7q\xee\rq\xfa\xe4\xff\x00i\xd6n\\t\xdd\xb4}\x07\x15\xd3F\xbb\xa2\xd4\xd2\xbf\xa9\x85J1\xa8\xf5:\x8b\xef\x04\xad\xc4\ru\xa6J\x06yX\x89\xc8#\xd8\xd70\x9a]\xd4:\x9a\xda\xdcB\xc9&\xeca\x85M\xa4x\x86\xfbIu\x11\xc8^\x1c\xe4\xc4\xe7\x8f\xc3\xd2\xbd\xcb\xe1\xed\xf7\x86u\xad6MCU\x16\xd1\xbc}#\xbb\x00m\xf7\x04\xf5\x15\xd5S\xea\xb5\xe3\xcf\x0fv]\xba|\xbf\xaf\x91\x8b\x9dj:K\xdeG\x9fj\x9au\xeb\xe9\x96\xfau\x84\x129\x90\xe1\xb6\x0e\xc3\xd4\xfdH\xae3PmCKyt\xe9\x1a\xe2\xdd\x1b\x06H\x8b\x10\x1b\xb8$t\xafv\xf8\x99\xe3=#E\xb1\xb5\x87LKy\xe5\xdaWd\x18\xdb\x1e@ \xe4w\xaf\x02\xd4u)\xf5\x9dH\xdd]c{\x906\xa0\xc0\x03\xd2\xb9\xea\xaaq\xa6\x9a\x93\xe6\xfd\r(\xceswq\xb4K\xb6S\xdc\r5\xe4y\xdc\xa6\xe1\x1a\x06bG\xa9\xaa\xd6l\xbet\xd9\xe8T\x9c\x03V\xa4\x0b\x14\x11\xd9I\xf2\x95\x05\xf6\xfa\x12;\xd3\xc6\x93\xfd\x9de\x1d\xcd\xda3\xdc\xdc\x8cZZ\x0c\xeel\xf4\x91\x80\xfe\x1f\xee\x8e\xac}\x87<\xed\xbd\xd9\xba*YX\xb6\xa1\xab\x08\x9c\xf9V\xe0\x19\xa7q\xc0H\xd4e\x9b\xf2\xce=I\x03\xbdA\xa9^\x7fh_\xcdu\xb4/\x98\xd9T\x1d\x11G\n\xbf\x80\x00~\x15{Sv\xb3\xb4{E?\xe9/\xb4^\x10~\xe9\x07"<\xf7\xc1\xe5\xbd\xc0\x1d\xab\x14\x12\x07\xb5f\xcaD\xa20[\x19\x07<\x0cv\xa7\x1d\xb9\x07\xa1\xfe\xe84\xebr6eT\x13\xceA\xa4\x08$\xce\xdc\x02:.i\x81_%\xa9\xfb\x9d\x0e\xd2x\xc7L\xd22l\x00\xf5\xc8\xcd4|\xe7\x93Hb\xb3\x17>\xc3\xf4\xabv\xb2\x1bgI\x94\xb8e!\x94\xa9\xc1\x0c:\x10{U`\x81\x98\x02v\xa9\xa7\x16?*\x8f\x94\x0e\xf4!\x1e\x83\xe1\x8d~;\xbdN\xea\xe23\x1d\xb6\xab,[e\x0f\x81\x05\xe8\xcf\xf1\x83\xc2\xb9\xef\x9e\x0f^\x0f^\x7fU\xd2,\xae\xaf\xe4\x8e\xd86\x95\xa8\x06\xfd\xe5\x85\xf3mL\xfa\xc7#v>\x8f\x8f\xf7\x8ddX\xb6\xc9\xdd\xb3\x80\xc8A\xc5=.\xee\xeem\x16\xd6i\x0c\xb6\xc8\xdf"\xc9\xc9O\xf7OP=\x87\x15OT\x02\x9d\x1a\xf2\xd6\xeda\xbd\xb5\x9a\xdc\x9er\xeb\x80G\xa8=\x08\xf7\x15\xd3\xdek\x16\x1a~\x9e\xb6\xd0)}\x8b\x8d\xa0\xe0\x1f\xa9\xac\xdd>\xfe\xf7K\x87e\x9d\xd4\xa9\x1a\xa39\x1b\xb2\x87\xdbi\xe3\xadgM\xad\xdcH\xe5\xa5\x8fO\x94\xb1\xc9f\xb2\x8c\x1f\xc4\x85\x14\xf9\xb9P\xadr\x9d\xfe\xa7q\xa8\xca^b1\xd9T`\n\xb9\xa2h\x9a\x85\xec\xd1\xdc\xc7h\xff\x00eG\x05\xae$\xc4q/\xd5\xdb\x0b\xfa\xd2\xa7\x88.\xe1\x94y"\xc6\xdf#;\xe0\xb2\x8fp\xfa\x12\xb9\xfdi\xf6\xf7\xd7\x1a\xa5\xe8mB\xe6\xe2\xed\xf1\xf24\xf2\x92\x14}9\xe3\xe9\x8a\x95\xab\x1fC^\xeaM2\xd3V\xb9\x92\xd1?\xb4\xefwd\xc9"\xff\x00\xa3[\xfb\xe0\xfd\xf3\xfe\xf6\x14z5e\xdc\xeb\x8d\x03\xbc\x90\xdc=\xc6\xa1&|\xdb\xc6<\xaez\x84\'\x9c\xf6\xdd\xc7\xa0\xf5\xaa\xf7\xb7,\x1a\xe62\xc5b,YbC\x85Rx\xce+\'\x19\xef\xf9\xd0\xd8$N\x8c\x82#\x90\xf8a\x82\x01\xe3>\xb5_?\x95H\xa7q\xd8\x0e3\xc6i\xb2*\xab\x90\xa4\x95\xed\x9aLa\xbbke\t\xc5J$S\x92\x00\xc8\x15^\x9c\xa7\x07$P\x04\xac\xa6M\xbcaI\xc0\x14>\xcd\xbbW#\x1f\xad<8\xfb6\x18\xe0\x97-\x91U\xcbd\xd0\x04\x91\x8d\xf2*g\x82y\xa1\x94\xedfc\x92y\x18\xa9-W\xf7\xae\xdd\x91\x19\xbfJc\x9c\xa0\x01}\xa8\x01\xd0\xb1w\xc6x\n\x7f\x95\\\x95~[h\x97\xe5\xdc\xa1\x98\x8f@*\xad\xaa\x0f=C\x1e\x08\xc1\xc5X\x8d\xc4\x97\n\xf2\x11\x81\xf2(\xf5\x02\x9a\x11$w;"\x96YyF]\x81\x7f\x1e\x95\x92NI54\x8cc2FI85\x05&\xc0S\xda\xb54\xd6\x0b&\xd6m\xa0)\xe4\xfd+1\x00,7\x1c\x0c\xf5\xad("\x02F\x19\xcf@)\xa0dZ\x9e\xc5\x95U3\x9c\x02j\x90ROJ\x9e\xe5\xbc\xc7.F;T\nH9\x1d\xa9=\xc6<#/\xde\x18\xe7\xbd\x05ZWm\xa3\xa9\xe0R\x16b\xd9\xe4\x9atJwu\xc0\xeb\x9a\x00\x89\x94\xa9\xc3\x0c\x11@\x1b\x8e;\x9a\x96\xe0\x0f7r\xe7i\xe8MJ\xb6\xd2C\x07\xda\x9dp\xbf\xc3\x9e\xe7\xfc\xf3E\x80\xff\xd9'

    
try:
    from base64 import b64encode, urlsafe_b64decode
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Cipher import AES
except:os.system('pip install pycryptodome')
class cryption:

    def __init__(self, auth:str):
        self.key = bytearray(self.secret(auth), 'UTF-8')
        self.iv = bytearray.fromhex('0' * 32)

    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        return b64encode(
            AES.new(self.key, AES.MODE_CBC, self.iv)
            .encrypt(pad(text.encode('UTF-8'),AES.block_size))
        ).decode('UTF-8')


    def decrypt(self, text):
        return unpad(
            AES.new(self.key, AES.MODE_CBC, self.iv)
            .decrypt(urlsafe_b64decode(text.encode('UTF-8')))
            ,AES.block_size
        ).decode('UTF-8')
    
    
    def changeAuthType(self, auth_enc):
        lowercase = 'abcdefghijklmnopqrstuvwxyz'
        uppercase = 'abcdefghijklmnopqrstuvwxyz'.upper()
        digits = '0123456789'
        n = ''
        for s in auth_enc:
            if s in lowercase:
                n += chr(((32 - (ord(s) - 97)) % 26) + 97)
            elif s in uppercase:
                n += chr(((29- (ord(s) - 65)) % 26) + 65)
            elif s in digits:
                n += chr(((13 - (ord(s)- 48)) % 10) + 48)
            else:
                n += s
        return n
    
from requests.exceptions import HTTPError , ReadTimeout , ConnectionError
from requests.sessions import Session ; Session = Session()
from json import dumps,loads
from requests.exceptions import HTTPError , ReadTimeout , ConnectionError
from requests.sessions import Session ; Session = Session()
from json import dumps,loads
import requests
from requests import get

import os
import re

import io
import urllib

def get_video_thumbnail_bytes(video_path):
    if os.path.exists(video_path):
        try:
            from moviepy.editor import VideoFileClip
            from PIL import Image
            video = VideoFileClip(video_path)
            frame = video.get_frame(0)
            image = Image.fromarray(frame)
            byte_arr = io.BytesIO()
            image.save(byte_arr, format='JPEG')
            byte_arr.seek(0)
            return byte_arr.getvalue()
        except:
            raise Exception("An error occurred while processing the video file.")
    elif re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', video_path):  # if it's a download link
        try:
            response = urllib.request.urlopen(video_path)
            video_bytes = response.read()
            video = VideoFileClip(io.BytesIO(video_bytes))
            frame = video.get_frame(0)
            image = Image.fromarray(frame)
            byte_arr = io.BytesIO()
            image.save(byte_arr, format='JPEG')
            byte_arr.seek(0)
            return byte_arr.getvalue()
        except:
            raise Exception("An error occurred while downloading and processing the video file.")
    else:
        raise ValueError("Invalid input. Please provide a valid local file path or a download link.")
    
from PIL import Image
import io

def image_to_bytes(image_path):
    with Image.open(image_path) as img:
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        byte_data = buffer.getvalue()
    return byte_data

class req:

    def __init__(self,auth:str):
        self.auth = auth
        self.enc = cryption(auth)

    def send_request(self,data:dict,method:str,type_method:str="rubino"):

        if type_method == "rubino":

            data_json = {
                "api_version": "0",
                "auth": self.auth,
                "client":confing.android,
                "data": data,
                "method": method
            }
            
        elif type_method == "messenger":

            data_json = {
                "api_version": "5",
                "auth": self.auth,
                "data_enc": self.enc.encrypt(
                    dumps({
                        "method": method,
                        "input": data,
                        "client": confing.android
                    })
                )
            }

        while True:
            try:
                response = Session.post(
                    url=confing.server[type_method],
                    headers=confing.headers,
                    json=data_json
                )
            except HTTPError as err:
                raise HTTPError(f"HTTP Error {err.args[0]}")
            except ReadTimeout:
                raise ReadTimeout('Time out')
            except ConnectionError:
                raise ConnectionError('Check your internet connection')
            except:
                continue
            else:
                if 'data_enc' in  response.json():
                    return loads(self.enc.decrypt(response.json()['data_enc']))
                return response.json()
        
    def requestUploadFile(self,file_name:str,size:str,file_type:str,profile_id:str=None):
        return self.send_request({
            "file_name": file_name,
            "file_size": str(size), 
            "file_type": file_type,
            "profile_id": profile_id
        },"requestUploadFile")

    def upload(self, post_file, post_type: str, profile_id: str = None):
        file_byte_code = post_file if isinstance(post_file, bytes) else open(post_file, "rb").read()
        upload_res = self.requestUploadFile("video.mp4" if post_type == "Video" else "picture.jpg", len(file_byte_code), post_type, profile_id)
        if upload_res is not None and upload_res["status"] == "OK":
            upload_res = upload_res["data"]
            total_part = len(file_byte_code) // 131072
            upload_data = 0
            for part in range(1, total_part + 2):
                byte_part = file_byte_code[131072 * (part - 1): 131072 * part]
                header = {
                    "part-number": str(part),
                    "total-part": str(total_part + 1),
                    "auth": self.auth,
                    "hash-file-request": upload_res["hash_file_request"],
                    "file-id": str(upload_res["file_id"]),
                    "content-type": "application/octet-stream",
                    "content-length": str(len(byte_part)),
                    "Host": upload_res["server_url"].replace("https://", "").replace("/UploadFile.ashx", ""),
                    "Connection": "Keep-Alive",
                    "accept-encoding": "gzip",
                    "user-agent": "okhttp/3.12.1",
                }
                while True:
                    try:
                        response = Session.post(data=byte_part, url=upload_res["server_url"], headers=header)
                        if response.status_code == 200:
                            upload_data += len(byte_part)
                            RED = "\033[31m"
                            GREEN = "\033[32m"
                            YELLOW = "\033[33m"
                            CYAN = "\033[36m"
                            BOLD = "\033[1m"
                            RESET = "\033[0m"
                            progress = upload_data / len(file_byte_code)
                            progress_bar_length = 100
                            filled_length = int(progress_bar_length * progress)
                            progress_bar = f"[{'=' * filled_length}{'.' * (progress_bar_length - filled_length)}]"
                            print(f"\r{RESET}{YELLOW}{BOLD}Post File --{CYAN}{BOLD}| Upload {RESET} {GREEN}{upload_data / (1024 * 1024):.2f} MB {CYAN}{BOLD} total {RESET} {progress_bar} {progress * 100:.2f}%{RESET} in {RESET} {YELLOW}{len(file_byte_code) / (1024 * 1024):.2f} MB {CYAN}{BOLD}", end="\r")
                            break
                    except ConnectionError:raise ConnectionError('Check your internet connection')
            print()
            return [upload_res, response.json()["data"]["hash_file_receive"]]
        return upload_res


class DateInfo:
    def __init__(self, data: Dict[str, Any]):
        self.jalali = data.get('jalali')
        self.miladi = data.get('miladi')
        self.ghamari = data.get('ghamari')
def getVideoData(bytes:bytes):
        try:
            from moviepy.editor import VideoFileClip
            with NamedTemporaryFile(delete=False, dir=".") as temp_video:
                temp_video.write(bytes)
                temp_path = temp_video.name
            chmod(temp_path, 0o777)
            try:
                from PIL import Image
            except ImportError:
                system("pip install pillow")
                from PIL import Image
            with VideoFileClip(temp_path) as clip:
                duration = clip.duration
                resolution = clip.size
                thumbnail = clip.get_frame(0)
                thumbnail_image = Image.fromarray(thumbnail)
                thumbnail_buffer = BytesIO()
                print(thumbnail_buffer)
                thumbnail_image.save(thumbnail_buffer, format="JPEG")
                thumbnail_b64 = thumbnail_buffer.getvalue()
                clip.close()
            remove(temp_path)
            return thumbnail_b64
        except ImportError:
            print("pip install moviepy")
            return confing.th
        except Exception as e:print(e)
class SeasonInfo:
    def __init__(self, data: Dict[str, Any]):
        self.number = data.get('number')
        self.name = data.get('name')

class TimeInfo:
    def __init__(self, data: Dict[str, Any]):
        self.hour = data.get('hour')
        self.minute = data.get('minute')
        self.second = data.get('second')

class DayInfo:
    def __init__(self, data: Dict[str, Any]):
        self.number = data.get('number')
        self.name_week = data.get('name_week')
        self.name_month = data.get('name_month')

class MonthInfo:
    def __init__(self, data: Dict[str, Any]):
        self.number = data.get('number')
        self.name_past = data.get('name_past')
        self.name = data.get('name')

class YearInfo:
    def __init__(self, data: Dict[str, Any]):
        self.number = data.get('number')
        self.name = data.get('name')
        self.name_past = data.get('name_past')
        self.remaining = data.get('remaining')
        self.leap = data.get('leap')

class OccasionInfo:
    def __init__(self, data: Dict[str, Any]):
        self.miladi = data.get('miladi')
        self.jalali = data.get('jalali')
        self.ghamari = data.get('ghamari')

class TimeData:
    def __init__(self, data: Dict[str, Any]):
        self.timestamp = data.get('timestamp')
        self.date = DateInfo(data.get('date', {}))
        self.season = SeasonInfo(data.get('season', {}))
        self.time = TimeInfo(data.get('time', {}))
        self.day = DayInfo(data.get('day', {}))
        self.month = MonthInfo(data.get('month', {}))
        self.year = YearInfo(data.get('year', {}))
        self.occasion = OccasionInfo(data.get('occasion', {}))

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4, default=lambda o: o.__dict__)

class IPInfo:
    def __init__(self, data: Dict[str, Any]):
        self.ip = data.get('IP')
        self.country = data.get('Country')
        self.city = data.get('City')
        self.isp = data.get('ISP')
        self.timezone = data.get('timzone')
        self.org = data.get('org')
        self.country_code = data.get('countryCode')

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4)

def __request_url():
    import random
    return f"https://rubino{random.randint(1,59)}.iranlms.ir/"
from typing import Union, Optional
from pathlib import Path

_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]
def get_useragent():
    import random
    return random.choice(_useragent_list)
class api:
    def download_post_rubika(
            share_url:str,
            #return_choice:None = False
    ):
        body = {'url': share_url}
        request = urllib3.PoolManager()
        response = request.request(
            'POST',
            'https://api-free.ir/api/rubino-dl.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
            
    def download_story_rubika(
            username:str
    ):
        body = {'id': username}
        request = urllib3.PoolManager()
        response = request.request(
            'POST',
            'https://api-free.ir/api2/story_rubino.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
    def search_page_rubino(
            text:str
    ):
        body = {'user': text}
        request = urllib3.PoolManager()
        response = request.request(
            'GET',
            'https://api-free.ir/api/rubino-search.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
def _req(term, results, lang, start, proxies, timeout):
    resp = get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": get_useragent()
        },
        params={
            "q": term,
            "num": results + 2,  # Prevents multiple requests
            "hl": lang,
            "start": start,
        },
        proxies=proxies,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp
import random

class Bot():
    """rubino class"""
    def __init__(self,auth,platform="m.rubika.ir",lang_code="fa") -> None:
        self.auth=auth
        self.platform=platform
        self.lang_code=lang_code
        #{"app_name": "Main","app_version": "3.0.2"dd,"lang_code": "fa","package": "app.rbmain.a","platform": "Android"}
    def _request_url(self):
        import random
        return f"https://rubino{random.randint(1,59)}.iranlms.ir/"
    def get_link(self):
        return self._request_url()
    def _reuests_post(self,methode:str,data:dict):
        request = urllib3.PoolManager()

        if self.platform == "m.rubika.ir" or self.platform == "web" or self.platform == "PWA":
            body = {
                "auth":self.auth,
                "api_version":"0",
                "client":{
                    "app_name":"Main",
                    "app_version":"2.2.4",
                    "package":"m.rubika.ir",
                    "platform":"PWA"
                },
                "data":data,
                "method":methode
            }
        elif self.platform == "android" or self.platform == "Android" or self.platform == "rubix":
            body = {
                "auth":self.auth,
                "api_version":"0",
                "client":{
                    "app_name": "Main",
                    "app_version": "3.0.2",
                    "lang_code": self.lang_code,
                    "package": "app.rbmain.a",
                    "platform": "Android"
                },
                "data":data,
                "method":methode
            }
        response = request.request(
            'POST',
            self.get_link(),json=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'data' in response_data:
                    return response_data['data']
            else:
                return response_data['status_det']
        else :
            raise Exception("Request Error Server")
    def edit_info_page(
        self,
        username_me:str,
        name=str,
        bio=None,
        phone=None,
        email=None,
        website=None
        ):
        """
        - username_me : در این مقدر باید آیدی پیجی که میخاین ادیت شه وارد کنید
        """
        profile_id=requests.post(f"https://api-free.ir/api/rubino-search.php?user={username_me}").json()['result']['data']['profiles'][0]['id']
        data = {
            "profile_id":profile_id,
            "username":username_me,
            "name":name,
            "bio":bio,
            "phone":phone,
            "email":email,
            "website":website
        }
        methode = "updateProfile"
        req_get = self._reuests_post(methode=methode,data=data)
        return req_get
    def create_page(
            self,
            username:str,
            name:str = "codern",
            bio:str = None,
            phone=None,
            email=None,
            website=None
            ):
        data = {
            "username":username,
            "name":name,
            "bio":bio,
            "phone":phone,
            "email":email,
            "website":website
        }
        methode = "createPage"

        request = self._reuests_post(methode=methode,data=data)
        return request
    def Download_story(self,username):
        return api.download_story_rubika(username)
    def get_comments(self,post_id,post_profile_id,profile_id=None):
        data = {
            "equal": False,
            "limit": 100,
            "sort": "FromMax",
            "post_id": post_id,
            "profile_id": profile_id,
            "post_profile_id": post_profile_id
        }
        methode = "getComments"
        request = self._reuests_post(methode=methode,data=data)
        return request
    def get_all_profile(self):
        data = {"equal":False,"limit":10,"sort":"FromMax"}
        methode = 'getProfileList'
        request = self._reuests_post(methode=methode,data=data)
        return request
    def get_me_info(self,profile_id):
        """- دریافت اطلاعات پیج"""
        data = {"profile_id":profile_id}
        methode = 'getMyProfileInfo'
        request = self._reuests_post(methode=methode,data=data)
        return request
    def Like(self,post_id,target_post_id):
        data ={"action_type":"Like","post_id":post_id,"post_profile_id":target_post_id,"profile_id":[]}
        methode = 'likePostAction'
        request = self._reuests_post(methode=methode,data=data)
        return request
    
    #--------------------------------------------

    def comment(self,text,post_id,post_target_id,profile_id=None):
        import random
        data = {
            "content": text,
            "post_id": post_id,
            "post_profile_id": post_target_id,
            "rnd":f"{random.randint(100000,999999999)}" ,
            "profile_id":profile_id
        }
        methode = 'addComment'
        while True:
            try:return self._reuests_post(methode=methode,data=data)
            except:return "error"
    
    def get_link_share(self,post_id,post_profile,prof=None):
        data = {
            "post_id":post_id,
            "post_profile_id":post_profile,
            "profile_id":prof
        }
        methode = 'getShareLink'
        return self._reuests_post(methode=methode,data=data)
    
    
    def is_Exist_Username(self,username):
        if username.startswith("@"):
            username = username.split("@")[1]
            data = {"username": username}
        else:data = {"username": username}
        methode = "isExistUsername"
        return self._reuests_post(methode=methode,data=data)
    
    def add_View_Story(self,target_story_id,ids:list,profile_id=None):
        data = {
            "profile_id":profile_id,
            "story_ids":ids,
            "story_profile_id":target_story_id
        }
        methode = 'addViewStory'
        return self._reuests_post(methode=methode,data=data)
               

    def save_post(self,post_id,post_profile_id,prof=None):
        data = {
            "action_type":"Bookmark",
            "post_id":post_id,
            "post_profile_id":post_profile_id,
            "profile_id":prof
        }
        methode ='postBookmarkAction'
        return self._reuests_post(methode=methode,data=data)
               

    def un_like(self,post_id,post_profile_id):
        data = {
            "action_type":"Unlike",
            "post_id":post_id,
            "post_profile_id":post_profile_id,
            "profile_id":[]
        }
        methode ='likePostAction'
        return self._reuests_post(methode=methode,data=data)
    def get_Suggested(self,profile_id=None):
        data = {
            "profile_id":profile_id,
            "limit": 20,
            "sort": "FromMax"
        }
        methode = 'getSuggested'
        return self._reuests_post(methode=methode,data=data)
    def image_to_bytes(self, image_path):
        with Image.open(image_path) as img:
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            byte_data = buffer.getvalue()
        return byte_data

    def check_url_content_type(self, url):
        response = requests.head(url)
        content_type = response.headers.get('Content-Type', '').lower()
        print(f"post type {content_type}")
        if 'image' in content_type:
            return 'image'
        elif 'video' in content_type:
            return 'video'
        return None

    def upload_file(self, file, file_type, profile_id):
        return req(self.auth).upload(file, file_type, profile_id)
        
    def get_video_resolution(self,download_link):
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(download_link)
            width = clip.w
            height = clip.h
            clip.close()
            return [width, height]
        except ModuleNotFoundError:
            print("pip install moviepy")
            return [668,789]
        except Exception as e:
            return [668,789]
    def add_Post(self,post_file: str, caption: str = None, time: int = 1, size: Any = [668, 798], thumbnail_file: str = None, profile_id: str = None):
        from concurrent.futures import ThreadPoolExecutor
        if size == "Auto" or size =="auto":
            try:
                size=self.get_video_resolution(post_file)
                print(size)
            except Exception as e:
                print(f"error data resolution  auto [668,789]")
        http = urllib3.PoolManager(num_pools=10, headers={'Connection': 'keep-alive'})
        def get_file_content(file):
            if file.startswith("https://"):
                content_type = self.check_url_content_type(file)
                if content_type not in ['image', 'video']:
                    return None, None
                response = http.request('GET', file)
                print("GET <<< Data byte.")
                return response.data, "Picture" if content_type == 'image' else "Video"
            else:
                post_extension = file.split(".")[-1].lower()
                if post_extension in ["mp4", "mov", "mkv"]:
                    return open(file, 'rb').read(), "Video"
                elif post_extension in ["jpg", "jpeg", "png"]:
                    return open(file, 'rb').read(), "Picture"
                else:
                    return None, None

        post_file_content, post_type = get_file_content(post_file)
        if post_file_content is None:
            return "Invalid file or URL"

        def get_thumbnail_content(thumbnail, post_file_content):
            if thumbnail and thumbnail.startswith("https://"):
                response = http.request('GET', thumbnail)
                content_type = response.headers.get('content-type', '').lower()
                if 'image' in content_type:
                    return response.data
                else:
                    return confing.th
            elif thumbnail:
                return image_to_bytes(thumbnail)
            else:
                try:
                    print("GET <<< thumbnail Byte.")
                    return getVideoData(post_file_content)
                except ModuleNotFoundError:
                    return confing.th
        thumbnail_content = get_thumbnail_content(thumbnail_file, post_file_content)
        def upload_file_concurrently(file_content, file_type, profile_id):
            return self.upload_file(file_content, file_type, profile_id)

        with ThreadPoolExecutor(max_workers=2) as executor:
            post_res = executor.submit(upload_file_concurrently, post_file_content, post_type, profile_id).result()
            tumb_res = executor.submit(upload_file_concurrently, thumbnail_content, "Picture", profile_id).result()

        data = {
            "caption": caption,
            "file_id": post_res[0]["file_id"],
            "hash_file_receive": post_res[1],
            "height": str(min(size[1], 862)),
            "width": str(min(size[0], 848)),
            "is_multi_file": False,
            "post_type": post_type,
            "rnd": random.randint(100000, 999999999),
            "tagged_profiles": [],
            "thumbnail_file_id": tumb_res[0]["file_id"],
            "thumbnail_hash_file_receive": tumb_res[1],
            "profile_id": profile_id
        }

        if post_type == "Video":
            data.update({
                "duration": str(time),
                "snapshot_file_id": tumb_res[0]["file_id"],
                "snapshot_hash_file_receive": tumb_res[1]
            })

        return req(self.auth).send_request(data, "addPost")

    def get_Post_Likes(self,post_profile_id:str,post_id:str,max_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        data = {
            "equal": equal,
            "limit": limit,
            "max_id": max_id,
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "sort": sort,
            "profile_id": profile_id
        }
        return self._reuests_post(methode='getPostLikes',data=data)
    
    def get_Story(self,story_profile_id:str,story_ids:list,profile_id:str=None):
        return self._reuests_post(data={
            "profile_id": profile_id,
            "story_ids": story_ids,
            "story_profile_id": story_profile_id
        },methode="getStory")
    
    def get_Story_Viewers(self,story_id:str,limit:int=50,profile_id:str=None):
        return self._reuests_post(data={
            "limit": limit,
            "profile_id": profile_id,
            "story_id": story_id
        },methode="getStoryViewers")
    
    def get_My_Archive_Stories(self,sort:str="FromMax",limit:int=10,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "profile_id": profile_id
        },methode="getMyArchiveStories")
    
    def get_Page_Highlights(self,target_profile_id:str,sort:str="FromMax",limit:int=10,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },methode="getProfileHighlights")
    
    def create_Highlight(self,highlight_name:str,story_ids:list,highlight_cover_picture:str,profile_id:str=None):
        highlight_cover_res = self.req.upload(highlight_cover_picture,"Picture",profile_id)
        return self._reuests_post(data={
            "highlight_cover": {
                "highlight_file_id": highlight_cover_res[0]["file_id"],
                "highlight_hash_file_receive": highlight_cover_res[1],
                "type": "File"
            },
            "highlight_name": highlight_name,
            "story_ids": story_ids,
            "profile_id": profile_id
        },methode="addHighlight")
    
    def highlight_Story(self,highlight_id:str,story_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "highlight_id": highlight_id,
            "story_id": story_id,
            "profile_id": profile_id
        },methode="highlightStory")
    
    def remove_Story_From_Highlight(self,highlight_id:str,remove_story_ids:list,profile_id:str=None):
        return self._reuests_post(data={
            "highlight_id": highlight_id,
            "remove_story_ids": remove_story_ids,
            "updated_parameters":["remove_story_ids"],
            "profile_id": profile_id
        },methode="editHighlight")
    
    def get_Hash_Tag_Trend(self,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "profile_id": profile_id
        },methode="getHashTagTrend")
    
    def get_Explore_Posts(self,sort:str="FromMax",limit:int=51,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "profile_id": profile_id
        },methode="getExplorePosts")
    
    def get_Tagged_Posts(self,target_profile_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },methode="getTaggedPosts")
    
    def delete_Comment(self,post_id:str,comment_id:str,text:str,profile_id:str=None):
        return self._reuests_post(data={
            "model": "Comment",
            "post_id": post_id,
            "record_id": comment_id,
            "profile_id": profile_id
        },methode="removeRecord")
    
    def like_Comment(self,comment_id:str,post_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action_type": "Like",
            "comment_id": comment_id,
            "post_id": post_id,
            "profile_id": profile_id
        },methode="likeCommentAction")
    
    def un_like_Comment(self,comment_id:str,post_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action_type": "Unlike",
            "comment_id": comment_id,
            "post_id": post_id,
            "profile_id": profile_id
        },methode="likeCommentAction")
    
    def get_Comments(self,post_profile_id:str,post_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "sort": sort,
            "profile_id": profile_id
        },methode="getComments")
    
    def request_Follow(self,followee_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "f_type": "Follow",
            "followee_id": followee_id,
            "profile_id": profile_id
        },methode="requestFollow")
    
    def un_Follow(self,followee_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "f_type": "Unfollow",
            "followee_id": followee_id,
            "profile_id": profile_id
        },methode="requestFollow")
    
    def get_Page_Follower(self,target_profile_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "f_type": "Follower",
            "limit": limit,
            "sort": sort,
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },methode="getProfileFollowers")
    
    def get_Page_Following(self,target_profile_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "f_type": "Following",
            "limit": limit,
            "sort": sort,
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },methode="getProfileFollowers")
    
    def search_Follower(self,target_profile_id:str,username:str,max_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "max_id": max_id,
            "search_type": "Follower",
            "sort": sort,
            "target_profile_id": target_profile_id,
            "username": username,
            "profile_id": profile_id
        },methode="getProfileFollowers")
    
    def search_Following(self,target_profile_id:str,username:str,max_id:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "max_id": max_id,
            "search_type": "Following",
            "sort": sort,
            "target_profile_id": target_profile_id,
            "username": username,
            "profile_id": profile_id
        },methode="getProfileFollowers")
    
    def get_NewFollow_Requests(self,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "profile_id": profile_id
        },methode="getNewFollowRequests")
    
    def accept_Request_Follow(self,request_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action": "Accept",
            "request_id": request_id,
            "profile_id": profile_id
        },methode="actionOnRequest")
    
    def decline_Request_Follow(self,request_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action": "Decline",
            "request_id": request_id,
            "profile_id": profile_id
        },methode="actionOnRequest")
    def un_save_Post(self,post_profile_id:str,post_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action_type": "Unbookmark",
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "track_id": "Related",
            "profile_id": profile_id
        },methode="postBookmarkAction")
    
    def get_Saved_Posts(self,sort:str="FromMax",limit:int=51,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "profile_id": profile_id
        },methode="getBookmarkedPosts")
    
    def search_Page(self,username:str,sort:str="FromMax",limit:int=50,equal:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "equal": equal,
            "limit": limit,
            "sort": sort,
            "username": username,
            "profile_id": profile_id
        },methode="searchProfile")
    
    def block_Page(self,target_profile_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action": "Block",
            "blocked_id": target_profile_id,
            "profile_id": profile_id
        },methode="setBlockProfile")
    
    def un_block_Page(self,target_profile_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "action": "Unblock",
            "blocked_id": target_profile_id,
            "profile_id": profile_id
        },methode="setBlockProfile")
    
    def report_Page(self,post_id:str,reason:int=2,profile_id:str=None):
        return self._reuests_post(data={
            "model": "Profile",
            "reason": reason,
            "record_id": post_id,
            "profile_id": profile_id
        },methode="setReportRecord")

    def delete_Post(self,post_id:str,profile_id:str=None):
        return self._reuests_post(data={
            "model": "Post",
            "record_id": post_id,
            "profile_id": profile_id
        },methode="removeRecord")
    
    def delete_Story(self,story_id:list,profile_id:str=None):
        return self._reuests_post(data={
            "profile_id": profile_id,
            "story_id": story_id,
        },methode="deleteStory")
    
    def set_Page_Status(self,profile_status:str="Private",profile_id:str=None):
        return self._reuests_post(data={
            "profile_status": profile_status,
            "profile_id": profile_id
        },methode="updateProfile")

    def allow_Send_MessagePv(self,is_message_allowed:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "is_message_allowed": is_message_allowed,
            "profile_id": profile_id
        },methode="updateProfile")
    
    def edit_Notification(self,is_mute:bool=False,profile_id:str=None):
        return self._reuests_post(data={
            "is_mute": is_mute,
            "profile_id": profile_id
        },methode="updateProfile")
    
    def upload_avatar(self,prof_file:str,profile_id:str=None):
        prof_res = req(self.auth).upload(prof_file,"Picture",profile_id)
        return self._reuests_post(data={
            "file_id": prof_res[0]["file_id"],
            "hash_file_receive": prof_res[1],
            "thumbnail_file_id": prof_res[0]["file_id"],
            "thumbnail_hash_file_receive": prof_res[1],
            "profile_id": profile_id
        },methode="updateProfilePhoto")
    def add_Story(self,post_file:str,duration:int=27,size:list=[668,798],thumbnail_file:str=None,profile_id:str=None):
        
        if post_file.split(".")[-1] == "mp4" or post_file.split(".")[-1] == "mov" or post_file.split(".")[-1] == "mkv" or "https://":
            try:
                if "https://" in post_file:
                    tumb_res , post_res = req(self.auth).upload(image_to_bytes(thumbnail_file) if type(thumbnail_file) is str else confing.th,"Picture",profile_id) , req(self.auth).upload(requests.get(post_file).content,"Video",profile_id)
                else :
                    tumb_res , post_res = req(self.auth).upload(image_to_bytes(thumbnail_file) if type(thumbnail_file) is str else confing.th,"Picture",profile_id) , req(self.auth).upload(post_file,"Video",profile_id)
            except ModuleNotFoundError:
                print("pip install moviepy")
                tumb_res , post_res = req(self.auth).upload(confing.th,"Picture",profile_id) , req(self.auth).upload(post_file,"Video",profile_id)
            data = {
                "duration": str(duration),
                "file_id": post_res[0]["file_id"],
                "hash_file_receive": post_res[1],
                "height": 1280 if size[1] > 1280 else size[1],
                "story_type": "Video",
                "rnd": random.randint(100000, 999999999),
                "snapshot_file_id": tumb_res[0]["file_id"],
                "snapshot_hash_file_receive": tumb_res[1],
                "thumbnail_file_id": tumb_res[0]["file_id"],
                "thumbnail_hash_file_receive": tumb_res[1],
                "width": 720 if size[0] > 720 else size[0],
                "profile_id": profile_id
            }
                
        elif post_file.split(".")[-1] == "jpg" or post_file.split(".")[-1] == "png":
            post_res = req(self.auth).upload(post_file,"Picture",profile_id)

            data = {
                "file_id": post_res[0]["file_id"],
                "hash_file_receive": post_res[1],
                "height": 1280 if size[1] > 1280 else size[1],
                "story_type": "Picture",
                "rnd": random.randint(100000, 999999999),
                "thumbnail_file_id": post_res[0]["file_id"],
                "thumbnail_hash_file_receive": post_res[1],
                "width": 720 if size[0] > 720 else size[0],
                "profile_id": profile_id
            }
        else:
            return "file address eror"
        return req(self.auth).send_request(data,"addStory")['data']
    def delete_Page(self,page_profile_id:str):
        return self._reuests_post(data={
            "model": "Profile",
            "record_id": page_profile_id,
            "profile_id": None
        },methode="removeRecord")
    
    def add_Post_View_Count(self,post_profile_id:str,post_id:str):
        return self._reuests_post(data={
            "post_id": post_id,
            "post_profile_id": post_profile_id
        },methode="addPostViewCount")

    def add_Post_View_Time(self,post_profile_id:str,post_id:str,duration:int,profile_id:str=None):
        return self._reuests_post(data={
            "duration": duration,
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "profile_id": profile_id
        },methode="addPostViewTime")['data']