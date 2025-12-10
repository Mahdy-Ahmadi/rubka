import asyncio,aiohttp,random,tempfile,os,io
from rubka.asynco import Robot, Message,filters
from PIL import Image, ImageDraw, ImageFont, ImageFilter


Token = "" #توکن ربات شما


bot = Robot(Token, show_progress=True)
NUM_MINES = 5
ROWS = 5
COLS = 5
MIN_NUMBER = 1
MAX_NUMBER = 100
board = [' ' for _ in range(9)]
player_X = None
player_O = None
current_player = None
game_active = False
font_path = "arial.ttf"

async def fetch_poll():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.rubka.ir/poll", timeout=10) as response:
            return await response.json()
async def GH():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api-free.ir/api/GH.php", timeout=10) as response:
            return await response.json()
def draw_board_doz(chat_id):
    BOARD_FILE = f"board_{chat_id}.png"
    img = Image.new('RGB', (400, 400), color='#333333')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 75)
    except IOError:
        font = ImageFont.load_default()
    line_color = '#555555'
    for i in range(1, 3):
        draw.line((i * 133, 0, i * 133, 400), fill=line_color, width=8, joint="curve")
        draw.line((0, i * 133, 400, i * 133), fill=line_color, width=8, joint="curve")
    border_color = "#999999"
    draw.rounded_rectangle([0, 0, 400, 400], radius=30, outline=border_color, width=10)
    for i in range(9):
        row, col = divmod(i, 3)
        text = board[i] if board[i] != ' ' else str(i + 1)
        if text == 'X':
            text_color = "#FF5733" 
            glow_color = "#FF8A80"
        elif text == 'O':
            text_color = "#4F87FF"
            glow_color = "#80C7FF"
        else:
            text_color = "#E0E0E0"
            glow_color = "#B0B0B0"
        
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_position = (col * 133 + (133 - text_width) / 2, row * 133 + (133 - text_height) / 2)
        draw.text((text_position[0] + 3, text_position[1] + 3), text, font=font, fill=glow_color)
        draw.text(text_position, text, font=font, fill=text_color)
    img.save(BOARD_FILE)
    return BOARD_FILE

player_choice = {}
game_active = False
def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return "tie"
    if (choice1 == "سنگ" and choice2 == "قیچی") or \
       (choice1 == "کاغذ" and choice2 == "سنگ") or \
       (choice1 == "قیچی" and choice2 == "کاغذ"):
        return choice1
    return choice2

def check_winner():
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in lines:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    if ' ' not in board:
        return 'Tie'
    return None
@bot.on_message()
async def start_rock_paper_scissors(bot: Robot, message: Message):
    text = message.text.strip()
    global game_active
    if text == "سنگ کاغذ قیچی":
        if game_active:
            await bot.send_message(message.chat_id, "بازی در حال اجراست. لطفاً منتظر بمانید.\n\n» **Rubka Library**", reply_to_message_id=message.message_id)
            return
        player_choice.clear()  
        game_active = True
        await bot.send_image(message.chat_id, path="100.jpg",text="بازی سنگ کاغذ قیچی شروع شد!\nاولین بازیکن سنگ، کاغذ یا قیچی را انتخاب کن.\n\n» **Rubka Library**", reply_to_message_id=message.message_id)

@bot.on_message()
async def rps_game(bot: Robot, message: Message):
    user_choice = message.text.strip()
    if message.text not in ["سنگ", "کاغذ", "قیچی"]:
        return
    images = {
        "سنگ": "sang.jpg",
        "کاغذ": "kaqaz.jpg",
        "قیچی": "gheichi.jpg"
    }
    if user_choice not in images:
        await message.reply("لطفاً یکی از این گزینه‌ها رو انتخاب کن: سنگ، کاغذ یا قیچی.")
        return
    bot_choice = random.choice(["سنگ", "کاغذ", "قیچی"])
    def winner(u, b):
        if u == b:
            return "equal"
        if (u == "سنگ" and b == "قیچی") or \
           (u == "قیچی" and b == "کاغذ") or \
           (u == "کاغذ" and b == "سنگ"):
            return "user"
        return "bot"
    result = winner(user_choice, bot_choice)
    if result == "equal":text = f"من {bot_choice} انتخاب کردم.\n😅 مساوی شد!"
    elif result == "user":text = f"من {bot_choice} انتخاب کردم.\n🎉 تو بردی!"
    else:text = f"من {bot_choice} انتخاب کردم.\n😈 من بردم!"
    await bot.send_image(
        message.chat_id,
        path=images[bot_choice],
        text=f"انتخاب من: {bot_choice}\n\n{text}",
        reply_to_message_id=message.message_id
    )
