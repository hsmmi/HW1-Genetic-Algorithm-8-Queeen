import copy
import random
import matplotlib.pyplot as plt


class board:
    def __init__(self, board_size: int) -> None:
        """Initialize board"""
        self.board_size = board_size
        # Permutation of numbers from 0 to board_size - 1
        self.board = [i for i in range(board_size)]
        random.shuffle(self.board)
        self.fitness = self.find_fitness()

    def find_fitness(self) -> int:
        """Find fitness of board"""
        fitness = 0
        for i in range(self.board_size):
            for j in range(i + 1, self.board_size):
                # Check for horizontal and diagonal attacks
                if self.board[i] != self.board[j] and abs(
                    self.board[i] - self.board[j]
                ) != abs(i - j):
                    fitness += 1
        return fitness


class GA:
    def __init__(self, population_size: int, board_size: int) -> None:
        """Initialize genetic algorithm"""
        self.population_size = population_size
        self.board_size = board_size
        self.population = [board(board_size) for i in range(population_size)]
        self.fitness_evaluations = population_size
        self.population = sorted(
            self.population, key=lambda x: x.fitness, reverse=True
        )
        self.solve_8_queen()

    def crossover(self, parent1: board, parent2: board) -> board:
        """Crossover between two parents"""
        # Select random crossover point
        crossover_point = random.randint(1, self.board_size - 2)

        offspring1 = copy.deepcopy(parent1)
        offspring2 = copy.deepcopy(parent2)

        offspring1.board = parent1.board[:crossover_point]
        offspring2.board = parent2.board[:crossover_point]
        for i in range(self.board_size):
            if parent2.board[i] not in offspring1.board:
                offspring1.board.append(parent2.board[i])
            if parent1.board[i] not in offspring2.board:
                offspring2.board.append(parent1.board[i])

        return offspring1, offspring2

    def mutate(self, offspring: board, prob: float = 0.8) -> board:
        """Mutate offspring"""
        if random.random() < prob:
            # Swap two random positions
            pos1, pos2 = random.sample(range(self.board_size), 2)
            offspring.board[pos1], offspring.board[pos2] = (
                offspring.board[pos2],
                offspring.board[pos1],
            )
        return offspring

    def evolve(self) -> None:
        # Select 5 random parents
        parents = random.sample(self.population, 5)

        # Find 2 best parents
        parent1, parent2 = sorted(
            parents, key=lambda x: x.fitness, reverse=True
        )[:2]

        # Create offspring
        offspring1, offspring2 = self.crossover(parent1, parent2)

        # Mutate offsprings
        offspring1 = self.mutate(offspring1)
        offspring2 = self.mutate(offspring2)

        # Find fitness of offsprings
        offspring1.fitness = offspring1.find_fitness()
        offspring2.fitness = offspring2.find_fitness()
        self.fitness_evaluations += 2

        # Replace worst two individuals with offsprings
        self.population[-2] = offspring1
        self.population[-1] = offspring2

        # Sort based on fitness
        self.population = sorted(
            self.population, key=lambda x: x.fitness, reverse=True
        )

    def solve_8_queen(self) -> None:
        """Solve 8-Queen problem using genetic algorithm"""
        best_fitness = []
        avg_fitness = []
        while (
            self.population[0].fitness != 28
            and self.fitness_evaluations < 10000
        ):
            self.evolve()
            best_fitness.append(self.population[0].fitness)
            avg_fitness.append(
                sum([i.fitness for i in self.population])
                / self.population_size
            )

        print(f"Solution found in generation {self.fitness_evaluations}")
        print(f"Solution: {self.population[0].board}")

        # Plot fitness graph
        plt.plot(best_fitness, label="Best Fitness")
        plt.plot(avg_fitness, label="Average Fitness")
        plt.xlabel("Fitness Evaluations")
        plt.ylabel("Fitness")

        plt.legend()
        plt.show()


solution = GA(100, 8)

print("Finished")
