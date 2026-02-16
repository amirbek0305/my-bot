import asyncio
import os
import re
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from dotenv import load_dotenv
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime

load_dotenv()

# ================== SOZLAMALAR ==================
TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL_USERNAME = "mahalliyarizalar"

# ================== FSM ==================
class ReportState(StatesGroup):
    category = State()
    description = State()
    location = State()
    photo = State()

# ================== BOT ==================
bot = Bot(TOKEN)
dp = Dispatcher()

# ================== KEYBOARDLAR ==================
category_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛣 Yo‘l"), KeyboardButton(text="💡 Chiroq")],
        [KeyboardButton(text="🚰 Suv"), KeyboardButton(text="🗑 Axlat")],
        [KeyboardButton(text="🔥 Gaz"), KeyboardButton(text="🧱 Boshqa")]
    ],
    resize_keyboard=True
)

location_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]],
    resize_keyboard=True
)

skip_photo_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⏭ Rasm yo‘q")]],
    resize_keyboard=True
)

# ================== SO'KINISH FILTER ==================
BAD_WORDS = [
    # Uzbek
    "baxil","bildirqsan","bodom","bo'ldi-pechak","bo'ri","bo'rttirmoq","bo'rsildoq","buvsi","chayon","chayono'g'ri",
"chayqov","cho't","cho'tir","cho'tka","dangasa","dangasalik","darrov","dars","daxshat","daydi",
"dehqon","dil","dildor" ,"dilgor","am bosh","ambosh","ami teshik gar","amiteshik gar","amiteshikgar","horomdan bolgan","horomilar","horomi","chochobosh","am yalr","amyalar","dilsiyoh","dilxasta","do'kay","do'ppiday","do'ppisiga",
"do'pposiga","g'adir","g'adir-budur","g'ajak","g'ajimoq","g'alat","g'alati","g'andirak","g'andiraklamoq","g'ang",
"g'angimoq","g'anim","g'animlik","g'animona","g'animchasiga","g'ash","g'ashiq","g'ashlik","g'ashlamoq","g'avvos",
"g'avvoslik","g'ayrat","g'ayratli","g'ayratsiz","g'azab","g'azabdor","g'azabli","g'azabnok","g'azablanish","g'azablanmoq",
"g'ildirak","g'ildiraklamoq","g'ira-shira","g'ov","g'ovur","g'ovurgo'dak","g'oz","g'ozmoq","g'ubor","g'ul",
"g'ulg'ula","g'ulg'ulali","g'ulg'ulasiz","g'umon","g'ur","g'urur","g'ururli","g'urursiz","ahmoq","jinni","tentak","devona","g'ashiq","telba","jallob","yaroqsiz","bepul","bemaza",
"beor","beadab","behayo","behayot",
"bad","yaramas","ijir","ijirsigan","iflos","kirxona",
"shilqim","shilta","shilqor","aqlsiz",
"g'ovur","g'ovurgo'dak","do'ppiday","do'ppisiga","do'pposiga","kalava","kaltak","kaltaklamoq","kuturgan","kuturmagan",
"latta","latto","lat-yor","miyasiz","miyasi past","mijg'ova","mog'or","mog'orlamoq","moxov","noxun",
"nohaq","o'jar","o'pka","pand bermoq","pand-pand","pastkash","pastkashlik","peshana","pishiq","pishirim",
"qaltis","qasos","qo'pol","qo'poruvchi","qo'rqoq","rasvo","rusvay","safro","safrodor","saraton",
"sarg'ish","sarsor","sarson","sarson-sargardon","shafqatsiz","shil","shilqor","shilqim","shilta","shilqorlik",
"tabarruk","tabarrukot","talvasas","talvasa","tentaklik","tentaklarcha","tirs","tirsak","tirsillamoq","tob",
"tob-toqat","to'g'ri","to'g'rilik","to'g'risiz","to'g'risizlik","to'zon","to'zima","to'kin","to'kis","to'kma",
"to'la","to'lalik","to'ldirma","to'ldirmoq","to'lib-to'shib","to'lim","to'lin","to'liq","to'liqlik","to'lqin",
"to'mtoq","to'nka","to'ng","to'ng'iz","to'ng'ich","to'ng'ichlik","to'ng'lik","to'ng'moq","ahmoq", "ahmoqh", "ahmoqq", "ahmok", "axmoq", "ahmok", "ahmoq!", "ahmoq?", "ahmoq.", "ahmoq 😡", "😡 ahmoq", "ahmoq 🤬", "🤬 ahmoq", "ahmoq 👎", "👎 ahmoq", "a-h-m-o-q", "a.h.m.o.q", "a_h_m_o_q", "a|h|m|o|q", "a/h/m/o/q", "@hmoq", "@xmoq", "@hmok", "ahm0q", "@hm0q", "ahmoq1", "ahmoq123", "ahmoq bola", "ahmoq odam", "ahmoqman", "ahmoqsan", "ahmoqdir", "ahmoqlar", "ahmoqlik", "am bosh", "ambosh", "amb0sh", "@mbosh", "am-bosh", "am_bosh", "ami teshik gar", "amiteshik gar", "amiteshikgar", "ami teshikgar", "ami teshik gar", "ami teshikgar", "amiteshik-gar", "ami-teshik-gar", "am yalr", "amyalar", "am yalar", "am-yalar", "am_yalar", "baxil", "bax!l", "bax1l", "b@xil", "baxil!", "baxil?", "baxil.", "baxil odam", "baxil kishi", "baxillik", "baxilman", "baxilsan", "bildirqsan", "bildirqs@n", "bildirqSan", "bildirq-san", "bildirq_san", "bildirqsanlik", "bildirqsanman", "bildirqsansan", "bildirqsanlar", "bodom", "bod0m", "b0dom", "bodom!", "bodom?", "bodom.", "bo'ldi-pechak", "boldi-pechak", "bo'ldi pechak", "boldi pechak", "bo'ldipechak", "bo'ldi-pechak!", "bo'ldi-pechak?", "bo'ldi-pechak.", "bo'ri", "bori", "bo'ri!", "bo'ri?", "bo'ri.", "b0'ri", "bori", "bo'rttirmoq", "borttirmoq", "bo'rttirmok", "borttirmok", "bo'rttirm@q", "bo'rsildoq", "borsildoq", "bo'rsild0q", "borsild0q", "bo'rsild@q", "buvsi", "buvs! buvsi!", "buvsi?", "buvsi.", "b@vsi", "buvsi kishi"



    # Russian
    "блять", "блядь", "бля", "блядина", "блядский", "блядство", "блядюга",
"blyat", "blyad", "blya", "blyadina", "blyadskiy", "blyadstvo", "blyaduga",
"bl@t", "bl@d", "bl@", "bl@din@", "bl@dskiy", "bl@dstvo", "bl@duga",
"b1@t", "b1@d", "b1@", "b1@din@", "b1@dskiy", "b1@dstvo", "b1@duga",
"блять", "блядь", "бля", "блядина", "блядский", "блядство", "блядюга",
"blyat", "blyad", "blya", "blyadina", "blyadskiy", "blyadstvo", "blyaduga",
"блять", "блядь", "бля", "блядина", "блядский", "блядство", "блядюга",
"bl@t", "bl@d", "bl@", "bl@din@", "bl@dskiy", "bl@dstvo", "bl@duga",
"b l y a t", "b-l-y-a-t", "b_l_y_a_t", "b|lyat", "b/lyat", r"b\ l\ y\ a\ t",
"b l y a d", "b-l-y-a-d", "b_l_y_a_d", "b|lyad", "b/lyad", r"b\ l\ y\ a\ d",
"b l y a", "b-l-y-a", "b_l_y_a", "b|lya", "b/lya", r"b\ l\ y\ a","yibanalar","kotlar","amlar"
"$lyat", "$lyad", "$lya", "$lyadina", "$lyadskiy", "$lyadstvo", "$lyaduga",
"5lyat", "5lyad", "5lya", "5lyadina", "5lyadskiy", "5lyadstvo", "5lyaduga",
"bl9at", "bl9ad", "bl9a", "bl9adina", "bl9adskiy", "bl9adstvo", "bl9aduga",
"бл9ть", "бл9дь", "бл9", "бл9дина", "бл9дский", "бл9дство", "бл9дюга",
"пизда", "пиздец", "пиздеть", "пиздишь", "пиздюк", "пиздюлина", "пиздюли", "пиздюля", "пиздёж", "пиздобратия",
"pizda", "pizdets", "pizdet", "pizdish", "pizdyuk", "pizdyulina", "pizdyuli", "pizdyulya", "pizdyozh", "pizdobratiya",
"пиzда", "пиzдец", "пиzдеть", "пиzдишь", "пиzдюк", "пиzдюлина", "пиzдюли", "пиzдюля", "пиzдёж", "пиzдобратия",
"p!zda", "p!zdets", "p!zdet", "p!zdish", "p!zdyuk", "p!zdyulina", "p!zdyuli", "p!zdyulya", "p!zdyozh", "p!zdobratiya",
"pi3da", "pi3dets", "pi3det", "pi3dish", "pi3dyuk", "pi3dyulina", "pi3dyuli", "pi3dyulya", "pi3dyozh", "pi3dobratiya",
"ебать", "ебись", "ебло", "ебальник", "ебанутый", "ебанат", "ебанашка", "ебашить", "ёбнуть", "ёбаный", "ебливый", "ёбарь",
"ebat", "ebis", "eblo", "ebalnik", "ebanuty", "ebanat", "ebanashka", "ebashat", "yobnut", "yobany", "eblivy", "yobar",
"е6ать", "е6ись", "е6ло", "е6альник", "е6анутый", "е6анат", "е6анашка", "е6ашить", "ё6нуть", "ё6аный", "е6ливый", "ё6арь",
"e6@t", "e6is", "e6lo", "e6alnik", "e6anuty", "e6anat", "e6anashka", "e6ashat", "y6nut", "y6any", "e6livy", "y6ar",
"еб@ть", "еб@сь", "еб@ло", "еб@льник", "еб@нутый", "еб@нат", "еб@нашка", "еб@шить", "ёб@нуть", "ёб@ный", "еб@ливый", "ёб@рь",
"huy", "huya", "huyoviy", "huyovo", "huynya", "huylo", "huita", "huesos", "huila", "huev", "huylan", "huyarit",
"xuy", "xuya", "xuyoviy", "xuyovo", "xuynya", "xuylo", "xuita", "xuesos", "xuila", "xuev", "xuylan", "xuyarit",
"ху1", "ху1я", "ху1ёвый", "ху1ёво", "ху1йня", "ху1йло", "ху1ита", "ху1есос", "ху1ила", "ху1ев", "ху1йлан", "ху1ярить",
"сука", "cука", "cyka", "suka", "cykа", "sукa", "syka", "sykа", "suuka", "sukka", "ssuka", "sukaa", "suka!", "suka?", "suka...", "suka!!!", "suka???",
"çuka", "çуka", "cүka", "sүka", "suk@", "$uka", "$uk@", "5uka", "5uk@", "zuка", "zuк@",
"sukablyat", "sukasyn", "sukam", "sukan", "sukang", "sukalar", "sukachi", "sukabola", "sukavoy",
"suka 😡", "suka 😠", "suka 🤬", "suka 👎", "suka 💩", "suka 🐕", "suka 🐶", "😡 suka", "👎 suka",
"sooka", "sooqa", "soqa", "soka", "so'ka", "suqa", "suqqa",
"cyka 😡", "cyka 😠", "cyka 🤬", "cyka 👎", "cyka 💩", "cyka 🐕", "cyka 🐶", "😡 cyka", "👎 cyka",
"охуеть", "охуенный", "охуительный", "охереть", "охренеть", "похую",
"ohuet", "ohueniy", "ohuitelny", "oheret", "ohrenet", "pohuyu",
"нахуй", "похуй", "нихуя", "хуй знает", "хуй с ним",
"nahuy", "pohuy", "nihuya", "huy znaet", "huy s nim",
"выебываться", "выебать", "доебаться", "заебать", "заебаться", "наебать", "наебаться", "обоссаться",
"vyebyvatsya", "vyebat", "doebatsya", "zaebat", "zaebatsya", "naebat", "naebatsya", "obossatsya",
"гондон", "гондона", "gondon", "gondona", "гандон", "гандоны", "gandon", "gondoni",
"мудак", "мудила", "мудозвон", "мудоеб", "мудя", "mudak", "mudila", "mudozvon", "mudoyeb", "mudya",
"говно", "говнюк", "говнарь", "говёный", "гавно", "govno", "govnyuk", "govnar", "govyony", "gavno",
"жопа", "жопой", "жополизание", "жополиз", "zhopa", "zhopoy", "zhopolizanie", "zhopoliz",
"срать", "срака", "срань", "сраный", "сральник", "ссать", "ссышь", "ссака", "ссанина", "ссаки",
"srat", "sraka", "sran", "srany", "sralnik", "ssat", "ssish", "ssaka", "ssanina", "ssaki",
"пердёж", "пердеть", "пердун", "пердунья", "пердак", "пердячий", "perdyozh", "perdet", "perdu"
    # English
    "anal","anus","ass","asshole","assfucker","asswipe","arse","arsehole",
"bastard","bitch","bisexual","blowjob","bollocks","boner","boob","boobs","breasts","bugger","bullshit","butt","buttplug","bdsm",
"cocksucker","cock","clit","clitoris","cum","cunt","cocks","cocksucking","cumshot","coon","crap","creampie",
"dick","dildo","dyke","damn","dickhead","dong","douche","douchebag",
"ejaculate","erection",
"fag","faggot","fap","fapfap","felching","fellatio","foreskin","fuck","fucker","fucking","fucktard","fudgepacker","fuk","fisting","footjob",
"gangbang","gay","goddamn","gook","gspot","gash",
"handjob","hell","homo","hooker","horny","hoe","ho",
"jerkoff","jizz","jackoff","jigaboo","jism",
"kike","kock","kunt","kum",
"labia","lesbian","lmao","lmfao","lust",
"masochist","masturbate","molester","motherfucker","muff","minge","muffdiver","milf",
"nazi","negro","nigga","nigger","nutsack","nympho",
"paki","pedo","pedophile","pecker","pee","peehole","penis","penisfucker","piss","porn","porno","pornography","pube","pubes","pussy","prick","prostitute",
"queef","queer","queers",
"rape","raping","rapist","rectum","retard","rimjob",
"scat","schlong","scrotum","semen","sex","sexy","shag","shit","shitting","shitty","slut","smegma","snatch","spastic","sperm","spic","spick","splooge","spooge","strap-on","suck","sucks","sucker","sucking","suckmy","suckmycock","suckmydick","sissy",
"tard","tits","titties","titty","tosser","turd","twat","twunt",
"vagina","vibrator","vulva","vjayjay","voyeur",
"wang","wank","wanker","whore","willy","wankjob",
"yiffy","yobbo",
"fuk","phuk","fuking","phucking","fuker","phuker","fuckshit","shitfuck","shitface","assface","dickface","cuntface","motherfuck","mthrfkr","mtherfkr","biatch","btch","cnt","dik","d1ck","c0ck","p0rn","pr0n","prn","sx","s3x","fck","fcking"
"anal", "anus", "ass", "assface", "assfucker", "asshole", "arse", "arsehole", "asswipe", "asswipes", 
"bastard", "bitch", "bisexual", "biatch", "bl*wjob", "blow job", "bollocks", "boner", "boob", "boobs", "breasts", "btch", "bdsm", "bugger", "bullshit", "butt", "buttplug", 
"c0ck", "clit", "clitoris", "cock", "cocks", "cocksucker", "cocksucking", "cnt", "coon", "crap", "creampie", "cum", "cumshot", "cunt", "cuntface", 
"d1ck", "damn", "dick", "dickface", "dickhead", "dik", "dildo", "dong", "douche", "douchebag", "dyke", 
"ejaculate", "erection", 
"f@g", "f@ggot", "fag", "faggot", "fap", "fapfap", "fck", "fcker", "fcking", "felching", "fellatio", "foreskin", "fk", "fuck", "fucker", "fucking", "fucktard", "fudgepacker", "fuk", "fuking", "fuker", 
"g@y", "gangbang", "gay", "goddamn", "gook", "gspot", "gash", 
"handjob", "hell", "hoe", "homo", "hooker", "ho", "horny", 
"incest", 
"jackoff", "jerkoff", "jigaboo", "jism", "jizz", 
"kike", "kock", "kunt", "kum", 
"labia", "lesbian", "lmao", "lmfao", "lust", 
"masochist", "masturbate", "mtherfcker", "milf", "minge", "molester", "motherfuck", "motherfucker", "muff", "muffdiver", "mthrfkr", "mtherfkr", 
"nazi", "negro", "nigga", "nigger", "nutsack", "nympho", 
"orgasm", "orgasmic", 
"p0rn", "p@ki", "p3do", "p3dophile", "paki", "pedo", "pedophile", "pecker", "pee", "peehole", "penis", "penisfucker", "phuk", "phuker", "phucking", "piss", "porn", "porno", "pornography", "pr0n", "prn", "prick", "prostitute", "pube", "pubes", "pussy", 
"queef", "queer", "queers", 
"rape", "raping", "rapist", "rectum", "retard", "rimjob", 
"s3x", "scat", "schlong", "scrotum", "semen", "sex", "sexy", "shag", "shit", "shitface", "shitfuck", "shitting", "shitty", "slut", "smegma", "snatch", "spastic", "sperm", "spic", "spick", "splooge", "spooge", "strap-on", "suck", "suckmy", "suckmycock", "suckmydick", "sucks", "sucker", "sucking", "sissy", "sx", 
"tard", "tits", "titties", "titty", "tosser", "turd", "twat", "twunt", 
"vagina", "vibrator", "vulva", "vjayjay", "voyeur", 
"wang", "wank", "wanker", "wankjob", "whore", "willy", 
"yiffy", "yobbo","atif am bosh"
]