@bot.on_message()
async def stop_game(bot: Robot, message: Message):
    global game_active,player_choice
    if message.text.strip() == "توقف سنگ کاغذ قیچی":
        if not game_active:
            await bot.send_message(message.chat_id, "هیچ بازی فعالی در حال اجرا نیست.\n\n» **Rubka Library**", reply_to_message_id=message.message_id)
            return
        game_active = False
        player_choice.clear()
        await bot.send_message(message.chat_id, "⛔ بازی سنگ کاغذ قیچی متوقف شد.\nبرای شروع دوباره «شروع بازی سنگ کاغذ قیچی» را ارسال کنید.\n\n» **Rubka Library**", reply_to_message_id=message.message_id)
@bot.on_message(filters.text_contains_any(["جرعت","حقیقت","جرعت و حقیقت","جرعت حقیقت","حقیقت و جرعت"]))
async def handle_challenge(bot: Robot, message: Message):
    data = await GH()
    await message.reply(f"{data['result']}\n\n» **Rubka Library**")


@bot.on_message(filters.text_contains_any(["اسم و فامیل", "بازی اسم و فامیل"]))
async def esm_famil(bot: Robot, message: Message):
    categories = [
        "اسم",
        "فامیل",
        "حیوان",
        "اشیا",
        "شهر",
        'کشور',
        "استان"
    ]
    letters = list("ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی")
    category = random.choice(categories)
    letter = random.choice(letters)

    await message.reply(
        f"🎯 **چالش اسم و فامیل!**\n\n"
        f"یک **{category}** با حرف **{letter}** بگو 👇🔥\n\n"
        f"» **Rubka Library**",
    )

def create_board():
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    mines = random.sample(range(ROWS * COLS), NUM_MINES)
    for mine in mines:
        row, col = divmod(mine, COLS)
        board[row][col] = '💣'
    return board

