# Genetic-Chess-Algorithm
A Python machine learning project that is made to learn the optimal chess strategies. By using a previous Genetic Algorithm project to mutate and cross breed piece evaluations, this project spawns thousands of randomized neural profiles, competes against each other in automated matches.

<p>
  <img src="https://img.shields.io/badge/Python-0D1117?style=for-the-badge&logo=python&logoColor=38BDF8" alt="Python" />
  <img src="https://img.shields.io/badge/Evolutionary_Computation-0D1117?style=for-the-badge&color=0D1117" alt="Evolutionary computation" />
  <img src="https://img.shields.io/badge/Minimax_%2B_Alpha--Beta-0D1117?style=for-the-badge&color=0D1117" alt="Minimax and alpha-beta pruning" />
  <img src="https://img.shields.io/badge/Stockfish_Integration-0D1117?style=for-the-badge&color=0D1117" alt="Stockfish integration" />
</p>

I built Genetic Chess Algorithm as the next step after my [Genetic Algorithm](https://github.com/kadenyip/Genetic-Algorithm) project, which evolved random characters into a target phrase. I wanted to apply the same ideas—fitness, selection, elitism, crossover, and mutation—to a problem where a good decision depends on an opponent's response.

The result is a Python chess experiment that evolves five material weights and uses them inside a minimax search with alpha-beta pruning. It connects legal move generation, position evaluation, evolutionary optimization, SVG board rendering, opening-book access, and a Stockfish opponent.

The most valuable part of building it was discovering where an apparently reasonable objective failed: gaining material did not necessarily lead to checkmate, a high fitness score could come from a lucky opponent, and a deeper search could multiply training time. Those problems shaped the implementation and the next experiments.

**Current status:** a working development prototype with an evolutionary training loop and an automated Stockfish demonstration. Training still uses short games against random Black moves. The code has remaining evaluation and game-loop issues documented below; playing strength and speed improvements have not been established through a reproducible benchmark.

## Contents

- [From the original project to chess](#from-the-original-project-to-chess)
- [What the project implements](#what-the-project-implements)
- [Run the project](#run-the-project)
- [Architecture](#architecture)
- [How evolution and search work](#how-evolution-and-search-work)
- [Challenges, solutions, and lessons](#challenges-solutions-and-lessons)
- [Observations and current limitations](#observations-and-current-limitations)
- [Next steps](#next-steps)

## From the original project to chess

My first genetic algorithm had a precise target: a string. A character either matched its target position or it did not. Chess introduced delayed consequences, competing decisions, and an imperfect way to measure success.

| Design choice | Original phrase project | Genetic Chess Algorithm |
| :--- | :--- | :--- |
| Genome | A string of characters | Five floating-point piece values |
| Fitness | Correct characters at matching positions | White's material advantage after a simulated game |
| Candidate evaluation | Compare a string with a known answer | Play a game using the candidate's evaluation weights |
| Crossover | Combine sections of two strings | Combine sections of two weight lists |
| Mutation | Replace individual characters | Adjust individual weights numerically |
| Elitism | Preserve the top 10% | Preserve the top 10% |
| Main challenge | Converge toward an explicit target | Design a useful objective under uncertainty |

The chess version preserves the evolutionary structure while adding adversarial search and an external engine integration. Only the five material weights evolve. Legal chess rules come from `python-chess`; terminal scores and the positional heuristic are programmed explicitly.

## What the project implements

- **Evolutionary optimization:** populations of 50 genomes, elite preservation, parent selection, crossover, and independent mutation of each weight.
- **Adversarial search:** recursive minimax with alpha-beta cutoffs and reversible board updates.
- **Position evaluation:** evolved material weights, explicit checkmate and draw scores, and a small bonus for an opposing king farther from the center.
- **Chess state management:** legal moves, SAN parsing, UCI move conversion, and FEN synchronization through `python-chess`.
- **External engine integration:** Stockfish move selection with configurable strength settings and position-analysis requests.
- **Opening-book support:** weighted Polyglot lookup with a random fallback when the position is absent from the book.
- **Visual feedback:** a generated `board.svg` updated after moves in the demonstration.
- **Separate entry points:** terminal-only training and training followed by an automated game.

## Run the project

Run commands from the project directory so relative paths such as `gm2001.bin` and `board.svg` resolve correctly.

### 1. Install the Python dependencies

Use a compatible Python 3 installation and a virtual environment. Development history includes Python 3.10; dependencies are currently unpinned, so this is not a guaranteed compatibility matrix.

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the packages:

```bash
python -m pip install python-chess stockfish
```

### 2. Run training only

```bash
python genetic_visuals.py
```

This creates a population and prints a candidate's fitness and weights after each generation. It does not start the external Stockfish executable or render a game. Training can take substantial time because fitness evaluation repeatedly searches game trees.

### 3. Configure Stockfish for the demonstration