def normalize_text(text: str) -> str:
    """Textni kichik harf va faqat harflar raqam va bo'shliqlar bilan ishlash"""
    text = text.lower()
    text = re.sub(r'[^a-zа-яё0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def contains_bad_words(text: str) -> bool:
    clean_text = normalize_text(text)
    for word in BAD_WORDS:
        if re.search(rf'\b{re.escape(word)}\b', clean_text):
            return True
    return False

# ================== /start ==================
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    name = message.from_user.first_name or message.from_user.username
    await message.answer(
        f"Assalomu Aleykum Hurmatli {name}\n\n"
        "Bu *Mahalla Muammo Bot*.\n\n"
        "👇 Muammo turini tanlang:",
        reply_markup=category_kb,
        parse_mode="Markdown"
    )
    await state.set_state(ReportState.category)

# ================== /help ==================
@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "ℹ️ *Mahalla Muammo Bot haqida*\n\n"
        "Bu bot orqali siz mahalladagi muammolarni yubora olasiz:\n\n"
        "1️⃣ Muammo turini tanlaysiz\n"
        "2️⃣ Tavsif yozasiz\n"
        "3️⃣ Joylashuv yuborasiz\n"
        "4️⃣ Rasm yuborasiz (ixtiyoriy)\n\n"
        "📌 Yuborilgan muammo mas’ullarga yetkaziladi.\n"
        "📸 Rasm majburiy emas.\n\n"
        "/start — Botni qayta boshlash\n\n"
        "Yaratuvchi: @hojievsss\n\n"
        "Telegram Kanal: t.me/mahalliyarizalar",
        parse_mode="Markdown"
    )