def calculate_adjacent_mines(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == '💣':
                continue
            mine_count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= row + i < ROWS and 0 <= col + j < COLS:
                        if board[row + i][col + j] == '💣':
                            mine_count += 1
            if mine_count > 0:
                board[row][col] = str(mine_count)
    return board

def draw_board(board):
    cell_size = 60
    width = COLS * cell_size
    height = ROWS * cell_size
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    try:font = ImageFont.truetype("arial.ttf", 40)
    except IOError:font = ImageFont.load_default()

    for row in range(ROWS):
        for col in range(COLS):
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            draw.rectangle([x1, y1, x2, y2], outline='black', width=3)
            cell_value = board[row][col]
            text_width, text_height = draw.textbbox((x1, y1), cell_value, font=font)[2:4]
            text_x = x1 + (cell_size - text_width) / 2
            text_y = y1 + (cell_size - text_height) / 2
            draw.text((text_x, text_y), cell_value, font=font, fill='black')

    return img

def display_board(board):
    return "\n".join(" ".join(str(cell) for cell in row) for row in board)

def check_win(board):
    for row in board:
        if ' ' in row:
            return False
    return True

async def start_game(message: Message, bot: Robot):
    player_id = message.sender_id
    board = create_board()
    board_with_numbers = calculate_adjacent_mines(board)
    hidden_board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    board_image = draw_board(hidden_board)
    image_path = "board_image.png"
    board_image.save(image_path)
    
    await bot.send_message(message.chat_id, "بازی مین‌روب شروع شد! جدول به شکل زیر است:")
    await bot.send_image(message.chat_id, path=image_path, text="جدول بازی:")
    
    await bot.send_message(message.chat_id, "لطفاً خانه‌ای که می‌خواهید انتخاب کنید را وارد کنید (فرمت: ردیف، ستون).")
    game_state = {}
    def check_move(move, player_id):
        try:
            row, col = map(int, move.split(","))
            if row < 1 or row > ROWS or col < 1 or col > COLS:
                return "شماره ردیف یا ستون معتبر نیست!"
            if hidden_board[row-1][col-1] != ' ':
                return "این خانه قبلاً انتخاب شده!"
            
            if board[row-1][col-1] == '💣':
                hidden_board[row-1][col-1] = '💣'
                return f"🚨 شما به مین برخورد کردید! بازی تمام شد."
            else:
                hidden_board[row-1][col-1] = board[row-1][col-1]
                if check_win(hidden_board):
                    return f"🎉 شما بازی رو بردید! تمام خانه‌ها پاک شده‌اند."
                return None
        except ValueError:
            pass
    game_state[player_id] = {'board': hidden_board}
    @bot.on_message()
    async def handle_user_move(bot: Robot, response: Message):
        if response.sender_id == message.sender_id:
            move = response.text.strip()
            result = check_move(move, response.sender_id)
            
            if result:
                await bot.send_message(message.chat_id, result)
                del game_state[response.sender_id]
            else:
                board_image = draw_board(hidden_board)
                board_image.save(image_path) 
                await bot.send_message(message.chat_id, "گام بعدی خود را وارد کنید:")
                await bot.send_image(message.chat_id, path=image_path, text="جدول به روز شده:")

async def start_guessing_game(message: Message, bot: Robot):
    number_to_guess = random.randint(MIN_NUMBER, MAX_NUMBER)
    attempts = 0
    max_attempts = 10
    game_state = {message.sender_id: {'number': number_to_guess, 'attempts': attempts}}
    await bot.send_message(message.chat_id, f"بازی حدس عدد شروع شد! من یک عدد تصادفی بین {MIN_NUMBER} تا {MAX_NUMBER} انتخاب کرده‌ام. سعی کن حدس بزنی!")
    await bot.send_message(message.chat_id, f"حداکثر {max_attempts} تلاش داری. بگو حدس تو چیه؟")
    @bot.on_message()
    async def handle_guess(bot: Robot, response: Message):
        if response.sender_id != message.sender_id:
            return 
        try:guess = int(response.text.strip())
        except ValueError:return
        game_info = game_state[response.sender_id]
        game_info['attempts'] += 1
        if guess < game_info['number']:
            response_text = "عدد حدسی شما کوچک‌تر است. دوباره امتحان کنید!"
        elif guess > game_info['number']:
            response_text = "عدد حدسی شما بزرگ‌تر است. دوباره امتحان کنید!"
        else:
            response_text = f"تبریک! شما عدد {game_info['number']} را در {game_info['attempts']} تلاش حدس زدید!"
            del game_state[response.sender_id]
        if game_info['attempts'] >= max_attempts:
            response_text = f"متاسفم، شما نتوانستید عدد را حدس بزنید. عدد صحیح {game_info['number']} بود."
            del game_state[response.sender_id]
        await bot.send_message(message.chat_id, response_text)
PUZZLE_SIZE = 3  
IMAGE_PATH = 'path_to_your_image.jpg'  


def split_image(image_path, size=PUZZLE_SIZE):
    
    image = Image.open(image_path)
    image_width, image_height = image.size
    piece_width = image_width // size
    piece_height = image_height // size
    
    pieces = []
    for i in range(size):
        for j in range(size):
            
            box = (j * piece_width, i * piece_height, (j + 1) * piece_width, (i + 1) * piece_height)
            piece = image.crop(box)
            pieces.append(piece)
    return pieces


def get_image_data(pieces):
    file_data = []
    for idx, piece in enumerate(pieces):
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            piece.save(temp_file, 'JPEG')
            file_data.append(temp_file.name)  
    return file_data


async def start_puzzle_game(message: Message, bot: Robot):
    
    pieces = split_image(IMAGE_PATH)
    shuffled_pieces = random.sample(pieces, len(pieces))  
    image_data = get_image_data(shuffled_pieces)

    
    game_state = {message.sender_id: {'pieces': shuffled_pieces, 'image_data': image_data, 'puzzle': pieces}}

    await bot.send_message(message.chat_id, "بازی پازل شروع شد! قطعات تصویر به طور تصادفی جابجا شده‌اند. لطفاً قطعات را به درستی مرتب کنید.")

    
    for idx, file_path in enumerate(image_data):
        await bot.send_image(message.chat_id, file_path, text=f"قطعه {idx + 1}")

    await bot.send_message(message.chat_id, "برای مرتب کردن قطعات، شماره قطعه را وارد کن.")

    @bot.on_message()
    async def handle_puzzle_move(bot: Robot, response: Message):
        if response.sender_id != message.sender_id:
            return
        try:
            piece_num = int(response.text.strip()) - 1
            if piece_num < 0 or piece_num >= len(image_data):
                await bot.send_message(message.chat_id, "شماره قطعه معتبر نیست.")
                return
            shuffled_pieces[piece_num], shuffled_pieces[(piece_num + 1) % len(shuffled_pieces)] = shuffled_pieces[(piece_num + 1) % len(shuffled_pieces)], shuffled_pieces[piece_num]
            new_image_data = get_image_data(shuffled_pieces)
            for idx, file_path in enumerate(new_image_data):
                await bot.send_image(message.chat_id, file_path, text=f"قطعه {idx + 1}")
            await bot.send_message(message.chat_id, "قطعه جابجا شد. لطفاً ادامه بدهید.")
            if check_puzzle_completion(game_state[message.sender_id]):
                await bot.send_message(message.chat_id, "تبریک! شما پازل را با موفقیت حل کردید!")
                del game_state[message.sender_id]  
        except ValueError:...
    def check_puzzle_completion(game_info):
        return game_info['pieces'] == game_info['puzzle']

@bot.on_message(filters.text_contains_any(["پازل", "حل پازل"]))
async def play_puzzle_game(bot: Robot, message: Message):
    await start_puzzle_game(message, bot)
@bot.on_message(filters.text_contains_any(["حدس عدد", "حدس اعداد"]))
async def play_guessing_game(bot: Robot, message: Message):
    await start_guessing_game(message, bot)

@bot.on_message(filters.text_contains_any(["مین‌روب", "مین روب"]))
async def play_minesweeper(bot: Robot, message: Message):
    await start_game(message, bot)
@bot.on_message(filters.text_contains_any(["راهنما", "help"]) & filters.is_group)
async def handle_challenge2(bot: Robot, message: Message):
    await message.reply(f""">{await message.name}
━━━━━━━━━━━━━━
> 💠 **راهنمای ربات سرگرمی**
> به ربات خوش آمدید! اینجا مجموعه‌ای از بازی‌ها و چالش‌های سرگرم‌کننده داریم!

━━━━━━━━━━━━━━━━━━
> 🎮 **بازی‌ها**

> 🔹 **سنگ کاغذ قیچی** — شروع: «سنگ کاغذ قیچی» | توقف: «توقف سنگ کاغذ قیچی»  
> 🔹 **بازی دوز** — شروع: «شروع بازی» | پیوستن: «پیوستن» | توقف: «توقف بازی»  
> 🔹 **گل یا پوچ** — شروع: «گل یا پوچ» | انتخاب: «چپ» یا «راست»  
> 🔹 **تاس سه‌بعدی** — ارسال: «تاس»  
> 🔹 **پازل** — ارسال: «پازل» یا «حل پازل»  
> 🔹 **حدس عدد** — ارسال: «حدس عدد»  
> 🔹 **مین‌روب** — ارسال: «مین روب» | توقف: «توقف مین روب»

━━━━━━━━━━━━━━━━━━
> 🔥 **چالش‌ها**

> 🔹 **جرأت و حقیقت** — ارسال: «جرعت» یا «حقیقت»  
> 🔹 **اسم و فامیل** — ارسال: «اسم و فامیل»  
> 🔹 **کوییز** — ارسال: «کوییز»

━━━━━━━━━━━━━━━━━━
> ⚙️ **نکات مهم**

> • در بازی‌ها فقط بازیکنان فعال می‌توانند حرکت کنند.  
> • تمامی بازی‌ها بعد از اتمام قابل شروع دوباره هستند.
> • اگر بازی متوقف شود، بازیکنان می‌توانند دوباره شروع کنند.

> برای پشتیبانی و گزارش باگ‌ها، پیام دهید!  
> **سازنده: Rubka Library**
""")
@bot.on_message(filters.is_private)
async def handle_challenge3(bot: Robot, message: Message):
    await message.reply(f"""
پیام پی وی
""")
@bot.on_message(filters.text_contains_any(["تاس"]))
async def handle_challenge(bot: Robot, message: Message):
    dice_number = random.randint(1, 6)
    dice_size = (200, 200)
    dice_image = Image.new('RGB', dice_size, color='#ffffff')
    draw = ImageDraw.Draw(dice_image)
    positions = {
        1: [(100, 100)],  
        2: [(50, 50), (150, 150)],  
        3: [(50, 50), (100, 100), (150, 150)],  
        4: [(50, 50), (50, 150), (150, 50), (150, 150)],  
        5: [(50, 50), (50, 150), (100, 100), (150, 50), (150, 150)],  
        6: [(50, 50), (50, 100), (50, 150), (150, 50), (150, 100), (150, 150)]  
    }
    light_color = (255, 255, 255)
    shadow_color = (80, 80, 80)
    shadow_image = Image.new('RGBA', dice_size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_image)
    for pos in positions[dice_number]:
        shadow_draw.ellipse((pos[0]-25, pos[1]-25, pos[0]+25, pos[1]+25), fill=shadow_color)
    shadow_image = shadow_image.filter(ImageFilter.GaussianBlur(radius=5))
    for pos in positions[dice_number]:
        draw.ellipse((pos[0]-20, pos[1]-20, pos[0]+20, pos[1]+20), fill='black')
    dice_image_with_shadow = Image.alpha_composite(shadow_image.convert('RGBA'), dice_image.convert('RGBA'))
    for pos in positions[dice_number]:
        draw.ellipse((pos[0]-18, pos[1]-18, pos[0]+18, pos[1]+18), fill=light_color)
    dice_image = dice_image_with_shadow.convert('RGB')
    dice_image.save("dice_image_3d_final.png")
    await bot.send_image(
        chat_id=message.chat_id,
        reply_to_message_id=message.message_id,
        path="dice_image_3d_final.png",
        text=f"نتیجه تاس: {dice_number}\n\n» **Rubka Library**"
    )
@bot.on_message(filters.text_contains_any(["چالش","کوییز","Quiz"]))
async def handle_challenge(bot: Robot, message: Message):
    sent = await message.reply("درحال دریافت اطلاعات چالش لطفا منتظر باشید...")
    try:
        poll_data = await fetch_poll()
        await bot.send_poll(
            chat_id=message.chat_id,
            question=poll_data["question"],
            options=poll_data["options"],
            type="Quiz",
            hint=poll_data.get("hint", ""),
            correct_option_index=0,
            reply_to_message_id=message.message_id
        )

        await sent.delete()
    except Exception as e:
        await sent.delete()
        await message.reply(f"Error {e}")
daze = {}
@bot.on_message(filters.text_contains_any(["گل یا پوچ"]))
async def handle_game(bot: Robot, message: Message):
    if message.sender_id not in daze:
        daze[message.sender_id] = {}
    await bot.send_image(
        message.chat_id,
        path="mosht2.jpg",
        text="گل توی راست هست یا چپ؟\n\n» **Rubka Library**",
        reply_to_message_id=message.message_id
    )
    daze[message.sender_id]['state'] = "waiting"
    daze[message.sender_id]['answer'] = random.choice(["راست", "چپ"])

@bot.on_message()
async def check_choice(bot: Robot, message: Message):
    if message.text not in ["چپ", "راست"]:
        return
    user = daze.get(message.sender_id)
    if not user or user.get("state") != "waiting":
        return
    correct = user["answer"]
    cool = "rast.jpg" if correct == "راست" else "chap.jpg"
    if message.text == correct:
        result = f"آفرین {correct} گفتی، بردی! 🎉\n\n» **Rubka Library**"
    else:
        result = f"اشتباه گفتی 😅 گل توی {correct} بود!\n\n» **Rubka Library**"
    await bot.send_image(
        message.chat_id,
        path=cool,
        text=result,
        reply_to_message_id=message.message_id
    )
    user["state"] = None
@bot.on_message()
async def handler(bot: Robot, message: Message):
    global player_X, player_O, current_player, game_active, board
    text = message.text.strip()
    if text == "توقف بازی":
        if not game_active:
            await bot.send_message(message.chat_id, "بازی فعالی در حال اجرا نیست.\n\n» **Rubka Library**", reply_to_message_id=message.message_id)
            return
        game_active = False
        player_X = None
        player_O = None
        current_player = None
        board = [' ' for _ in range(9)]
        await bot.send_message(
            message.chat_id,
            "⛔ بازی دوز متوقف شد.\nبرای شروع دوباره «شروع بازی» را ارسال کنید.\n\n» **Rubka Library**",
            reply_to_message_id=message.message_id
        )
        return
    if text == "شروع بازی":
        if game_active:
            await bot.send_message(message.chat_id, "بازی در حال اجراست. لطفاً منتظر بمانید.\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
            return
        player_X = message.sender_id
        player_O = None
        current_player = player_X
        board = [' ' for _ in range(9)]
        game_active = True
        board_file = draw_board_doz(message.chat_id)
        await bot.send_message(message.chat_id, f"🏁 بازی شروع شد!\nبازیکن X: شما\nبرای پیوستن نفر دوم، پیام 'پیوستن' را ارسال کنید.\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
        await bot.send_image(message.chat_id, board_file, text="جدول بازی دوز")
        return
    if text == "پیوستن":
        if not game_active:
            await bot.send_message(message.chat_id, "هیچ بازی فعالی وجود ندارد. ابتدا 'شروع بازی' را ارسال کنید.\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
            return
        if player_O:
            await bot.send_message(message.chat_id, "بازیکن دوم قبلاً وارد بازی شده است.\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
            return
        if message.sender_id == player_X:
            await bot.send_message(message.chat_id, "شما بازیکن اول هستید. منتظر نفر دوم باشید.\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
            return
        player_O = message.sender_id
        board_file = draw_board_doz(message.chat_id)
        await bot.send_message(message.chat_id, f"🎮 بازیکن دوم وارد شد!\nبازیکن O: شما\nنوبت بازیکن X است.\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
        await bot.send_image(message.chat_id, board_file, text="نوبت بازیکن X\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
        return

    if game_active and message.sender_id in [player_X, player_O]:
        if message.sender_id != current_player:
            return
        if not text.isdigit() or not (1 <= int(text) <= 9):
            return
        pos = int(text) - 1
        if board[pos] != ' ':
            await bot.send_message(message.chat_id, "این خانه قبلاً پر شده است. خانه دیگری انتخاب کنید.\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
            return
        board[pos] = 'X' if message.sender_id == player_X else 'O'
        winner = check_winner()
        board_file = draw_board_doz(message.chat_id)
        if winner:
            game_active = False
            if winner == 'Tie':
                await bot.send_image(message.chat_id, board_file, text="⚖️ بازی مساوی شد!\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
                await bot.send_message(message.chat_id, "بازی به پایان رسید. برای شروع بازی جدید 'شروع بازی' را ارسال کنید.\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
            else:
                await bot.send_image(message.chat_id, board_file, text=f"🏆 بازیکن {winner} برنده شد!\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
                await bot.send_message(message.chat_id, f"بازیکن {winner} برنده شد! 🎉\nبرای شروع بازی جدید 'شروع بازی' را ارسال کنید.\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
            return
        current_player = player_O if current_player == player_X else player_X
        await bot.send_image(message.chat_id, board_file, text=f"نوبت بازیکن {'X' if current_player == player_X else 'O'}\n\n» **Rubka Library**",reply_to_message_id=message.message_id)
        return
bot.run(sleep_time=0)