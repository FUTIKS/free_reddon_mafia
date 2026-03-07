from decouple import config
from mafia_bot.utils import games_state
from aiogram.utils.keyboard import InlineKeyboardBuilder
from mafia_bot.models import  PriceStones, User, UserRole
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from core.constants import ROLE_PRICES_IN_MONEY,ROLE_PRICES_IN_STONES




def remove_prefix(text):
    return text.lstrip('@')

def start_inline_btn(user_id):
    from mafia_bot.handlers.main_functions import get_lang

    lang = get_lang(user_id)

    TEXTS = {
        "uz": {
            "roles_info": "ℹ️ Rollar haqida ma'lumot",
            "add_info": "☑️ Botni guruhga qo'shish haqida ma'lumot",
            "add_bot": "➕ Botni guruhga qo'shish",
            "profile": "👤 Profil",
            "roles": "🎭 Rollar",
        },
        "ru": {
            "roles_info": "ℹ️ Информация о ролях",
            "add_info": "☑️ Как добавить бота в группу",
            "add_bot": "➕ Добавить бота в группу",
            "profile": "👤 Профиль",
            "roles": "🎭 Роли",
        },
        "en": {
            "roles_info": "ℹ️ Role information",
            "add_info": "☑️ How to add the bot to a group",
            "add_bot": "➕ Add bot to group",
            "profile": "👤 Profile",
            "roles": "🎭 Roles",
        },
        "tr": {
            "roles_info": "ℹ️ Roller hakkında bilgi",
            "add_info": "☑️ Botu gruba ekleme hakkında bilgi",
            "add_bot": "➕ Botu gruba ekle",
            "profile": "👤 Profil",
            "roles": "🎭 Roller",
        },
        "qz": {
            "roles_info": "ℹ️ Ролдер туралы ақпарат",
            "add_info": "☑️ Ботты топқа қосу туралы ақпарат",
            "add_bot": "➕ Ботты топқа қосу",
            "profile": "👤 Профиль",
            "roles": "🎭 Ролдер",
        },
    }

    t = TEXTS.get(lang, TEXTS["uz"])

    keyboard1 = InlineKeyboardButton(text=t["roles_info"], url="https://t.me/MafiaRedDon_Roles/39")
    keyboard2 = InlineKeyboardButton(text=t["add_info"], url="https://t.me/MafiaRedDon_Roles/96")
    keyboard3 = InlineKeyboardButton(
        text=t["add_bot"],
        url=f"https://t.me/{remove_prefix(config('BOT_USERNAME'))}?startgroup=true"
    )
    keyboard5 = InlineKeyboardButton(text=t["profile"], callback_data="profile")
    keyboard6 = InlineKeyboardButton(text=t["roles"], callback_data="role_menu")

    design = [
        [keyboard1],
        [keyboard2],
        [keyboard3],
        [keyboard5],
        [keyboard6],
    ]

    return InlineKeyboardMarkup(inline_keyboard=design)




