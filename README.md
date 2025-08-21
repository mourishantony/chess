# ♟️ Python Chess Game

A fully functional chess game built with Python, featuring both player-vs-player and player-vs-AI modes. The game includes a complete chess engine with move validation, special moves (castling, en passant, pawn promotion), and three difficulty levels of AI opponents.

## 🎮 Features

### Core Gameplay
- **Complete Chess Rules**: All standard chess rules implemented including castling, en passant, pawn promotion, and check/checkmate detection
- **Move Validation**: Real-time validation of legal moves
- **Undo/Redo**: Full move history with undo functionality
- **Game States**: Checkmate and stalemate detection

### Game Modes
- **Player vs Player**: Local two-player mode
- **Player vs AI**: Three difficulty levels:
  - **Easy**: Random move selection
  - **Medium**: Basic Minimax algorithm (depth 1)
  - **Hard**: Advanced Minimax algorithm (depth 2)

### User Interface
- **Interactive GUI**: Built with Pygame
- **Visual Feedback**: 
  - Highlighted selected pieces
  - Possible move indicators
  - Move history display
  - Game status notifications
- **Pawn Promotion**: Visual selection menu for promoted pieces
- **Move Animation**: Smooth piece movement animations

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Setup
1. Clone or download this repository
2. Install required dependencies:
```bash
pip install pygame
```

3. Run the game:
```bash
python ChessGame.py
```

## 🎯 How to Play

### Starting the Game
1. Launch `ChessGame.py`
2. Choose your game mode from the main menu:
   - **Player vs Player**: Two humans play against each other
   - **Player vs AI**: Play against the computer
3. If playing against AI, select difficulty level:
   - **Easy**: Random moves
   - **Medium**: Basic strategy
   - **Hard**: More challenging AI

### Controls
- **Mouse**: Select and move pieces
- **Z Key**: Undo last move
- **R Key**: Reset game
- **Undo Button**: Click to undo last move
- **Reset Button**: Click to start new game

### Game Rules
- **White always moves first**
- **Check**: Your king is under attack
- **Checkmate**: Game ends when king is in check with no legal moves
- **Stalemate**: Game ends in draw when no legal moves but not in check
- **Pawn Promotion**: When a pawn reaches the opposite end, promote to Queen, Rook, Bishop, or Knight
- **Castling**: Move king and rook simultaneously under specific conditions
- **En Passant**: Special pawn capture move

## 🏗️ Project Structure

```
chess/
├── ChessEngine.py      # Core chess engine and AI
├── ChessGame.py        # Pygame GUI and main game loop
├── README.md          # This file
└── images/            # Chess piece sprites
    ├── bB.png         # Black Bishop
    ├── bK.png         # Black King
    ├── bN.png         # Black Knight
    ├── bp.png         # Black Pawn
    ├── bQ.png         # Black Queen
    ├── bR.png         # Black Rook
    ├── wB.png         # White Bishop
    ├── wK.png         # White King
    ├── wN.png         # White Knight
    ├── wp.png         # White Pawn
    ├── wQ.png         # White Queen
    └── wR.png         # White Rook
```

## 🧠 Technical Details

### Chess Engine (`ChessEngine.py`)
- **GameState Class**: Manages the complete game state
- **Move Generation**: Efficient move calculation for all pieces
- **AI Implementation**: Minimax algorithm with configurable depth
- **Position Evaluation**: Material-based scoring system

### GUI System (`ChessGame.py`)
- **Pygame Integration**: Smooth 60 FPS rendering
- **Responsive Design**: Handles window resizing and mouse events
- **Visual Effects**: Animated piece movements and highlights
- **Menu System**: Intuitive game mode and difficulty selection

### Key Classes
- `GameState`: Core game logic and state management
- `Move`: Represents individual chess moves with validation
- `AIPlayer`: Computer opponent with three difficulty levels
- `CastleRights`: Manages castling permissions

## 🎨 Customization

### Adding New Features
The modular design makes it easy to extend functionality:

1. **New AI Strategies**: Modify `AIPlayer` class in `ChessEngine.py`
2. **UI Themes**: Change colors in `ChessGame.py` constants
3. **Additional Game Modes**: Extend the main menu system
4. **Piece Images**: Replace images in the `images/` folder

### Configuration
Key constants in `ChessGame.py`:
- `WIDTH`, `HEIGHT`: Board dimensions
- `MAX_FPS`: Animation smoothness
- `SQ_SIZE`: Individual square size

## 🐛 Troubleshooting

### Common Issues
- **Pygame not found**: Install with `pip install pygame`
- **Images not loading**: Ensure `images/` folder is in the same directory
- **Game won't start**: Check Python version (3.6+ required)

### Performance Tips
- Close other applications for better AI performance
- Lower difficulty for faster AI moves
- The game runs smoothly on most modern systems

## 📝 Future Enhancements
- [ ] Online multiplayer support
- [ ] Save/load game functionality
- [ ] Chess notation (PGN) support
- [ ] Additional AI difficulty levels
- [ ] Tournament mode
- [ ] Move hints and analysis

## 🤝 Contributing
Feel free to fork this project and submit pull requests for improvements!

## 📄 License
This project is open source and available under the MIT License.

---

**Enjoy playing chess!** ♟️
