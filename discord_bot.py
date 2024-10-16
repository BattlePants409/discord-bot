import discord
import os
import requests
import itertools
from discord.ext import commands
from dotenv import load_dotenv

# Define the point values for each card
card_points = {
    "Academy Manufactor": 9,
    "Aesi, Tyrant of Gyre Strait": 9,
    "Aetherflux Reservoir": 15,
    "Aggravated Assault": 12,
    "Akroma's Will": 10,
    "Alchemist's Talent": 9,
    "All is Dust": 8,
    "Ancient Copper Dragon": 6,
    "Ancient Greenwarden": 5,
    "Ancient Tomb": 11,
    "Archangel of Thune": 4,
    "Ashnod's Altar": 10,
    "Assassin's Trophy": 5,
    "Aura Shards": 10,
    "Avacyn, Angel of Hope": 7,
    "Azusa, Lost but Seeking": 7,
    "Basalt Monolith": 7,
    "Beastmaster Ascension": 6,
    "Beledros Witherbloom": 4,
    "Blightsteel Colossus": 6,
    "Bloom Tender": 4,
    "Bitterblossom": 10,
    "Bolas's Citadel": 9,
    "Bonny Paul, Clearcutter": 5,
    "Branching Evolution": 7,
    "Brass's Bounty": 6,
    "Burgeoning": 17,
    "Buried Alive": 10,
    "Cabal Coffers": 10,
    "Caduceus, Staff of Hermes": 5,
    "Captivating Vampire": 7,
    "Captain Sisay": 5,
    "Case of the Locked Hothouse": 9,
    "Cathars' Crusade": 15,
    "Chrome Mox": 9,
    "Chulane, Teller of Tales": 9,
    "Circle of Dreams Druid": 4,
    "City on Fire": 6,
    "Coat of Arms": 10,
    "Colossus Hammer": 4,
    "Commandeer": 7,
    "Consecrated Sphinx": 6,
    "Craterhoof Behemoth": 16,
    "Cyberdrive Awakener": 12,
    "Cyclonic Rift": 20,
    "Cultivator Colossus": 16,
    "Dauthi Voidwalker": 5,
    "Dark Ritual": 5,
    "Darksteel Monolith": 4,
    "Deadly Rollick": 8,
    "Defiler of Vigor": 4,
    "Deflecting Swat": 15,
    "Delighted Halfling": 3,
    "Demonic Consultation": 10,
    "Demonic Tutor": 8,
    "Descendants' Path": 7,
    "Devoted Druid": 7,
    "Diabolic Intent": 6,
    "Dictate of Erebos": 7,
    "Displacer Kitten": 8,
    "Doubling Season": 8,
    "Druid Class": 4,
    "Dryad of the Ilysian Grove": 6,
    "Eerie Ultimatum": 5,
    "Echoes of Eternity": 6,
    "Eladamri's Call": 5,
    "Eldrazi Monument": 9,
    "Elesh Norn, Grand Cenobite": 9,
    "Elven Chorus": 4,
    "Emergent Ultimatum": 12,
    "Emrakul, the Promised End": 8,
    "Emrakul, the World Anew": 10,
    "Enlightened Tutor": 5,
    "Entomb": 6,
    "Esper Sentinel": 8,
    "Excalibur, Sword of Eden": 4,
    "Exploration": 8,
    "Exquisite Blood": 11,
    "Eye of Ugin": 7,
    "Fabricate": 4,
    "Field of the Dead": 9,
    "Fierce Guardianship": 17,
    "Flawless Maneuver": 15,
    "Flusterstorm": 5,
    "Force of Negation": 5,
    "Force of Will": 7,
    "Frantic Search": 4,
    "Freed from the Real": 10,
    "Funeral Room // Awakening Hall": 5,
    "Glen Elendra Archmage": 8,
    "Goldspan Dragon": 8,
    "Grand Arbiter Agustin IV": 8,
    "Grave Pact": 8,
    "Growing Rites of Itlimoc // Itlimoc, Cradle of the Sun": 5,
    "Guardian Project": 6,
    "Hallowed Haunting": 4,
    "Hardened Scales": 5,
    "Heroic Intervention": 6,
    "Hullbreaker Horror": 5,
    "Hunting Velociraptor": 6,
    "Idyllic Tutor": 6,
    "Imperial Seal": 6,
    "Inkshield": 8,
    "Insurrection": 10,
    "Intruder Alarm": 13,
    "Isochron Scepter": 8,
    "Jadzi, Oracle of Arcavios // Journey to the Oracle": 8,
    "Jaheira, Friend of the Forest": 6,
    "Jeska's Will": 15,
    "Jetmir, Nexus of Revels": 11,
    "Kappa Cannoneer": 10,
    "Karmic Guide": 6,
    "Karn's Temporal Sundering": 10,
    "Kinnan, Bonder Prodigy": 8,
    "Klauth, Unrivaled Ancient": 7,
    "Kodama of the East Tree": 14,
    "Koma, the Cosmos Serpent": 5,
    "Kozilek, the Broken Reality": 7,
    "Kozilek, the Great Distortion": 8,
    "Krark-Clan Ironworks": 9,
    "Kuldotha Forgemaster": 4,
    "Last March of the Ents": 7,
    "Lim-Dul's Vault": 4,
    "Living Death": 9,
    "Lotus Petal": 8,
    "Lurking Predators": 9,
    "Mana Drain": 13,
    "Mana Vault": 11,
    "Marionette Master": 7,
    "Meathook Massacre II": 4,
    "Mirari's Wake": 5,
    "Misdirection": 4,
    "Mishra's Workshop": 8,
    "Mizzix's Mastery": 10,
    "Moonshaker Cavalry": 16,
    "Mondrak, Glory Dominus": 5,
    "Morophon, the Boundless": 7,
    "Mother of Runes": 8,
    "Mox Amber": 10,
    "Mox Diamond": 9,
    "Mox Opal": 10,
    "Murderous Redcap": 11,
    "Mystical Tutor": 6,
    "Mystic Remora": 8,
    "Necropotence": 12,
    "Night of the Sweets' Revenge": 8,
    "Nykthos, Shrine to Nyx": 10,
    "Nyxbloom Ancient": 6,
    "Ophiomancer": 8,
    "Ohran Frostfang": 5,
    "Old Gnawbone": 8,
    "Oracle of Mul Daya": 5,
    "Orcish Bowmasters": 8,
    "Overwhelming Stampede": 7,
    "Path to Exile": 4,
    "Peregrine Drake": 12,
    "Permission Denied": 5,
    "Phyrexian Altar": 10,
    "Pitiless Plunderer": 10,
    "Profane Tutor": 4,
    "Purphoros, God of the Forge": 10,
    "Ragavan, Nimble Pilferer": 4,
    "Revel in Riches": 8,
    "Rhystic Study": 11,
    "Roaming Throne": 7,
    "Rise and Shine": 6,
    "Rise of the Dark Realms": 6,
    "Rise of the Eldrazi": 10,
    "Ruinous Ultimatum": 17,
    "Rusko, Clockmaker": 8,
    "Sakura Tribe Scout": 7,
    "Sanctum Weaver": 5,
    "Savage Ventmaw": 5,
    "Scion of Draco": 9,
    "Scroll Rack": 4,
    "Scute Swarm": 11,
    "Seedborn Muse": 12,
    "Selvala, Heart of the Wilds": 9,
    "Sephara, Sky's Blade": 5,
    "Sensei's Divining Top": 5,
    "Serra Ascendant": 8,
    "Serra's Sanctum": 11,
    "Shadow of the Second Sun": 4,
    "Sheoldred, the Apocalypse": 8,
    "Sheoldred, Whispering One": 5,
    "Simic Ascendancy": 7,
    "Simulacrum Synthesizer": 9,
    "Sisay, Weatherlight Captain": 5,
    "Skullclamp": 8,
    "Smothering Tithe": 20,
    "Sneak Attack": 13,
    "Solemnity": 7,
    "Solitary Confinement": 10,
    "Solve the Equation": 5,
    "Sol Ring": 10,
    "Sorin Markov": 7,
    "Sphinx of the Second Sun": 4,
    "Steelshaper's Gift": 5,
    "Stoneforge Mystic": 8,
    "Stonehewer Giant": 7,
    "Storm-Kiln Artist": 6,
    "Storm the Vault // Vault of Catlacan": 11,
    "Swan Song": 5,
    "Sword of Feast and Famine": 11,
    "Sword of Fire and Ice": 6,
    "Sword of Forge and Frontier": 7,
    "Sword of Light and Shadow": 5,
    "Sword of Truth and Justice": 7,
    "Sword of Wealth and Power": 7,
    "Sterling Grove": 5,
    "Teferi's Protection": 10,
    "Temple of the False God": 6,
    "Terror of the Peaks": 6,
    "The Great Henge": 11,
    "The Meathook Massacre": 6,
    "The One Ring": 13,
    "Thousand-Year Storm": 5,
    "Three Tree City": 11,
    "Time Sieve": 16,
    "Toski, Bearer of Secrets": 5,
    "Triumph of the Hordes": 16,
    "Ugin, the Spirit Dragon": 7,
    "Ulamog the Ceaseless Hunger": 7,
    "Ulamog, the Defiler": 8,
    "Ulamog, the Infinite Gyre": 7,
    "Unbound Flourishing": 8,
    "Underworld Breach": 8,
    "Unwinding Clock": 5,
    "Uro, Titan of Nature's Wrath": 6,
    "Urza, Lord High Artificer": 8,
    "Urza's Incubator": 10,
    "Urza's Ruinous Blast": 8,
    "Urza's Saga": 10,
    "Utvara Hellkite": 6,
    "Valgavoth, Terror Eater": 5,
    "Vampiric Tutor": 8,
    "Walk the Aeons": 5,
    "Warren Soultrader": 11,
    "Wayward Swordtooth": 6,
    "Whir of Invention": 5,
    "Wilderness Reclamation": 4,
    "Worldly Tutor": 5,
    "Yawgmoth, Thran Physician": 6,
    "Yuriko, the Tiger's Shadow": 6,
    "Zopandrel, Hunger Dominus": 4
}




