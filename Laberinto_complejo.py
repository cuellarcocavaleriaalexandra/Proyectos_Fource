import numpy as np  # Librería para trabajar con matrices y cálculos numéricos
import random  # Librería para generar números y elecciones aleatorias
import matplotlib.pyplot as plt  # Librería para crear gráficos
import matplotlib.animation as animation  # Librería para crear animaciones
from matplotlib.colors import ListedColormap  # Herramienta para definir colores personalizados en gráficos


class DeliveryEnvironment:
    def __init__(self, grid_size=15, num_delivery_zones=3, num_obstacles=20):
        """
        Inicializa el entorno donde operará el agente de entrega.
        """
        self.grid_size = grid_size
        # Crear un mapa vacío (matriz llena de ceros)
        self.city_map = np.zeros((grid_size, grid_size), dtype=int)
        
        # Definir la posición del almacén central en el medio del mapa
        self.warehouse = (grid_size // 2, grid_size // 2)  # Dividir el tamaño de la cuadrícula entre 2
        self.city_map[self.warehouse[0], self.warehouse[1]] = 2  # Marcar el almacén con un "2"
        
        # Llamar a las funciones para colocar obstáculos y zonas de entrega
        self._place_obstacles(num_obstacles)
        self.delivery_zones = self._place_zones(num_delivery_zones)

    def _place_obstacles(self, num_obstacles):
        """
        Coloca obstáculos aleatorios en el mapa.
        """
        for _ in range(num_obstacles):
            while True:
                # Elegir coordenadas aleatorias dentro de los límites del mapa
                x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
                if self.city_map[x, y] == 0:  # Verificar que la celda está vacía
                    self.city_map[x, y] = 1  # Colocar un obstáculo ("1")
                    break  # Salir del bucle una vez que se ha colocado

    def _place_zones(self, num_zones):
        """
        Coloca zonas de entrega aleatorias en el mapa.
        """
        delivery_zones = []  # Lista para guardar las posiciones de las zonas de entrega
        for _ in range(num_zones):
            while True:
                # Elegir coordenadas aleatorias dentro de los límites del mapa
                x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
                if self.city_map[x, y] == 0:  # Verificar que la celda está vacía
                    self.city_map[x, y] = 3  # Colocar una zona de entrega ("3")
                    delivery_zones.append((x, y))  # Guardar la posición
                    break  # Salir del bucle una vez que se ha colocado
        return delivery_zones  # Devolver las posiciones de las zonas de entrega

    def print_city_map(self):
        """
        Imprime el mapa de la ciudad en la consola.
        """
        # Definir símbolos para representar cada tipo de celda
        symbols = {0: '.', 1: '#', 2: 'W', 3: 'D'}  # Libre, Obstáculo, Almacén, Zona de entrega
        for row in self.city_map:
            print(' '.join(symbols[cell] for cell in row))  # Convertir la fila a símbolos y mostrarla

    def train_delivery_agent(self, episodes=1000, max_steps=100):
        """
        Entrena un agente de entrega con el algoritmo Q-Learning.
        """
        # Definir los movimientos posibles: Norte, Sur, Oeste, Este
        actions = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        q_table = {}  # Tabla Q para almacenar los valores de cada estado-acción
        rewards_per_episode = []  # Lista para guardar las recompensas de cada episodio
        tracked_episodes = []  # Lista para guardar las trayectorias de los episodios

        # Definir hiperparámetros
        learning_rate = 0.1  # Velocidad de aprendizaje
        discount_factor = 0.9  # Importancia de las recompensas futuras
        epsilon = 1.0  # Probabilidad inicial de exploración
        epsilon_decay = 0.995  # Reducción gradual de epsilon
        min_epsilon = 0.01  # Valor mínimo de epsilon

        for episode in range(episodes):  # Repetir para cada episodio
            x, y = self.warehouse  # Iniciar en el almacén
            deliveries = {zone: 0 for zone in self.delivery_zones}  # Zonas de entrega pendientes
            total_reward = 0  # Recompensa acumulada en el episodio
            steps = 0  # Contador de pasos
            episode_track = [(x, y)]  # Guardar la trayectoria del agente

            while steps < max_steps:  # Mientras no se alcance el límite de pasos
                state = (x, y, tuple(sorted(deliveries.items())))  # Definir el estado actual

                # Decidir acción: exploración o explotación
                if random.uniform(0, 1) < epsilon:
                    action = random.choice(list(actions.keys()))  # Elegir acción aleatoria
                else:
                    action = max(actions.keys(), key=lambda a: q_table.get((state, a), 0))  # Elegir mejor acción
                    # usa lambda para definir una función que: Toma un argumento a: 
                    # a es una posible acción (por ejemplo, 0, 1, 2, o 3).

                dx, dy = actions[action]  # Obtener el movimiento correspondiente a la acción
                # Por ejemplo, si action=0 (Norte), dx=-1 y dy=0

                nx, ny = x + dx, y + dy  # Calcular las nuevas coordenadas
                 # Sumar dx y dy a la posición actual (x, y)

                # Verificar si las nuevas coordenadas son válidas (dentro del mapa y no hay obstáculo)
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and self.city_map[nx, ny] != 1:
                    x, y = nx, ny  # Actualizar posición del agente

                # Calcular recompensa
                reward = -1  # Penalización por moverse
                if (x, y) in deliveries and deliveries[(x, y)] == 0:  # Si llega a una zona de entrega pendiente
                    reward += 50  # Dar recompensa por completar la entrega
                    deliveries[(x, y)] = 1  # Marcar la entrega como completada

                # Actualizar Q-Table
                next_state = (x, y, tuple(sorted(deliveries.items())))  # Estado siguiente
                old_value = q_table.get((state, action), 0)  # Valor actual en la Q-Table
                next_max = max([q_table.get((next_state, a), 0) for a in actions.keys()])  # Mejor valor futuro
                # Esto crea una lista con los valores Q de todas las posibles acciones desde el estado next_state.
                # a: Es una acción posible desde ese estado.
                    
                q_table[(state, action)] = old_value + learning_rate * (
                    reward + discount_factor * next_max - old_value)  # Fórmula Q-Learning

                # Actualizar métricas del episodio
                total_reward += reward
                steps += 1
                episode_track.append((x, y))  # Guardar la posición actual

                # Terminar el episodio si todas las entregas están completas
                if all(deliveries.values()):
                    break

            # Guardar los resultados del episodio
            rewards_per_episode.append(total_reward)
            tracked_episodes.append(episode_track)
            epsilon = max(min_epsilon, epsilon * epsilon_decay)  # Reducir epsilon gradualmente

        return q_table, rewards_per_episode, tracked_episodes[-100:]  # Retornar los últimos 100 episodios

    def visualize_q_table(self, q_table):
        """
        Imprime las 10 mejores entradas de la Q-Table.
        """
        print("\nResumen de Q-Table:")
        for (state, action), value in sorted(q_table.items(), key=lambda item: item[1], reverse=True)[:10]:
            print(f"Estado: {state}, Acción: {action}, Valor Q: {value:.2f}")

    def animate_delivery(self, tracked_episodes):
        """
        Crea una animación para mostrar el movimiento del agente.
        """
        cmap = ListedColormap(['white', 'gray', 'green', 'red'])  # Definir colores para el mapa

        fig, ax = plt.subplots(figsize=(8, 8))  # Crear figura

        def update(frame): # se ejecutará cada vez que se muestre un nuevo "fotograma" de la animación.
            # El argumento frame indica el índice del episodio actual que se está mostrando.

            ax.clear()
            ax.imshow(self.city_map, cmap=cmap, interpolation='nearest')  # Mostrar el mapa
            # self.city_map: Es el mapa donde se encuentran el almacén, los obstáculos y las zonas de entrega.
            #cmap: Define los colores para representar cada tipo de celda (blanco para celdas libres, gris para obstáculos, etc.).
            # interpolation='nearest': Asegura que los píxeles del mapa se vean nítidos.

            x, y = zip(*tracked_episodes[frame])  # Traer trayectoria del episodio
            # tracked_episodes[frame]: Obtiene la lista de posiciones del agente en el episodio correspondiente al fotograma actual (frame).
            #Por ejemplo: [(5, 5), (5, 6), (6, 6)] es una trayectoria donde el agente se mueve.
            #zip(*...): Separa las posiciones en dos listas:
            # x: Lista de las coordenadas verticales (filas).
            # y: Lista de las coordenadas horizontales (columnas).
            
            ax.plot(y, x, marker='o', color='blue', markersize=10, label="Trayectoria")  # Dibujar trayectoria
            ax.legend(loc="upper right")
            plt.title(f"Episodio {frame + 1}")

        anim = animation.FuncAnimation(fig, update, frames=len(tracked_episodes), repeat=False)
        plt.show()

    def visualize_rewards(self, rewards):
        """
        Grafica las recompensas obtenidas por episodio.
        """
        plt.plot(rewards)
        plt.xlabel("Episodios")
        plt.ylabel("Recompensas Totales")
        plt.title("Recompensas por Episodio")
        plt.show()


def main():
    # Crear el entorno de simulación
    env = DeliveryEnvironment(grid_size=15, num_delivery_zones= 5, num_obstacles=10)
    print("Mapa de la Ciudad:")
    env.print_city_map()

    # Entrenar el agente
    print("\nIniciando entrenamiento del agente...")
    q_table, rewards, tracked_episodes = env.train_delivery_agent(episodes=1000, max_steps=100)

    # Mostrar la Q-Table
    env.visualize_q_table(q_table)

    # Animar el movimiento del agente
    print("\nAnimando el movimiento del agente...")
    env.animate_delivery(tracked_episodes)

    # Graficar recompensas
    print("\nVisualizando recompensas acumuladas...")
    env.visualize_rewards(rewards)


if __name__ == "__main__":
    main()
