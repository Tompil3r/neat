import os.path


class GenomeSavingCallback():
    def __init__(self, population, top=1, override=True, dir='', filenames=[]):
        self.top = top if top > 0 else population
        self.override = override
        self.filepaths = [os.path.join(dir, filename) for filename in filenames] if len(filenames) == top else \
        [os.path.join(dir, f'genome-{idx}.cfg' if self.override else f'genome-{idx}') for idx in range(top)]


    def __call__(self, neat, generation, sort=False):
        if sort:
            neat.sort_genomes()
        
        if self.override:
            for idx in range(self.top):
                neat.genomes[idx].save(path=self.filepaths[idx])
            
            return

        for idx in range(self.top):
            neat.genomes[idx].save(path=self.filepaths[idx] + f'-gen-{generation}.cfg')


class GenerationTermination():
    def __init__(self, stop_generation):
        self.stop_generation = stop_generation


    def __call__(self, neat, curr_generation):
        return curr_generation < self.stop_generation


class FitnessTermination():
    def __init__(self, termination_fitness, top=1):
        self.termination_fitness = termination_fitness
        self.top = top
    

    def __call__(self, neat, sorted=False):
        if sorted:
            for idx in range(self.top):
                if neat.genomes[idx].fitness < self.termination_fitness:
                    return False
        
            return True
        
        count = 0

        for genome in neat.genomes:
            if genome.fitness >= self.termination_fitness:
                count += 1

                if count == self.top:
                    return True
        
        return False




