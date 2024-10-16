# AI-Dino-Bot

AI Dino Bot is a Python-based game that mimics the popular T-Rex browser game, with an added AI component. Using the NEAT algorithm (NeuroEvolution of Augmenting Topologies), the game trains neural networks to control a dino that jumps over obstacles. The project utilizes Pygame for game development and showcases how machine learning can be integrated into a simple game environment.

## Requirements
Python 3.x

pygame library

neat-python library

## Installation
Install dependencies:

```bash
pip install pygame neat-python
```

## How to run

#### Clone the repository
```bash
git clone https://github.com/surysaroch/AI-Dino-Bot.git
cd AI-Dino-Bot
```

#### Run the game
```bash
python dino.py
```

## NEAT Algorithm Configuration
The NEAT configuration is defined in the neat-config file, which controls:

- Population size
- Fitness criteria
- Mutation rates
- Neural network structure

## Gameplay Logic
- Dino Actions: Jumps when close to obstacles.
- Obstacles: Randomized between small and big types, moving leftward across the screen.
- Ground Scrolling: Continuously loops to simulate movement.
- Score Display: Increases over time as dinos avoid obstacles.

## Contributing
Feel free to open issues or submit pull requests for improvements.
