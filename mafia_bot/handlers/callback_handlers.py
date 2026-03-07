from aiogram import F
from dispatcher import dp, bot
from django.db.models import Sum
from aiogram.fsm.context import FSMContext 
from mafia_bot.utils import games_state,USER_LANG_CACHE
from aiogram.types import CallbackQuery
from mafia_bot.models import   User,PremiumGroup,MostActiveUser, UserRole
from mafia_bot.handlers.main_functions import (add_visit, get_mafia_members,get_first_name_from_players,  send_safe_message,get_description_lang,
                                               mark_confirm_done, mark_hang_done,mark_night_action_done,get_lang_text,get_role_labels_lang,get_actions_lang)
from mafia_bot.buttons.inline import (
       cart_inline_btn,  com_inline_btn,     
       language_keyboard,   pay_for_money_inline_btn,  role_shop_inline_keyboard,
    shop_inline_btn, start_inline_btn, roles_inline_btn, com_inline_action_btn,
    confirm_hang_inline_btn)




# Callbackdan kelganda
@dp.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    await callback.answer()
    tg_id = callback.from_user.id
    user = User.objects.filter(telegram_id=tg_id).first()
    if not user:
        user = User.objects.create(
            telegram_id=tg_id,
            lang ='uz',
            first_name=callback.from_user.first_name,
            username=callback.from_user.username
        )
    t = get_lang_text(int(tg_id))
    user_role = UserRole.objects.filter(user_id=user.id)
    text =""
    for user_r in user_role:
        role_name = dict(get_role_labels_lang(tg_id)).get(user_r.role_key, "Noma'lum rol")
        text += f"🎭 {role_name} -  {user_r.quantity}\n"
    result = MostActiveUser.objects.filter(user_id=user.id).aggregate(
    total_played=Sum('games_played'),
    total_wins=Sum('games_win')
    )

    total_played = result['total_played'] or 0
    total_wins = result['total_wins'] or 0

    await callback.message.edit_text(
        text=t['user_profile'].format(
            first_name=callback.from_user.first_name,
            coin=user.coin,
            stones=user.stones,
            protection=user.protection,
            hang_protect=user.hang_protect,
            docs=user.docs,
            geroy_protect=user.geroy_protection,
            wins=total_wins,
            all_played=total_played,
            text=text
        ),
        parse_mode="HTML",reply_markup=cart_inline_btn(tg_id)
    )

@dp.callback_query(F.data == "cart")
async def cart_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(
        reply_markup=shop_inline_btn(callback.from_user.id)
    )


@dp.callback_query(F.data == ("roles_back_main"))
async def back_callback_special(callback: CallbackQuery):
    t = get_lang_text(callback.from_user.id)
    await callback.message.edit_text(
    text=t['greating_message'],
    parse_mode="HTML",
    reply_markup=start_inline_btn(callback.from_user.id)
)
    
@dp.callback_query(F.data == ("language"))
async def language_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text = "Language / Tilni tanlang / Выберите язык / Dil seçin:",
        reply_markup=language_keyboard()
    )
    
   
# Callbackdan kelganda
@dp.callback_query(F.data.startswith("back_"))
async def back_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    place = callback.data.split("_")[1]
    t = get_lang_text(callback.from_user.id)
    if place== "profile":
        await profile_callback(callback)
    elif place == "money":
        button = pay_for_money_inline_btn(callback.from_user.id,is_money=True)
        await callback.message.edit_text(
            text=t['payment_method_choose'],
            reply_markup=button
        )
    elif place == "stone":
        button = pay_for_money_inline_btn(callback.from_user.id,is_money=False)
        await callback.message.edit_text(
            text=t['payment_method_choose'],
            reply_markup=button
        )
    


