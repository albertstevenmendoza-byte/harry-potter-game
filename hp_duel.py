#!/usr/bin/env python3
"""
hp_duel.py — Harry Potter Dueling Game (2-Player Local)
Requires: rich >= 13.0  →  pip install rich

Run:  python hp_duel.py
"""

from __future__ import annotations
import math
import sys
import time
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich.prompt import Prompt
from rich.rule import Rule
from rich.align import Align
from rich import box

console = Console()

# ══════════════════════════════════════════════════════════════
#  DATA
# ══════════════════════════════════════════════════════════════

SPELLS: dict[str, dict] = {
    "expelliarmus":       {"name": "Expelliarmus",       "damage": 25,  "type": "disarming",   "color": "red",
                           "description": "The Disarming Charm — forces the wand away.",
                           "flavor":      "A jet of scarlet light erupts from the wand tip."},
    "stupefy":            {"name": "Stupefy",            "damage": 30,  "type": "stunning",    "color": "red",
                           "description": "The Stunning Spell — renders the target unconscious.",
                           "flavor":      "A bolt of red energy streaks through the air."},
    "avada kedavra":      {"name": "Avada Kedavra",      "damage": 80,  "type": "unforgivable","color": "green",
                           "description": "The Killing Curse — the most terrible Unforgivable.",
                           "flavor":      "A blinding flash of sickly green light tears forward."},
    "crucio":             {"name": "Crucio",             "damage": 45,  "type": "unforgivable","color": "yellow",
                           "description": "The Cruciatus Curse — inflicts unbearable pain.",
                           "flavor":      "The air warps and shudders with dark energy."},
    "imperio":            {"name": "Imperio",            "damage": 20,  "type": "unforgivable","color": "yellow",
                           "description": "The Imperius Curse — places the victim under control.",
                           "flavor":      "A haze of pale light drifts toward the target."},
    "sectumsempra":       {"name": "Sectumsempra",       "damage": 55,  "type": "dark",        "color": "red",
                           "description": "A dark slashing curse invented by Severus Snape.",
                           "flavor":      "Invisible blades cut through the air like a scythe."},
    "protego":            {"name": "Protego",            "damage": -20, "type": "shield",      "color": "blue",
                           "description": "The Shield Charm — restores up to 20 HP.",
                           "flavor":      "A shimmering barrier of silver light materializes."},
    "diffindo":           {"name": "Diffindo",           "damage": 35,  "type": "severing",    "color": "red",
                           "description": "The Severing Charm — cuts or tears the target.",
                           "flavor":      "A sharp crimson slash tears through the air."},
    "confringo":          {"name": "Confringo",          "damage": 40,  "type": "blasting",    "color": "orange3",
                           "description": "The Blasting Curse — causes the target to explode.",
                           "flavor":      "A burst of flames detonates on impact."},
    "bombarda":           {"name": "Bombarda",           "damage": 38,  "type": "blasting",    "color": "orange3",
                           "description": "Creates a concussive explosion on impact.",
                           "flavor":      "A concussive shockwave ripples outward."},
    "incendio":           {"name": "Incendio",           "damage": 32,  "type": "fire",        "color": "orange1",
                           "description": "The Fire-Making Spell — conjures flames.",
                           "flavor":      "A tongue of bright fire lashes forward."},
    "flipendo":           {"name": "Flipendo",           "damage": 22,  "type": "knockback",   "color": "blue",
                           "description": "The Knockback Jinx — sends the target flying.",
                           "flavor":      "A blue flash sends the target stumbling."},
    "locomotor mortis":   {"name": "Locomotor Mortis",   "damage": 18,  "type": "binding",     "color": "magenta",
                           "description": "The Leg-Locker Curse — binds the legs together.",
                           "flavor":      "Dark tendrils spiral around the target's legs."},
    "petrificus totalus": {"name": "Petrificus Totalus", "damage": 28,  "type": "binding",     "color": "blue",
                           "description": "The Full Body-Bind Curse — complete paralysis.",
                           "flavor":      "The target snaps to rigid attention, unable to move."},
    "levicorpus":         {"name": "Levicorpus",         "damage": 15,  "type": "jinx",        "color": "yellow",
                           "description": "Hoists the target upside-down by an ankle.",
                           "flavor":      "The target is yanked into the air, dangling helplessly."},
    "expulso":            {"name": "Expulso",            "damage": 42,  "type": "blasting",    "color": "orange3",
                           "description": "Causes an object to explode from internal pressure.",
                           "flavor":      "The target detonates in a shower of force."},
    "reducto":            {"name": "Reducto",            "damage": 36,  "type": "blasting",    "color": "blue",
                           "description": "The Reductor Curse — blasts solid objects apart.",
                           "flavor":      "A bolt of blue energy obliterates the target."},
    "furnunculus":        {"name": "Furnunculus",        "damage": 12,  "type": "jinx",        "color": "green",
                           "description": "Causes the target to break out in painful boils.",
                           "flavor":      "A sickly green hex finds its mark."},
    "langlock":           {"name": "Langlock",           "damage": 10,  "type": "jinx",        "color": "magenta",
                           "description": "Glues the tongue to the roof of the mouth.",
                           "flavor":      "A quiet hex silences the target mid-word."},
    "densaugeo":          {"name": "Densaugeo",          "damage":  8,  "type": "jinx",        "color": "green",
                           "description": "Causes the target's teeth to enlarge grotesquely.",
                           "flavor":      "A poorly-aimed but effective jinx lands true."},
}

