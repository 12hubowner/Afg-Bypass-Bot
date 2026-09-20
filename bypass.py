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

TOKEN = os.environ.get("DISCORD_TOKEN")
RTAO_API_KEY = os.environ.get("RTAO_API_KEY")

if not TOKEN:
    raise SystemExit("ERROR: DISCORD_TOKEN environment variable is not set.")
if not RTAO_API_KEY:
    raise SystemExit("ERROR: RTAO_API_KEY environment variable is not set.")

# ... rest of your code ...
