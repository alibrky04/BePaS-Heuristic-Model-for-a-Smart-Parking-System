class Machine:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.jobs = []  # List of jobs currently assigned
        self.load = 0  # Sum of the lengths of assigned jobs

    def add_job(self, job):
        self.jobs.append(job)
        self.load += job.length

    def remove_job(self, job):
        if job in self.jobs:
            self.jobs.remove(job)
            self.load -= job.length

    def update_jobs(self, decay):
        """
        In rounds after the first, decrease the duration of each job.
        Remove any job whose duration becomes <= 0.
        """
        new_jobs = []
        new_load = 0
        for job in self.jobs:
            job.duration -= decay
            if job.duration > 0:
                new_jobs.append(job)
                new_load += job.length
        self.jobs = new_jobs
        self.load = new_load

    def __repr__(self):
        return f"Machine({self.machine_id}, load={self.load}, jobs={self.jobs})"
