import matplotlib.pyplot as plt
import random

def fitness_function(chromosome, jobs, num_of_machines):
    # Initialize completion time matrix for machines
    machine_completion_times = [0] * num_of_machines
    # Initialize completion time for each job
    job_completion_times = [0] * len(jobs)

    # determine the max num of operations between all jobs
    num_of_operations = []
    for job in jobs:
        num_of_operations.append(len(job))
    max_operations = max(num_of_operations)

    # iterate through operations in all jobs
    for operation_index in range(max_operations):
        for job_index in chromosome:
            # get the current job
            job = jobs[job_index - 1]
            if operation_index < len(job):
                # getting the required operation of the current job
                (job_id, machine, duration) = job[operation_index]
                # finding the start and end time
                start_time = max(machine_completion_times[machine - 1], job_completion_times[job_id - 1])
                end_time = start_time + duration
                # modify machine and job completion times
                machine_completion_times[machine - 1] = end_time
                job_completion_times[job_id - 1] = end_time

    # The fitness value is the maximum completion time of all jobs
    fitness_value = max(job_completion_times)
    return fitness_value

def Selection(jobs: list):
    # for maximum number of new induviduals will be (n*(n-1))/2
    n = len(jobs)
    itera_num = n * 10
    Num_jobs = []
    # finding the number for each job
    for N in range(n):
        Num_jobs.append(jobs[N][0][0])

    # At least 2 minimum values
    if n < 2:
        print("The list needs to have at least two elements to swap.")
        return jobs[0]
    else:
        New_Chromosomes = []
        for N in range(itera_num):
            random.shuffle(Num_jobs)
            New_Chromosomes.append(Num_jobs.copy())
            

        # Convert to tuples to remove duplicates lists
        New_Chromosomes = set(tuple(sublist) for sublist in New_Chromosomes)
        # Convert tuples back to lists
        New_Chromosomes = [list(item) for item in New_Chromosomes] 
    return New_Chromosomes

def Evaluation(Chromosomes:list, jobs,num_of_machines):
    parents = []
    fitness = []
    for Chromosome in Chromosomes:
        fit = fitness_function(Chromosome,jobs,num_of_machines)
        fitness.append(fit)

    # Find the index of the first minimum value
    min_index = fitness.index(min(fitness))
    # Add that chromosome as parent
    parents.append(Chromosomes[min_index])
    fit_pop = fitness.copy()
    fit_pop.pop(min_index)
    if len(fit_pop) >= 1:
        second_min_index = fit_pop.index(min(fit_pop))
        # Adjust the second index because the list size has changed after the first pop
        if second_min_index >= min_index:
            second_min_index += 1
        parents.append(Chromosomes[second_min_index])
    return parents,fitness

def Crossover(parents:list):
    # getting random position for crossover such that it will not be equals 0 or last position
    crossover = random.sample(range(len(parents[0])), 1)
    while crossover[0] == 0 or crossover[0] == len(parents[0]):
        crossover = random.sample(range(len(parents[0])), 1)
    # Doing crossover operation
    if(len(parents) >= 2):
        child_one = parents[0][:crossover[0]]
        child_one = child_one + [job for job in parents[1] if job not in child_one]
        child_two = parents[1][:crossover[0]]
        child_two = child_two + [job for job in parents[0] if job not in child_two ]
        return child_one,child_two
    else:
        return parents[0],parents[0]
    
def Mutation(child_one:list, child_two:list):
    value_one_list = random.sample(range(len(child_one)), 1)
    value_one = value_one_list[0]
    value_two_list = random.sample(range(len(child_one)), 1)
    value_two = value_two_list[0]
    while value_one == value_two:
        value_one_list = random.sample(range(len(child_one)), 1)
        value_one = value_one_list[0]

    child_one[value_one], child_one[value_two] = child_one[value_two], child_one[value_one]

    value_one_list = random.sample(range(len(child_two)), 1)
    value_one = value_one_list[0]
    value_two_list = random.sample(range(len(child_two)), 1)
    value_two = value_two_list[0]
    while value_one == value_two:
        value_one_list = random.sample(range(len(child_two)), 1)
        value_one = value_one_list[0]

    child_two[value_one], child_two[value_two] = child_two[value_two], child_two[value_one]

    return child_one,child_two

