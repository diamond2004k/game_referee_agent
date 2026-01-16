# Rock–Paper–Scissors–Plus

A command-line game in Python that extends the classic Rock–Paper–Scissors game with a special **"bomb"** move. Play against a bot and enjoy a best-of-three rounds challenge.

---

## Features

- Classic Rock–Paper–Scissors gameplay
- **Special move:** `bomb` (can only be used once per game per player)
- Bot with random move logic, including `bomb`
- Score tracking for each round
- Detailed round history
- Optional Google ADK integration for tool-based game management

---

## Gameplay Rules

1. The game is **best of 3 rounds**.
2. Valid moves:  
   - `rock`  
   - `paper`  
   - `scissors`  
   - `bomb` (once per game)
3. **Bomb** overrides normal moves and guarantees a win unless both players use it simultaneously.
4. Invalid moves will **waste the round**.
5. Scores are tracked after each round and a final winner is announced at the end.

---

1. (Optional) Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. Install dependencies (for using Google ADK, otherwise no extra packages needed):

```bash
pip install -r requirements.txt
```

---

## How to Play

Run the game:

```bash
python withADK.py
```

Follow the prompts:

1. Enter your move (`rock`, `paper`, `scissors`, `bomb`)
2. The bot will randomly select its move
3. Scores and results are displayed after each round
4. After 3 rounds, the final winner is announced

---

## Code Structure

* `initialize_game_state()` – Sets up initial game state
* `validate_move()` – Ensures user input is valid and enforces bomb usage
* `resolve_round()` – Determines the winner of a round
* `update_game_state()` – Updates scores and round history
* `get_bot_move()` – Bot logic for selecting moves
* `play_round()` – Handles a single round
* `play_game()` – Main game loop
* `Agent` & `tool` – Optional Google ADK integration

---

## Example Output

```
Welcome to Rock–Paper–Scissors–Plus!
Rules:
- Best of 3 rounds
- Moves: rock, paper, scissors, bomb (once only)
- Invalid input wastes the round

Round 1/3
Enter your move: rock
You played: rock
Bot played: scissors
Result: You win this round!
Score → You: 1 | Bot: 0
```
Do you want me to do that too?
```
