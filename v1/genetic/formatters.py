from v1.genetic.Constants import NUMBER_OF_SIMULATIONS, NUMBER_OF_ROUNDS, MINIMUM_JOB_LENGTH, MAXIMUM_JOB_LENGTH, \
    NUMBER_OF_MACHINES, \
    NUMBER_OF_JOBS_PER_ROUND, DECAY_PER_ROUND, SIMULATION_DISTRIBUTION, MEAN, DEVIATION, SCALE, NUMBER_OF_CHROMOSOMES, \
    NUMBER_OF_GEN


def create_machine_lines(machines):
    text_with_spaces = f""
    for machine in machines:
        text_with_spaces += f"Machine Created ID:{machine.machine_id} | Initial Load:{machine.load} | Jobs : []\n"
    return text_with_spaces


def create_job_lines(jobs):
    text_with_spaces = f""
    for job in jobs:
        text_with_spaces += f"Job Created ID:{job.job_id} | Job Length:{job.length} | Job Duration : {job.duration}\n"
    return text_with_spaces


def create_section_line(text, total_length=60, fill_char='-'):
    """
    Creates a section header line with the given text in the middle.
    The overall line length will be exactly total_length characters.

    If the text is too long, it will be truncated.
    """
    # Insert a space before and after the text
    text_with_spaces = f" {text} "
    # Truncate if needed
    if len(text_with_spaces) > total_length:
        text_with_spaces = text_with_spaces[:total_length]

    fill_total = total_length - len(text_with_spaces)
    left_fill = fill_total // 2
    right_fill = fill_total - left_fill

    return f"{fill_char * left_fill}{text_with_spaces}{fill_char * right_fill}"


def create_machine_state_line(machine_list):
    text_with_spaces = ""
    for machine in machine_list:
        machine_id_str = f"Machine ID:{machine.machine_id}"
        load_str = f"Load:{machine.load}"
        jobs_str = f"Jobs:{machine.jobs}"
        # Left-align each field within its fixed width:
        # Machine ID: 20 characters, Load: 10 characters, Jobs: 30 characters.
        line = f"{machine_id_str:<20}{load_str:<10}{jobs_str:<30}\n"
        text_with_spaces += line
    return text_with_spaces


def create_machine_state_histogram_line(machine_list):
    """
    For each machine in machine_list, this function creates a line in the format:
      "Machine ID:{machine.machine_id} Start|( {bar} ) {machine.load}"
    where {bar} is a sequence of '-' characters whose length equals the machine's load.
    The bar is padded (with spaces) to the width of the longest bar among all machines,
    so that the load numbers align vertically.
    """
    if not machine_list:
        return ""

    # Find the maximum load to determine the padding width
    max_load = max(machine.load for machine in machine_list)

    result = ""
    for machine in machine_list:
        bar = "-" * machine.load
        # Pad the bar to max_load characters, then append the machine.load after the bar.
        line = f"Machine ID:{machine.machine_id} Start|{bar:<{max_load}}|{machine.load}\n"
        result += line
    return result


def format_parameters():
    text_with_spaces = (
        f"NUMBER_OF_SIMULATIONS: {NUMBER_OF_SIMULATIONS}\n"
        f"NUMBER_OF_ROUNDS: {NUMBER_OF_ROUNDS}\n"
        f"MINIMUM_JOB_LENGTH: {MINIMUM_JOB_LENGTH}\n"
        f"MAXIMUM_JOB_LENGTH: {MAXIMUM_JOB_LENGTH}\n"
        f"NUMBER_OF_MACHINES: {NUMBER_OF_MACHINES}\n"
        f"NUMBER_OF_JOBS_PER_ROUND: {NUMBER_OF_JOBS_PER_ROUND}\n"
        f"DECAY_PER_ROUND: {DECAY_PER_ROUND}\n"
        f"NUMBER_OF_CHROMOSOMES : {NUMBER_OF_CHROMOSOMES}\n"
        f"NUMBER_OF_GEN: {NUMBER_OF_GEN}\n"
        f"SIMULATION_DISTRIBUTION: {SIMULATION_DISTRIBUTION}\n"
        f"MEAN: {MEAN}\n"
        f"DEVIATION: {DEVIATION}\n"
        f"SCALE: {SCALE}\n"
    )
    return text_with_spaces