CHARACTERS: dict[str, dict] = {
    "harry":     {"name": "Harry Potter",     "hp": 120, "bonus": 1.10, "sig": "expelliarmus",
                  "color": "bright_red",   "art": "( ⚡ )",
                  "lore": "Marked by Voldemort's curse — raw defiance fuels his magic."},
    "hermione":  {"name": "Hermione Granger", "hp": 110, "bonus": 1.20, "sig": "stupefy",
                  "color": "bright_yellow","art": "( 📚 )",
                  "lore": "Encyclopedic knowledge of spells gives Hermione unmatched precision."},
    "ron":       {"name": "Ron Weasley",      "hp": 130, "bonus": 1.00, "sig": "diffindo",
                  "color": "bright_red",   "art": "( 🦁 )",
                  "lore": "Heart of a lion — stubbornness keeps him standing longer than most."},
    "voldemort": {"name": "Lord Voldemort",   "hp": 115, "bonus": 1.35, "sig": "avada kedavra",
                  "color": "bright_green", "art": "( ☠ )",
                  "lore": "The Dark Lord's power is absolute. His curses carry death itself."},
    "snape":     {"name": "Severus Snape",    "hp": 115, "bonus": 1.25, "sig": "sectumsempra",
                  "color": "bright_white", "art": "( 🖤 )",
                  "lore": "Inventor of Sectumsempra. His dueling mastery is without peer."},
}

WANDS: dict[str, dict] = {
    "holly":  {"name": "Holly",   "core": "Phoenix Feather",   "modifier": "expelliarmus",
               "bonus": 1.15, "flavor": "Chosen by Harry Potter himself.  Good against the Dark Arts.",
               "effect": "+15% Expelliarmus"},
    "vine":   {"name": "Vine",    "core": "Dragon Heartstring", "modifier": "petrificus totalus",
               "bonus": 1.15, "flavor": "Seeks owners of hidden depths.  Hermione's wand.",
               "effect": "+15% Petrificus Totalus"},
    "elder":  {"name": "Elder",   "core": "Thestral Tail Hair", "modifier": "avada kedavra",
               "bonus": 1.20, "flavor": "The most powerful wand ever crafted — the Deathstick.",
               "effect": "+20% Avada Kedavra"},
    "walnut": {"name": "Walnut",  "core": "Dragon Heartstring", "modifier": "confringo",
               "bonus": 1.15, "flavor": "Powerful and demanding.  Requires a versatile caster.",
               "effect": "+15% Confringo"},
    "ash":    {"name": "Ash",     "core": "Unicorn Hair",       "modifier": "expelliarmus",
               "bonus": 1.15, "flavor": "Loyal to its owner.  Never works as well for another.",
               "effect": "+15% Expelliarmus"},
}