# Callbackdan kelganda
@dp.callback_query(F.data.startswith("buy_"))
async def buy_callback(callback: CallbackQuery):
    thing_to_buy = callback.data.split("_")[1]
    price = callback.data.split("_")[2]
    tg_id = callback.from_user.id
    user = User.objects.filter(telegram_id=callback.from_user.id).first()
    result = MostActiveUser.objects.filter(user_id=user.id).aggregate(
    total_played=Sum('games_played'),
    total_wins=Sum('games_win')
)

    total_played = result['total_played'] or 0
    total_wins = result['total_wins'] or 0

    if not user:
        user = User.objects.create(
            telegram_id=callback.from_user.id,
            lang ='uz',
            first_name=callback.from_user.first_name,
            username=callback.from_user.username
        )
    t = get_lang_text(tg_id)
    if thing_to_buy == "protection":
        if user.coin >= 250:
            user.coin -= 250
            user.protection += 1
            user.save()
            await callback.message.edit_text(
                 text=t['user_profile'].format(
                first_name=callback.from_user.first_name,
                coin=user.coin,
                stones=user.stones,
                protection=user.protection,
                hang_protect=user.hang_protect,
                docs=user.docs,
                geroy_protect=user.geroy_protection,
                wins=total_wins,
                all_played=total_played,
                text=""
            ),
                parse_mode="HTML",
                reply_markup=cart_inline_btn(tg_id)
            )
        else:
            await callback.answer(text=t['not_enough_money'], show_alert=True)
    elif thing_to_buy == "docs":
        if user.coin >= 250:
            user.coin -= 250
            user.docs += 1
            user.save()
            await callback.message.edit_text(
                text=t['user_profile'].format(
                    first_name=callback.from_user.first_name,
                    coin=user.coin,
                    stones=user.stones,
                    protection=user.protection,
                    hang_protect=user.hang_protect,
                    wins=total_wins,
                    all_played=total_played,
                    docs=user.docs,
                    geroy_protect=user.geroy_protection,
                    text=""
                ),
                parse_mode="HTML",
                reply_markup=cart_inline_btn(tg_id)
            )
        else:
            await callback.answer(text=t['not_enough_money'], show_alert=True)
    elif thing_to_buy == "hangprotect":
        if price == "1" and user.coin >= 20000:
            user.coin -= 20000
            user.hang_protect += 1
            user.save()
        elif price == "2" and user.stones >= 20:
            user.stones -= 20
            user.hang_protect += 1
            user.save()
        else:
            await callback.answer(text=t['not_enough_money'], show_alert=True)
            return
        await callback.message.edit_text(
                text=t['user_profile'].format(
                    first_name=callback.from_user.first_name,
                    coin=user.coin,
                    stones=user.stones,
                    protection=user.protection,
                    hang_protect=user.hang_protect,
                    docs=user.docs,
                    geroy_protect=user.geroy_protection,
                    wins=total_wins,
                    all_played=total_played,
                    text=""
                ),
                parse_mode="HTML",
                reply_markup=cart_inline_btn(tg_id)
            )
    elif thing_to_buy == "activerole":
        await callback.message.edit_text(
            text=t['buy_role'],
            reply_markup=role_shop_inline_keyboard(tg_id)
        )
    elif thing_to_buy == "geroyprotect":
        if user.coin >= 10000:
            user.coin -= 10000
            user.geroy_protection += 1
            user.save()
            await callback.message.edit_text(
                text=t['user_profile'].format(
                    first_name=callback.from_user.first_name,
                    coin=user.coin,
                    stones=user.stones,
                    protection=user.protection,
                    hang_protect=user.hang_protect,
                    docs=user.docs,
                    geroy_protect=user.geroy_protection,
                    wins=total_wins,
                    all_played=total_played,
                    text=""
                ),
                parse_mode="HTML",
                reply_markup=cart_inline_btn(tg_id)
            )
        else:
            await callback.answer(text=t['not_enough_money'], show_alert=True)

@dp.callback_query(F.data.startswith("active_"))
async def buy_role_callback(call: CallbackQuery, state: FSMContext):
    
    role_key = call.data.split("_")[1]
    price = int(call.data.split("_")[2])
    
    if price<75:
        currency = "stones"
    else:
        currency = "money"

    user = User.objects.filter(telegram_id=call.from_user.id).first()
    if not user:
        user = User.objects.create(
            telegram_id=call.from_user.id,
            lang ='uz',
            first_name=call.from_user.first_name,
            username=call.from_user.username
        )
    t = get_lang_text(call.from_user.id)
    if currency == "stones":
        if user.stones < price:
            return await call.answer(t['not_enough_stones'], show_alert=True)
        user.stones -= price

    if currency == "money":
        if user.coin < price:
            return await call.answer(t['not_enough_money'], show_alert=True)
        user.coin -= price

    await user.asave(update_fields=["stones", "coin"])
    user_role, created = UserRole.objects.get_or_create(user=user, role_key=role_key)
    if not created:
        user_role.quantity += 1
    user_role.save()

    await call.answer(t['role_bought'], show_alert=True)

    await call.message.edit_text(
        text=t['role_bought'] + "\n\n" + t['buy_another_role'],
        reply_markup=role_shop_inline_keyboard(call.from_user.id)
    )

    

# Callbackdan kelganda
@dp.callback_query(F.data == ("role_menu"))
async def roles_callback(callback: CallbackQuery):
    await callback.answer()
    t = get_lang_text(callback.from_user.id)
    await callback.message.edit_text(t['roles_list'],reply_markup=roles_inline_btn(callback.from_user.id))


@dp.callback_query(F.data.startswith("money_"))
async def buy_money_handler(callback: CallbackQuery):
    await callback.answer()
    t = get_lang_text(callback.from_user.id)
    if callback.data == "money_stone":
        button = pay_for_money_inline_btn(callback.from_user.id, is_money=False)
    else:
        button = pay_for_money_inline_btn(callback.from_user.id, is_money=True)
    await callback.message.edit_text(
        text=t['payment_method_choose'],
        reply_markup=button
    )
    

        

    
    


@dp.callback_query(F.data.startswith("roles_"))
async def roles_specific_callback(callback: CallbackQuery):
    role_name = callback.data.split("_")[1]
    DESCRIPTIONS = get_description_lang(callback.from_user.id)
    if role_name in DESCRIPTIONS:
        await callback.answer(text=DESCRIPTIONS[role_name], show_alert=True)