def cart_inline_btn(tg_id):
    from mafia_bot.handlers.main_functions import get_lang

    lang = get_lang(tg_id)
    user = User.objects.filter(telegram_id=tg_id).first()

    TEXTS = {
        "uz": {
            "toggle_protection":f"🛡 - {'🟢 ON' if user.is_protected else ' 🔴 OFF'}",
            "toggle_doc": f"📂 - {'🟢 ON' if user.is_doc else ' 🔴 OFF'}",
            "shop": "🛒 Do'kon",
        },
        "ru": {
            "toggle_protection":f"🛡 - {'🟢 ВКЛ' if user.is_protected else ' 🔴 ВЫКЛ'}",
            "toggle_doc": f"📂 - {'🟢 ВКЛ' if user.is_doc else ' 🔴 ВЫКЛ'}",
            "shop": "🛒 Магазин",
        },
        "en": {
            "toggle_protection":f"🛡 - {'🟢 ON' if user.is_protected else ' 🔴 OFF'}",
            "toggle_doc": f"📂 - {'🟢 ON' if user.is_doc else ' 🔴 OFF'}",
            "shop": "🛒 Shop",
        },
        "tr": {
            "toggle_protection":f"🛡 - {'🟢 ON' if user.is_protected else ' 🔴 OFF'}",
            "toggle_doc": f"📂 - {'🟢 ON' if user.is_doc else ' 🔴 OFF'}",
            "shop": "🛒 Mağaza",
        },
        "qz": {
            "toggle_protection":f"🛡 - {'🟢 ВКЛ' if user.is_protected else ' 🔴 ВЫКЛ'}",
            "toggle_doc": f"📂 - {'🟢 ВКЛ' if user.is_doc else ' 🔴 ВЫКЛ'}",
            "shop": "🛒 Дүкен",
        },
    }

    t = TEXTS.get(lang, TEXTS["uz"])

    rows = [
        [
            InlineKeyboardButton(text=t["toggle_protection"], callback_data="toggle_protection"),
            InlineKeyboardButton(text=t["toggle_doc"], callback_data="toggle_doc"),
        ],
        [InlineKeyboardButton(text=t["shop"], callback_data="cart")],
    ]


    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)

    return keyboard

def shop_inline_btn(tg_id):
    from mafia_bot.handlers.main_functions import get_lang

    lang = get_lang(tg_id)

    TEXTS = {
        "uz": {
            "protect": "🛡 Ximoya - 250 💵",
            "docs": "📂 Hujjatlar - 500 💵",
            "role": "🎭 Rol sotib olish",
            "back": "⬅️ Orqaga",
        },
        "ru": {
            "protect": "🛡 Защита - 250 💵",
            "docs": "📂 Документы - 500 💵",
            "role": "🎭 Купить роль",
            "back": "⬅️ Назад",
        },
        "en": {
            "protect": "🛡 Protection - 250 💵",
            "docs": "📂 Documents - 500 💵",
            "role": "🎭 Buy role",
            "back": "⬅️ Back",
        },
        "tr": {
            "protect": "🛡 Koruma - 250 💵",
            "docs": "📂 Belgeler - 500 💵",
            "role": "🎭 Rol satın al",
            "back": "⬅️ Geri",
        },
        "qz": {
            "protect": "🛡 Қорғау - 250 💵",
            "docs": "📂 Құжаттар - 500 💵",
            "role": "🎭 Роль сатып алу",
            "back": "⬅️ Артқа",
        },
    }

    t = TEXTS.get(lang, TEXTS["uz"])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["protect"], callback_data="buy_protection_0")],
            [InlineKeyboardButton(text=t["docs"], callback_data="buy_docs_0")],
            [InlineKeyboardButton(text=t["role"], callback_data="buy_activerole_0")],
            [InlineKeyboardButton(text=t["back"], callback_data="back_profile")],
        ]
    )

    return keyboard


def get_role_price(role_key: str):
    if role_key in ROLE_PRICES_IN_STONES:
        return "💎", ROLE_PRICES_IN_STONES[role_key]
    if role_key in ROLE_PRICES_IN_MONEY:
        return "💵", ROLE_PRICES_IN_MONEY[role_key]
    return "", 0

def role_shop_inline_keyboard(user_id):
    builder = InlineKeyboardBuilder()
    from mafia_bot.handlers.main_functions import get_roles_choices_lang
    ROLES_CHOICES = get_roles_choices_lang(user_id)
    roles = ROLES_CHOICES[:-2]

    for role_key, role_name in roles:
        cur, price = get_role_price(role_key)

        builder.add(
            InlineKeyboardButton(
                text=f"{role_name} - {cur} {price}",
                callback_data=f"active_{role_key}_{price}",
            )
        )

    builder.add(
        InlineKeyboardButton(
            text="⬅️ ",
            callback_data="back_profile"
        )
    )

    builder.adjust(2, 2, 2, 2, 2, 2, 2, 2, 2, 1)
    return builder.as_markup()