# ================== CATEGORY ==================
@dp.message(ReportState.category)
async def category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("📝 Muammoni qisqacha yozing:")
    await state.set_state(ReportState.description)

# ================== DESCRIPTION ==================
@dp.message(ReportState.description)
async def description(message: Message, state: FSMContext):
    # 🔹 So'kinish filter
    if contains_bad_words(message.text):
        await message.answer(
            "❌ Iltimos, so‘kinish ishlatmang. Muammoni boshqa so‘zlar bilan yozing."
        )
        return  # Xabar qabul qilinmaydi, foydalanuvchi qaytadan yozadi

    # Agar so'kinish bo'lmasa, davom etamiz
    await state.update_data(description=message.text)
    await message.answer(
        "📍 Muammo joylashuvini yuboring:",
        reply_markup=location_kb
    )
    await state.set_state(ReportState.location)

# ================== LOCATION ==================
@dp.message(ReportState.location, F.location)
async def location(message: Message, state: FSMContext):
    await state.update_data(location=message.location)
    await message.answer(
        "📸 Rasm yuboring (ixtiyoriy):",
        reply_markup=skip_photo_kb
    )
    await state.set_state(ReportState.photo)

@dp.message(ReportState.location)
async def location_error(message: Message):
    await message.answer(
        "❗ Iltimos, joylashuvni 📍 tugma orqali yuboring.",
        reply_markup=location_kb
    )

