from __future__ import annotations
import asyncio
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

def is_admin(uid):
    return uid in settings.bot_admin_ids

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 服务状态", callback_data="status")],
        [InlineKeyboardButton(text="👤 用户管理", callback_data="users")],
        [InlineKeyboardButton(text="🌐 节点检测", callback_data="nodes")],
        [InlineKeyboardButton(text="⚠️ 告警中心", callback_data="alerts")],
    ])

def back():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ 返回", callback_data="home")]
    ])

async def api(path):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            settings.app_base_url + path,
            headers={"X-Admin-Token": settings.app_admin_token}
        )
        return r.json()

@dp.message(CommandStart())
async def start(msg: Message):
    if not is_admin(msg.from_user.id):
        await msg.answer("❌ 无权限")
        return
    await msg.answer("🚀 控制面板", reply_markup=main_menu())

@dp.callback_query(F.data == "home")
async def home(cb: CallbackQuery):
    await cb.message.edit_text("🚀 控制面板", reply_markup=main_menu())
    await cb.answer()

@dp.callback_query(F.data == "status")
async def status(cb: CallbackQuery):
    data = await api("/ops/status")
    await cb.message.edit_text(str(data), reply_markup=back())
    await cb.answer()

@dp.callback_query(F.data == "users")
async def users(cb: CallbackQuery):
    data = await api("/admin/users")
    await cb.message.edit_text(str(data), reply_markup=back())
    await cb.answer()

@dp.callback_query(F.data == "nodes")
async def nodes(cb: CallbackQuery):
    data = await api("/ops/health")
    await cb.message.edit_text(str(data), reply_markup=back())
    await cb.answer()

@dp.callback_query(F.data == "alerts")
async def alerts(cb: CallbackQuery):
    data = await api("/alerts")
    await cb.message.edit_text(str(data), reply_markup=back())
    await cb.answer()

async def main():
    bot = Bot(settings.bot_token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())