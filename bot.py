#!/usr/bin/env python3
"""
SUPER DIGGER's Discord Bot – Afg Bypass
"""

import os
import time
import re
import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor

import discord
from discord import app_commands
from discord.ext import commands

# ====================================================================
# CONFIG (loaded from Render environment variables)
# ====================================================================
TOKEN = os.environ.get("DISCORD_TOKEN")
RTAO_API_KEY = os.environ.get("RTAO_API_KEY")
OWNER_ID = 1456353767606849628

if not TOKEN:
    raise SystemExit("ERROR: DISCORD_TOKEN environment variable is not set.")
if not RTAO_API_KEY:
    raise SystemExit("ERROR: RTAO_API_KEY environment variable is not set.")

# ====================================================================
# BYPASS ENGINE – RTAO API
# ====================================================================
def _bypass_rtao(url):
    try:
        api_url = "https://api.rtao.lol/bypass"
        headers = {
            "x-api-key": RTAO_API_KEY,
            "Content-Type": "application/json",
        }
        params = {"url": url}
        response = requests.get(api_url, headers=headers, params=params, timeout=60)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" or data.get("success") is True:
                return data.get("result") or data.get("bypassed") or data.get("url")
            if "result" in data:
                return data["result"]
        return None
    except Exception as e:
        print(f"[Rtao API Error] {e}")
        return None


def getKey(url, param1=None, param2=None, param3=False):
    result = _bypass_rtao(url)
    if result:
        return str(result)
    return "bypass fail"

# ====================================================================
# DISCORD BOT
# ====================================================================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=["!", "."], intents=intents)

auto_mode_users = {}
bot_start_time = time.time()
executor = ThreadPoolExecutor(max_workers=3)


def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.user.id == OWNER_ID


def is_owner_ctx(ctx) -> bool:
    return ctx.author.id == OWNER_ID

# ==================== BYPASS VIEW ====================
class BypassView(discord.ui.View):
    def __init__(self, token, display_name, elapsed):
        super().__init__()
        self.token = token

        copy_pc = discord.ui.Button(label="📋 Copy (PC)", style=discord.ButtonStyle.primary)

        async def copy_pc_callback(interaction):
            await interaction.response.send_message(f"```{self.token}```", ephemeral=True)

        copy_pc.callback = copy_pc_callback
        self.add_item(copy_pc)

        copy_mobile = discord.ui.Button(label="📱 Copy (Mobile)", style=discord.ButtonStyle.success)

        async def copy_mobile_callback(interaction):
            await interaction.response.send_message(f"`{self.token}`", ephemeral=True)

        copy_mobile.callback = copy_mobile_callback
        self.add_item(copy_mobile)

        self.add_item(discord.ui.Button(
            label="Server",
            style=discord.ButtonStyle.link,
            url="https://discord.gg/ht9Jhn2n8P"
        ))

# ==================== CORE BYPASS FUNCTION ====================
async def run_bypass(ctx, url: str):
    is_interaction = hasattr(ctx, "response")

    try:
        start_time = time.time()
        result = await asyncio.get_event_loop().run_in_executor(
            executor, getKey, url, None, None, False
        )
        elapsed = round(time.time() - start_time, 2)

        if is_interaction:
            display_name = ctx.user.display_name
            mention = ctx.user.mention
        else:
            display_name = ctx.author.display_name
            mention = ctx.author.mention

        if result and not result.startswith("bypass fail"):
            embed = discord.Embed(
                title="✅ Afg Bypass Success",
                description=f"**Result:**\n```{result}```",
                color=discord.Color.green(),
            )
            embed.set_footer(text=f"Requested by {display_name} · ⏱️ {elapsed}s")

            if is_interaction:
                await ctx.followup.send(
                    content=mention, embed=embed,
                    view=BypassView(result, display_name, elapsed)
                )
            else:
                await ctx.reply(
                    content=mention, embed=embed,
                    view=BypassView(result, display_name, elapsed)
                )
        else:
            embed = discord.Embed(
                title="❌ Afg Bypass Failed",
                description=result or "Unknown error",
                color=discord.Color.red(),
            )
            if is_interaction:
                await ctx.followup.send(content=mention, embed=embed)
            else:
                await ctx.reply(content=mention, embed=embed)
    except Exception as e:
        error_msg = f"❌ Error: `{str(e)[:200]}`"
        embed = discord.Embed(description=error_msg, color=discord.Color.red())
        if is_interaction:
            await ctx.followup.send(content=mention, embed=embed)
        else:
            await ctx.reply(content=mention, embed=embed)

# ==================== ON_READY ====================
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"⚠️ Slash sync error: {e}")
    print(f"✅ AFG BYPASS BOT ONLINE - {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Afg Bypass | /bypass <url>"
        )
    )