# ── Tunable constants ──────────────────────────────────────────
ROUNDS_TO_WIN  = 3
REPEAT_PENALTY = 0.50
PROTEGO_CAP    = 20
HP_BAR_WIDTH   = 28

# ── Spell-type → Rich color ────────────────────────────────────
TYPE_COLORS: dict[str, str] = {
    "disarming": "red", "stunning": "red", "unforgivable": "bright_green",
    "dark": "red", "shield": "blue", "severing": "red", "blasting": "orange3",
    "fire": "orange1", "knockback": "blue", "binding": "magenta", "jinx": "yellow",
}

# ══════════════════════════════════════════════════════════════
#  CORE LOGIC  (pure — no I/O)
# ══════════════════════════════════════════════════════════════

def get_spell(raw: str) -> Optional[dict]:
    return SPELLS.get(raw.strip().lower())


def resolve_damage(
    spell: dict, char_bonus: float,
    wand_mod: str, wand_bonus: float,
    last_spell: Optional[str]
) -> tuple[int, list[str]]:
    """
    Returns (final_damage, notes).
    Negative damage means heal the caster (Protego).
    """
    notes: list[str] = []

    if spell["type"] == "shield":
        heal = min(math.ceil(abs(spell["damage"]) * char_bonus), PROTEGO_CAP)
        notes.append(f"[bold blue]🛡  Shield Charm — +{heal} HP restored.[/bold blue]")
        return -heal, notes

    base = float(spell["damage"]) * char_bonus
    if char_bonus != 1.0:
        notes.append(f"[dim]Character bonus ×{char_bonus:.2f}[/dim]")

    if spell["name"].lower() == wand_mod.lower():
        base *= wand_bonus
        notes.append(f"[bold yellow]✦ Wand affinity ×{wand_bonus:.2f}![/bold yellow]")

    if last_spell and last_spell.lower() == spell["name"].lower():
        base *= REPEAT_PENALTY
        notes.append(
            f"[bold red]⚠  Diminishing returns — "
            f"{int(REPEAT_PENALTY*100)}% damage (spell overused!)[/bold red]"
        )

    return max(1, math.ceil(base)), notes


class Player:
    def __init__(self, num: int, char_key: str, wand_key: str):
        c = CHARACTERS[char_key]
        w = WANDS[wand_key]
        self.num        = num
        self.char_key   = char_key
        self.char_name  = c["name"]
        self.char_color = c["color"]
        self.char_art   = c["art"]
        self.char_lore  = c["lore"]
        self.char_sig   = c["sig"]
        self.max_hp     = c["hp"]
        self.hp: int    = c["hp"]
        self.bonus      = c["bonus"]
        self.wand_key   = wand_key
        self.wand_name  = w["name"]
        self.wand_core  = w["core"]
        self.wand_mod   = w["modifier"]
        self.wand_bonus = w["bonus"]
        self.rounds_won = 0
        self.last_spell: Optional[str] = None

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, n: int) -> None:
        self.hp = max(0, self.hp - n)

    def heal(self, n: int) -> None:
        self.hp = min(self.max_hp, self.hp + n)

    def reset_for_round(self) -> None:
        self.hp = self.max_hp
        self.last_spell = None


def process_turn(caster: Player, target: Player, raw: str) -> dict:
    """
    Validate + apply one turn.  Returns result dict.
    Side-effects: mutates HP and last_spell on a valid cast.
    """
    spell = get_spell(raw)
    if spell is None:
        return {"valid": False, "spell": None, "damage": 0, "notes": []}

    dmg, notes = resolve_damage(
        spell, caster.bonus, caster.wand_mod, caster.wand_bonus, caster.last_spell
    )
    if dmg < 0:
        caster.heal(abs(dmg))
    else:
        target.take_damage(dmg)
    caster.last_spell = spell["name"]
    return {"valid": True, "spell": spell, "damage": dmg, "notes": notes}

