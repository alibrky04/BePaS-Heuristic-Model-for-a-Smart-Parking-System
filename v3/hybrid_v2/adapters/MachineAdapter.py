from v3.hybrid_v2.models.Machine import Machine
from v3.hybrid_v2.models.MachineAlien import MachineAlien


class MachineAdapter:
    def __init__(self, number_of_machines):
        self.machines_alien = [MachineAlien(i) for i in range(number_of_machines)]
        self.machines_native = [Machine(i.number) for i in self.machines_alien]

    def get_machines_native(self):
        return self.machines_native

    def get_machines_alien(self):
        return self.machines_alien
