import pygame
import random


# Constants
WIDTH, HEIGHT = 1000, 600
NUM_BOIDS = 200
MAX_SPEED = 3
BOID_RADIUS = 5
BOID_COLOR = (0, 0, 255)
WINDOW_COLOR = (0, 0, 0)
BOID_SEP_DIST = 50
BOID_ALIGN_DIST = 100
BOID_COHESION_DIST = 100
SEP_WEIGHT = 0.1
ALIGN_WEIGHT = 0.1
COHESION_WEIGHT = 0.1

class Boid:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED

    def update(self, flock):
        separation = self.calculate_separation(flock)
        alignment = self.calculate_alignment(flock)
        cohesion = self.calculate_cohesion(flock)

        self.velocity += separation * SEP_WEIGHT + alignment * ALIGN_WEIGHT + cohesion * COHESION_WEIGHT
        self.velocity = self.velocity.normalize() * MAX_SPEED

        # Update position
        new_position = self.position + self.velocity

        # Avoid screen borders
        avoid_border_dist = 50
        if new_position.x < avoid_border_dist:
            self.velocity.x += 1.0
        elif new_position.x > WIDTH - avoid_border_dist:
            self.velocity.x -= 1.0

        if new_position.y < avoid_border_dist:
            self.velocity.y += 1.0
        elif new_position.y > HEIGHT - avoid_border_dist:
            self.velocity.y -= 1.0

        self.position += self.velocity


    def calculate_separation(self, flock):
        steer = pygame.math.Vector2(0, 0)
        count = 0

        # Minimum distance to maintain between Boids
        min_distance = 50

        for boid in flock:
            dist = self.position.distance_to(boid.position)
            if dist > 0 and dist < min_distance:
                diff = self.position - boid.position
                diff = diff.normalize() / dist
                steer += diff
                count += 1

        if count > 0:
            steer /= count

        if steer.length() > 0:
            steer = steer.normalize()
            steer *= MAX_SPEED
            steer -= self.velocity
            steer = steer.normalize()

        return steer


    def calculate_alignment(self, flock):
        steer = pygame.math.Vector2(0, 0)
        count = 0
        avg_velocity = pygame.math.Vector2(0, 0)

        for boid in flock:
            dist = self.position.distance_to(boid.position)
            if dist > 0 and dist < BOID_ALIGN_DIST:
                avg_velocity += boid.velocity
                count += 1

        if count > 0:
            avg_velocity /= count
            avg_velocity = avg_velocity.normalize() * MAX_SPEED
            steer = avg_velocity - self.velocity
            steer = steer.normalize()

        return steer

    def calculate_cohesion(self, flock):
        steer = pygame.math.Vector2(0, 0)
        count = 0
        avg_position = pygame.math.Vector2(0, 0)

        for boid in flock:
            dist = self.position.distance_to(boid.position)
            if dist > 0 and dist < BOID_COHESION_DIST:
                avg_position += boid.position
                count += 1

        if count > 0:
            avg_position /= count
            desired = avg_position - self.position
            desired = desired.normalize() * MAX_SPEED
            steer = desired - self.velocity
            steer = steer.normalize()

        return steer

    def draw(self, screen):
        pygame.draw.circle(screen, BOID_COLOR, (int(self.position.x), int(self.position.y)), BOID_RADIUS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids Simulation")
    clock = pygame.time.Clock()

    boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BOIDS)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WINDOW_COLOR)

        for boid in boids:
            boid.update(boids)
            boid.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