def pay_for_money_inline_btn(tg_id, is_money):
    from mafia_bot.handlers.main_functions import get_lang

    lang = get_lang(tg_id)

    TEXTS = {
        "uz": {
            "card": "💳 Kartadan 💳 kartaga",
            "stars": "⭐ Telegram yulduzlar evaziga",
            "back": "⬅️ Orqaga",
        },
        "ru": {
            "card": "💳 С карты на карту",
            "stars": "⭐ За Telegram звёзды",
            "back": "⬅️ Назад",
        },
        "en": {
            "card": "💳 Card to card",
            "stars": "⭐ Pay with Telegram Stars",
            "back": "⬅️ Back",
        },
        "tr": {
            "card": "💳 Karttan karta",
            "stars": "⭐ Telegram yıldızları ile",
            "back": "⬅️ Geri",
        },
        "qz": {
            "card": "💳 Карттан карта",
            "stars": "⭐ Telegram жұлдыздарымен",
            "back": "⬅️ Артқа",
        },
    }

    t = TEXTS.get(lang, TEXTS["uz"])

    if is_money:
        callback1 = "p2p_money"
        callback2 = "star_money"
    else:
        callback1 = "p2p_stone"
        callback2 = "star_stone"

    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text=t["card"], callback_data=callback1)
    )
    builder.add(
        InlineKeyboardButton(text=t["stars"], callback_data=callback2)
    )
    builder.add(
        InlineKeyboardButton(text=t["back"], callback_data="back_profile")
    )

    builder.adjust(1)
    return builder.as_markup()

import json
MONEY_FOR_STAR = {
    1000: 7,
    10000: 77,
    50000: 340,
    100000: 680,
}

STONE_FOR_STAR = {
    1: 7,
    10: 68,
    30: 185,
    50: 237,
    70: 382,
    100: 513,
}


def pay_using_stars_inline_btn(is_money: bool):
    builder = InlineKeyboardBuilder()

    cost = PriceStones.objects.first()
    if not cost:
        cost = PriceStones.objects.create()

    money_map = json.loads(cost.money_in_star or "{}")
    stone_map = json.loads(cost.stone_in_star or "{}")

    if is_money:
        for money_amount, star_amount in money_map.items():
            builder.add(
                InlineKeyboardButton(
                    text=f"💶 {money_amount} - ⭐ {star_amount}",
                    callback_data=f"pul_{money_amount}_{star_amount}"
                )
            )
    else:
        for stone_amount, star_amount in stone_map.items():
            builder.add(
                InlineKeyboardButton(
                    text=f"💎 {stone_amount} - ⭐ {star_amount}",
                    callback_data=f"olmos_{stone_amount}_{star_amount}"
                )
            )

    builder.add(
        InlineKeyboardButton(
            text="⬅️",
            callback_data="back_profile"
        )
    )

    builder.adjust(1)
    return builder.as_markup()


# Roles inline button
def roles_inline_btn(user_id):
    builder = InlineKeyboardBuilder()
    
    from mafia_bot.handlers.main_functions import get_roles_choices_lang
    ROLES_CHOICES = get_roles_choices_lang(user_id)
    for role in ROLES_CHOICES:
        button = InlineKeyboardButton(text=role[1], callback_data=f"roles_{role[0]}")
        builder.add(button)
    builder.adjust(2)
    keyboard = builder.as_markup()
    return keyboard   
        
# Join game button
def join_game_btn(uuid,chat_id):
    from mafia_bot.handlers.main_functions import get_lang_text
    t = get_lang_text(int(chat_id))
    text = t["join_game"]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=text,
                url=f"https://t.me/{remove_prefix(config('BOT_USERNAME'))}?start={uuid}"  # game.code yoki game.uuid
            )]
        ]
    )
    return keyboard