# ================== PHOTO ==================
@dp.message(ReportState.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_id = message.photo[-1].file_id

    await send_to_admin(message, data, photo_id)

    await message.answer(
        "✅ Muammo yuborildi. Rahmat!",
        reply_markup=category_kb
    )
    await state.clear()

@dp.message(ReportState.photo, F.text == "⏭ Rasm yo‘q")
async def skip_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    await send_to_admin(message, data, None)
    await message.answer(
        "✅ Muammo yuborildi. Rahmat!",
        reply_markup=category_kb
    )
    await state.clear()

@dp.message(ReportState.photo)
async def photo_error(message: Message):
    await message.answer(
        "📸 Rasm yuboring yoki ⏭ Rasm yo‘q tugmasini bosing.",
        reply_markup=skip_photo_kb
    )

# ================== ADMIN'GA ==================
async def send_to_admin(message, data, photo_id):
    try:
        loc = data["location"]
        maps = f"https://maps.google.com/?q={loc.latitude},{loc.longitude}"

        text = (
            "🧾 Yangi muammo\n\n"
            f"👤 User: @{message.from_user.username or 'yo‘q'}\n"
            f"📌 Tur: {data['category']}\n"
            f"📝 Tavsif: {data['description']}\n"
            f"📍 Lokatsiya: {maps}\n"
            f"🕒 Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )

        if photo_id:
            await bot.send_photo(
                chat_id=ADMIN_ID,
                photo=photo_id,
                caption=text
            )
        else:
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=text
            )

        print("✅ Admin’ga yuborildi")

    except Exception as e:
        print("❌ ADMIN’GA YUBORILMADI")
        print(e)

# ================== RUN ==================
async def main():
    while True:
        try:
            print("🤖 Bot ishlayapti...")
            await dp.start_polling(bot)
        except Exception as e:
            print(f"❌ Bot to'xtadi, qayta ishga tushirilmoqda: {e}")
            await asyncio.sleep(5)  # 5 soniya kutib, qayta ishga tushirish

if __name__ == "__main__":
    asyncio.run(main())
