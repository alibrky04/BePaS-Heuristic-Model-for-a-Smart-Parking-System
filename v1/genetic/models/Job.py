class Job:
    def __init__(self, job_id, length, duration):
        self.job_id = job_id
        self.length = length
        self.duration = duration

    def __repr__(self):
        return f"Job({self.job_id}, L={self.length}, D={self.duration})"