# Go to bot inline button
def go_to_bot_inline_btn(chat_id,number=1):
    from mafia_bot.handlers.main_functions import get_lang_text
    t = get_lang_text(int(chat_id))
    if number == 1:
        text = t["view_role"]
    elif number == 2:
        text = t["go_to_bot"]
    elif number == 3:
        text = t["vote"]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=text,
                url=f"https://t.me/{remove_prefix(config('BOT_USERNAME'))}"  
            )]
        ]
    )
    return keyboard

# Doctor inline button
def doc_btn(players,doctor_id=None,game_id=None,chat_id=None,day=None):
    builder = InlineKeyboardBuilder()
    game = games_state.get(int(game_id), {})
    used_self = game.get("limits", {}).get("doc_self_heal_used", set())
    for player in players :
        first_name = player.get("first_name")
        tg_id = player.get("tg_id")
        if tg_id == doctor_id and doctor_id in used_self:
            continue
        callback=f"doc_{tg_id}_{game_id}_{chat_id}_{day}"
    
        button = InlineKeyboardButton(
            text=first_name,
            callback_data=callback
        )
        builder.add(button)
    builder.add(
        InlineKeyboardButton(
            text="🚷",
            callback_data=f"doc_no_{game_id}_{chat_id}_{day}"
        )
    )

    builder.adjust(1)
    return builder.as_markup()


# Commander inline button
def com_inline_btn(game_id,chat_id,day=None):
    builder = InlineKeyboardBuilder()
    button1 = InlineKeyboardButton(text="🔫", callback_data=f"com_shoot_{game_id}_{chat_id}_{day}")
    button2 = InlineKeyboardButton(text="🔍", callback_data=f"com_protect_{game_id}_{chat_id}_{day}")
    builder.add(button1)
    builder.add(button2)
    builder.add(
        InlineKeyboardButton(
            text="🚷",
            callback_data=f"com_no_{game_id}_{chat_id}_{day}"
        )
    )
    builder.adjust(1)
    return builder.as_markup()

# Com inline action button
def com_inline_action_btn(action,game_id,chat_id,day=None,com_id=None):
    builder = InlineKeyboardBuilder()
    game = games_state.get(int(game_id), {})
    alive_players = game.get("alive", [])
    users_map = game.get("users_map", {})
    alive_users_qs = [users_map[tg_id] for tg_id in alive_players if tg_id in users_map]
    for user in alive_users_qs:
        
        if user.get("tg_id") == com_id:
            continue
        button = InlineKeyboardButton(
            text=f"{user.get("first_name")}",
            callback_data=f"{action}_{user.get("tg_id")}_{game_id}_{day}"
        )
        builder.add(button)
    builder.add(
        InlineKeyboardButton(
            text="🔙",
            callback_data=f"com_back_{game_id}_{chat_id}_{day}"
        )
    )
    builder.adjust(1)
    return builder.as_markup()

# Kamikaze inline button

def action_inline_btn(action,own_id,players,game_id,chat_id,day=None):
    builder = InlineKeyboardBuilder()

    for player in players:
        tg_id = player.get("tg_id")
        first_name = player.get("first_name")
        if tg_id == own_id:
            continue
        text = first_name 
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"{action}_{tg_id}_{game_id}_{chat_id}_{day}"
        )
        builder.add(button)
    
    button = InlineKeyboardButton(
        text="🚷 ",
        callback_data=f"{action}_no_{game_id}_{chat_id}_{day}"
    )
    builder.add(button)

    builder.adjust(1)
    return builder.as_markup()

def confirm_hang_inline_btn(voted_user_id,game_id,chat_id,yes=0, no=0):
    builder = InlineKeyboardBuilder()
    button_yes = InlineKeyboardButton(
        text=f"👍 {yes}",
        callback_data=f"con_yes_{voted_user_id}_{game_id}_{chat_id}"
    )
    button_no = InlineKeyboardButton(
        text=f"👎 {no}",
        callback_data=f"con_no_{voted_user_id}_{game_id}_{chat_id}"
    )
    builder.add(button_yes)
    builder.add(button_no)
    builder.adjust(2)
    return builder.as_markup()


    