@dp.callback_query(F.data.startswith("doc_"))
async def doc_heal_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)

    parts = callback.data.split("_")    
    target_id = parts[1]  
    chat_id = int(parts[3])
    day = parts[4]
    doctor_id = callback.from_user.id

    game = games_state.get(int(parts[2]))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('doc_heal')}\n\n{t['late']}", parse_mode="HTML")
        return
    if not doctor_id in game["alive"]:
        return
    
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('doc_heal')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        try:
            await send_safe_message(
            chat_id=chat_id,
            text=tg['no_go_doc']
        )
        except:
            pass
        return
    
    target_id = int(target_id)
    # doc o'zini 1 martadan ko'p heal qila olmaydi
    if target_id == doctor_id:
        used_self = game["limits"]["doc_self_heal_used"]
        if doctor_id in used_self:
            return
        used_self.add(doctor_id)

    # ✅ night action saqlash
    game["night_actions"]["doc_target"] = target_id
    add_visit(game=game, visitor_id=doctor_id, house_id=target_id, invisible=False)


    # username olish (players object bo'lsa)
    target_name = get_first_name_from_players(target_id)

    text = f"{get_actions_lang(callback.from_user.id).get('doc_heal')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}"

    await callback.message.edit_text(text=text, parse_mode="HTML")
    try:
        await send_safe_message(
            chat_id=chat_id,
            text=tg['go_doc']
        )
    except:
        pass
    

@dp.callback_query(F.data.startswith("daydi_"))
async def daydi_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)

    parts = callback.data.split("_")
    house_id = parts[1]
    chat_id = int(parts[3])
    day = parts[4]

    daydi_id = callback.from_user.id

    game = games_state.get(int(parts[2]))
    if not game:
        return
    
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('daydi_watch')}\n\n{t['late']}", parse_mode="HTML")
        return
    if not daydi_id in game["alive"]:
        return
    mark_night_action_done(game, callback.from_user.id)
    if house_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('daydi_watch')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        try:
            await send_safe_message(
                chat_id=chat_id,
                text=tg['daydi_no_go']
            )
        except:
            pass
        return
    house_id = int(house_id)

    # ✅ Daydi qayerga bordi
    game["night_actions"]["daydi_house"] = house_id
    

    # username topish (players object list bo‘lsa)
    target_name = get_first_name_from_players(house_id)
    await callback.message.edit_text(
        text=f"{get_actions_lang(callback.from_user.id).get('daydi_watch')}\n\n<a href='tg://user?id={house_id}'>{target_name}</a> {t['action_choose']}",
        parse_mode="HTML"
    )
    try:
        await send_safe_message(chat_id=chat_id, text=tg['daydi_go'])
    except:
        pass
    


@dp.callback_query(F.data.startswith("com_"))
async def com_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)

    parts = callback.data.split("_")
    action = parts[1]     
    chat_id = int(parts[3])
    day = parts[4]
    com_id = callback.from_user.id
    game = games_state.get(int(parts[2]))
    if not game:
        return
    if not com_id in game["alive"]:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('com_deside')}\n\n{t['late']}", parse_mode="HTML")
        return
    mark_night_action_done(game, callback.from_user.id)
    if action == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('com_deside')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        try:
            await send_safe_message(
                chat_id=chat_id,
                text=tg['com_no_go']
            )
        except:
            pass
        return
    elif action == "back":
        await callback.message.edit_text(
            text=get_actions_lang(callback.from_user.id).get("com_deside"),
            reply_markup=com_inline_btn(game_id=int(parts[2]), chat_id=chat_id,day=day)
        )
        return
    
    if action == "shoot":
        try:
            await send_safe_message(chat_id=chat_id, text=tg['com_shoot'])
        except:
            pass
        await callback.message.edit_text(
            text=get_actions_lang(callback.from_user.id).get("com_shoot"),
            reply_markup=com_inline_action_btn(action="shoot",chat_id=chat_id, game_id=int(parts[2]),com_id=com_id,day=day)
        )
        return

    try:
        await send_safe_message(chat_id=chat_id, text=tg['com_check'])
    except:
        pass
    await callback.message.edit_text(
        text=get_actions_lang(callback.from_user.id).get("com_check"),
        reply_markup=com_inline_action_btn(action="search",chat_id=chat_id, game_id=int(parts[2]),com_id=com_id,day=day)
    )


