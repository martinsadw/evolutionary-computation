import random
import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# http://mnemstudio.org/particle-swarm-introduction.htm


class Particle:
    def __init__(self, pos, fitness_func):
        num_dimensions = len(pos)

        self.pos = pos
        self.vel = [0 for x in range(num_dimensions)]

        self.local_best = fitness_func(self)
        self.local_best_pos = self.pos[:]

    def __repr__(self):
        format_str = "{0:.2f}"

        pos_str = str([format_str.format(i) for i in self.pos])
        vel_str = str([format_str.format(i) for i in self.vel])
        string = "(" + pos_str + " | " + vel_str + "): " + str(self.local_best)

        return string


def fitness(particle):
    x = particle.pos[0]
    y = particle.pos[1]

    # return x**2 + 5*y**2 - 4*x*y + y**3 - 3*x**3 + x**4
    return x**2 + y**2 - 4*x*y + 0.2*(x**2)*(y**2)


def pso(num_particles, num_iterations, a, b, c, low_limit, high_limit, fitness_func):
    num_dimensions = len(low_limit)

    particles = [Particle([0 for x in range(num_dimensions)], fitness_func)]

    global_best = particles[0].local_best
    global_best_pos = particles[0].local_best_pos

    for x in range(num_particles-1):
        new_pos = [random.randrange(low_limit[x], high_limit[x])
                   for x in range(num_dimensions)]
        new_particle = Particle(new_pos, fitness_func)

        if (new_particle.local_best < global_best):
            global_best = new_particle.local_best
            global_best_pos = new_particle.local_best_pos

        particles.append(new_particle)

    np_data = np.array([copy.deepcopy(particles)])

    for x in range(num_iterations):
        for particle in particles:
            for d in range(num_dimensions):
                random_local = random.random()
                random_global = random.random()

                vel_contribution = a * particle.vel[d]
                local_contribution = b * random_local * \
                    (particle.local_best_pos[d] - particle.pos[d])
                global_contribution = c * random_global * \
                    (global_best_pos[d] - particle.pos[d])

                particle.vel[d] = vel_contribution + \
                    local_contribution + global_contribution
                particle.pos[d] += particle.vel[d]

            new_fitness = fitness(particle)
            if (new_fitness < particle.local_best):
                particle.local_best = new_fitness
                particle.local_best_pos = particle.pos[:]

                if (new_fitness < global_best):
                    global_best = new_fitness
                    global_best_pos = particle.pos[:]

        # print(str(global_best_pos) + " -> " + str(global_best))
        np_data = np.append(np_data, [copy.deepcopy(particles)], axis=0)

    if num_dimensions == 2:
        fig = plt.figure()
        fig.suptitle('PSO')

        xlist = np.linspace(low_limit[0], high_limit[0], 400)
        ylist = np.linspace(low_limit[1], high_limit[1], 400)
        X, Y = np.meshgrid(xlist, ylist)
        Z = X**2 + Y**2 - 4*X*Y + 0.2*(X**2)*(Y**2)

        cp = plt.contour(X, Y, Z, 20)
        # plt.clabel(cp, inline=True, fontsize=8)

        # plt.plot([1,2,3,4], [1,4,9,16], 'ro')
        # plt.scatter([particle.pos[0] for particle in particles], [particle.pos[1] for particle in particles])
        # plt.scatter(*zip(*[particle.pos for particle in particles]), s=10)

        scat = plt.scatter([], [], s=10)

        def anim_func(frame, *fargs):
            scat.set_offsets(np.hstack([particle.pos for particle in frame]))

        def init_func():
            scat.set_offsets([])

        anim = animation.FuncAnimation(
            fig, anim_func, frames=np_data, init_func=init_func, interval=200)
        # anim.save('test.mp4', fps=30, extra_args=['-vcodec', 'x264'])

        plt.show()
    # print(particles)

    list.sort(particles, key=fitness_func)
    print(particles[0])


pso(100, 10, 0.2, 0.2, 0.6, (-20, -20), (20, 20), fitness)