def don_inline_btn(players,  game_id, chat_id, don_id,day=None):
    builder = InlineKeyboardBuilder()

    roles_map = games_state.get(int(game_id), {}).get("roles", {})

    for player in players:
        tg_id = player.get("tg_id")
        first_name = player.get("first_name")
        role = roles_map.get(tg_id)

        if tg_id == don_id:
            continue
        
        if role == "mafia":
            continue
        elif role == "spy":
            text = f"🦇 {first_name}"
        elif role == "adv":
            text = f"👨🏻‍💻 {first_name}"
        else:
            text = first_name

        builder.add(
            InlineKeyboardButton(
                text=text,
                callback_data=f"don_{tg_id}_{game_id}_{chat_id}_{day}"
            )
        )
    builder.add(
        InlineKeyboardButton(
            text="🚷 ",
            callback_data=f"don_no_{game_id}_{chat_id}_{day}"
    ))

    builder.adjust(1)
    return builder.as_markup()


def mafia_inline_btn(players, game_id,day=None):
    builder = InlineKeyboardBuilder()

    roles_map = games_state.get(int(game_id), {}).get("roles", {})

    for player in players:
        tg_id = player.get("tg_id")
        first_name = player.get("first_name")
        role = roles_map.get(tg_id)

        
        
        if role == "mafia":
            continue
        elif role == "don":
            continue
        elif role == "spy":
            text = f"🦇 {first_name}"
        elif role == "adv":
            text = f"👨🏻‍💻 {first_name}"
        else:
            text = first_name

        builder.add(
            InlineKeyboardButton(
                text=text,
                callback_data=f"mafia_{tg_id}_{game_id}_{day}"
            )
        )
    builder.add(
        InlineKeyboardButton(
            text="🚷 ",
            callback_data=f"mafia_no_{game_id}_{day}"
    ))
    builder.adjust(1)
    return builder.as_markup()


def adv_inline_btn(players,  game_id, chat_id,day=None):
    builder = InlineKeyboardBuilder()
    roles_map = games_state.get(int(game_id), {}).get("roles", {})
    for player in players:
        tg_id = player.get("tg_id")
        first_name = player.get("first_name")
        role = roles_map.get(tg_id)
        if role not in ["don", "mafia"]:
            continue
        if role == "don":
            text = f"🤵🏻 {first_name}"
        else:
            text = f"🤵🏼 {first_name}"
        builder.add(
            InlineKeyboardButton(
                text=text,
                callback_data=f"adv_{tg_id}_{game_id}_{chat_id}_{day}"
            )
        )
    builder.add(
        InlineKeyboardButton(
            text="🚷 ",
            callback_data=f"adv_no_{game_id}_{chat_id}_{day}"
    ))

    builder.adjust(1)
    return builder.as_markup()




def hang_inline_btn(players, own_id, game_id, chat_id,day=None):
    builder = InlineKeyboardBuilder()

    for tg_id, first_name in players.values():
        if tg_id == own_id:
            continue
        text = first_name
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"hang_{tg_id}_{game_id}_{chat_id}_{day}"
        )
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup()





def language_keyboard():
    builder = InlineKeyboardBuilder()
    languages = [
        ("uz", "🇺🇿 O'zbekcha"),
        ("ru", "🇷🇺 Русский"),
        ("en", "🇬🇧 English"),
        ("tr", "🇹🇷 Türkçe"),
        ("qz", "🇰🇿 Қазақша"),
    ]
    for code, name in languages:
        builder.add(
            InlineKeyboardButton(
                text=name,
                callback_data=f"lang_{code}"
            )
        )
    builder.adjust(1)
    return builder.as_markup()