@dp.callback_query(F.data.startswith("shoot_"))
async def com_shoot_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)

    parts = callback.data.split("_")
    target_id = int(parts[1])

    com_id = callback.from_user.id

    game = games_state.get(int(parts[2]))
    day = parts[3]
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{t.get('com_shoot')}\n\n{t['late']}", parse_mode="HTML")
        return
    if not com_id in game["alive"]:
        return
    

    game["night_actions"]["com_shoot_target"] = target_id
    add_visit(game, com_id, target_id, False)


    target_name = get_first_name_from_players( target_id)

    await callback.message.edit_text(
        text=f"{get_actions_lang(callback.from_user.id).get('com_shoot')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}.",
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("search_"))
async def com_protect_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)

    parts = callback.data.split("_")
    target_id = int(parts[1])
    day = parts[3]
    com_id = callback.from_user.id

    game = games_state.get(int(parts[2]))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('com_check')}\n\n{t['late']}", parse_mode="HTML")
        return
    if not com_id in game["alive"]:
        return
   

    # ✅ Action saqlaymiz
    game["night_actions"]["com_check_target"] = target_id
    add_visit(game, com_id, target_id, False)


    target_name = get_first_name_from_players( target_id)

    await callback.message.edit_text(
        text=f"{get_actions_lang(callback.from_user.id).get('com_check')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}.",
        parse_mode="HTML"
    )

    
@dp.callback_query(F.data.startswith("lover_"))
async def lover_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)

    parts = callback.data.split("_")
    target_id = parts[1]
    chat_id = int(parts[3])
    day = parts[4]
    lover_id = callback.from_user.id

    game = games_state.get(int(parts[2]))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('lover_block')}\n\n {t['late']}", parse_mode="HTML")
        return
    if not lover_id in game["alive"]:
        return
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('lover_block')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        try:
            await send_safe_message(
                chat_id=chat_id,
                text=tg['lover_no_go']
            )
        except:
            pass
        return
    target_id = int(target_id)
    # ✅ lover action saqlash
    game["night_actions"]["lover_block_target"] = target_id
    add_visit(game=game, visitor_id=lover_id, house_id=target_id, invisible=False)

    target_name = get_first_name_from_players(target_id)

    text = f"{get_actions_lang(callback.from_user.id).get('lover_block')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}."

    await callback.message.edit_text(text=text, parse_mode="HTML")

    await send_safe_message(
        chat_id=chat_id,
        text=tg['lover_go']
    )
    return

@dp.callback_query(F.data.startswith("killer_"))
async def killer_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)

    parts = callback.data.split("_")
    target_id = parts[1]
    chat_id = int(parts[3])
    day = parts[4]
    killer_id = callback.from_user.id

    game = games_state.get(int(parts[2]))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('killer_kill')}\n\n{t['late']}", parse_mode="HTML")
        return
    if not killer_id in game["alive"]:
        return
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('killer_kill')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=chat_id,
            text=tg['killer_no_go']
        )
        return
    target_id = int(target_id)
    # ✅ killer action saqlash
    game["night_actions"]["killer_target"].append(target_id)

    target_name = get_first_name_from_players(target_id)
    add_visit(game=game, visitor_id=killer_id, house_id=target_id, invisible=False)

    text = f"{get_actions_lang(callback.from_user.id).get('killer_kill')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}."

    await callback.message.edit_text(text=text, parse_mode="HTML")

    await send_safe_message(
        chat_id=chat_id,
        text=tg['killer_go']
    )
    return

@dp.callback_query(F.data.startswith("santa_"))
async def santa_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)

    parts = callback.data.split("_")
    target_id = parts[1]
    chat_id = int(parts[3])
    day = parts[4]
    santa_id = callback.from_user.id

    game = games_state.get(int(parts[2]))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('santa')}\n\n{t['late']}", parse_mode="HTML")
        return
    if not santa_id in game["alive"]:
        return
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('santa')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=chat_id,
            text=tg['santa_no_go']
        )
        return
    target_id = int(target_id)
    # ✅ killer action saqlash
    user = User.objects.filter(telegram_id=target_id).first()
    if not user:
        user = User.objects.create(
            telegram_id=target_id,
            lang ='uz',
            first_name=callback.from_user.first_name,
            username=callback.from_user.username
        )
    user.coin += 20
    user.save()
    target_name = get_first_name_from_players(target_id)
    add_visit(game=game, visitor_id=santa_id, house_id=target_id, invisible=False)

    text = f"{get_actions_lang(callback.from_user.id).get('santa')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}."

    await callback.message.edit_text(text=text, parse_mode="HTML")
    await send_safe_message(
        chat_id=target_id,
        text=t['santa_gift']
    )
    await send_safe_message(
        chat_id=chat_id,
        text=tg['santa_go']
    )
    return

@dp.callback_query(F.data.startswith("kaldun_"))
async def kaldun_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)

    parts = callback.data.split("_")
    target_id = parts[1]
    chat_id = int(parts[3])
    day = parts[4]
    kaldun_id = callback.from_user.id

    game = games_state.get(int(parts[2]))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('kaldun_spell')}\n\n{t['late']}", parse_mode="HTML")
        return
    if not kaldun_id in game["alive"]:
        return
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('kaldun_spell')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=chat_id,
            text=tg['kaldun_no_go']
        )
        return

    target_id = int(target_id)

    # ✅ kaldun action saqlash
    game["night_actions"]["kaldun_target"] = target_id
    
    add_visit(game=game, visitor_id=kaldun_id, house_id=target_id, invisible=False)
    target_name = get_first_name_from_players(target_id)

    text = f"{get_actions_lang(callback.from_user.id).get('kaldun_spell')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}."

    await callback.message.edit_text(text=text, parse_mode="HTML")

    await send_safe_message(
        chat_id=chat_id,
        text=tg["kaldun_go"]
    )
    return


