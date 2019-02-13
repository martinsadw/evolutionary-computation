import configparser


class Config:
    def __init__(self):
        self.max_velocity = 1

        self.max_stagnation = 1
        self.num_particles = 1

        self.inertia_parameter = 1
        self.local_influence_parameter = 1
        self.global_influence_parameter = 1

    @classmethod
    def load_from_file(cls, config_filename):
        config = cls()

        with open(config_filename, 'r') as config_file:
            config_string = config_file.read()
        config_values = configparser.ConfigParser(inline_comment_prefixes=(";",))
        config_values.read_string(config_string)

        config.max_velocity = float(config_values['section']['acs.pso.maxVelocity'])

        config.max_stagnation = int(config_values['section']['acs.pso.maxStagnation'])
        config.num_particles = int(config_values['section']['acs.pso.numParticles'])

        config.inertia_parameter = float(config_values['section']['acs.pso.inertiaParameter'])
        config.local_influence_parameter = float(config_values['section']['acs.pso.localInfluenceParameter'])
        config.global_influence_parameter = float(config_values['section']['acs.pso.globalInfluenceParameter'])

        return config

    @classmethod
    def load_test(cls):
        config = cls()

        config.max_velocity = 2

        config.max_stagnation = 500
        config.num_particles = 30

        config.inertia_parameter = 1.0
        config.local_influence_parameter = 0.3
        config.global_influence_parameter = 0.2

        return config
