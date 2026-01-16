from typing import Dict
import random

# --- Google ADK imports ---
try:
    from google.adk import Agent, tool
except ImportError:
    def tool(func):
        return func

    class Agent:
        def __init__(self, name, description, tools):
            self.name = name
            self.description = description
            self.tools = tools


# ----------------------------
# Constants & Rules
# ----------------------------

VALID_MOVES = ["rock", "paper", "scissors", "bomb"]

WIN_RULES = {
    ("rock", "scissors"),
    ("scissors", "paper"),
    ("paper", "rock")
}


# ----------------------------
# Game State Initialization
# ----------------------------

def initialize_game_state() -> Dict:
    return {
        "round": 1,
        "max_rounds": 3,
        "user_score": 0,
        "bot_score": 0,
        "user_bomb_used": False,
        "bot_bomb_used": False,
        "history": []
    }


# ----------------------------
# ADK TOOLS
# ----------------------------

@tool
def validate_move(move: str, bomb_used: bool) -> Dict:
    """
    Validates user input and enforces bomb usage constraint.
    """
    move = move.lower().strip()

    if move not in VALID_MOVES:
        return {"valid": False, "reason": "Invalid move"}

    if move == "bomb" and bomb_used:
        return {"valid": False, "reason": "Bomb already used"}

    return {"valid": True, "reason": "OK", "move": move}


@tool
def resolve_round(user_move: str, bot_move: str) -> str:
    """
    Determines the winner of a round based on game rules.
    """
    if user_move == "bomb" and bot_move == "bomb":
        return "draw"
    if user_move == "bomb":
        return "user"
    if bot_move == "bomb":
        return "bot"

    if user_move == bot_move:
        return "draw"

    if (user_move, bot_move) in WIN_RULES:
        return "user"

    return "bot"


@tool
def update_game_state(
    state: Dict,
    result: str,
    user_move: str,
    bot_move: str
) -> Dict:
    """
    Mutates and persists game state after each round.
    """
    if user_move == "bomb":
        state["user_bomb_used"] = True
    if bot_move == "bomb":
        state["bot_bomb_used"] = True

    if result == "user":
        state["user_score"] += 1
    elif result == "bot":
        state["bot_score"] += 1

    state["history"].append({
        "round": state["round"],
        "user_move": user_move,
        "bot_move": bot_move,
        "winner": result
    })

    state["round"] += 1
    return state


# ----------------------------
# Bot Move Logic
# ----------------------------

def get_bot_move(bot_bomb_used: bool) -> str:
    possible_moves = ["rock", "paper", "scissors"]
    if not bot_bomb_used:
        possible_moves.append("bomb")
    return random.choice(possible_moves)


# ----------------------------
# ADK Agent Definition
# ----------------------------

game_referee_agent = Agent(
    name="game_referee_agent",
    description="Referee agent for Rock–Paper–Scissors–Plus",
    tools=[validate_move, resolve_round, update_game_state]
)


# ----------------------------
# Game Flow
# ----------------------------

def explain_rules():
    print("Welcome to Rock–Paper–Scissors–Plus!")
    print("Rules:")
    print("- Best of 3 rounds")
    print("- Moves: rock, paper, scissors, bomb (once only)")
    print("- Invalid input wastes the round\n")


def play_round(state: Dict) -> Dict:
    print(f"Round {state['round']}/{state['max_rounds']}")
    user_input = input("Enter your move: ")

    validation = validate_move(user_input, state["user_bomb_used"])

    if not validation["valid"]:
        print(f"Invalid move: {validation['reason']}. Round wasted.\n")
        state["round"] += 1
        return state

    user_move = validation["move"]
    bot_move = get_bot_move(state["bot_bomb_used"])

    result = resolve_round(user_move, bot_move)
    state = update_game_state(state, result, user_move, bot_move)

    print(f"You played: {user_move}")
    print(f"Bot played: {bot_move}")

    if result == "draw":
        print("Result: Draw")
    elif result == "user":
        print("Result: You win this round!")
    else:
        print("Result: Bot wins this round!")

    print(f"Score → You: {state['user_score']} | Bot: {state['bot_score']}\n")
    return state


def play_game():
    state = initialize_game_state()
    explain_rules()

    while state["round"] <= state["max_rounds"]:
        state = play_round(state)

    print("Game Over!")
    if state["user_score"] > state["bot_score"]:
        print("Final Result: You Win 🎉")
    elif state["bot_score"] > state["user_score"]:
        print("Final Result: Bot Wins 🤖")
    else:
        print("Final Result: It's a Draw 🤝")


# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":
    play_game()