# ══════════════════════════════════════════════════════════════
#  UI HELPERS
# ══════════════════════════════════════════════════════════════

_TITLE = r"""
  ██╗  ██╗██████╗     ██████╗ ██╗   ██╗███████╗██╗
  ██║  ██║██╔══██╗    ██╔══██╗██║   ██║██╔════╝██║
  ███████║██████╔╝    ██║  ██║██║   ██║█████╗  ██║
  ██╔══██║██╔═══╝     ██║  ██║██║   ██║██╔══╝  ██║
  ██║  ██║██║         ██████╔╝╚██████╔╝███████╗███████╗
  ╚═╝  ╚═╝╚═╝         ╚═════╝  ╚═════╝╚══════╝╚══════╝"""

_VICTORY = r"""
  ╦  ╦╦╔═╗╔╦╗╔═╗╦═╗╦ ╦
  ╚╗╔╝║║    ║ ║ ║╠╦╝╚╦╝
   ╚╝ ╩╚═╝ ╩ ╚═╝╩╚═ ╩ """


def _rule(title: str = "", style: str = "yellow") -> None:
    console.print(Rule(title, style=style))


def _hp_bar(current: int, maximum: int) -> Text:
    ratio  = max(0.0, current / maximum)
    filled = int(ratio * HP_BAR_WIDTH)
    empty  = HP_BAR_WIDTH - filled
    color  = "green" if ratio > 0.5 else ("yellow" if ratio > 0.25 else "red")
    bar    = Text()
    bar.append("█" * filled, style=color)
    bar.append("░" * empty,  style="dim white")
    bar.append(f"  {current}/{maximum}", style="white")
    return bar


def _show_status(p1: Player, p2: Player) -> None:
    for p in (p1, p2):
        console.print(
            f"  [bold {p.char_color}]{p.char_name}[/bold {p.char_color}]"
            f"  [dim](Round wins: {p.rounds_won})[/dim]"
        )
        console.print("  HP: ", end="")
        console.print(_hp_bar(p.hp, p.max_hp))
    console.print()


def show_spell_list() -> None:
    t = Table(
        title="[bold yellow]✦  Known Spells  ✦[/bold yellow]",
        box=box.SIMPLE_HEAD, header_style="bold white",
        border_style="dim yellow", show_lines=False,
    )
    t.add_column("Spell",      style="bold white",  width=22, no_wrap=True)
    t.add_column("Damage",     style="bold yellow", width=8,  justify="right")
    t.add_column("Type",       style="dim white",   width=14)
    t.add_column("Description",style="white",       width=42)

    for sp in sorted(SPELLS.values(), key=lambda s: s["damage"], reverse=True):
        dmg = sp["damage"]
        c   = TYPE_COLORS.get(sp["type"], "white")
        dmg_str = (
            f"[green]+{abs(dmg)} HP[/green]" if dmg < 0
            else f"[{c}]{dmg}[/{c}]"
        )
        t.add_row(f"[bold]{sp['name']}[/bold]", dmg_str,
                  f"[dim]{sp['type'].title()}[/dim]",
                  f"[dim white]{sp['description']}[/dim white]")
    console.print(t)


# ──────────────────────────────────────────────────────────────
# SELECTION SCREENS
# ──────────────────────────────────────────────────────────────