@dp.callback_query(F.data.startswith("drunk_"))
async def drunk_callback(callback: CallbackQuery):
    await callback.answer()

    parts = callback.data.split("_")
    target_raw = parts[1]
    game_id = int(parts[2])
    chat_id = int(parts[3])
    day = parts[4]
    drunk_id = callback.from_user.id

    game = games_state.get(game_id)
    if not game:
        return
    t = get_lang_text(drunk_id)
    tu = get_lang_text(chat_id)
    if day != str(game['meta']['day']):
        await callback.message.edit_text(
            f"{get_actions_lang(drunk_id).get('drunk_action')}\n\n{t['late']}",
            parse_mode="HTML"
        )
        return

    if drunk_id not in game["alive"]:
        return

    mark_night_action_done(game, drunk_id)
    await callback.message.edit_reply_markup(None)

    if target_raw == "no":
        await callback.message.edit_text(
            f"{get_actions_lang(drunk_id).get('drunk_action')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=chat_id,
            text=tu['drunk_no_go']
        )
        return

    target_id = int(target_raw)

    # 🔒 GAME LOGIC — O‘ZGARMAGAN
    game["night_actions"]["drunk_target"] = target_id
    add_visit(game=game, visitor_id=drunk_id, house_id=target_id, invisible=False)

    target_name = get_first_name_from_players(target_id)

    await send_safe_message(
        chat_id=chat_id,
        text=tu['drunk_go']
    )

    await callback.message.edit_text(
        f"{get_actions_lang(drunk_id).get('drunk_action')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}.",
        parse_mode="HTML"
    )


@dp.callback_query(F.data.startswith("don_"))
async def don_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = callback.data.split("_")[2]
    day = callback.data.split("_")[4]
    
    don_id = callback.from_user.id
    
    game = games_state.get(int(game_id))
    
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('don_kill')}\n\n{t['late']}", parse_mode="HTML")
        return
    
    if not don_id in game["alive"]:
        return
    
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('don_kill')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        
        return
    
    # ✅ night action saqlash
    game["night_actions"]["don_kill_target"] = int(target_id)
    add_visit(game=game, visitor_id=don_id, house_id=target_id, invisible=False)
    
    
    target_name = get_first_name_from_players(int(target_id))
    mafia_name = get_first_name_from_players(don_id)
    mafia_members = get_mafia_members(int(game_id))
    

    text_for_mafia = (
        f"🤵🏻 Don <a href='tg://user?id={don_id}'>{mafia_name}</a> - <a href='tg://user?id={target_id}'>{target_name}</a> uchun ovoz berdi"
    )

    for member_id in mafia_members:
        if member_id == don_id:
            continue
        try:
            await send_safe_message(
                chat_id=member_id,
                text=text_for_mafia,
                parse_mode="HTML"
            )
        except Exception as e:
            pass
    
    await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('don_kill')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}")
    

@dp.callback_query(F.data.startswith("mafia_"))
async def mafia_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = callback.data.split("_")[2]
    day = callback.data.split("_")[3]
    
    mafia_id = callback.from_user.id
    
    game = games_state.get(int(game_id))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('mafia_vote')}\n\n{t['late']}", parse_mode="HTML")
        return
    
    if not mafia_id in game["alive"]:
        return
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('mafia_vote')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        return
    # ✅ night action saqlash
    game["night_actions"]["mafia_vote"].append(int(target_id))
    
    
    target_name = get_first_name_from_players(int(target_id))
    mafia_name = get_first_name_from_players(mafia_id)
    mafia_members = get_mafia_members(int(game_id))
    

    text_for_mafia = (
        f"🤵🏼 Mafiya a'zosi <a href='tg://user?id={mafia_id}'>{mafia_name}</a> - <a href='tg://user?id={target_id}'>{target_name}</a> uchun ovoz berdi"
    )

    for member_id in mafia_members:
        if member_id == mafia_id:
            continue

        try:
            await send_safe_message(
                chat_id=member_id,
                text=text_for_mafia,
                parse_mode="HTML"
            )
        except Exception as e:
            pass
    
    await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('mafia_vote')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}")


