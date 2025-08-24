import asyncio
import aiohttp
from rubka.asynco import Robot
from rubka.context import Message
from rubka.button import InlineBuilder

bot = Robot(
    token="token",
    show_progress=True,
    timeout=900
)


user_modes = {}

COMPREHENSIVE_CRYPTO_LIST = [
    
    {'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'btc', 'aliases': ['btc', 'bitcoin', 'xbt']},
    {'id': 'ethereum', 'name': 'Ethereum', 'symbol': 'eth', 'aliases': ['eth', 'ethereum']},
    {'id': 'tether', 'name': 'Tether', 'symbol': 'usdt', 'aliases': ['usdt', 'tether']},
    {'id': 'usd-coin', 'name': 'USD Coin', 'symbol': 'usdc', 'aliases': ['usdc', 'usd coin']},
    {'id': 'binancecoin', 'name': 'BNB', 'symbol': 'bnb', 'aliases': ['bnb', 'binancecoin', 'binance coin']},
    {'id': 'ripple', 'name': 'XRP', 'symbol': 'xrp', 'aliases': ['xrp', 'ripple']},
    {'id': 'solana', 'name': 'Solana', 'symbol': 'sol', 'aliases': ['sol', 'solana']},
    {'id': 'cardano', 'name': 'Cardano', 'symbol': 'ada', 'aliases': ['ada', 'cardano']},
    {'id': 'dogecoin', 'name': 'Dogecoin', 'symbol': 'doge', 'aliases': ['doge', 'dogecoin']},
    {'id': 'dai', 'name': 'Dai', 'symbol': 'dai', 'aliases': ['dai']},
    
    
    {'id': 'shiba-inu', 'name': 'Shiba Inu', 'symbol': 'shib', 'aliases': ['shib', 'shiba inu', 'shiba']},
    {'id': 'pepe', 'name': 'Pepe', 'symbol': 'pepe', 'aliases': ['pepe']},
    {'id': 'bonk', 'name': 'Bonk', 'symbol': 'bonk', 'aliases': ['bonk']},
    {'id': 'floki', 'name': 'FLOKI', 'symbol': 'floki', 'aliases': ['floki']},
    {'id': 'safemoon-2', 'name': 'SafeMoon', 'symbol': 'sfm', 'aliases': ['sfm', 'safemoon', 'safemoon-2']},

    
    {'id': 'avalanche-2', 'name': 'Avalanche', 'symbol': 'avax', 'aliases': ['avax', 'avalanche', 'avalanche-2']},
    {'id': 'tron', 'name': 'TRON', 'symbol': 'trx', 'aliases': ['trx', 'tron']},
    {'id': 'polkadot', 'name': 'Polkadot', 'symbol': 'dot', 'aliases': ['dot', 'polkadot']},
    {'id': 'chainlink', 'name': 'Chainlink', 'symbol': 'link', 'aliases': ['link', 'chainlink']},
    {'id': 'matic-network', 'name': 'Polygon', 'symbol': 'matic', 'aliases': ['matic', 'polygon', 'matic-network']},
    {'id': 'litecoin', 'name': 'Litecoin', 'symbol': 'ltc', 'aliases': ['ltc', 'litecoin']},
    {'id': 'bitcoin-cash', 'name': 'Bitcoin Cash', 'symbol': 'bch', 'aliases': ['bch', 'bitcoin cash', 'bitcoin-cash']},
    {'id': 'internet-computer', 'name': 'Internet Computer', 'symbol': 'icp', 'aliases': ['icp', 'internet computer', 'internet-computer']},
    {'id': 'ethereum-classic', 'name': 'Ethereum Classic', 'symbol': 'etc', 'aliases': ['etc', 'ethereum classic', 'ethereum-classic']},
    {'id': 'cosmos', 'name': 'Cosmos', 'symbol': 'atom', 'aliases': ['atom', 'cosmos', 'cosmos hub']},
    {'id': 'stellar', 'name': 'Stellar', 'symbol': 'xlm', 'aliases': ['xlm', 'stellar', 'lumens']},
    {'id': 'near', 'name': 'NEAR Protocol', 'symbol': 'near', 'aliases': ['near', 'near protocol']},
    {'id': 'algorand', 'name': 'Algorand', 'symbol': 'algo', 'aliases': ['algo', 'algorand']},
    {'id': 'hedera-hashgraph', 'name': 'Hedera', 'symbol': 'hbar', 'aliases': ['hbar', 'hedera', 'hedera-hashgraph']},
    {'id': 'filecoin', 'name': 'Filecoin', 'symbol': 'fil', 'aliases': ['fil', 'filecoin']},
    {'id': 'aptos', 'name': 'Aptos', 'symbol': 'apt', 'aliases': ['apt', 'aptos']},
    {'id': 'fantom', 'name': 'Fantom', 'symbol': 'ftm', 'aliases': ['ftm', 'fantom']},
    {'id': 'tezos', 'name': 'Tezos', 'symbol': 'xtz', 'aliases': ['xtz', 'tezos']},
    {'id': 'neo', 'name': 'NEO', 'symbol': 'neo', 'aliases': ['neo']},
    {'id': 'eos', 'name': 'EOS', 'symbol': 'eos', 'aliases': ['eos']},
    {'id': 'monero', 'name': 'Monero', 'symbol': 'xmr', 'aliases': ['xmr', 'monero']},
    {'id': 'zcash', 'name': 'Zcash', 'symbol': 'zec', 'aliases': ['zec', 'zcash']},
    {'id': 'dash', 'name': 'Dash', 'symbol': 'dash', 'aliases': ['dash']},
    {'id': 'elrond-erd-2', 'name': 'MultiversX', 'symbol': 'egld', 'aliases': ['egld', 'elrond', 'multiversx']},
    {'id': 'sui', 'name': 'Sui', 'symbol': 'sui', 'aliases': ['sui']},
    {'id': 'kaspa', 'name': 'Kaspa', 'symbol': 'kas', 'aliases': ['kas', 'kaspa']},
    {'id': 'vechain', 'name': 'VeChain', 'symbol': 'vet', 'aliases': ['vet', 'vechain']},
    {'id': 'iota', 'name': 'IOTA', 'symbol': 'miota', 'aliases': ['iota', 'miota']},
    {'id': 'mina-protocol', 'name': 'Mina', 'symbol': 'mina', 'aliases': ['mina', 'mina protocol', 'mina-protocol']},
    {'id': 'kava', 'name': 'Kava', 'symbol': 'kava', 'aliases': ['kava']},
    {'id': 'icon', 'name': 'ICON', 'symbol': 'icx', 'aliases': ['icx', 'icon']},
    {'id': 'celo', 'name': 'Celo', 'symbol': 'celo', 'aliases': ['celo']},
    {'id': 'zilliqa', 'name': 'Zilliqa', 'symbol': 'zil', 'aliases': ['zil', 'zilliqa']},
    {'id': 'waves', 'name': 'Waves', 'symbol': 'waves', 'aliases': ['waves']},
    {'id': 'kusama', 'name': 'Kusama', 'symbol': 'ksm', 'aliases': ['ksm', 'kusama']},
    {'id': 'conflux-token', 'name': 'Conflux', 'symbol': 'cfx', 'aliases': ['cfx', 'conflux', 'conflux-token']},
    {'id': 'thorchain', 'name': 'THORChain', 'symbol': 'rune', 'aliases': ['rune', 'thorchain']},
    
    
    {'id': 'optimism', 'name': 'Optimism', 'symbol': 'op', 'aliases': ['op', 'optimism']},
    {'id': 'arbitrum', 'name': 'Arbitrum', 'symbol': 'arb', 'aliases': ['arb', 'arbitrum']},
    {'id': 'immutable-x', 'name': 'Immutable X', 'symbol': 'imx', 'aliases': ['imx', 'immutable x', 'immutable-x']},
    {'id': 'stacks', 'name': 'Stacks', 'symbol': 'stx', 'aliases': ['stx', 'stacks']},
    {'id': 'metis-token', 'name': 'Metis', 'symbol': 'metis', 'aliases': ['metis', 'metis-token']},
    {'id': 'loopring', 'name': 'Loopring', 'symbol': 'lrc', 'aliases': ['lrc', 'loopring']},
    {'id': 'celer-network', 'name': 'Celer Network', 'symbol': 'celr', 'aliases': ['celr', 'celer', 'celer-network']},
    
    
    {'id': 'uniswap', 'name': 'Uniswap', 'symbol': 'uni', 'aliases': ['uni', 'uniswap']},
    {'id': 'lido-dao', 'name': 'Lido DAO', 'symbol': 'ldo', 'aliases': ['ldo', 'lido', 'lido dao']},
    {'id': 'aave', 'name': 'Aave', 'symbol': 'aave', 'aliases': ['aave']},
    {'id': 'the-graph', 'name': 'The Graph', 'symbol': 'grt', 'aliases': ['grt', 'the graph', 'graph']},
    {'id': 'maker', 'name': 'Maker', 'symbol': 'mkr', 'aliases': ['mkr', 'maker']},
    {'id': 'synthetix-network-token', 'name': 'Synthetix', 'symbol': 'snx', 'aliases': ['snx', 'synthetix', 'synthetix-network-token']},
    {'id': 'curve-dao-token', 'name': 'Curve DAO Token', 'symbol': 'crv', 'aliases': ['crv', 'curve', 'curve dao']},
    {'id': 'pancakeswap-token', 'name': 'PancakeSwap', 'symbol': 'cake', 'aliases': ['cake', 'pancakeswap', 'pancakeswap-token']},
    {'id': '1inch', 'name': '1inch', 'symbol': '1inch', 'aliases': ['1inch']},
    {'id': 'compound-governance-token', 'name': 'Compound', 'symbol': 'comp', 'aliases': ['comp', 'compound', 'compound-governance-token']},
    {'id': 'sushi', 'name': 'SushiSwap', 'symbol': 'sushi', 'aliases': ['sushi', 'sushiswap']},
    {'id': 'dydx', 'name': 'dYdX', 'symbol': 'dydx', 'aliases': ['dydx']},
    {'id': 'gmx', 'name': 'GMX', 'symbol': 'gmx', 'aliases': ['gmx']},
    {'id': 'injective-protocol', 'name': 'Injective', 'symbol': 'inj', 'aliases': ['inj', 'injective', 'injective-protocol']},
    {'id': 'quant-network', 'name': 'Quant', 'symbol': 'qnt', 'aliases': ['qnt', 'quant', 'quant-network']},
    {'id': 'balancer', 'name': 'Balancer', 'symbol': 'bal', 'aliases': ['bal', 'balancer']},
    {'id': 'rocket-pool', 'name': 'Rocket Pool', 'symbol': 'rpl', 'aliases': ['rpl', 'rocket pool']},
    {'id': 'frax-share', 'name': 'Frax Share', 'symbol': 'fxs', 'aliases': ['fxs', 'frax share']},
    {'id': 'yearn-finance', 'name': 'yearn.finance', 'symbol': 'yfi', 'aliases': ['yfi', 'yearn', 'yearn-finance']},

    
    {'id': 'the-sandbox', 'name': 'The Sandbox', 'symbol': 'sand', 'aliases': ['sand', 'the sandbox', 'sandbox']},
    {'id': 'decentraland', 'name': 'Decentraland', 'symbol': 'mana', 'aliases': ['mana', 'decentraland']},
    {'id': 'axie-infinity', 'name': 'Axie Infinity', 'symbol': 'axs', 'aliases': ['axs', 'axie infinity', 'axie']},
    {'id': 'apecoin', 'name': 'ApeCoin', 'symbol': 'ape', 'aliases': ['ape', 'apecoin']},
    {'id': 'gala', 'name': 'Gala', 'symbol': 'gala', 'aliases': ['gala']},
    {'id': 'enjincoin', 'name': 'Enjin Coin', 'symbol': 'enj', 'aliases': ['enj', 'enjin', 'enjincoin']},
    {'id': 'illuvium', 'name': 'Illuvium', 'symbol': 'ilv', 'aliases': ['ilv', 'illuvium']},
    {'id': 'stepn', 'name': 'STEPN', 'symbol': 'gmt', 'aliases': ['gmt', 'stepn']},
    {'id': 'vulcan-forged', 'name': 'Vulcan Forged', 'symbol': 'pyr', 'aliases': ['pyr', 'vulcan forged', 'vulcan-forged']},
    {'id': 'magic', 'name': 'Magic', 'symbol': 'magic', 'aliases': ['magic']},
    {'id': 'wax', 'name': 'WAX', 'symbol': 'waxp', 'aliases': ['waxp', 'wax']},
    
    
    {'id': 'render-token', 'name': 'Render Token', 'symbol': 'rndr', 'aliases': ['rndr', 'render', 'render token']},
    {'id': 'bittorrent', 'name': 'BitTorrent', 'symbol': 'btt', 'aliases': ['btt', 'bittorrent']},
    {'id': 'chiliz', 'name': 'Chiliz', 'symbol': 'chz', 'aliases': ['chz', 'chiliz']},
    {'id': 'fetch-ai', 'name': 'Fetch.ai', 'symbol': 'fet', 'aliases': ['fet', 'fetch.ai', 'fetch ai']},
    {'id': 'livepeer', 'name': 'Livepeer', 'symbol': 'lpt', 'aliases': ['lpt', 'livepeer']},
    {'id': 'ocean-protocol', 'name': 'Ocean Protocol', 'symbol': 'ocean', 'aliases': ['ocean', 'ocean-protocol']},
    {'id': 'ankr', 'name': 'Ankr', 'symbol': 'ankr', 'aliases': ['ankr']},
    {'id': 'basic-attention-token', 'name': 'Basic Attention Token', 'symbol': 'bat', 'aliases': ['bat', 'basic attention token']},
    {'id': 'siacoin', 'name': 'Siacoin', 'symbol': 'sc', 'aliases': ['sc', 'siacoin']},
    {'id': 'storj', 'name': 'Storj', 'symbol': 'storj', 'aliases': ['storj']},
    {'id': 'holotoken', 'name': 'Holo', 'symbol': 'hot', 'aliases': ['hot', 'holo', 'holotoken']},
    {'id': 'trust-wallet-token', 'name': 'Trust Wallet Token', 'symbol': 'twt', 'aliases': ['twt', 'trust wallet token']},
    {'id': 'ethereum-name-service', 'name': 'Ethereum Name Service', 'symbol': 'ens', 'aliases': ['ens', 'ethereum name service']},
    {'id': 'api3', 'name': 'API3', 'symbol': 'api3', 'aliases': ['api3']},
    {'id': 'mask-network', 'name': 'Mask Network', 'symbol': 'mask', 'aliases': ['mask', 'mask-network']},
    {'id': 'helium', 'name': 'Helium', 'symbol': 'hnt', 'aliases': ['hnt', 'helium']},
    {'id': '0x', 'name': '0x', 'symbol': 'zrx', 'aliases': ['zrx', '0x']},
    {'id': 'oasis-network', 'name': 'Oasis Network', 'symbol': 'rose', 'aliases': ['rose', 'oasis-network']},
    {'id': 'nexo', 'name': 'Nexo', 'symbol': 'nexo', 'aliases': ['nexo']},
    {'id': 'celsius-degree-token', 'name': 'Celsius', 'symbol': 'cel', 'aliases': ['cel', 'celsius']},
    {'id': 'theta-token', 'name': 'Theta Network', 'symbol': 'theta', 'aliases': ['theta', 'theta-token']},
    
]


async def fetch_and_reply(message: Message, mode: str, delete: bool = False):
    base_url = {
        "iron": "https://v3.api-free.ir/codern-gpt/",
        "gpt": "https://v3.api-free.ir/openai/"
    }

    url = (
        f"{base_url[mode]}?text={message.text}"
        f"&token=d619ccac72b765923508c79da83951cf"
        f"&chat_id={message.sender_id}"
    )

    if delete:
        url += "&delete=true"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    if mode == "iron":
                        data = await resp.json()
                        result = data.get("result", "وب‌سرویس پاسخی برنگرداند!")
                    else:  
                        result = await resp.text()
                    await message.reply(result.strip())
                else:
                    await message.reply(f"خطا در دریافت پاسخ: {resp.status}")
    except Exception as e:
        await message.reply(f"خطا در ارتباط با وب‌سرویس: {e}")


@bot.on_message(commands=['start', 'help'])
async def handle_start(bot: Robot, message: Message):
    await message.reply_image(
    path="https://m.media-amazon.com/images/I/61aVMQqtjPL.jpg",
    text=(
        "🤖✨ به ربات هوش مصنوعی خوش آمدید!\n\n"
        "🔹 لطفاً یکی از حالت‌های زیر را انتخاب کنید:\n"
        "   🟢 /iron → Codern GPT\n"
        "   🔵 /gpt → OpenAI GPT-4\n\n"
        "📌 دستورات کاربردی:\n"
        "   ✨ /zekr → دریافت یک ذکر تصادفی\n"
        "   📈 /chart btc → مشاهده قیمت لحظه‌ای ارزهای دیجیتال (btc, eth, ...)\n"
        "   🗑️ /delete → پاک کردن حافظه گفتگو\n\n"
        "⚡ از تجربه‌ی هوش مصنوعی لذت ببرید! ⚡"
    )
)



@bot.on_message(commands=['iron'])
async def handle_iron(bot: Robot, message: Message):
    user_modes[message.sender_id] = "iron"
    await message.reply("✅ حالت روی Codern GPT تنظیم شد.")

@bot.on_message(commands=['gpt'])
async def handle_gpt(bot: Robot, message: Message):
    user_modes[message.sender_id] = "gpt"
    await message.reply("✅ حالت روی OpenAI GPT-4 تنظیم شد.")


@bot.on_message(commands=['delete'])
async def handle_delete(bot: Robot, message: Message):
    mode = user_modes.get(message.sender_id, "iron")
    await fetch_and_reply(message, mode, delete=True)
    await message.reply("🗑️ حافظه چت شما پاک شد.")


@bot.on_message(commands=['rubino'])
async def handle_rubino(bot: Robot, message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            return await message.reply("❗ لطفا لینک پست روبینو را وارد کنید\nمثال: /rubino https://rubika.ir/post/XXXX")

        post_url = parts[1]
        api_url = f"https://api-free.ir/api/rubino-dl.php?url={post_url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("ok"):
                        result = data.get("result", {})

                        caption = result.get("caption", "بدون کپشن")
                        video_url = result.get("url")
                        page_username = result.get("page_username", "نامشخص")
                        like_count = result.get("like", 0)
                        comment_count = result.get("comment", 0)
                        view_count = result.get("view", 0)
                        follower_page = result.get("follower_page", 0)

                        text = (
                            f"🎬 ویدیو دانلود شد!\n\n"
                            f"📝 کپشن:\n{caption}\n\n"
                            f"👤 پیج: @{page_username}\n"
                            f"👥 فالوور: {follower_page}\n\n"
                            f"👍 لایک‌ها: {like_count}\n"
                            f"💬 کامنت‌ها: {comment_count}\n"
                            f"👁️ بازدید: {view_count}"
                        )

                        await bot.send_video(message.chat_id, video_url, text=text, reply_to_message_id=message.message_id)
                    else:
                        await message.reply("❌ خطا در دریافت اطلاعات از روبینو!")
                else:
                    await message.reply(f"❌ خطا در اتصال ({resp.status})")
    except Exception as e:
        await message.reply(f"❌ خطا: {e}")


@bot.on_message(commands=['zekr'])
async def handle_zekr(bot: Robot, message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://v3.api-free.ir/zekr/") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await message.reply(f"📿 ذکر امروز:\n\n{data.get('zekr')}")
                else:
                    await message.reply("خطا در دریافت ذکر!")
    except Exception as e:
        await message.reply(f"❌ خطا: {e}")

def find_crypto(query: str):
    if not query or not isinstance(query, str):
        return None
        
    clean_query = query.lower().strip()

    for crypto in COMPREHENSIVE_CRYPTO_LIST:
        if clean_query in crypto['aliases']:
            return crypto
    
    return None
@bot.on_message(commands=['chart'])
async def handle_chart(bot: Robot, message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            return await message.reply("❗ لطفا نماد یا نام ارز را وارد کنید.\nمثال: /chart shiba")

        
        user_query = parts[1]
        
        
        
        crypto_info = find_crypto(user_query)

        
        if not crypto_info:
            return await message.reply(f"❌ ارز «{user_query}» پشتیبانی نمی‌شود یا نامعتبر است.")

        
        crypto_id_for_api = crypto_info['id']
        
        await message.reply(f"✅ {crypto_info['name']} ({crypto_info['symbol'].upper()}) یافت شد. در حال دریافت اطلاعات...")

        api_url = f"http://v3.api-free.ir/arz2/?crypto={crypto_id_for_api}"
        print(api_url)
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("ok"):
                        result = data.get("result", {})


                        name = result.get("name", "نامشخص")
                        symbol = result.get("symbol", "---")
                        logo = result.get("logo", None)

                        
                        rank = result.get("rank", "نامشخص")
                        description = result.get("description", "ندارد")
                        categories = result.get("categories", [])
                        price_usd = result.get("current_price_usd", 0)
                        market_cap = result.get("market_cap_usd", 0)
                        market_cap_change_24h = result.get("market_cap_change_24h", 0)
                        high_24h = result.get("24h_high", 0)
                        low_24h = result.get("24h_low", 0)
                        change_24h = result.get("price_change_percentage_24h", 0)
                        change_7d = result.get("7d_change_percentage", 0)
                        change_30d = result.get("30d_change_percentage", 0)
                        ath = result.get("ath", 0)
                        ath_date = result.get("ath_date", "نامشخص")
                        ath_change = result.get("ath_change_percentage", 0)
                        atl = result.get("atl", 0)
                        atl_date = result.get("atl_date", "نامشخص")
                        atl_change = result.get("atl_change_percentage", 0)
                        volume = result.get("total_volume_usd", 0)
                        circulating = result.get("circulating_supply", 0)
                        total_supply = result.get("total_supply", 0)
                        max_supply = result.get("max_supply", "نامحدود")
                        site = result.get("official_site", "ندارد")
                        twitter = result.get("twitter", "ندارد")
                        reddit = result.get("reddit", "ندارد")
                        github = result.get("github_repos", [])
                        blockchain_sites = result.get("blockchain_site", [])
                        chart_url = result.get("chart_7d_url")

                        
                        change_emoji = "📈" if float(change_24h) >= 0 else "📉"

                        
                        reply_text = (
                            f"📊 اطلاعات لحظه‌ای {name} ({symbol.upper()})\n\n"
                            f"🔢 رتبه: {rank}\n"
                            f"💵 قیمت دلاری: ${price_usd}\n"
                            f"🏦 ارزش بازار: ${market_cap:,}\n"
                            f"💹 تغییر ارزش بازار ۲۴ساعت: ${market_cap_change_24h:,}\n"
                            f"📈 بالاترین ۲۴ساعت: ${high_24h}\n"
                            f"📉 پایین‌ترین ۲۴ساعت: ${low_24h}\n\n"
                            f"{change_emoji} تغییرات ۲۴ساعت: {round(change_24h, 2)}%\n"
                            f"📊 تغییرات ۷ روز: {round(change_7d, 2)}%\n"
                            f"📅 تغییرات ۳۰ روز: {round(change_30d, 2)}%\n\n"
                            f"🚀 ATH (بیشترین قیمت): ${ath} در تاریخ {ath_date}\n"
                            f"📉 تغییر نسبت به ATH: {round(ath_change, 2)}%\n"
                            f"⚫ ATL (کمترین قیمت): ${atl} در تاریخ {atl_date}\n"
                            f"📈 تغییر نسبت به ATL: {round(atl_change, 2)}%\n\n"
                            f"💹 حجم معاملات: ${volume:,}\n"
                            f"🔄 عرضه در گردش: {circulating:,.2f}\n"
                            f"📦 کل عرضه: {total_supply:,.2f}\n"
                            f"♾ حداکثر عرضه: {max_supply if max_supply else 'نامحدود'}\n\n"
                            f"🏷 دسته‌بندی‌ها: {', '.join(categories) if categories else 'ندارد'}\n\n"
                        )

                        
                        print(await message.reply_image(chart_url, text=reply_text))

                    else:
                        await message.reply("❌ وب‌سرویس اطلاعاتی برای این ارز پیدا نکرد.")
                else:
                    await message.reply(f"❌ خطا در اتصال به وب‌سرویس قیمت ارز ({resp.status})")
    except Exception as e:
        await message.reply(f"❌ یک خطای پیش‌بینی نشده رخ داد: {e}")


@bot.on_message()
async def handle_all_messages(bot: Robot, message: Message):
    known_commands = [
        "start", "help", "iron", "gpt", "delete",
        "rubino", "zekr", "chart"]
    cmd = message.text.split()[0][1:]  
    if cmd in known_commands:
        return  
    mode = user_modes.get(message.sender_id, "iron")
    asyncio.create_task(fetch_and_reply(message, mode))

async def main():
    await bot.run()
if __name__ == "__main__":
    asyncio.run(main())
