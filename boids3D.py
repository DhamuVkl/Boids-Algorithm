import numpy as np
import random
import math
from OpenGL.GL import *

from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Boid parameters
NUM_BOIDS = 50
BOID_SPEED = 5
BOID_VISION_RADIUS = 100
SEPARATION_FACTOR = (
    0.5  # You might want to adjust this if boids move out of view too quickly
)
ALIGNMENT_FACTOR = 0.1
COHESION_FACTOR = 0.1
PREDATOR_AVOIDANCE_FACTOR = 1.0


class Boid:
    def __init__(self):
        """
        Initializes a boid with a random position and velocity within specified ranges.
        """
        self.position = np.random.uniform(-100, 100, size=3)
        self.velocity = self.generate_non_zero_velocity()
        self.normalize(self.velocity)
        self.velocity *= BOID_SPEED

    def generate_non_zero_velocity(self):
        """
        Generates a non-zero velocity vector for the boid.
        """
        velocity = np.random.uniform(-1, 1, size=3)
        while np.linalg.norm(velocity) == 0:
            velocity = np.random.uniform(-1, 1, size=3)
        return velocity

    def update(self, boids, predator):
        """
        Updates the boid's position and velocity based on separation, alignment, cohesion, and predator avoidance behaviors.
        """
        separation_vector, alignment_vector, cohesion_vector = self.calculate_vectors(
            boids
        )
        predator_avoidance_vector = self.avoid_predator(predator)

        self.velocity = (
            self.velocity
            + (separation_vector * SEPARATION_FACTOR)
            + (alignment_vector * ALIGNMENT_FACTOR)
            + (cohesion_vector * COHESION_FACTOR)
            + (predator_avoidance_vector * PREDATOR_AVOIDANCE_FACTOR)
        )
        self.normalize(self.velocity)
        self.velocity *= BOID_SPEED

        self.position += self.velocity
        self.keep_within_bounds()

    def calculate_vectors(self, boids):
        """
        Calculates the separation, alignment, and cohesion vectors for the boid based on the positions and velocities of other nearby boids.
        """
        separation_vector = np.zeros(3)
        alignment_vector = np.zeros(3)
        cohesion_vector = np.zeros(3)
        neighbor_count = 0
        for other_boid in boids:
            if other_boid is not self:
                distance = self.calculate_distance(other_boid.position)
                if 0 < distance < BOID_VISION_RADIUS:
                    separation_vector += self.position - other_boid.position
                    alignment_vector += other_boid.velocity
                    cohesion_vector += other_boid.position
                    neighbor_count += 1
        if np.linalg.norm(separation_vector) == 0:
            separation_vector += np.random.uniform(-0.1, 0.1, size=3)
        if neighbor_count > 0:
            alignment_vector /= neighbor_count
            cohesion_vector /= neighbor_count
            cohesion_vector -= self.position
            self.normalize(separation_vector)
        return separation_vector, alignment_vector, cohesion_vector

    def avoid_predator(self, predator):
        """
        Calculates the avoidance vector for the boid based on the position of a predator.
        """
        direction = self.position - predator.position
        distance = self.calculate_distance(direction)
        if distance < BOID_VISION_RADIUS:
            self.normalize(direction)
            return direction
        return np.zeros(3)

    def normalize(self, vector):
        """
        Normalizes a vector to have a magnitude of 1.
        """
        magnitude = np.linalg.norm(vector)
        vector /= magnitude

    def calculate_distance(self, other_position):
        """
        Calculates the distance between the boid and another position.
        """
        return np.linalg.norm(self.position - other_position)

    def keep_within_bounds(self):
        """
        Keeps the boid within specified bounds.
        """
        for i in range(3):
            self.position[i] = self.position[i] % 200 - 100


class Predator:
    def __init__(self):
        self.position = [
            random.uniform(-100, 100),
            random.uniform(-100, 100),
            random.uniform(-100, 100),
        ]
        self.velocity = [0, 0, 0]  # Predator remains stationary for simplicity

    def update(self, boids):
        pass  # Predator doesn't move in this example


boids = [Boid() for _ in range(NUM_BOIDS)]
predator = Predator()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Adjusted camera position for better viewing
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)

    # Draw boids as larger spheres
    glColor3f(1, 1, 1)  # White color
    for boid in boids:
        glPushMatrix()
        glTranslatef(boid.position[0], boid.position[1], boid.position[2])
        glutSolidSphere(5, 10, 10)
        glPopMatrix()

    # Draw predator
    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(predator.position[0], predator.position[1], predator.position[2])
    glutSolidSphere(3, 10, 10)
    glPopMatrix()

    glutSwapBuffers()


def update(value):
    for boid in boids:
        boid.update(boids, predator)
    glutPostRedisplay()
    glutTimerFunc(10, update, 0)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Boids Simulation")
    # OpenGL initialization
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(display)
    glutTimerFunc(10, update, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