@dp.callback_query(F.data.startswith("adv_"))
async def adv_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = int(callback.data.split("_")[2])
    chat_id = int(callback.data.split("_")[3])
    day = callback.data.split("_")[4]
    adv_id = callback.from_user.id
    
    game = games_state.get(int(game_id))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('adv_mask')}\n {t['late']}", parse_mode="HTML")
        return
    
    if not adv_id in game["alive"]:
        return
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('adv_mask')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=int(chat_id),
            text=tg['adv_no_go']
        )
        return
    # ✅ night action saqlash
    game["night_actions"]["advokat_target"] = int(target_id)
    add_visit(game=game, visitor_id=adv_id, house_id=target_id, invisible=False)
    
    await send_safe_message(
        chat_id=int(chat_id),
        text=tg['adv_go'],
    )
    
    target_name = get_first_name_from_players(int(target_id))
    adv_name = get_first_name_from_players(adv_id)
    mafia_members = get_mafia_members(int(game_id))
    

    text_for_mafia = (
        f"👨🏼‍💼 Advokat {adv_name} tanlovi: <a href='tg://user?id={target_id}'>{target_name}</a>"
    )

    for member_id in mafia_members:
        if member_id == adv_id:
            continue

        try:
            await send_safe_message(
                chat_id=member_id,
                text=text_for_mafia,
                parse_mode="HTML"
            )
        except Exception as e:
            pass
    

    await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('adv_mask')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}")


@dp.callback_query(F.data.startswith("spy_"))
async def spy_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = callback.data.split("_")[2]
    chat_id = int(callback.data.split("_")[3])
    day = callback.data.split("_")[4]
    spy_id = callback.from_user.id
    
    game = games_state.get(int(game_id))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('spy_check')}\n\n{t['late']}", parse_mode="HTML")
        return
    
    if not spy_id in game["alive"]:
        return
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('spy_check')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=int(chat_id),
            text=tg['spy_no_go']
        )
        return
    
    # ✅ night action saqlash
    game["night_actions"]["spy_target"] = int(target_id)
    add_visit(game=game, visitor_id=spy_id, house_id=target_id, invisible=False)
    
    await send_safe_message(
        chat_id=int(chat_id),
        text=tg['spy_go'],
    )
    
    target_name = get_first_name_from_players(int(target_id))
    spy_name = get_first_name_from_players(spy_id)
    mafia_members = get_mafia_members(int(game_id))
    text_for_mafia = (
        f"🦇 Ayg'oqchi {spy_name} tanlovi: <a href='tg://user?id={target_id}'>{target_name}</a>"
    )
    for member_id in mafia_members:
        if member_id == spy_id:
            continue

        try:
            await send_safe_message(
                chat_id=member_id,
                text=text_for_mafia,
                parse_mode="HTML"
            )
        except Exception as e:
            pass
    
    
    await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('spy_check')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}")


@dp.callback_query(F.data.startswith("lab_"))
async def lab_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = int(callback.data.split("_")[2])
    chat_id = int(callback.data.split("_")[3])
    day = callback.data.split("_")[4]
    
    lab_id = callback.from_user.id
    
    game = games_state.get(int(game_id))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('lab_action')}\n\n{t['late']}", parse_mode="HTML")
        return
    
    if not lab_id in game["alive"]:
        return
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('lab_action')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=int(chat_id),
            text=tg['lab_no_go']
        )
        return
    
    # ✅ night action saqlash
    game["night_actions"]["lab_target"] = int(target_id)
    add_visit(game=game, visitor_id=lab_id, house_id=target_id, invisible=False)
    
    await send_safe_message(
        chat_id=int(chat_id),
        text=tg['lab_go'],
    )
    
    target_name = get_first_name_from_players(int(target_id))
    
    await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('lab_action')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}")


@dp.callback_query(F.data.startswith("arrow_"))
async def arrow_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = callback.data.split("_")[2]
    chat_id = int(callback.data.split("_")[3])
    day = callback.data.split("_")[4]
    
    arrow_id = callback.from_user.id
    
    game = games_state.get(int(game_id))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('arrow_kill')}\n\n{t['late']}", parse_mode="HTML")
        return
    
    if not arrow_id in game["alive"]:
        return
    
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('arrow_kill')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=int(chat_id),
            text=tg['arrow_no_go']
        )   
        return
    # ✅ night action saqlash
    game["night_actions"]["arrow_target"] = int(target_id)
    add_visit(game=game, visitor_id=arrow_id, house_id=target_id, invisible=True)
    
    await send_safe_message(
        chat_id=int(chat_id),
        text=tg['arrow_go'],
    )
    
    target_name = get_first_name_from_players(int(target_id))
    
    await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('arrow_kill')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}")


@dp.callback_query(F.data.startswith("trap_"))
async def trap_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = callback.data.split("_")[2]
    chat_id = int(callback.data.split("_")[3])
    day = callback.data.split("_")[4]
    
    trap_id = callback.from_user.id
    
    game = games_state.get(int(game_id))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('trap_place')}\n\n{t['late']}", parse_mode="HTML")
        return
    
    if not trap_id in game["alive"]:
        return
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('trap_place')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=int(chat_id),
            text=tg['trap_no_go']
        )
        return
    
    # ✅ night action saqlash
    game["night_actions"]["trap_house"] = int(target_id)
    
    await send_safe_message(
        chat_id=int(chat_id),
        text=tg['trap_go'],
    )
    
    target_name = get_first_name_from_players(int(target_id))
    
    await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('trap_place')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}")