def select_character(player_num: int) -> str:
    console.clear()
    _rule(f"⚡  Player {player_num} — Choose Your Character  ⚡")

    keys   = list(CHARACTERS.keys())
    panels = []
    for i, key in enumerate(keys, 1):
        c = CHARACTERS[key]
        body = (
            f"[bold {c['color']}]{c['art']}[/bold {c['color']}]\n"
            f"[bold white]{c['name']}[/bold white]\n\n"
            f"[yellow]HP:[/yellow] {c['hp']}\n"
            f"[yellow]Power:[/yellow] ×{c['bonus']:.2f}\n"
            f"[yellow]Sig spell:[/yellow] {c['sig'].title()}\n\n"
            f"[dim italic]{c['lore']}[/dim italic]"
        )
        panels.append(Panel(
            body,
            title=f"[bold yellow][{i}] {key.title()}[/bold yellow]",
            border_style="yellow", width=26, padding=(0, 1),
        ))

    console.print(Columns(panels, equal=True, expand=False))
    console.print()

    while True:
        raw = Prompt.ask(
            f"  [bold white]Player {player_num}: enter character name[/bold white]"
        ).strip().lower()
        if raw in keys:
            console.print(
                f"\n  [bold green]✓  {CHARACTERS[raw]['name']} enters the arena![/bold green]"
            )
            time.sleep(0.7)
            return raw
        console.print(f"  [bold red]✗  '{raw}' is not valid. "
                      f"Choose from: {', '.join(k.title() for k in keys)}[/bold red]")


def select_wand(player_num: int, char_key: str) -> str:
    console.clear()
    _rule(f"⚡  Player {player_num} — Choose Your Wand  ⚡")

    keys = list(WANDS.keys())
    t = Table(box=box.ROUNDED, border_style="yellow",
              header_style="bold yellow", show_lines=True)
    t.add_column("#",        style="bold white",  width=4,  justify="center")
    t.add_column("Wood",     style="bold yellow", width=10)
    t.add_column("Core",     style="white",       width=20)
    t.add_column("Affinity", style="green",       width=20)
    t.add_column("Flavour",  style="dim white",   width=40)
    for i, key in enumerate(keys, 1):
        w = WANDS[key]
        t.add_row(str(i), w["name"], w["core"], w["effect"], w["flavor"])
    console.print(t)
    console.print()

    while True:
        raw = Prompt.ask(
            f"  [bold white]Player {player_num} ({CHARACTERS[char_key]['name']}): "
            f"enter wand wood[/bold white]"
        ).strip().lower()
        if raw in keys:
            w = WANDS[raw]
            console.print(
                f"\n  [bold green]✓  The {w['name']} wand ({w['core']}) "
                f"chooses you![/bold green]"
            )
            console.print(f"  [dim italic]{w['flavor']}[/dim italic]")
            time.sleep(0.9)
            return raw
        # also accept the wand name spelled out
        name_map = {v["name"].lower(): k for k, v in WANDS.items()}
        if raw in name_map:
            raw = name_map[raw]
            w = WANDS[raw]
            console.print(
                f"\n  [bold green]✓  The {w['name']} wand ({w['core']}) "
                f"chooses you![/bold green]"
            )
            time.sleep(0.9)
            return raw
        console.print(f"  [bold red]✗  '{raw}' is not valid. "
                      f"Choose from: {', '.join(k.title() for k in keys)}[/bold red]")


# ──────────────────────────────────────────────────────────────
# MATCH / ROUND SCREENS
# ──────────────────────────────────────────────────────────────

def show_matchup(p1: Player, p2: Player) -> None:
    console.clear()
    console.print("[bold red]\n  ╔══╗ ╦ ╦ ╔═╗ ╦   \n  ║  ║ ║ ║ ╠═  ║   \n  ╚══╝ ╚═╝ ╚═╝ ╩═╝[/bold red]",
                  justify="center")

    def card(p: Player) -> str:
        return (
            f"[bold {p.char_color}]{p.char_art}[/bold {p.char_color}]\n"
            f"[bold white]Player {p.num}[/bold white]\n"
            f"[bold yellow]{p.char_name}[/bold yellow]\n\n"
            f"Wand: [yellow]{p.wand_name}[/yellow] / [dim]{p.wand_core}[/dim]\n"
            f"HP:   [green]{p.max_hp}[/green]"
        )

    console.print(
        Columns([
            Panel(card(p1), border_style="yellow", width=30),
            Align(Panel("[bold red]\n VS \n[/bold red]",
                        border_style="red", width=9, padding=(2, 1)), align="center"),
            Panel(card(p2), border_style="yellow", width=30),
        ]), justify="center"
    )
    console.print()
    _rule("⚡  LET THE DUEL BEGIN  ⚡", style="bold red")
    input("\n  [Press ENTER to start Round 1] ")


