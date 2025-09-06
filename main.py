import discord
from discord.ext import commands
import json, random, os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables
TOKEN = os.getenv("DISCORD_TOKEN")  # Bot token from .env

if not TOKEN:
    print("❌ DISCORD_TOKEN not found in environment variables")
    exit(1)

SCENARIO_FILE = "scenarios.json"

def load_scenarios():
    if not os.path.exists(SCENARIO_FILE):
        return []
    with open(SCENARIO_FILE, "r") as f:
        return json.load(f)

def save_scenarios(scenarios):
    with open(SCENARIO_FILE, "w") as f:
        json.dump(scenarios, f, indent=2)

SCENARIOS = load_scenarios()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

user_sessions = {}

class ATCButton(discord.ui.Button):
    def __init__(self, option_index, user_id, scenario_index, session):
        option_text = session[scenario_index]["options"][option_index]
        super().__init__(label=option_text[:80], style=discord.ButtonStyle.primary)
        self.option_index = option_index
        self.user_id = user_id
        self.scenario_index = scenario_index
        self.session = session

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your training session.", ephemeral=True)
            return

        scenario = self.session[self.scenario_index]
        correct_index = scenario["answer"]

        if self.option_index == correct_index:
            embed = discord.Embed(
                title="🎯 Excellent Work!",
                description=f"**Your Answer:** {scenario['options'][self.option_index]}\n\n**Explanation:** {scenario['explanation']}",
                color=discord.Color.green()
            )
            embed.add_field(name="✅ Status", value="Correct!", inline=False)
        else:
            embed = discord.Embed(
                title="📚 Learning Opportunity",
                description=f"**Your Answer:** {scenario['options'][self.option_index]}\n**Correct Answer:** {scenario['options'][correct_index]}\n\n**Explanation:** {scenario['explanation']}",
                color=discord.Color.red()
            )
            embed.add_field(name="❌ Status", value="Incorrect - Keep practicing!", inline=False)

        embed.set_footer(text=f"Scenario {self.scenario_index + 1} of {len(self.session)}")
        await interaction.response.edit_message(content="", embed=embed, view=None)

        next_index = self.scenario_index + 1
        if next_index < len(self.session):
            next_scenario = self.session[next_index]
            embed = discord.Embed(
                title=f"✈️ Scenario {next_index+1}",
                description=next_scenario["scenario"],
                color=discord.Color.blue()
            )
            await interaction.followup.send(embed=embed, view=ATCTrainer(self.user_id, next_index, self.session), ephemeral=True)
        else:
            await interaction.followup.send("🎉 Training complete! Great job, controller.", ephemeral=True)

class ATCTrainer(discord.ui.View):
    def __init__(self, user_id, scenario_index, session):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.scenario_index = scenario_index
        self.session = session
        scenario = session[scenario_index]

        for i, option in enumerate(scenario["options"]):
            self.add_item(ATCButton(i, user_id, scenario_index, session))

@bot.tree.command(name="atc", description="Start ATC training scenarios")
async def atc(interaction: discord.Interaction):
    if not SCENARIOS:
        await interaction.response.send_message("⚠️ No scenarios available. Staff can add some with /addscenario.", ephemeral=True)
        return

    session = random.sample(SCENARIOS, len(SCENARIOS))
    user_sessions[interaction.user.id] = session

    first = session[0]
    embed = discord.Embed(
        title="✈️ Scenario 1",
        description=first["scenario"],
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=ATCTrainer(interaction.user.id, 0, session), ephemeral=True)

@bot.tree.command(name="addscenario", description="Add a new ATC training scenario (staff only)")
@commands.has_permissions(manage_guild=True)
async def addscenario(interaction: discord.Interaction,
                      scenario: str,
                      option1: str,
                      option2: str,
                      option3: str,
                      correct: int,
                      explanation: str):

    global SCENARIOS

    if correct < 1 or correct > 3:
        await interaction.response.send_message("❌ Correct answer must be 1, 2, or 3.", ephemeral=True)
        return

    new_scenario = {
        "id": len(SCENARIOS) + 1,
        "scenario": scenario,
        "options": [option1, option2, option3],
        "answer": correct - 1,
        "explanation": explanation
    }

    SCENARIOS.append(new_scenario)
    save_scenarios(SCENARIOS)

    await interaction.response.send_message(f"✅ Scenario added: {scenario}", ephemeral=True)

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(e)

bot.run(TOKEN)