@dp.callback_query(F.data.startswith("snyper_"))
async def snyper_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = callback.data.split("_")[2]
    chat_id = int(callback.data.split("_")[3])
    day = callback.data.split("_")[4]
    
    snyper_id = callback.from_user.id
    
    game = games_state.get(int(game_id))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('snyper_kill')}\n\n{t['late']}", parse_mode="HTML")
        return
    
    if not snyper_id in game["alive"]:
        return
    
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('snyper_kill')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=int(chat_id),
            text=tg['snyper_no_go']
        )   
        return
    
    # ✅ night action saqlash
    game["night_actions"]["snyper_target"] = int(target_id)
    add_visit(game=game, visitor_id=snyper_id, house_id=target_id, invisible=True)
    
    await send_safe_message(
        chat_id=int(chat_id),
        text=tg['snyper_go']
    )
    
    target_name = get_first_name_from_players(int(target_id))
    
    await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('snyper_kill')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}")



@dp.callback_query(F.data.startswith("traitor_"))
async def spy_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = callback.data.split("_")[2]
    chat_id = int(callback.data.split("_")[3])
    day = callback.data.split("_")[4]
    
    traitor_id = callback.from_user.id
    game = games_state.get(int(game_id))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('traitor_choose')}\n\n{t['late']}", parse_mode="HTML")
        return
    if not traitor_id in game["alive"]:
        return
    
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('traitor_choose')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=int(chat_id),
            text=tg['traitor_no_go']
        )
        return
    
    # ✅ night action saqlash
    game["night_actions"]["traitor_target"] = int(target_id)
    add_visit(game=game, visitor_id=traitor_id, house_id=target_id, invisible=False)
    await send_safe_message(
        chat_id=int(chat_id),
        text=tg['traitor_go']
    )
    target_name = get_first_name_from_players(int(target_id))
    await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('traitor_choose')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}")
    


@dp.callback_query(F.data.startswith("snowball_"))
async def snowball_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = callback.data.split("_")[2]
    chat_id = int(callback.data.split("_")[3])
    day = callback.data.split("_")[4]
    
    snowball_id = callback.from_user.id
    game = games_state.get(int(game_id))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('snowball_kill')}\n\n{t['late']}", parse_mode="HTML")
        return
    if not snowball_id in game["alive"]:
        return
    
    mark_night_action_done(game, callback.from_user.id)
    if target_id == "no":
        # hech narsa qilmaslik
        await callback.message.edit_text(
            text=f"{get_actions_lang(callback.from_user.id).get('snowball_kill')}\n\n{t['action_no_choose']}",
            parse_mode="HTML"
        )
        await send_safe_message(
            chat_id=int(chat_id),
            text=tg['snowball_no_go']
        )
        return
    
    # ✅ night action saqlash
    game["night_actions"]["snowball_target"] = int(target_id)
    add_visit(game=game, visitor_id=snowball_id, house_id=target_id, invisible=False)
    await send_safe_message(
        chat_id=int(chat_id),
        text=tg['snowball_go']
    )
    target_name = get_first_name_from_players(int(target_id))
    await callback.message.edit_text(text=f"{get_actions_lang(callback.from_user.id).get('snowball_kill')}\n\n<a href='tg://user?id={target_id}'>{target_name}</a> {t['action_choose']}")



    

@dp.callback_query(F.data.startswith("hang_"))
async def hang_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    target_id = callback.data.split("_")[1]
    game_id = callback.data.split("_")[2]
    chat_id = int(callback.data.split("_")[3])
    day = callback.data.split("_")[4]
    shooter_id = callback.from_user.id
    shooter_name = callback.from_user.first_name
    game = games_state.get(int(game_id))
    if not game:
        return
    game_day = game['meta']['day']
    t = get_lang_text(callback.from_user.id)
    tg= get_lang_text(chat_id)
    if not day == str(game_day):
        await callback.message.edit_text(text=f"{t['hang_action']}\n\n{t['late']}", parse_mode="HTML")
        return
    if target_id == "no":
        await callback.message.edit_text(text=f"{t['hang_action']}\n\n{t['action_no_choose']}", parse_mode="HTML")
        await send_safe_message(
            chat_id=chat_id,
            text=f"🚷 <a href='tg://user?id={shooter_id}'>{shooter_name}</a> {tg['no_hang_choose']}"
        )
        game["day_actions"]['votes'].append("no_lynch")
        return
    
    game["day_actions"]['votes'].append(int(target_id))
    mark_hang_done(int(game_id), callback.from_user.id)
    
    user_map = game.get("users_map",{})
    user = user_map.get(int(target_id))
    await callback.message.edit_text(text=f"{t['hang_action']}\n\n<a href='tg://user?id={target_id}'>{user.get('first_name')}</a> {t['action_choose']}", parse_mode="HTML")
    await send_safe_message(
        chat_id=chat_id,
        text=f"<a href='tg://user?id={shooter_id}'>{shooter_name}</a> -> <a href='tg://user?id={target_id}'>{user.get('first_name')}</a> {tg['hang_choose']}"
    )

        
