import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Define the point values for each card
card_points = {
    "Aetherflux Reservoir": 15,
    "Ancient Tomb": 11,
    "Akroma's Will": 10,
    "All is Dust": 8,
    "Ashnod's Altar": 10,
    "Beastmaster Ascension": 6,
    "Bloom Tender": 4,
    "Bitterblossom": 10,
    "Bolas's Citadel": 9,
    "Cabal Coffers": 10,
    "Cathars' Crusade": 15,
    "Chrome Mox": 9,
    "Coat of Arms": 10,
    "Commandeer": 7,
    "Consecrated Sphinx": 6,
    "Cyclonic Rift": 20,
    "Dauthi Voidwalker": 5,
    "Dark Ritual": 5,
    "Deadly Rollick": 8,
    "Deflecting Swat": 15,
    "Delighted Halfling": 3,
    "Demonic Consultation": 10,
    "Demonic Tutor": 8,
    "Devoted Druid": 7,
    "Diabolic Intent": 6,
    "Dictate of Erebos": 7,
    "Displacer Kitten": 8,
    "Dockside Extortionist": 18,
    "Doubling Season": 8,
    "Eerie Ultimatum": 5,
    "Eladamri's Call": 5,
    "Eldrazi Monument": 9,
    "Elesh Norn, Grand Cenobite": 9,
    "Emrakul, the Promised End": 8,
    "Emrakul, the World Anew": 10,
    "Enlightened Tutor": 5,
    "Exquisite Blood": 10,
    "Esper Sentinel": 8,
    "Fierce Guardianship": 17,
    "Flawless Maneuver": 15,
    "Flusterstorm": 5,
    "Force of Negation": 5,
    "Force of Will": 7,
    "Glen Elendra Archmage": 8,
    "Grand Arbiter Agustin IV": 8,
    "Grave Pact": 8,
    "Growing Rites of Itlimoc": 5,
    "Guardian Project": 4,
    "Heroic Intervention": 6,
    "Hullbreaker Horror": 5,
    "Idyllic Tutor": 6,
    "Imperial Seal": 6,
    "Inkshield": 8,
    "Insurrection": 10,
    "Isochron Scepter": 8,
    "Jeweled Lotus": 10,
    "Jeska's Will": 15,
    "Karn's Temporal Sundering": 10,
    "Kinnan, Bonder Prodigy": 8,
    "Koma, the Cosmos Serpent": 5,
    "Kozilek, the Broken Reality": 7,
    "Kozilek, the Great Distortion": 9,
    "Lim-Dul's Vault": 4,
    "Living Death": 9,
    "Lotus Petal": 13,
    "Mana Crypt": 15,
    "Mana Drain": 13,
    "Mana Vault": 15,
    "Mirari's Wake": 5,
    "Misdirection": 4,
    "Moonshaker Cavalry": 16,
    "Mother of Runes": 8,
    "Mox Amber": 10,
    "Mox Diamond": 9,
    "Mox Opal": 10,
    "Mystical Tutor": 6,
    "Mystic Remora": 8,
    "Necropotence": 12,
    "Nyxbloom Ancient": 6,
    "Ophiomancer": 8,
    "Ohran Frostfang": 5,
    "Orcish Bowmasters": 8,
    "Overwhelming Stampede": 7,
    "Permission Denied": 5,
    "Phyrexian Altar": 10,
    "Purphoros, God of the Forge": 10,
    "Ragavan, Nimble Pilferer": 4,
    "Revel in Riches": 7,
    "Rhystic Study": 12,
    "Rise of the Eldrazi": 8,
    "Ruinous Ultimatum": 17,
    "Rusko, Clockmaker": 8,
    "Sanctum Weaver": 5,
    "Seedborn Muse": 12,
    "Sensei's Divining Top": 5,
    "Serra Ascendant": 8,
    "Serra's Sanctum": 11,
    "Sheoldred, the Apocalypse": 8,
    "Skullclamp": 8,
    "Smothering Tithe": 20,
    "Sneak Attack": 13,
    "Solitary Confinement": 10,
    "Sol Ring": 10,
    "Swan Song": 5,
    "Sword of Feast and Famine": 11,
    "Sword of Fire and Ice": 6,
    "Sword of Forge and Frontier": 7,
    "Sword of Light and Shadow": 5,
    "Sword of Truth and Justice": 7,
    "Sword of Wealth and Power": 7,
    "Teferi's Protection": 10,
    "Temple of the False God": 6,
    "Toski, Bearer of Secrets": 5,
    "Triumph of the Hordes": 16,
    "The Great Henge": 11,
    "The Meathook Massacre": 6,
    "The One Ring": 15,
    "Ulamog the Ceaseless Hunger": 7,
    "Ulamog, the Defiler": 8,
    "Underworld Breach": 8,
    "Urza's Ruinous Blast": 8,
    "Urza's Saga": 10,
    "Vampiric Tutor": 6,
    "Warren Soultrader": 11,
    "Worldly Tutor": 5,
    "Yuriko, the Tiger's Shadow": 6
}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='checkdeck')
async def check_deck(ctx, *, decklist: str):
    total_points = 0
    lines = decklist.split("\n")
    results = []
    
    for line in lines:
        try:
            card_name = line.strip().split(' ', 1)[1]
            points = card_points.get(card_name, 0)
            total_points += points
            results.append(f"{card_name}: {points} points")
        except IndexError:
            continue

    response = "\n".join(results)
    response += f"\n\n**Total Points**: {total_points}"
    
    # Discord's character limit is 2000 characters per message
    if len(response) > 2000:
        # Split the response into chunks
        for i in range(0, len(response), 2000):
            await ctx.send(response[i:i+2000])
    else:
        await ctx.send(response)

# Load environment variables from the .env file
load_dotenv()
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
