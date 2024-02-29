import pygame
import random
import numpy as np
import time

# Game configuration
snake_speed = 75
window_x = 800
window_y = 600

# Initialize pygame
pygame.init()

# Game window
pygame.display.set_caption('Snake AI')
game_window = pygame.display.set_mode((window_x, window_y))

# Colors
black = pygame.Color(0, 0, 0)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)

# Snake AI Class
class SnakeAI:
    def __init__(self, weights=None):
        self.weights = weights if weights is not None else np.random.uniform(-0.05, .05, 6)

    def decide_movement(self, snake_position, snake_body, fruit_position):
        possible_directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        direction_scores = {dir: 0 for dir in possible_directions}

        # Calculate the difference in position between the head and the fruit
        dx = fruit_position[0] - snake_position[0]
        dy = fruit_position[1] - snake_position[1]

        # Scale the weights' influence on decision scores
        weight_scaling_factor = 10.0

        direction_scores['RIGHT'] += self.weights[0] * dx / weight_scaling_factor
        direction_scores['LEFT'] += self.weights[1] * -dx / weight_scaling_factor
        direction_scores['DOWN'] += self.weights[2] * dy / weight_scaling_factor
        direction_scores['UP'] += self.weights[3] * -dy / weight_scaling_factor

        # Check for body/wall collisions
        for direction in possible_directions:
            future_position = self.get_future_position(snake_position, direction)
            if future_position in snake_body or not self.is_inside_boundaries(future_position):
                direction_scores[direction] += self.weights[4] * -.8  # Heavily penalize potential collisions

        # Choose the direction with the highest score
        best_direction = max(direction_scores, key=direction_scores.get)
        return best_direction


    def get_future_position(self, current_position, direction):
        future_position = current_position.copy()
        if direction == 'UP':
            future_position[1] -= 10
        elif direction == 'DOWN':
            future_position[1] += 10
        elif direction == 'LEFT':
            future_position[0] -= 10
        elif direction == 'RIGHT':
            future_position[0] += 10
        return future_position

    def is_inside_boundaries(self, position):
        return 0 <= position[0] < window_x and 0 <= position[1] < window_y

# Function to play game with AI
def play_game_with_ai(snake_ai):
    global snake_speed, window_x, window_y

    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    score = 0
    start_time = time.time()
    total_time_to_fruit = 0
    moves = 0

    while True:
        moves += 1
        if moves > 100000:
            break
        current_time = time.time()
        direction = snake_ai.decide_movement(snake_position, snake_body, fruit_position)

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
        elif direction == 'DOWN':
            snake_position[1] += 10
        elif direction == 'LEFT':
            snake_position[0] -= 10
        elif direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 1
            total_time_to_fruit += (current_time - start_time)
            start_time = current_time
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

        # Game Over conditions
        if (snake_position[0] < 0 or snake_position[0] >= window_x or
            snake_position[1] < 0 or snake_position[1] >= window_y or
            snake_position in snake_body[1:]):
            break
        
    average_time_to_fruit = total_time_to_fruit / score if score > 0 else float('inf')
    return score, average_time_to_fruit


def crossover(parent1, parent2):
    # Implementing a more complex crossover mechanism
    if play_game_with_ai(parent1) < play_game_with_ai(parent2):
        parent1, parent2 = parent2, parent1  # Swap parent1 and parent2

    crossover_point = np.random.randint(1, len(parent1.weights))
    new_weights = np.concatenate((parent1.weights[:crossover_point], parent2.weights[crossover_point:]))
    return SnakeAI(new_weights)

def mutate(snake):
    # Increase mutation strength for more significant changes
    mutation_strength = 0.2
    mutation_probability = 0.15  # 15% chance of mutation per weight
    for i in range(len(snake.weights)):
        if np.random.rand() < mutation_probability:
            snake.weights[i] += np.random.uniform(-mutation_strength, mutation_strength)
def genetic_algorithm(population_size, generations):
    population = [SnakeAI() for _ in range(population_size)]

    for generation in range(generations):
        fitness_scores = []

        for snake in population:
            score, avg_time_to_fruit= play_game_with_ai(snake)
            fitness = calculate_fitness(score, avg_time_to_fruit)
            fitness_scores.append((snake, fitness, score))  # Store the game score as well

        sorted_population = sorted(fitness_scores, key=lambda x: x[1], reverse=True)
        population = [snake for snake, _, _ in sorted_population[:population_size // 2]]

        # Crossover and mutation
        while len(population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2)
            mutate(child)
            population.append(child)

        best_fitness = sorted_population[0][1]
        best_score = sorted_population[0][2]  # Game score of the best snake
        print(f"Generation {generation + 1}, Best Fitness: {best_fitness}, Best Game Score: {best_score}")

    return sorted_population[0][0]


def calculate_fitness(score, avg_time_to_fruit):
    # Adjust these weights as needed
    score_weight = 1.5
    time_weight = 1.2  # Lower value encourages faster fruit consumption
    fitness = (score_weight * score) - (time_weight * avg_time_to_fruit)
    
    return fitness

def show_message(surface, message, font, size, color, position):
    font = pygame.font.SysFont(font, size)
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=position)
    surface.blit(text_surface, text_rect)
    pygame.display.update()
    
def play_visual_game_with_best_ai(best_snake):
    pygame.init()
    game_window = pygame.display.set_mode((window_x, window_y))
    fps = pygame.time.Clock()
    
    game_window.fill(black)  # Fill the screen with black
    show_message(game_window, "Press any key to begin", "arial", 24, (255, 255, 255), (window_x / 2, window_y / 2))
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    score = 0

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # Any key press will start the game
                waiting_for_key = False
    while True:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                quit()

        direction = best_snake.decide_movement(snake_position, snake_body, fruit_position)

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
        elif direction == 'DOWN':
            snake_position[1] += 10
        elif direction == 'LEFT':
            snake_position[0] -= 10
        elif direction == 'RIGHT':
            snake_position[0] += 10

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 1
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

        # Game Over conditions
        if (snake_position[0] < 0 or snake_position[0] >= window_x or 
            snake_position[1] < 0 or snake_position[1] >= window_y or 
            snake_position in snake_body[1:]):
            break

        # Drawing the game state
        game_window.fill(black)
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        # Show score
        show_score(score, game_window, 'white', 'times new roman', 20)

        pygame.display.update()
        fps.tick(snake_speed)

def show_score(score, surface, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    surface.blit(score_surface, score_rect)

if __name__ == "__main__":
    best_snake = genetic_algorithm(population_size=200, generations=50)
    print("Best AI Weights:", best_snake.weights)
    play_visual_game_with_best_ai(best_snake)
