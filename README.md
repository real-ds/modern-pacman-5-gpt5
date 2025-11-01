# 🎮 PAC-MAN: Retro Futuristic Edition

A modern recreation of the classic Pac-Man game with progressive levels, adaptive AI, and strategic power-ups. Built with Python and Pygame.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/license-Educational-orange.svg)

## 🎯 Features

### Core Gameplay
- Classic Pac-Man mechanics with modern enhancements
- 4 ghosts with unique AI personalities and behaviors
- Smooth grid-based movement with responsive controls
- Power pellets activate frightened mode for ghost hunting
- Progressive difficulty scaling across levels

### 4 Unique Ghost AIs
Each ghost has a distinct personality and hunting strategy:

- **Blinky (Red/Pink)** - The Chaser
  - Aggressively pursues Pac-Man directly
  - Most dangerous in open spaces
  - Target: Player's current position

- **Pinky (Pink)** - The Ambusher
  - Attempts to position ahead of player
  - Cuts off escape routes
  - Target: 4 tiles ahead of player's direction

- **Inky (Cyan)** - The Flanker
  - Strategic positioning based on player movement
  - Unpredictable attack patterns
  - Target: 2 tiles ahead of player

- **Clyde (Orange)** - The Wildcard
  - Shy behavior - flees when close
  - Chases when far away
  - Target: Player when distant, scatter point when close

### Progressive Level System
- Infinite level progression with increasing difficulty
- Each level increases ghost speed by 10%
- Ghosts become more aggressive with faster mode switching
- 1000 point bonus for completing each level
- Fresh maze generation for each level

### Strategic Power-Ups
Three collectible power-ups spawn periodically (every 15 seconds):

- ⚡ **Speed Boost** - Move 50% faster for 5 seconds
- 🛡️ **Shield** - Protects from one ghost collision
- ❄️ **Freeze** - Slows all ghosts by 70% for 5 seconds

Power-ups have visual pulsing effects and disappear after 10 seconds if not collected.

### Polished UI
- Real-time score tracking with large display
- Lives counter with visual Pac-Man icons
- Level indicator showing current progress
- Power-up mode timer with progress bar
- Active power-up indicator
- Particle effects for pellets, deaths, and celebrations

### Complete Menu System
- Attractive start menu with controls
- Pause functionality (P key)
- Game over screen with final statistics
- Smooth state transitions

### Visual Effects
- Particle system for enhanced feedback
- Pellet collection particles
- Death burst effects
- Shield break visualization
- Level completion celebration
- Smooth animations and transitions

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Local Installation

```bash
# Clone the repository
git clone <repository-url>
cd modern-packman-5-claudecodeagent

# Install dependencies
pip install -r requirements.txt --break-system-packages

# Run the game
python main.py
```

