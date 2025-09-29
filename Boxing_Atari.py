import gymnasium as gym
import ale_py
import numpy as np
import matplotlib.pyplot as plt
import cv2
from collections import defaultdict

# Inicializamos el entorno de Boxing de Atari - Gymnasium
env = gym.make("ALE/Boxing-v5", render_mode="human", obs_type="grayscale")

# Función para discretizar el estado
def discretizar(observation):
    # Redimensionar la observación a un tamaño más manejable
    resized = cv2.resize(observation, (10, 10))
    # Normalizar y discretizar los valores
    discretized = (resized / 255 * 10).astype(np.int32)
    # Convertir el array a una tupla para que sea hashable
    return tuple(discretized.flatten())

def train(episodes):
    # Crear una tabla Q inicializada con ceros para todas las combinaciones de estado y acción
    q_table = defaultdict(lambda: np.zeros(env.action_space.n))

    # Parámetros de Q-learning
    learning_rate = 0.15            
    discount_factor = 0.99         
    epsilon = 1                    
    epsilon_decay_rate = 0.0005    
    rng = np.random.default_rng()  

    # Inicializa un array para almacenar las recompensas obtenidas en cada episodio
    rewards_per_episode = np.zeros(episodes)

    # Bucle principal de entrenamiento
    for i in range(episodes): 
        
        state = env.reset()[0]
        state = discretizar(state)  # Discretizar el estado inicial
        terminated = False
        truncated = False
        total_reward = 0


        while not terminated and not truncated:
            # Decisión de acción: explorar o explotar
            if rng.random() < epsilon:
                action = env.action_space.sample()
            else: 
                action = np.argmax(q_table[state])

            # Realizar acción
            new_state, reward, terminated, truncated, _ = env.step(action)
            new_state = discretizar(new_state)

            # Actualizar la tabla Q
            old_value = q_table[state][action]
            next_max = np.max(q_table[new_state])
            
            # Fórmula Q-learning
            new_value = old_value + learning_rate * (
                reward + discount_factor * next_max - old_value
            )
            q_table[state][action] = new_value
            
            state = new_state
            total_reward += reward

            # Renderizar el entorno
            env.render()

        # Registrar recompensa total del episodio
        rewards_per_episode[i] = total_reward

        # Reducir epsilon
        epsilon = max(epsilon - epsilon_decay_rate, 0)

        # Imprimir progreso
        if (i + 1) % 100 == 0: 
            print(f"Episodio: {i + 1} - Recompensa total: {total_reward}")

    env.close()

    # Mostrar algunos valores de la Q-table
    print("\nMuestra de la Q-table:")
    #for idx, (state, actions) in enumerate(list(q_table.items())[:10]):
       # print(f"Estado: {state[:10]}..., Acciones: {actions}")

    # Graficar rendimiento
    sum_rewards = np.zeros(episodes)
    for t in range(episodes):
        sum_rewards[t] = np.sum(rewards_per_episode[max(0, t-100):(t+1)])
    plt.plot(sum_rewards)
    plt.xlabel('Episodios')
    plt.ylabel('Suma de recompensas en 100 episodios')
    plt.title('Rendimiento acumulado en el entorno de Boxing')
    plt.show()

# Ejecutar el entrenamiento
if __name__ == "__main__":
    train(100)