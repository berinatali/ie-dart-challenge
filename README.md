# 🎯 Industrial Engineering Dart Challenge

A desktop game built with Python and Tkinter that mixes **dart throwing** with an **Industrial Engineering quiz**. Hit the moving target to score dart points, then answer a question to earn bonus points. You have 5 minutes and 5 lives, so make every throw and every answer count.

> The in-game interface and the quiz questions are in **Turkish**.

## ✨ Features

- Physics-based dart throwing with gravity, adjustable angle and a power meter
- Dotted aiming guide that previews the first part of the dart's path
- Real dart-style scoring: the closer to the center, the more points you get
- "Who Wants to Be a Millionaire"-style quiz screen with 254 Industrial Engineering questions
- Hint system: a wrong answer gives you a hint and a second chance
- 5-minute countdown, 5 lives, pause, restart and a session scoreboard
- Animated forest background with fireflies
- Fullscreen mode with a responsive layout
- No external dependencies, standard library only

## 📦 Requirements

- Python 3.8 or newer
- Tkinter (included with the standard Python installers for Windows and macOS)

On some Linux distributions you may need to install it separately:

```bash
sudo apt install python3-tk
```

## 🚀 Getting Started

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python dart_game.py
```

On macOS/Linux you may need to use `python3` instead of `python`.

## 🎮 How to Play

1. Press **Space** to start the power meter.
2. Press **Space** again at the right moment to throw the dart. Use **↑ / ↓** to change the angle before throwing.
3. If you hit the board, you score dart points based on where the dart lands, then a quiz question appears.
4. Answer the question to earn extra points. A round consists of 5 questions.
5. Score as many points as you can before the 5 minutes run out.

### Dart scoring

| Ring | Points |
|------|--------|
| Bullseye (center) | 50 |
| Outer bull | 25 |
| Green ring | 20 |
| Cream ring | 15 |
| Red ring | 10 |
| Outer cream ring | 5 |
| Edge | 1 |

Missing the board gives no points, but it does **not** end the game.

### Quiz scoring

| Result | Points |
|--------|--------|
| Correct on the first try | +100 |
| Correct after using the hint | +50 |
| Two first-try answers in a row | +50 bonus |

### Lives

- You start with **5 lives** (♥).
- If you answer wrong even after the hint, you lose **1 life**.
- When all lives are gone, the game ends and you must wait **5 minutes** before playing again.

### Controls

| Key | Action |
|-----|--------|
| `Space` | Start power meter / throw |
| `↑` / `↓` | Adjust throwing angle |
| `A` `B` `C` `D` | Select an answer |
| `P` | Pause / resume |
| `Esc` / `F11` | Toggle fullscreen |

## ❓ Question Pool

Questions cover topics such as inventory and production planning, quality control, lean manufacturing, operations research, statistics, engineering economics, work study and ergonomics, facility layout and logistics, project management, forecasting and simulation, supply chain, scheduling and maintenance.

The game remembers which questions have been asked in `seen_questions.json`, which is created next to the script. Unseen questions are always served first, so each new game feels different. Delete that file to reset the history.

### Adding your own questions

Open `dart_game.py` and add a line to the `_RAW` list using this format:

```python
("Question text?", "Correct answer", "Wrong 1", "Wrong 2", "Wrong 3", "Hint shown after a wrong answer"),
```

The correct answer is always listed first. The game shuffles the options automatically.

## ⚙️ Configuration

You can tweak the game by editing the constants at the top of `dart_game.py`:

| Constant | Description |
|----------|-------------|
| `GAME_TIME` | Game length in seconds (default `300`) |
| `GRAV` | Gravity strength (lower is easier) |
| `POWER_SPEED` | Power meter speed (lower is easier) |
| `HIT_R` | Hit radius of the target |
| `QUESTIONS_PER_ROUND` | Number of questions per round |
| `WIN_SCORE` | Score needed to see the "Congratulations" screen |
| `RING_SCORES` | Points awarded for each ring |

## 📁 Project Structure

```
.
├── dart_game.py          # The whole game
├── seen_questions.json   # Generated automatically at runtime
└── README.md
```

Tip: add `seen_questions.json` to your `.gitignore`, since it is local play history.

## 🛠️ Built With

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)

## 📄 License

Add a license of your choice, for example MIT, by creating a `LICENSE` file in the repository.