@dp.callback_query(F.data.startswith("con_"))
async def confirm_callback(callback: CallbackQuery):
    parts = callback.data.split("_")
    confirmation = str(parts[1])
    target_id = int(parts[2])
    game_id = int(parts[3])
    chat_id = int(parts[4])
    voter_id = callback.from_user.id
    game = games_state.get(int(game_id))
    if not game:
        return
    t = get_lang_text(callback.from_user.id)
    if not voter_id in game["alive"]:
        if voter_id in game["dead"]:
            await callback.answer(text=t['dead_cant_vote'])
            return
        if voter_id not in game["players"]:
            await callback.answer(text=t['no_player'])
        return
    if target_id == voter_id:
        await callback.answer(text=t['cant_vote_self'])
        return
    if voter_id == game["night_actions"]["lover_block_target"]:
        await callback.answer(text=t['lover_waiting'])
        return
    
    if not target_id in game["alive"]:
        return
    if confirmation == "yes":
        if voter_id not in game["day_actions"]["hang_yes"]:
            game["day_actions"]["hang_yes"].append(voter_id)
        else:
            game["day_actions"]["hang_yes"].remove(voter_id)
        if voter_id in game["day_actions"]["hang_no"]:
            game["day_actions"]["hang_no"].remove(voter_id)
        
    else:
        if voter_id not in game["day_actions"]["hang_no"]:
            game["day_actions"]["hang_no"].append(voter_id)
        else:
            game["day_actions"]["hang_no"].remove(voter_id)
        if voter_id in game["day_actions"]["hang_yes"]:
            game["day_actions"]["hang_yes"].remove(voter_id)
    
    mark_confirm_done(int(game_id), voter_id)
    
    
    await callback.answer(text=t['vote_accepted'])
    yes = len(game["day_actions"]["hang_yes"])
    no = len(game["day_actions"]["hang_no"])
    
    await update_hang_votes(voter_id=target_id,game_id=int(game_id),chat_id=chat_id,yes=yes,no=no)
    
    
async def update_hang_votes(voter_id,game_id: int, chat_id: int, yes: int, no: int):
    game = games_state.get(int(game_id))
    if not game:
        return
    msg_id = game['day_actions']['hang_confirm_msg_id']
    try:
        await bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=msg_id,
        reply_markup=confirm_hang_inline_btn(voted_user_id=voter_id,game_id=int(game_id),chat_id=chat_id,yes=yes,no=no)
    )
    except Exception as e:
        pass
    



    
    
    
    
    




def set_user_lang(callback, lang: str):
    tg_id = callback.from_user.id
    username = callback.from_user.username
    first_name = callback.from_user.first_name
    
    User.objects.update_or_create(
        telegram_id=tg_id,
        defaults={"lang": lang,
                  "username": username,
                  "first_name": first_name}
    )
    USER_LANG_CACHE[tg_id] = lang




@dp.callback_query(F.data.startswith("lang_"))
async def set_language_callback(callback: CallbackQuery):
    lang = callback.data.split("_")[1]

    set_user_lang(callback, lang)

    texts = {
        "uz": "✅ Til o'zbek tiliga o'zgartirildi",
        "ru": "✅ Язык изменён на русский",
        "en": "✅ Language changed to English",
        "tr": "✅ Dil Türkçe olarak değiştirildi",
        "qz": "✅ Тіл қазақ тіліне өзгертілді"
    }
    await callback.message.edit_text(texts.get(lang, texts["uz"]),reply_markup=start_inline_btn(callback.from_user.id))
    
   


    
@dp.callback_query(F.data.startswith("toggle_"))
async def toggle_profile_callback(callback: CallbackQuery):
    await callback.answer()
    setting = callback.data.split("_")[1]
    chat_id = callback.from_user.id
    user = User.objects.filter(telegram_id=chat_id).first()
    if setting == "protection":
        user.is_protected = not user.is_protected
    elif setting == "doc":
        user.is_doc = not user.is_doc
    user.save()
    text =""
    user_role = UserRole.objects.filter(user_id=user.id)
    for user_r in user_role:
        role_name = dict(get_role_labels_lang(chat_id)).get(user_r.role_key, "Noma'lum rol")
        text += f"🎭 {role_name} -  {user_r.quantity}\n"
    t = get_lang_text(chat_id)
    result = MostActiveUser.objects.filter(user_id=user.id).aggregate(
    total_played=Sum('games_played'),
    total_wins=Sum('games_win')
)

    total_played = result['total_played'] or 0
    total_wins = result['total_wins'] or 0

    await callback.message.edit_text(
        text=t['user_profile'].format(
            first_name=callback.from_user.first_name,
            coin=user.coin,
            stones=user.stones,
            protection=user.protection,
            docs=user.docs,
            wins=total_wins,
            all_played=total_played,
            text=text
        ),
        parse_mode="HTML",reply_markup=cart_inline_btn(chat_id)
    )