def show_round_header(round_num: int, p1: Player, p2: Player) -> None:
    console.clear()
    best_of = ROUNDS_TO_WIN * 2 - 1
    _rule(f" ⚡  ROUND {round_num}  ⚡  (Best of {best_of}) ")
    _show_status(p1, p2)


def prompt_spell(caster: Player, target: Player) -> str:
    _rule(f" {caster.char_name}'s Turn ", style="bold white")
    _show_status(caster, target)
    if caster.last_spell:
        console.print(
            f"  [dim]Last spell: [italic]{caster.last_spell}[/italic] "
            f"— casting it again deals 50% damage.[/dim]"
        )
    console.print(
        "  [dim white](Type [bold]LIST[/bold] to see all spells  |  "
        "[bold]QUIT[/bold] to exit)[/dim white]"
    )
    return Prompt.ask(f"\n  [bold yellow]⚡  {caster.char_name}, cast your spell[/bold yellow]")


def show_invalid(raw: str) -> None:
    console.print(
        f"\n  [bold red]✗  '{raw}' is not a known spell![/bold red]\n"
        f"  [dim]Your wand sparks and fizzles — you lose your turn.[/dim]\n"
    )
    time.sleep(0.8)


def show_resolution(result: dict, caster: Player, target: Player) -> None:
    spell  = result["spell"]
    damage = result["damage"]
    c      = TYPE_COLORS.get(spell["type"], "white")
    traj   = "  ─── ✨ ── ✨ ─── ✨ ──>"
    if spell["type"] == "unforgivable":
        traj = "  ═══ ☠  ══ ☠  ═══ ☠  ══>"
    elif spell["name"].lower() == "expelliarmus":
        traj = "  ~~~~ ✦ ~~ ✦ ~~~~ ✦ ~~>"

    console.print()
    console.print(
        f"  [{c}]{traj}[/{c}]"
        f"  [bold white]{spell['name'].upper()}[/bold white]"
    )
    console.print(f"  [dim italic]{spell['flavor']}[/dim italic]")
    console.print()
    time.sleep(0.35)

    if damage < 0:
        console.print(
            f"  [bold blue]🛡  {caster.char_name} raises a shield — "
            f"restored {abs(damage)} HP![/bold blue]"
        )
    elif spell["type"] == "unforgivable":
        console.print(
            f"  [bold bright_green]☠  {caster.char_name} unleashes "
            f"{spell['name'].upper()}!  "
            f"{target.char_name} takes [bold red]{damage}[/bold red] damage!"
            f"[/bold bright_green]"
        )
    else:
        console.print(
            f"  [{c}]✨  {caster.char_name} casts {spell['name']}!  "
            f"{target.char_name} takes [bold red]{damage}[/bold red] damage![/{c}]"
        )

    for note in result["notes"]:
        console.print(f"     {note}")
    console.print()
    time.sleep(0.7)


def show_round_result(winner: Player, loser: Player, round_num: int) -> None:
    _rule(f" ⚡  Round {round_num} Over  ⚡ ", style="bold red")
    console.print(
        f"\n  [bold green]★  {winner.char_name} wins Round {round_num}!  ★[/bold green]"
    )
    console.print(f"  [dim]{loser.char_name} has fallen.[/dim]\n")
    time.sleep(1.2)


def show_score(p1: Player, p2: Player) -> None:
    _rule(" Scoreboard ", style="yellow")
    for p in (p1, p2):
        stars = "★" * p.rounds_won + "☆" * (ROUNDS_TO_WIN - p.rounds_won)
        console.print(
            f"  [bold yellow]{p.char_name}[/bold yellow]  "
            f"[green]{stars}[/green]  ({p.rounds_won} / {ROUNDS_TO_WIN})"
        )
    console.print()
    input("  [Press ENTER to continue] ")


