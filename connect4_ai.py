"""
Connect-4 AI with Minimax and Alpha-Beta Pruning
Subject: Artificial Intelligence (Course Code: 202044503) - Semester V
Unit 3: Game Playing & Planning / Adversarial Search

Team Members:
- Vishrut Sharma (12402080601153)
- Yatharth Metha (12402080601160)
- Ved Tailor (12402080601145)
"""

import tkinter as tk
from tkinter import messagebox
import math
import random
import time

# --- Board Dimensions & Constants ---
ROWS = 6
COLS = 7
WINDOW_LENGTH = 4

EMPTY = 0
HUMAN_PIECE = 1  # Red
AI_PIECE = 2     # Yellow

# Column exploration order prioritizing center for maximum alpha-beta cutoffs
COL_ORDER = [3, 2, 4, 1, 5, 0, 6]

# Visual Palette
COLOR_BG = "#131625"
COLOR_PANEL = "#1b1f38"
COLOR_BOARD = "#1f2a58"
COLOR_SLOT_EMPTY = "#0d1127"
COLOR_HUMAN = "#ff3b5c"       # Bright Red
COLOR_HUMAN_HOVER = "#ff758f"
COLOR_AI = "#ffc107"          # Vivid Amber / Gold
COLOR_WIN_GLOW = "#00e676"    # Emerald Green highlight for winning streak
COLOR_TEXT = "#e0e6ed"
COLOR_MUTED = "#8b9bb4"
COLOR_ACCENT = "#4f46e5"

