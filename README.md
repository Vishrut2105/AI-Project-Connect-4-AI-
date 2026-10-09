# Intelligent Connect-4 AI (Minimax with Alpha-Beta Pruning & Heuristic Evaluation)

**Course:** B.Tech Information Technology (Semester V)  
**Subject:** Artificial Intelligence (Course Code: 202044503)  
**Topic:** Unit 3 - Game Playing & Planning / Adversarial Search (Related to Practical #9)  
**Team Members:** 
- Vishrut Sharma (12402080601153)
- Yatharth Metha (12402080601160)
- Ved Tailor (12402080601145)

---

## 1. Project Overview

This project implements an intelligent game-playing agent for **Connect-4** (a 2-player zero-sum connection game on a $6 \times 7$ vertical grid) using the **Minimax Algorithm** enhanced with **Alpha-Beta Cut-offs (Pruning)** and a custom **Heuristic Evaluation Function**.

Unlike Tic-Tac-Toe (which has a tiny state space of ~250,000 states), Connect-4 has over **$4.5 \times 10^{12}$ valid game states**. Therefore, this project implements a production-grade AI search architecture:
1. **Depth-Limited Minimax Search:** Evaluates scenarios up to configurable depths (e.g., Depth 4 to 6).
2. **Alpha-Beta Pruning:** Dramatically cuts unpromising branches, reducing the effective branching factor.
3. **Move Ordering Optimization:** Evaluates moves starting from the central columns (where strategic control is highest), maximizing early Alpha-Beta cut-offs.
4. **Heuristic Evaluation Function:** Evaluates incomplete board states using sliding 4-cell window scoring (center control, 3-in-a-row with open threats, double-threat setups).

---

## 2. Key Features

- 🧠 **Minimax Search with Alpha-Beta Pruning:** Intelligent lookahead decisions that block human attacks and execute winning setups.
- ⚡ **Live AI Search Analytics:** Real-time counter of **Nodes Explored**, **Alpha-Beta Cutoffs**, and **Compute Time (seconds)** on every turn—ideal for live demonstration during evaluation.
- 🎚️ **Adjustable Difficulty / Search Depth:**
  - Easy (Depth 2)
  - Medium (Depth 4)
  - Hard (Depth 5)
  - Master (Depth 6)
- 🔴 **Interactive Hover Preview:** Moving the mouse over any column previews the dropping slot with animated color feedback.
- 🏆 **Winning Streak Highlight:** Automatically identifies and illuminates the connected 4 tokens with a glowing green ring upon game completion.
- 📊 **Persistent Session Scoreboard:** Tracks Player (Red) Wins, AI (Yellow) Wins, and Draws.
- 🔄 **Restart & Rematch Options:** Includes an instant reset button, "Let AI Play First" toggle, and automatic rematch dialog.
- 📦 **Zero External Dependencies:** Built using Python's standard library (`tkinter`, `math`, `time`, `random`). No `pip install` required!

---

## 3. Tech Stack

- **Programming Language:** Python 3 (3.8+)
- **GUI Framework:** `tkinter` (Standard Library)
- **Dependencies:** None (`pip install` is NOT required)

---

## 4. How to Run the Project

### Step 1: Open the Project in VS Code
Open the `AI project Sem 5` folder in VS Code or any terminal.

### Step 2: Run the Application
Run the Python script directly:

```bash
python connect4_ai.py
```

---

## 5. Mathematical & Algorithmic Formulation

### Minimax Principle
The game tree alternates between:
- **MAX Node (AI):** Aims to maximize the evaluation function score:
  $$\text{Score}(s) = \max_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a))$$
- **MIN Node (Human):** Assumed to play rationally to minimize the AI's score:
  $$\text{Score}(s) = \min_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a))$$

### Alpha-Beta Pruning
- $\alpha$: Highest score guaranteed to the Maximizer so far.
- $\beta$: Lowest score guaranteed to the Minimizer so far.
- **Condition for Cutoff:** Whenever $\alpha \ge \beta$, the current branch is pruned because a rational opponent would never allow the game state to enter this path.
- Reduces theoretical search time from $\mathcal{O}(b^d)$ towards $\mathcal{O}(b^{d/2})$.

### Heuristic Window Scoring
For sliding 4-slot windows:
- 4 AI tokens: $+100,000$ (Instant Win)
- 3 AI tokens + 1 Empty: $+120$ (Direct Win Threat)
- 2 AI tokens + 2 Empty: $+15$
- Center column occupancy: $+30$ per piece (Central columns form more horizontal, vertical, and diagonal lines)
- 3 Opponent tokens + 1 Empty: $-140$ (Defensive Emergency Block)

---
