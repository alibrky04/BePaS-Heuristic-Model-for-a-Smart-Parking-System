import random
import subprocess
import re
import math as m
import json
from v2.nearest_lot.Simulator import Simulator
from v2.nearest_lot.Constants import *

class Controller:
    def __init__(self, COMMAND, glpk_folder_path, distribution, W_CAR = 5, MAP_SIZE = 50):
        self.simulator = Simulator()

        self.P_LOT = NUM_OF_LOTS
        self.W_CAR = W_CAR
        self.MAX_CAPACITY = MAX_CAPACITY
        self.MAP_SIZE = MAP_SIZE
        self.COMMAND = COMMAND
        self.glpk_folder_path = glpk_folder_path
        self.distribution = distribution

        # parking_spaces = [[park state, car_load, res time], x, y]
        self.parking_spaces = {f'p{i + 1}' : 
                               [[[0, 0, 0] for _ in range(self.MAX_CAPACITY)], random.randint(0, self.MAP_SIZE), 
                                random.randint(0, self.MAP_SIZE)] 
                               for i in range(self.P_LOT)}
        
        self.parking_spaces_loads = {f'p{i + 1}' : 0 for i in range(self.P_LOT)}
        self.number_of_cars = {f'p{i + 1}' : 0 for i in range(self.P_LOT)}
        self.waiting_cars = {f'Car{i + 1}': [0, 0, random.randint(0, self.MAP_SIZE), 
                                            random.randint(0, self.MAP_SIZE)] 
                                            for i in range(self.W_CAR)} # [num_of_people, res_time, x, y]

        self.total_of_differences = []
        self.epoch_car_num = []
        self.epoch_people_num = []
        self.epoch_lot_assigned_car_num = [{f'p{i + 1}' : 0 for i in range(self.P_LOT)} for _ in range(len(self.distribution))]
    
    def createCars(self, doChange = False, new_car_num = 5):
        if doChange:
            self.W_CAR = new_car_num

        self.waiting_cars = {f'Car{i + 1}': [random.randint(MIN_PEOPLE, MAX_PEOPLE), 0, random.randint(0, self.MAP_SIZE),
                                            random.randint(0, self.MAP_SIZE)] for i in range(self.W_CAR)}

        # print('The cars in the queuing area')
        # for i in range(self.W_CAR):
            # print(f'Number of people in car {i + 1} is', self.waiting_cars[f'Car{i + 1}'][0])

    def createData(self):
        data_start = """# Data section
data;

"""

        data_parking_space = "set ParkingSpaces :="

        for i in range(self.P_LOT):
            data_parking_space += f" p{i + 1}"
        
        data_parking_space += ";\n"

        data_waiting_cars = "set WaitingCars :="""
        
        for i in range(self.W_CAR):
            data_waiting_cars += f" Car{i + 1}"

        data_waiting_cars += ";\n\n"

        data_init_load = """param :
        initLoad :="""

        for space in self.parking_spaces:
            data_init_load += f"\n    {space}     {self.parking_spaces_loads[space]}"

        data_init_load += ";\n\n"

        data_max = """param :
        maxCarCapacity :="""

        for space in self.parking_spaces:
            data_max += f"\n    {space}     {self.MAX_CAPACITY}"

        data_max += ";\n\n"

        data_parked_car = """param :
        parked_car_num :="""

        for space in self.parking_spaces:
            data_parked_car += f"\n    {space}     {self.number_of_cars[space]}"

        data_parked_car += ";\n\n"

        data_num_people = """param :
        numPeopleInCar :="""

        for car, car_values in self.waiting_cars.items():
            data_num_people += f"\n    {car}     {car_values[0]}"

        data_num_people += ";"

        data = data_start + data_parking_space + data_waiting_cars + data_init_load + data_max + data_parked_car + data_num_people
        
        return data
    
    def createDataForCarModel(self):
        data_start = """# Data section
data;

"""

        data_parking_space = "set ParkingLots :="

        for i in range(self.P_LOT):
            data_parking_space += f" p{i + 1}"
        
        data_parking_space += ";\n"

        data_waiting_cars = "set WaitingCars :="""
        
        for i in range(self.W_CAR):
            data_waiting_cars += f" Car{i + 1}"

        data_waiting_cars += ";\n\n"

        data_init_load = """param :
        maxCarCapacity :="""

        for space in self.parking_spaces:
            data_init_load += f"\n    {space}     {self.MAX_CAPACITY}"

        data_init_load += ";\n\n"

        data_parked_car = """param :
        initNumOfCar :="""

        for space in self.parking_spaces:
            data_parked_car += f"\n    {space}     {self.number_of_cars[space]}"

        data_parked_car += ";"

        data = data_start + data_parking_space + data_waiting_cars + data_init_load + data_parked_car
        
        return data

    def writeData(self, path, model = 1):
        match model:
            case 1:
                data = self.createData()
            case 2:
                data = self.createDataForCarModel()
            case _:
                data = ""
        
        with open(path, 'w') as file:
            file.write(data)
        
    def runSolver(self, doPrint = False):
        result = subprocess.run(self.COMMAND, shell=True, cwd=self.glpk_folder_path, capture_output=True, text=True)

        if doPrint:
            print("Output:", result.stdout)
            print("Error:", result.stderr)

    def takeOutput(self):
        try:
            with open(self.glpk_folder_path + "/SPS.out", 'r') as file:
                solver_output = file.read()
                
                car_assignments = {}
                parking_space_loads = {}
                total_of_differences = 0

                car_assignments_pattern = re.compile(r'isCarAssigned\[(\w+),(\w+)\].val = (\d+)')
                parking_space_load_pattern = re.compile(r'parkingSpaceLoad\[(\w+)\].val = (\d+)')
                load_total_of_differences_pattern = re.compile(r'totalLoadGap.val = (\d+)')

                for line in solver_output.split('\n'):
                    if line.strip():
                        car_match = car_assignments_pattern.match(line)
                        load_match = parking_space_load_pattern.match(line)
                        total_of_differences_match = load_total_of_differences_pattern.match(line)
                        if car_match:
                            car = car_match.group(1)
                            parking_space = car_match.group(2)
                            value = int(car_match.group(3))

                            if car not in car_assignments:
                                car_assignments[car] = {}

                            car_assignments[car][parking_space] = value
                        elif load_match:
                            parking_space = load_match.group(1)
                            load_value = int(load_match.group(2))

                            parking_space_loads[parking_space] = load_value
                        elif total_of_differences_match:
                            total_of_differences = int(total_of_differences_match.group(1))

                assigned_parking_spaces = {}

                for car, spaces in car_assignments.items():
                    assigned_space = next((space for space, value in spaces.items() if value == 1), None)
                    assigned_parking_spaces[car] = assigned_space

                return assigned_parking_spaces, parking_space_loads, total_of_differences
        except FileNotFoundError:
            print(f'The file "{self.glpk_folder_path}" does not exist.')
            return None
        
    def takeOutputForCarModel(self):
        try:
            with open(self.glpk_folder_path + "/SPS_CAR.out", 'r') as file:
                solver_output = file.read()
                
                car_assignments = {}
                num_of_cars = {}
                total_of_differences = 0

                car_assignments_pattern = re.compile(r'isCarAssigned\[(\w+),(\w+)\].val = (\d+)')
                num_of_cars_pattern = re.compile(r'numOfCar\[(\w+)\].val = (\d+)')
                total_of_differences_pattern = re.compile(r'Total_of_Differences.val = (\d+)')

                for line in solver_output.split('\n'):
                    if line.strip():
                        car_match = car_assignments_pattern.match(line)
                        num_match = num_of_cars_pattern.match(line)
                        dif_match = total_of_differences_pattern.match(line)
                        if car_match:
                            car = car_match.group(1)
                            parking_space = car_match.group(2)
                            value = int(car_match.group(3))

                            if car not in car_assignments:
                                car_assignments[car] = {}

                            car_assignments[car][parking_space] = value
                        elif num_match:
                            parking_space = num_match.group(1)
                            num_of_cars_value = int(num_match.group(2))

                            num_of_cars[parking_space] = num_of_cars_value
                        elif dif_match:
                            total_of_differences = int(dif_match.group(1))

                assigned_parking_spaces = {}

                for car, spaces in car_assignments.items():
                    assigned_space = next((space for space, value in spaces.items() if value == 1), None)
                    assigned_parking_spaces[car] = assigned_space

                return assigned_parking_spaces, num_of_cars, total_of_differences
        except FileNotFoundError:
            print(f'The file "{self.glpk_folder_path}" does not exist.')
            return None
    
    def takeOutputForNearModel(self, nearModelType = 1):
        assigned_parking_spaces = {}
        parking_space_loads = {}
        total_of_differences = 0

        for car in self.waiting_cars:
            nearest_parking_lot = self.findNearestParkingLot(car)
            assigned_parking_spaces[car] = nearest_parking_lot
        
        if nearModelType == 1: # For people model comparison
            for car, ps in assigned_parking_spaces.items():
                if ps in parking_space_loads:
                    parking_space_loads[ps] += self.waiting_cars[car][0]
                else:
                    parking_space_loads[ps] = self.parking_spaces_loads[ps] + self.waiting_cars[car][0]

            for ps in self.parking_spaces_loads:
                if ps not in parking_space_loads:
                    parking_space_loads[ps] = self.parking_spaces_loads[ps]
        elif nearModelType == 2: # For car model comparison
            for car, ps in assigned_parking_spaces.items():
                parking_space_loads[ps] = self.number_of_cars[ps]

            for ps in self.number_of_cars:
                if ps not in parking_space_loads:
                    parking_space_loads[ps] = self.number_of_cars[ps]
        
        min_load = 100000
        for ps, load in parking_space_loads.items():
            min_load = min(load, min_load)

        for ps, load in parking_space_loads.items():
            total_of_differences += load - min_load

        return assigned_parking_spaces, parking_space_loads, total_of_differences
        
    def updateState(self, ct=0, isMaxday=0, simType = 3, nearModelType = 1):
        match simType:
            case 1:
                assigned_parking_spaces, parking_space_loads, total_of_differences = self.takeOutput()
            case 2:
                assigned_parking_spaces, parking_space_loads, total_of_differences = self.takeOutputForCarModel()
            case 3:
                assigned_parking_spaces, parking_space_loads, total_of_differences = self.takeOutputForNearModel(nearModelType)
            case _:
                assigned_parking_spaces, parking_space_loads, total_of_differences = {}, {}, 0

        # print()
        
        # Set reservations for the appended cars
        for car, value in self.waiting_cars.items():
            value[1] = self.simulator.SetTimeSlot()

        # Append the cars to the parking lots
        for car, parking_space in assigned_parking_spaces.items():
            for i, lot in enumerate(self.parking_spaces[parking_space][0]):
                if lot[0] == 0:
                    self.parking_spaces[parking_space][0][i] = [1, self.waiting_cars[car][0], self.waiting_cars[car][1]]
                    # print(f'{car} has been assigned to {parking_space}')
                    break

        # Adjust the load values of each parking lot
        for parking_space, value in parking_space_loads.items():
            if value is not None:
                self.parking_spaces_loads[parking_space] = value

        # Increase the number of cars in parking lots according to the solver
        for car, parking_space in assigned_parking_spaces.items():
            if parking_space is not None and simType != 3:
                self.number_of_cars[parking_space] += 1
            if isMaxday:
                self.epoch_lot_assigned_car_num[ct][parking_space] += 1

        # Used for storing total number of cars
        total_car = sum(self.number_of_cars.values())

        # Used for storing total number of people
        total_people = sum(self.parking_spaces_loads.values())

        # Store the total number of cars of this epoch
        self.epoch_car_num.append(total_car)

        # Store the total number of people of this epoch
        self.epoch_people_num.append(total_people)

        # Store the total_of_differences of this epoch
        self.total_of_differences.append(total_of_differences)
    
    def showParkingLots(self):
        for p, pl in self.parking_spaces.items():
            print(f'{p} :', ''.join('|#|  ' if space[0] == 1 else '| |  ' for space in pl[0]), f'({self.number_of_cars[p]})')

    def showData(self):
        print()

        # self.showParkingLots()
        
        print()

        for p,l in self.parking_spaces_loads.items():
            print(f'The load of {p} is {l}')
        
        print()

        print(f'Current total of differences is {self.total_of_differences[-1]}\n')

        print('***********************************************\n')

    def removeCars(self):
        for space, p_lots in self.parking_spaces.items():
            for i, car in enumerate(p_lots[0]):
                if car[0] == 1:
                    car[2] -= TIME_BETWEEN_ROUNDS
                    if car[2] <= 0:
                        # print(f'A car in the {space} and {i + 1}. lot has left')

                        self.parking_spaces_loads[space] -= car[1]
                        car[0] = car[1] = car[2] = 0
                        self.number_of_cars[space] -= 1

                        # self.showParkingLots()
                        # print()
        
    def storeData(self):
        with open(SIM_OUTPUT_FILE, 'r+') as simulation_file:
            try:
                ToD_str = ', '.join(map(str, self.total_of_differences))
                cars_str = ', '.join(map(str, self.distribution))
                
                try:
                    simulation_file.seek(0)
                    existing_data = json.load(simulation_file)
                except json.JSONDecodeError:
                    existing_data = []

                simulation_id = len(existing_data) + 1

                if SIMULATION_DISTRIBUTION == 1:
                    simulation_distribution = "uniform"
                elif SIMULATION_DISTRIBUTION == 2:
                    simulation_distribution = "normal"
                elif SIMULATION_DISTRIBUTION == 3:
                    simulation_distribution = "exponential"

                existing_data.append({
                    "simulation_id": simulation_id,
                    "simulation_distribution": simulation_distribution,
                    "ToD": ToD_str,
                    "car_batch_time": MAX_ROUNDS,
                    "num_of_parking_lots": self.P_LOT,
                    "num_of_cars": cars_str,
                    "min_people": MIN_PEOPLE,
                    "max_people": MAX_PEOPLE,
                    "mean": MEAN,
                    "deviation": DEVIATION,
                    "scale": SCALE
                })

                simulation_file.seek(0)
                json.dump(existing_data, simulation_file, indent=4)
                simulation_file.truncate()
            except Exception as e:
                print(f"Error writing to simulation file: {e}")
    
    def findNearestParkingLot(self, car):
        min_length = 100000
        nearest_parking_lot = ''
        for p, data in self.parking_spaces.items():
            """print(f'{p} x = {data[1]}, {p} y = {data[2]}')
            print(f'{car} x = {self.waiting_cars[car][2]}, {car} y = {self.waiting_cars[car][3]}')"""

            length = m.sqrt((data[1] - self.waiting_cars[car][2])**2 +
                            (data[2] - self.waiting_cars[car][3])**2)
            
            if length < min_length and self.number_of_cars[p] < self.MAX_CAPACITY:
                min_length = length
                nearest_parking_lot = p
        
        self.number_of_cars[nearest_parking_lot] += 1
        return nearest_parking_lot
    
    def __del__(self):
        pass