# Define your intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# Conditionally set message_content if it's available
if hasattr(intents, 'message_content'):
    intents.message_content = True

# Create the bot with the defined intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


def fetch_decklist(archidekt_url):
    try:
        deck_id = archidekt_url.split('/')[-1]
        api_url = f"https://archidekt.com/api/decks/{deck_id}/"
        response = requests.get(api_url)

        if response.status_code != 200:
            return None, None

        deck_data = response.json()
        decklist = [card['card']['oracleCard']['name'] for card in deck_data['cards']]

        # Find the commanders
        commanders = []
        for card in deck_data['cards']:
            if 'Commander' in card.get('categories', []):
                commanders.append(card['card']['oracleCard']['name'])

        return decklist, commanders
    except Exception as e:
        print(f"Error fetching decklist: {e}")
        return None, None



@bot.command(name='checkdeck')
async def check_deck(ctx, archidekt_url: str):
    decklist, commanders = fetch_decklist(archidekt_url)
    if not decklist:
        await ctx.send("Error fetching the decklist. Please check the URL and try again.")
        return

    # Check if any commander is restricted
    restricted_commanders = [commander for commander in commanders if commander in card_points]

    if restricted_commanders:
        await ctx.send(f"Your deck is not legal because the commander(s), **{', '.join(restricted_commanders)}**, is/are restricted.")
        return

    total_points = 0
    results = []

    # Filter decklist to include only cards with points > 0
    filtered_decklist = [(card_name, card_points.get(card_name, 0)) for card_name in decklist if card_points.get(card_name, 0) > 0]

    for card_name, points in filtered_decklist:
        total_points += points
        results.append((card_name, points))

    response = f"**Total Points**: {total_points}\n"

    if total_points > 100:
        points_to_remove = total_points - 100
        response += f"**Your deck exceeds 100 points by {points_to_remove} points.**\n"

        # Find the best combination of cards to cut that gets closest to reducing the total points to 100
        deck_sorted = sorted(results, key=lambda x: x[1], reverse=True)
        best_combination = None
        best_remaining_points = total_points

        # Try different combinations of cards to cut, starting from combinations of 1 card, 2 cards, etc.
        for r in range(1, len(deck_sorted) + 1):
            for combination in itertools.combinations(deck_sorted, r):
                combination_points = sum(card[1] for card in combination)
                new_total_points = total_points - combination_points

                # Stop if new total is less than or equal to 100
                if new_total_points <= 100:
                    remaining_points = 100 - new_total_points

                    if remaining_points < best_remaining_points:
                        best_combination = combination
                        best_remaining_points = remaining_points

                # Stop if we found the perfect combination
                if best_remaining_points == 0:
                    break
            if best_remaining_points == 0:
                break

        # Display recommended cuts
        response += "\n**Recommended Cuts:**\n"
        if best_combination:
            for card, points in best_combination:
                response += f"- {card}: {points} points\n"
            response += f"\n**New Total (after recommended cuts)**: {total_points - sum(card[1] for card in best_combination)} points"
        else:
            response += "No valid cuts found to bring the total to or under 100 points."

    else:
        response += "Your deck is within the 100-point limit.\n"

    if len(response) > 2000:
        for i in range(0, len(response), 2000):
            await ctx.send(response[i:i+2000])
    else:
        await ctx.send(response)





# Load the token from the environment variable
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Run the bot
bot.run(TOKEN)