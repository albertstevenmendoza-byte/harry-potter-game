# ⚡ HP Duel — Wizarding Duels in Your Terminal

A fully-featured, turn-based 2-player Harry Potter dueling game played in your
terminal.  Built with Python 3.10+ and the [Rich](https://github.com/Textualize/rich)
library for a cinematic UI.

---

## 🧙 Features

- **5 playable characters** — Harry, Hermione, Ron, Voldemort, Snape — unique HP & bonuses  
- **5 wands** — Holly, Vine, Elder, Walnut, Ash — each with a spell-affinity bonus  
- **20 canonical Harry Potter spells** — Expelliarmus to Avada Kedavra  
- **Spell validation** — type a real spell or lose your turn  
- **Diminishing returns** — spam the same spell for only 50 % damage  
- **Best-of-5 format** — first to 3 round wins takes the match  
- **Rich terminal UI** — HP bars, spell trajectories, panels, colour  

---

## 🗂 Files

```
hp_duel/
├── hp_duel.py        ← the whole game (single file)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Running

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/hp-duel.git
cd hp-duel

# 2. Virtual env (recommended)
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install
pip install -r requirements.txt

# 4. Play
python hp_duel.py
```

---

## 🎮 How to Play

1. Each player picks a **character** (enter the name, e.g. `harry`).
2. Each player picks a **wand** (enter the wood name, e.g. `elder`).
3. On your turn, **type a spell name** and press Enter.
   - Type `LIST` to see all spells and their damage (free action — no turn lost).
   - Type `QUIT` to exit.
4. **Invalid spell** → your turn is wasted.
5. **Casting the same spell twice in a row** → 50 % damage.
6. First player to win **3 rounds** wins the match.

---

## 📜 Licence

MIT — wield responsibly.