### Dependencies
```
pygame>=2.5.0
pygbag>=0.8.0 (for web deployment)
numpy>=1.24.0 (optional)
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** or **WASD** | Move Pac-Man |
| **P** | Pause/Resume game |
| **SPACE** | Start game / Restart after game over |
| **ESC** | Quit to menu / Exit game |

## 🎯 Gameplay Tips

1. **Master the Ghost Patterns**
   - Learn each ghost's behavior to predict movements
   - Use Blinky's aggressive nature to lead him into traps
   - Watch for Pinky's ambush attempts

2. **Strategic Power-Up Use**
   - Save shields for dangerous situations
   - Use speed boosts to quickly clear areas
   - Activate freeze when surrounded

3. **Power Pellet Timing**
   - Plan routes to chain ghost consumption
   - Each ghost eaten increases score exponentially
   - Power mode lasts 8 seconds - use wisely

4. **Level Progression**
   - Complete levels quickly for higher scores
   - Difficulty increases each level
   - Adapt strategy as ghosts get faster

## 📊 Scoring System

| Action | Points |
|--------|--------|
| Regular Pellet | 10 |
| Power Pellet | 50 |
| First Ghost | 200 |
| Second Ghost | 200 |
| Third Ghost | 200 |
| Fourth Ghost | 200 |
| Level Complete | 1000 |

## 🏗️ Project Structure

```
modern-packman-5-claudecodeagent/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── src/                   # Source code
│   ├── game.py           # Main game loop and state management
│   ├── config.py         # Game configuration and constants
│   │
│   ├── entities/         # Game entities
│   │   ├── player.py    # Pac-Man class
│   │   ├── ghost.py     # Base ghost class
│   │   ├── ghost_ai.py  # 4 unique ghost AIs
│   │   └── powerup.py   # Power-up system
│   │
│   ├── levels/          # Level management
│   │   ├── maze.py      # Maze structure and rendering
│   │   └── level_manager.py  # Level progression
│   │
│   ├── ui/              # User interface
│   │   ├── hud.py       # Heads-up display
│   │   ├── menus.py     # Menu screens
│   │   └── particles.py # Particle effects
│   │
│   └── utils/           # Utility functions
│       └── collision.py # Collision detection
│
├── assets/              # Game assets (optional)
│   ├── fonts/
│   ├── sounds/
│   └── images/
│
└── tests/               # Test files
```

## 🚀 Web Deployment

### Building for Web with Pygbag

```bash
# Install pygbag
pip install pygbag --break-system-packages

# Build for web
python -m pygbag .

# The game will be available as a web application
# Open the provided local URL in your browser
```

### Hosting Options
- **GitHub Pages**: Host the build output
- **Itch.io**: Upload as HTML5 game
- **Netlify/Vercel**: Deploy as static site

## 🎨 Visual Design

### Retro-Futuristic Color Palette
- **Background**: Deep space black (#0A0A0F)
- **Pac-Man**: Neon yellow (#FFFF00)
- **Walls**: Electric blue (#00F0FF)
- **Power-Ups**: Various neon colors
  - Speed: Neon green (#39FF14)
  - Shield: Neon blue (#00F0FF)
  - Freeze: Neon purple (#BF40BF)

### Performance
- Consistent 60 FPS gameplay
- Optimized rendering pipeline
- Efficient collision detection
- Smooth particle systems

## 📝 Development

### Built With
- **Python 3.10+**: Core language
- **Pygame 2.5+**: Game engine
- **Pygbag**: Web deployment framework

### Development Stages
The game was built in 5 progressive stages:
1. **Foundation**: Basic gameplay, maze, player movement
2. **Ghost AI**: 4 unique ghost behaviors, collision
3. **UI System**: HUD, menus, particles, game states
4. **Progression**: Level manager, power-ups, difficulty scaling
5. **Polish**: Documentation, web deployment, optimization

## 🎓 Educational Purpose

This is an educational recreation of Pac-Man for learning game development concepts:
- Game loop architecture
- AI pathfinding and behaviors
- State management
- Collision detection
- Particle systems
- Progressive difficulty

## 📜 License

This is an educational project. Original Pac-Man © Namco.

## 🙏 Credits

- **Original Game**: Toru Iwatani (Namco, 1980)
- **Recreation**: Built with Claude Code
- **Framework**: Pygame Community
- **Python**: Python Software Foundation

## 🐛 Known Issues

- Ghost pathfinding occasionally gets stuck in corners (rare)
- Particle effects may lag slightly on very low-end systems

## 🚧 Future Enhancements

Potential additions for future versions:
- Sound effects and music
- Achievement system
- High score persistence
- Additional maze layouts
- Mobile touch controls
- Multiplayer mode
- Leaderboards

## 📞 Support

For issues or questions:
1. Check the [issues](../../issues) page
2. Review the code documentation
3. Test with latest Python and Pygame versions

## 🎉 Enjoy the Game!

Have fun playing this modern take on the classic Pac-Man! Try to beat your high score and see how far you can progress through the levels!

---

**Made with ❤️ using Python and Pygame**

🤖 *Generated with [Claude Code](https://claude.com/claude-code)*
