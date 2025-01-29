def calculateMakeSpan(machine_list):
    max_span = 0
    for machine in machine_list:
        if machine.span > max_span:
            max_span = machine.span
    return max_span