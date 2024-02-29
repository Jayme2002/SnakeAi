
# **Snake AI Using Genetic Algorithm**

![snakegif](https://github.com/Jayme2002/SnakeAi/assets/132419605/6c24dc25-aa61-43ef-9093-77851b6f769b)

## **Project Overview**

This project implements a Snake game AI using a genetic algorithm in Python with Pygame for visualization. The goal is to evolve a neural network that controls the snake, maximizing score by eating food while avoiding walls and itself.

## **Features**

**Pygame Visualization:** Offers a real-time visual representation of the AI-controlled snake navigating the game environment.

**Genetic Algorithm:** Utilizes a genetic algorithm for evolving the snake's decision-making process over generations, improving its ability to play the game.

**Customizable Parameters:** Allows easy adjustments to the genetic algorithm parameters, such as population size and mutation rates, for experimentation.

## **Installation** 

To run this project, you will need Python and Pygame installed on your system. Follow these steps to set up the environment:

**Install Requirements:**
Ensure Python 3.x is installed.

**Install Pygame:** 
Copy code: pip install pygame

**Clone the Repository:**
Copy code: git clone https://github.com/jayme2002/SnakeAi.git

**OR**

**Download snake.py File:**
navigate to directory where the file is downloaded and run python3 snake.py

**Navigate to the Project Directory:**
bash
Copy code: cd SnakeAi

**Run the Game:**
Copy code: python3 snake.py

## **How It Works**

The AI controls the snake using a simple neural network where the weights are evolved using a genetic algorithm. At each step, the snake decides its next move based on its current position relative to the walls, its body, and the food.

## **Genetic Algorithm Process**

**Initial Population:** Randomly generated snakes with unique neural network weights.
Selection: Snakes are evaluated based on their performance in the game. The best-performing snakes are selected for reproduction.

**Crossover:** Selected snakes are paired to mix their weights, creating offspring with characteristics from both parents.

**Mutation:** Offspring weights are slightly mutated to introduce variability.

**Next Generation:** The process repeats over several generations, with each generation theoretically improving upon the last.

## **Configuration**

You can adjust various settings related to the snake's speed, window size, and genetic algorithm parameters within the snake.py file to see how they influence the AI's performance.