# ==================== SLASH COMMANDS ====================
@bot.tree.command(name="bypass", description="Bypass any link using Afg Bypass")
@app_commands.describe(url="Full URL to bypass")
async def slash_bypass(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    await run_bypass(interaction, url)


@bot.tree.command(name="auto", description="Toggle auto-bypass mode for yourself")
@app_commands.describe(mode="on or off")
async def slash_auto(interaction: discord.Interaction, mode: str):
    user_id = interaction.user.id
    if mode.lower() == "on":
        auto_mode_users[user_id] = True
        embed = discord.Embed(
            title="✅ Afg Auto-Bypass Enabled",
            description="I'll now automatically bypass any link you send.",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed)
    elif mode.lower() == "off":
        auto_mode_users.pop(user_id, None)
        embed = discord.Embed(
            title="❌ Afg Auto-Bypass Disabled", color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Invalid Mode", description="Use `on` or `off`",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="status", description="Bot status (Owner only)")
async def slash_status(interaction: discord.Interaction):
    if not is_owner(interaction):
        embed = discord.Embed(
            title="❌ Access Denied",
            description="This command is restricted to the bot owner.",
            color=discord.Color.red(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    uptime = int(time.time() - bot_start_time)
    embed = discord.Embed(
        title="📊 Afg Bypass Status",
        description=f"**Uptime:** {uptime//3600}h {uptime%3600//60}m\n"
                    f"**Servers:** {len(bot.guilds)}\n"
                    f"**Users:** {len(bot.users)}",
        color=discord.Color.blue(),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="shutdown", description="Shutdown bot (Owner only)")
async def slash_shutdown(interaction: discord.Interaction):
    if not is_owner(interaction):
        embed = discord.Embed(
            title="❌ Access Denied",
            description="This command is restricted to the bot owner.",
            color=discord.Color.red(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    embed = discord.Embed(
        title="🔄 Shutting Down...",
        description="Afg Bypass is going offline. Goodbye!",
        color=discord.Color.orange(),
    )
    await interaction.response.send_message(embed=embed)
    await bot.close()
    exit(0)


@bot.tree.command(name="help", description="Show all commands")
async def slash_help(interaction: discord.Interaction):
    embed = discord.Embed(title="🇦🇫 Afg Bypass - Commands", color=discord.Color.gold())
    embed.add_field(name="/bypass <url>", value="Bypass any link", inline=False)
    embed.add_field(name="/auto <on|off>", value="Toggle auto-bypass", inline=False)
    embed.add_field(name="/status", value="Bot status (Owner only)", inline=False)
    embed.add_field(name="/shutdown", value="Shutdown bot (Owner only)", inline=False)
    embed.add_field(name="/help", value="Show this help", inline=False)
    embed.add_field(name="!bypass <url> or .bypass <url>", value="Prefix command", inline=False)
    embed.set_footer(text="Afg Bypass • Owner ID: " + str(OWNER_ID))
    await interaction.response.send_message(embed=embed)

# ==================== PREFIX COMMANDS ====================
@bot.command(name="bypass", aliases=["b"])
async def prefix_bypass(ctx, *, url: str):
    await run_bypass(ctx, url)


@bot.command(name="auto")
async def prefix_auto(ctx, mode: str):
    user_id = ctx.author.id
    if mode.lower() == "on":
        auto_mode_users[user_id] = True
        await ctx.send("✅ Afg Auto-Bypass Enabled – I'll auto-bypass links you send.")
    elif mode.lower() == "off":
        auto_mode_users.pop(user_id, None)
        await ctx.send("❌ Afg Auto-Bypass Disabled")
    else:
        await ctx.send("❌ Invalid mode. Use `on` or `off`.")


@bot.command(name="status")
async def prefix_status(ctx):
    if not is_owner_ctx(ctx):
        await ctx.send("❌ Access Denied – Owner only.")
        return
    uptime = int(time.time() - bot_start_time)
    await ctx.send(
        f"📊 **Afg Bypass Status**\n"
        f"Uptime: {uptime//3600}h {uptime%3600//60}m\n"
        f"Servers: {len(bot.guilds)}\n"
        f"Users: {len(bot.users)}"
    )


@bot.command(name="shutdown")
async def prefix_shutdown(ctx):
    if not is_owner_ctx(ctx):
        await ctx.send("❌ Access Denied – Owner only.")
        return
    await ctx.send("🔄 Afg Bypass is shutting down...")
    await bot.close()
    exit(0)

# ==================== AUTO DETECT MESSAGES ====================
@bot.event
async def on_message(message):
    if message.author.bot:
        await bot.process_commands(message)
        return

    if message.author.id in auto_mode_users:
        urls = re.findall(r"https?://[^\s]+", message.content)
        if urls:
            async with message.channel.typing():
                await asyncio.sleep(1)
                await run_bypass(message, urls[0])

    await bot.process_commands(message)

# ==================== RUN ====================
if __name__ == "__main__":
    print(f"""
    ╔═══════════════════════════════════════╗
    ║   🇦🇫  AFG BYPASS BOT  🇦🇫          ║
    ║   Owner ID: {OWNER_ID}      ║
    ║   Commands: /bypass  !bypass .bypass ║
    ║   Auto-bypass: /auto on (Everyone!)  ║
    ║   API: Rtao.lol                     ║
    ╚═══════════════════════════════════════╝
    """)
    bot.run(TOKEN)