def Genetic_Algorithm(jobs:list):

    chromosomes = Selection(jobs)

    parents, fitness = Evaluation(chromosomes, jobs, num_of_machines)

    child_one, child_two = Crossover(parents)

    child_one, child_two = Mutation(child_one, child_two)

    fit = fitness_function(child_one, jobs, num_of_machines)
    fitness.append(fit)
    chromosomes.append(child_one)
    fit = fitness_function(child_two, jobs, num_of_machines)
    fitness.append(fit)
    chromosomes.append(child_two)

    itera_num = len(jobs) * 10
    for n in range(itera_num):
        parents, fitness = Evaluation(chromosomes, jobs, num_of_machines)
        child_one, child_two = Crossover(parents)
        child_one, child_two = Mutation(child_one, child_two)
        fit = fitness_function(child_one, jobs, num_of_machines)
        fitness.append(fit)
        chromosomes.append(child_one)
        fit = fitness_function(child_two, jobs, num_of_machines)
        fitness.append(fit)
        chromosomes.append(child_two)

    Best_chromosome_index =  fitness.index(min(fitness))
    Best_chromosome = chromosomes[Best_chromosome_index]
    #print(Best_chromosome)
    return Best_chromosome,fitness[Best_chromosome_index]

def Gantt_chart(chromosome: list, jobs: list, num_of_machines: int):
    # Initialize completion times for machines and jobs
    machine_completion_times = [0] * num_of_machines
    job_completion_times = [0] * len(jobs)
    machine_schedules = [[] for _ in range(num_of_machines)]

    # Determine the maximum number of operations across all jobs
    max_operations = max(len(job) for job in jobs)

    # Define a list of colors
    colors = [
        'tab:blue', 'tab:orange', 'tab:green', 'tab:red',
        'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
        'tab:olive', 'tab:cyan'
    ]

    # Iterate through each operation index
    for operation_index in range(max_operations):
        for job_index in chromosome:
            job = jobs[job_index - 1]
            if operation_index < len(job):
                job_id, machine, duration = job[operation_index]
                start_time = max(machine_completion_times[machine - 1], job_completion_times[job_id - 1])
                end_time = start_time + duration

                # Record the operation in the machine's schedule
                machine_schedules[machine - 1].append((job_id, operation_index + 1, start_time, end_time))
                machine_completion_times[machine - 1] = end_time
                job_completion_times[job_id - 1] = end_time

    # Draw the Gantt chart
    fig, ax = plt.subplots()
    y_labels = [f"Machine {i + 1}" for i in range(num_of_machines)]
    level_height = 0.2

    for i, tasks in enumerate(machine_schedules):
        for j, (job, operation, start, end) in enumerate(tasks):
            color = colors[j % len(colors)]
            ax.barh(i, end - start, left=start, height=level_height, align='center', color=color, alpha=0.8)
            task_label = f"({job}.{operation}: {start}->{end})"
            ax.text((start + end) / 2, i, task_label, ha='center', va='center', fontsize=8, color='black')

    ax.set_yticks(range(num_of_machines))
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('Time')
    ax.set_ylabel('Machines')
    ax.invert_yaxis()

    plt.show()

if __name__ == "__main__":
    jobs = []
    with open("jobs.txt", 'r+') as f:
        job_number = 1
        for line in f:
            if line.startswith("number of machines"):
                num_of_machines = int(line.split(':')[1].strip())
                continue
            job = []
            parts = line.split(', ')
            for process in parts[1:]:
                job.append((job_number, int(process.split(':')[0]), int(process.split(':')[1])))
            jobs.append(job)
            job_number += 1
    
    chromosome, fit = Genetic_Algorithm(jobs)
    Gantt_chart(chromosome, jobs, num_of_machines)