class Connect4AI:
    """Game logic and Minimax search agent with Alpha-Beta Pruning."""

    def __init__(self):
        self.nodes_explored = 0
        self.cutoffs = 0

    def create_board(self):
        return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return 0 <= col < COLS and board[0][col] == EMPTY

    def get_next_open_row(self, board, col):
        for r in range(ROWS - 1, -1, -1):
            if board[r][col] == EMPTY:
                return r
        return None

    def get_valid_locations(self, board):
        return [col for col in COL_ORDER if self.is_valid_location(board, col)]

    def winning_move(self, board, piece):
        """Checks if the piece player has 4 in a row. Returns (is_win, winning_coords)."""
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(board[r][c + i] == piece for i in range(4)):
                    return True, [(r, c + i) for i in range(4)]

        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(board[r + i][c] == piece for i in range(4)):
                    return True, [(r + i, c) for i in range(4)]

        # Positively sloped diagonals
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(board[r + i][c + i] == piece for i in range(4)):
                    return True, [(r + i, c + i) for i in range(4)]

        # Negatively sloped diagonals
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(board[r - i][c + i] == piece for i in range(4)):
                    return True, [(r - i, c + i) for i in range(4)]

        return False, []

    def is_terminal_node(self, board):
        ai_win, _ = self.winning_move(board, AI_PIECE)
        if ai_win:
            return True
        human_win, _ = self.winning_move(board, HUMAN_PIECE)
        if human_win:
            return True
        return len(self.get_valid_locations(board)) == 0

    def evaluate_window(self, window, piece):
        opp_piece = HUMAN_PIECE if piece == AI_PIECE else AI_PIECE
        score = 0

        p_count = window.count(piece)
        empty_count = window.count(EMPTY)
        opp_count = window.count(opp_piece)

        if p_count == 4:
            score += 100000
        elif p_count == 3 and empty_count == 1:
            score += 120
        elif p_count == 2 and empty_count == 2:
            score += 15

        if opp_count == 3 and empty_count == 1:
            score -= 140  # Heavily penalize letting opponent reach 3-in-a-row
        elif opp_count == 2 and empty_count == 2:
            score -= 10

        return score

    def score_position(self, board, piece):
        """Heuristic evaluation function for non-terminal states."""
        score = 0

        # Preference for center column control
        center_array = [board[r][COLS // 2] for r in range(ROWS)]
        center_count = center_array.count(piece)
        score += center_count * 30

        # Horizontal scoring
        for r in range(ROWS):
            row_array = board[r]
            for c in range(COLS - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Vertical scoring
        for c in range(COLS):
            col_array = [board[r][c] for r in range(ROWS)]
            for r in range(ROWS - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Positively sloped diagonal
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        # Negatively sloped diagonal
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with Alpha-Beta Pruning.
        Returns: (best_col, best_score)
        """
        self.nodes_explored += 1
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                ai_win, _ = self.winning_move(board, AI_PIECE)
                if ai_win:
                    return None, 1000000 + depth  # Prefer faster wins
                human_win, _ = self.winning_move(board, HUMAN_PIECE)
                if human_win:
                    return None, -1000000 - depth  # Delay inevitable loss
                return None, 0  # Draw
            else:
                return None, self.score_position(board, AI_PIECE)

        if maximizing_player:
            value = -math.inf
            best_col = valid_locations[0] if valid_locations else 0
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                # Create board copy for simulation
                temp_board = [row_vals[:] for row_vals in board]
                self.drop_piece(temp_board, row, col, AI_PIECE)
                _, new_score = self.minimax(temp_board, depth - 1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    self.cutoffs += 1
                    break  # Beta cut-off
            return best_col, value
        else:
            value = math.inf
            best_col = valid_locations[0] if valid_locations else 0
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                temp_board = [row_vals[:] for row_vals in board]
                self.drop_piece(temp_board, row, col, HUMAN_PIECE)
                _, new_score = self.minimax(temp_board, depth - 1, alpha, beta, True)
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    self.cutoffs += 1
                    break  # Alpha cut-off
            return best_col, value


class Connect4GUI:
    """Sleek Desktop GUI for Connect-4 AI using Tkinter."""

    def __init__(self, root):
        self.root = root
        self.root.title("Connect-4 AI (Minimax & Alpha-Beta Pruning) | Sem 5 AI Project")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        self.engine = Connect4AI()
        self.board = self.engine.create_board()
        self.game_over = False
        self.turn = HUMAN_PIECE  # Human starts by default
        self.winning_cells = []

        # Stats
        self.human_wins = 0
        self.ai_wins = 0
        self.draws = 0

        # Difficulty: (depth, label)
        self.difficulty_var = tk.StringVar(value="Hard (Depth 5)")
        self.depth_map = {
            "Easy (Depth 2)": 2,
            "Medium (Depth 4)": 4,
            "Hard (Depth 5)": 5,
            "Master (Depth 6)": 6
        }

        self.hover_col = None
        self.slot_radius = 28
        self.cell_size = 72

        self.build_ui()
        self.update_board_canvas()

    def build_ui(self):
        # Header / Title Card
        header_frame = tk.Frame(self.root, bg=COLOR_BG)
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 8))

        title_label = tk.Label(
            header_frame,
            text="🔴 CONNECT-4 AI 🟡",
            font=("Segoe UI", 18, "bold"),
            fg="#ffffff",
            bg=COLOR_BG
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Adversarial Search • Minimax with Alpha-Beta Cutoffs & Heuristic Evaluation",
            font=("Segoe UI", 9),
            fg=COLOR_MUTED,
            bg=COLOR_BG
        )
        subtitle_label.pack(pady=(2, 0))

        # Score & Status Bar
        top_bar = tk.Frame(self.root, bg=COLOR_PANEL, bd=1, relief=tk.SOLID)
        top_bar.pack(fill=tk.X, padx=20, pady=5)

        # Score widgets
        score_frame = tk.Frame(top_bar, bg=COLOR_PANEL)
        score_frame.pack(side=tk.LEFT, padx=15, pady=8)

        self.score_label = tk.Label(
            score_frame,
            text=f"Score  —  You (Red): {self.human_wins}  |  AI (Yellow): {self.ai_wins}  |  Draws: {self.draws}",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT,
            bg=COLOR_PANEL
        )
        self.score_label.pack(side=tk.LEFT)

        # Turn indicator
        self.status_badge = tk.Label(
            top_bar,
            text="Your Turn (Red)",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg=COLOR_HUMAN,
            padx=12,
            pady=4
        )
        self.status_badge.pack(side=tk.RIGHT, padx=15, pady=6)

        # Control Strip (Difficulty & Starter)
        ctrl_strip = tk.Frame(self.root, bg=COLOR_BG)
        ctrl_strip.pack(fill=tk.X, padx=20, pady=4)

        diff_lbl = tk.Label(ctrl_strip, text="Difficulty / Depth:", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT, bg=COLOR_BG)
        diff_lbl.pack(side=tk.LEFT, padx=(0, 6))

        for opt in ["Easy (Depth 2)", "Medium (Depth 4)", "Hard (Depth 5)"]:
            rb = tk.Radiobutton(
                ctrl_strip,
                text=opt.split()[0],
                variable=self.difficulty_var,
                value=opt,
                font=("Segoe UI", 9),
                fg=COLOR_TEXT,
                bg=COLOR_BG,
                activebackground=COLOR_BG,
                activeforeground=COLOR_TEXT,
                selectcolor=COLOR_PANEL,
                cursor="hand2"
            )
            rb.pack(side=tk.LEFT, padx=3)

        first_btn = tk.Button(
            ctrl_strip,
            text="Let AI Play First",
            command=self.set_ai_first,
            font=("Segoe UI", 9, "bold"),
            bg="#374151",
            fg="#ffffff",
            activebackground="#4b5563",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=8,
            pady=2,
            cursor="hand2"
        )
        first_btn.pack(side=tk.RIGHT)

        # Connect 4 Canvas
        canvas_width = COLS * self.cell_size
        canvas_height = ROWS * self.cell_size

        self.canvas_frame = tk.Frame(self.root, bg=COLOR_BOARD, padx=8, pady=8, bd=2, relief=tk.RIDGE)
        self.canvas_frame.pack(padx=20, pady=10)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg=COLOR_BOARD,
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack()

        # Canvas Event bindings
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_hover)
        self.canvas.bind("<Leave>", self.on_canvas_leave)

        # Live AI Analytics Bar (Node counter & pruning live metric)
        analytics_frame = tk.Frame(self.root, bg=COLOR_PANEL, bd=1, relief=tk.SOLID)
        analytics_frame.pack(fill=tk.X, padx=20, pady=4)

        self.analytics_label = tk.Label(
            analytics_frame,
            text="AI Engine Ready • Nodes Explored: 0 • Alpha-Beta Cutoffs: 0 • Compute Time: 0.00s",
            font=("Consolas", 9),
            fg="#93c5fd",
            bg=COLOR_PANEL,
            pady=6
        )
        self.analytics_label.pack()

        # Bottom Button Bar
        btn_bar = tk.Frame(self.root, bg=COLOR_BG)
        btn_bar.pack(fill=tk.X, padx=20, pady=(10, 15))

        reset_btn = tk.Button(
            btn_bar,
            text="🔄  Restart / Play Again",
            command=self.reset_game,
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_ACCENT,
            fg="#ffffff",
            activebackground="#4338ca",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor="hand2"
        )
        reset_btn.pack(side=tk.LEFT)

        info_btn = tk.Button(
            btn_bar,
            text="ℹ️  How AI Works (Viva Guide)",
            command=self.show_algorithm_info,
            font=("Segoe UI", 10),
            bg="#2d3748",
            fg="#e2e8f0",
            activebackground="#4a5568",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=8,
            cursor="hand2"
        )
        info_btn.pack(side=tk.RIGHT)

    def update_board_canvas(self):
        self.canvas.delete("all")

        for r in range(ROWS):
            for c in range(COLS):
                cx = c * self.cell_size + self.cell_size / 2
                cy = r * self.cell_size + self.cell_size / 2
                rad = self.slot_radius

                val = self.board[r][c]
                is_win_cell = (r, c) in self.winning_cells

                # Base slot color
                if val == EMPTY:
                    # Hover preview for next open slot in this column
                    next_open = self.engine.get_next_open_row(self.board, c)
                    if self.hover_col == c and r == next_open and not self.game_over and self.turn == HUMAN_PIECE:
                        color = COLOR_HUMAN_HOVER
                    else:
                        color = COLOR_SLOT_EMPTY
                    outline_color = "#232946"
                    width = 1
                elif val == HUMAN_PIECE:
                    color = COLOR_HUMAN
                    outline_color = COLOR_WIN_GLOW if is_win_cell else "#b91c1c"
                    width = 4 if is_win_cell else 2
                else:  # AI_PIECE
                    color = COLOR_AI
                    outline_color = COLOR_WIN_GLOW if is_win_cell else "#d97706"
                    width = 4 if is_win_cell else 2

                # Draw outer glow circle if winning cell
                if is_win_cell:
                    self.canvas.create_oval(
                        cx - rad - 4, cy - rad - 4,
                        cx + rad + 4, cy + rad + 4,
                        outline=COLOR_WIN_GLOW,
                        width=3
                    )

                self.canvas.create_oval(
                    cx - rad, cy - rad,
                    cx + rad, cy + rad,
                    fill=color,
                    outline=outline_color,
                    width=width
                )

                # Inner shine effect for 3D look
                if val != EMPTY:
                    self.canvas.create_oval(
                        cx - rad + 6, cy - rad + 5,
                        cx - rad + 18, cy - rad + 14,
                        fill="#ffffff",
                        outline="",
                        stipple="gray50"
                    )

    def on_canvas_hover(self, event):
        if self.game_over or self.turn != HUMAN_PIECE:
            return
        col = event.x // self.cell_size
        if 0 <= col < COLS and col != self.hover_col:
            self.hover_col = col
            self.update_board_canvas()

    def on_canvas_leave(self, event):
        self.hover_col = None
        self.update_board_canvas()

    def on_canvas_click(self, event):
        if self.game_over or self.turn != HUMAN_PIECE:
            return

        col = event.x // self.cell_size
        if not (0 <= col < COLS):
            return

        if not self.engine.is_valid_location(self.board, col):
            return

        # Human makes move
        row = self.engine.get_next_open_row(self.board, col)
        self.engine.drop_piece(self.board, row, col, HUMAN_PIECE)
        self.hover_col = None
        self.update_board_canvas()

        # Check win / draw
        is_win, coords = self.engine.winning_move(self.board, HUMAN_PIECE)
        if is_win:
            self.winning_cells = coords
            self.game_over = True
            self.human_wins += 1
            self.update_stats()
            self.status_badge.config(text="🎉 You Win!", bg="#10b981")
            self.update_board_canvas()
            self.root.after(300, lambda: self.prompt_replay("Congratulations! You beat the AI!"))
            return

        if len(self.engine.get_valid_locations(self.board)) == 0:
            self.game_over = True
            self.draws += 1
            self.update_stats()
            self.status_badge.config(text="Game Drawn!", bg="#6b7280")
            self.root.after(300, lambda: self.prompt_replay("Game ended in a draw!"))
            return

        # Switch to AI
        self.turn = AI_PIECE
        self.status_badge.config(text="AI Thinking...", bg=COLOR_AI, fg="#000000")
        self.root.update_idletasks()

        # Small delay so user sees move, then AI moves
        self.root.after(120, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return

        depth_str = self.difficulty_var.get()
        depth = self.depth_map.get(depth_str, 5)

        self.engine.nodes_explored = 0
        self.engine.cutoffs = 0

        start_time = time.time()
        col, _ = self.engine.minimax(self.board, depth, -math.inf, math.inf, True)
        elapsed = time.time() - start_time

        # Update Live Analytics
        self.analytics_label.config(
            text=f"AI Search: Depth {depth} | Nodes: {self.engine.nodes_explored:,} | "
                 f"Alpha-Beta Cutoffs: {self.engine.cutoffs:,} | Time: {elapsed:.3f}s"
        )

        if col is not None and self.engine.is_valid_location(self.board, col):
            row = self.engine.get_next_open_row(self.board, col)
            self.engine.drop_piece(self.board, row, col, AI_PIECE)
            self.update_board_canvas()

            # Check win / draw
            is_win, coords = self.engine.winning_move(self.board, AI_PIECE)
            if is_win:
                self.winning_cells = coords
                self.game_over = True
                self.ai_wins += 1
                self.update_stats()
                self.status_badge.config(text="AI Wins!", bg="#ef4444", fg="#ffffff")
                self.update_board_canvas()
                self.root.after(300, lambda: self.prompt_replay("AI won this match!"))
                return

            if len(self.engine.get_valid_locations(self.board)) == 0:
                self.game_over = True
                self.draws += 1
                self.update_stats()
                self.status_badge.config(text="Game Drawn!", bg="#6b7280", fg="#ffffff")
                self.root.after(300, lambda: self.prompt_replay("Game ended in a draw!"))
                return

        # Back to Human turn
        self.turn = HUMAN_PIECE
        self.status_badge.config(text="Your Turn (Red)", bg=COLOR_HUMAN, fg="#ffffff")

    def set_ai_first(self):
        if any(self.board[r][c] != EMPTY for r in range(ROWS) for c in range(COLS)):
            if not messagebox.askyesno("Reset Board?", "This will reset the board for AI to play first. Continue?"):
                return
        self.reset_game()
        self.turn = AI_PIECE
        self.status_badge.config(text="AI Thinking...", bg=COLOR_AI, fg="#000000")
        self.root.after(200, self.ai_move)

    def update_stats(self):
        self.score_label.config(
            text=f"Score  —  You (Red): {self.human_wins}  |  AI (Yellow): {self.ai_wins}  |  Draws: {self.draws}"
        )

    def reset_game(self):
        self.board = self.engine.create_board()
        self.game_over = False
        self.turn = HUMAN_PIECE
        self.winning_cells = []
        self.hover_col = None
        self.status_badge.config(text="Your Turn (Red)", bg=COLOR_HUMAN, fg="#ffffff")
        self.update_board_canvas()

    def prompt_replay(self, msg):
        res = messagebox.askyesno("Game Over", f"{msg}\n\nWould you like to play another round?")
        if res:
            self.reset_game()

    def show_algorithm_info(self):
        info_text = (
            "🧠 Connect-4 AI Technical Breakdown (Viva Q&A):\n\n"
            "1. Minimax Algorithm:\n"
            "   A recursive decision-making algorithm for 2-player zero-sum games. "
            "The AI maximizes the board evaluation score while simulating an opponent who minimizes it.\n\n"
            "2. Alpha-Beta Pruning:\n"
            "   Alpha (best score for Maximizer) and Beta (best score for Minimizer). "
            "When Alpha >= Beta, the remaining subtree cannot influence the optimal outcome and is cut off. "
            "This reduces time complexity from O(b^d) down towards O(b^(d/2)).\n\n"
            "3. Center-Column Move Ordering:\n"
            "   Examining column 3 first triggers maximum beta-cutoffs early, vastly accelerating the search.\n\n"
            "4. Heuristic Evaluation Function:\n"
            "   Scoring 4-cell sliding windows across horizontal, vertical, and diagonals: "
            "4-in-a-row (+100,000), 3-in-a-row with open slot (+120), center column control (+30)."
        )
        messagebox.showinfo("Algorithm & Viva Guide", info_text)


if __name__ == "__main__":
    app_root = tk.Tk()
    app = Connect4GUI(app_root)
    app_root.mainloop()
