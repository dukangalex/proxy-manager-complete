from __future__ import annotations
import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import httpx
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from shared.config import get_settings

settings = get_settings()
dp = Dispatcher()


def is_admin(user_id: int) -> bool:
    return user_id in settings.bot_admin_ids


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='服务管理', callback_data='svc')],
        [InlineKeyboardButton(text='用户管理', callback_data='usr')],
        [InlineKeyboardButton(text='节点管理', callback_data='node')],
        [InlineKeyboardButton(text='告警中心', callback_data='alert')],
    ])


def back_menu(target='home'):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='返回', callback_data=target)]])


async def api(method: str, path: str, data=None):
    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.request(method, settings.app_base_url + path, headers={'X-Admin-Token': settings.app_admin_token}, json=data)
        res.raise_for_status()
        return res.json()


@dp.message(CommandStart())
async def start(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer('unauthorized')
        return
    await message.answer('TG 控制室', reply_markup=main_menu())


@dp.callback_query(F.data == 'home')
async def home(callback: CallbackQuery):
    await callback.message.edit_text('TG 控制室', reply_markup=main_menu())
    await callback.answer()


@dp.callback_query(F.data == 'svc')
async def svc(callback: CallbackQuery):
    data = await api('GET', '/ops/status')
    await callback.message.edit_text(str(data), reply_markup=back_menu())
    await callback.answer()


@dp.callback_query(F.data == 'usr')
async def usr(callback: CallbackQuery):
    data = await api('GET', '/admin/users')
    await callback.message.edit_text(str(data), reply_markup=back_menu())
    await callback.answer()


@dp.callback_query(F.data == 'node')
async def node(callback: CallbackQuery):
    data = await api('GET', '/ops/health')
    await callback.message.edit_text(str(data), reply_markup=back_menu())
    await callback.answer()


@dp.callback_query(F.data == 'alert')
async def alert(callback: CallbackQuery):
    data = await api('GET', '/alerts')
    await callback.message.edit_text(str(data), reply_markup=back_menu())
    await callback.answer()


async def main():
    if not settings.bot_token:
        raise RuntimeError('BOT_TOKEN is empty')
    await dp.start_polling(Bot(settings.bot_token))


if __name__ == '__main__':
    asyncio.run(main())
