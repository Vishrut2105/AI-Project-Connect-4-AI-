Intelligent Connect-4 AI (Minimax with Alpha-Beta Pruning & Heuristic Evaluation)

Course: B.Tech Information Technology (Semester V)
Subject: Artificial Intelligence (Course Code: 202044503)
Topic: Unit 3 - Game Playing & Planning / Adversarial Search (Related to Practical #9)
Team Members:
- Vishrut Sharma (12402080601153)
- Yatharth Metha (12402080601160)
- Ved Tailor (12402080601145)

1. Project Overview
This project implements an intelligent game-playing agent for Connect-4 (a 2-player zero-sum connection game on a 6x7 vertical grid) using the Minimax Algorithm enhanced with Alpha-Beta Cut-offs (Pruning) and a custom Heuristic Evaluation Function.

Connect-4 has over 4.5 trillion valid game states. This project implements:
- Depth-Limited Minimax Search (Depth 2 to 6)
- Alpha-Beta Pruning to prune unpromising branches
- Move Ordering Optimization (center column priority for maximum cutoffs)
- Heuristic Evaluation Function (sliding 4-cell window scoring)

2. Key Features
- Minimax Search with Alpha-Beta Pruning
- Live AI Search Analytics: Nodes Explored, Alpha-Beta Cutoffs, and Compute Time
- Adjustable Difficulty: Easy (Depth 2), Medium (Depth 4), Hard (Depth 5), Master (Depth 6)
- Interactive Hover Preview of dropping disc
- Winning Streak Highlight: Glowing ring around the winning 4 tokens
- Persistent Session Scoreboard: Human Wins, AI Wins, Draws
- Instant Restart / Rematch Dialog
- Zero External Dependencies: Standard Python library only (tkinter)

3. Tech Stack
- Programming Language: Python 3 (3.8+)
- GUI Framework: tkinter (Standard Library)
- Dependencies: None (pip install is NOT required)

4. How to Run the Project
Step 1: Open the folder in VS Code / Terminal
Step 2: Run:
python connect4_ai.py