def show_winner(winner: Player, loser: Player) -> None:
    console.clear()
    console.print(_VICTORY, style="bold yellow", justify="center")
    console.print()
    console.print(
        Align(
            Panel(
                f"[bold yellow]🏆  WINNER: {winner.char_name.upper()}  🏆[/bold yellow]\n\n"
                f"[bold white]Player {winner.num} is victorious![/bold white]\n\n"
                f"[dim]{loser.char_name} has been defeated.[/dim]",
                border_style="yellow", padding=(1, 4),
            ),
            align="center",
        )
    )
    console.print()
    _rule("⚡  Thanks for dueling  ⚡", style="yellow")
    input("\n  [Press ENTER to quit] ")


# ══════════════════════════════════════════════════════════════
#  GAME LOOP
# ══════════════════════════════════════════════════════════════

def run_round(p1: Player, p2: Player, round_num: int) -> Player:
    """Play one round; return the winner."""
    show_round_header(round_num, p1, p2)
    turn_order = [p1, p2]   # p1 always goes first each round

    while p1.alive and p2.alive:
        caster = turn_order[0]
        target = turn_order[1]

        while True:   # inner loop: retry only for LIST, lose turn on bad spell
            raw = prompt_spell(caster, target)

            if raw.strip().upper() in ("QUIT", "Q", "EXIT"):
                console.print("\n  [dim]Mischief managed. Farewell.[/dim]\n")
                sys.exit(0)

            if raw.strip().upper() == "LIST":
                show_spell_list()
                continue   # re-prompt without consuming turn

            result = process_turn(caster, target, raw)

            if not result["valid"]:
                show_invalid(raw)
                break   # turn wasted — swap anyway

            show_resolution(result, caster, target)
            break

        # Swap turn order
        turn_order = [turn_order[1], turn_order[0]]

    # Determine round winner
    if not p1.alive and not p2.alive:
        # Double-KO: whoever took the last shot wins
        return turn_order[1]   # the one who just cast
    return p1 if p2.hp <= 0 else p2


def run_match(p1: Player, p2: Player) -> None:
    show_matchup(p1, p2)

    round_num = 1
    while p1.rounds_won < ROUNDS_TO_WIN and p2.rounds_won < ROUNDS_TO_WIN:
        winner = run_round(p1, p2, round_num)
        loser  = p2 if winner is p1 else p1
        winner.rounds_won += 1
        show_round_result(winner, loser, round_num)

        if p1.rounds_won < ROUNDS_TO_WIN and p2.rounds_won < ROUNDS_TO_WIN:
            show_score(p1, p2)
            p1.reset_for_round()
            p2.reset_for_round()
            round_num += 1

    match_winner = p1 if p1.rounds_won >= ROUNDS_TO_WIN else p2
    match_loser  = p2 if match_winner is p1 else p1
    show_winner(match_winner, match_loser)


def main() -> None:
    try:
        # ── Title screen ──────────────────────────────────────
        console.clear()
        console.print(_TITLE, style="bold yellow", justify="center")
        console.print(
            "\n  [bold white]✦  W I Z A R D I N G   D U E L S  ✦[/bold white]",
            justify="center"
        )
        console.print()
        _rule("⚡  Press ENTER to begin  ⚡", style="yellow")
        input()

        # ── Character & wand selection ────────────────────────
        ck1 = select_character(1)
        wk1 = select_wand(1, ck1)
        ck2 = select_character(2)
        wk2 = select_wand(2, ck2)

        p1 = Player(1, ck1, wk1)
        p2 = Player(2, ck2, wk2)

        if p1.char_key == p2.char_key:
            console.print(
                f"\n  [bold yellow]⚡  Mirror match!  Both chose "
                f"{p1.char_name}. Interesting...[/bold yellow]\n"
            )

        # ── Run the match ─────────────────────────────────────
        run_match(p1, p2)

    except (KeyboardInterrupt, EOFError):
        console.print("\n\n  [dim]Departing Hogwarts...[/dim]\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
