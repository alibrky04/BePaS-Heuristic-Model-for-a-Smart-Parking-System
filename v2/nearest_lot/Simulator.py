import json
import time
import random
import numpy as np
from scipy.stats import norm
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

from v2.nearest_lot import Constants as cnst

plt.rcParams['grid.linewidth'] = 0.25

class Simulator:
    def __init__(self, StartTime = time.time(), days = 1, weeks = 1, months = 1):
        self.StartTime = StartTime
        self.weeks = weeks
        self.months = months
        self.simDays = {'days' : days,
                        'weekDays' : self.weeks * 7,
                        'monthDays' : self.months * 30}
        
        self.xAxises = {'hours' : [i for i in range(1, self.simDays['days'] * 24 + 1)],
                        'weeks' : [i for i in range(1, self.simDays['weekDays'] * 24 + 1)],
                        'months' : [i for i in range(1, self.simDays['monthDays'] * 24 + 1)],
                        'pLots' : [i for i in range(3, 9)]}
        
        self.xAxisTicks = {'halfHours' : [1] + [i for i in range(1, self.simDays['days'] * 24 + 1) if i % (self.simDays['days'] * 2) == 0],
                            'pLots' : [i for i in range(3, 9)],
                            'weekDays' : [i * 24 for i in range(1, self.simDays['weekDays'] + 1)],
                            'monthWeeks' : [i * 180 for i in range(1, self.months * 4 + 1)]}
        self.data_num = 30
        self.reqSize = 0.29
        self.blockSize = 0.05

    def GetUpTime(self):
        Uptime = time.time() - self.StartTime
        return int(Uptime)
    
    def SetTimeSlot(self):
        return random.randint(30,180)

    def SetRemoveTime(self):
        RemoveTime = self.SetTimeSlot() + self.GetUpTime()
        return RemoveTime
    
    def normalDist(self, mean = 8, dev = 4, length = 24, distType = 1):
        match distType:
            case 1: # Frequency-like
                x = np.arange(1, length + 1)
                normalDist = np.ceil(norm.pdf(x, mean, dev) * 100)

                normalDist = [int(num) for num in normalDist]
            case 2: # Fixed
                normalDist = np.round(np.abs(np.random.normal(mean, dev, size=length)))

                normalDist = list(normalDist)

                normalDist = [int(num) for num in normalDist]

                for i in range(len(normalDist)):
                    if normalDist[i] == 0:
                        normalDist[i] = 1
            case 3: # Variable
                normalDist = []

                for _ in range(length):
                    normalDist.append(np.round(np.abs(np.random.normal(random.randrange(mean - 1, mean + 1), 
                                                                  random.randrange(dev - 1, dev + 1)))))

                normalDist = list(normalDist)

                normalDist = [int(num) for num in normalDist]

                for i in range(len(normalDist)):
                    if normalDist[i] == 0:
                        normalDist[i] = 1
            case _:
                normalDist = [1] * length

        return normalDist
    
    def uniformDist(self, l_bound = 1, u_bound = 10, length = 24):
        uniformdDist = []
        for _ in range(length):
            uniformdDist.append(random.randint(l_bound, u_bound))

        # print(f"Distribution: Uniform Distribution\nArrangement: {uniformdDist}")

        return uniformdDist

    def exponentialDist(self, start = 1, end = 12, scale = 6, length = 24, distType = 1):
        match distType:
            case 1: # Frequency-like
                factor = (end / start) ** (1 / (length - 1))
                exponentialDist = [round(start * (factor ** i)) for i in range(length)]
            case 2: # Fixed
                exponentialDist = np.ceil(np.random.exponential(scale=scale, size=length))

                exponentialDist = list(exponentialDist)

                exponentialDist = [int(num) for num in exponentialDist]

                for i in range(len(exponentialDist)):
                    if exponentialDist[i] > 9:
                        exponentialDist[i] = 9
                    elif exponentialDist[i] == 0:
                        exponentialDist[i] = 2
            case 3: # Variable
                exponentialDist = []

                for _ in range(length):
                    exponentialDist.append(np.ceil(np.random.exponential(scale=random.randrange(scale - 2, scale + 2))))

                exponentialDist = list(exponentialDist)

                exponentialDist = [int(num) for num in exponentialDist]

                for i in range(len(exponentialDist)):
                    if exponentialDist[i] > 9:
                        exponentialDist[i] = 9
                    elif exponentialDist[i] == 0:
                        exponentialDist[i] = 2
            case _:
                exponentialDist = [1] * length

        return exponentialDist
    
    def generateDistribution(self, genType = 1, distType = "UNIFORM", dLength = 24, dMean = cnst.MEAN, dDev = cnst.DEVIATION, dScale = cnst.SCALE):
        match (genType, distType):
            case (1, "NORMAL"): # Discrete, fixed, normal
                dSlice1 = self.normalDist(mean=5, dev=2, length=int(dLength/3), distType=2)
                dSlice2 = self.normalDist(mean=8, dev=2, length=int(dLength/3), distType=2)
                dSlice3 = self.normalDist(mean=5, dev=2, length=int(dLength/3), distType=2)
                distribution = dSlice1 + dSlice2 + dSlice3
            case (1, "EXPONENTIAL"): # Discrete, fixed, exponential
                dSlice1 = self.exponentialDist(scale=3, length=int(dLength/3), distType=2)
                dSlice2 = self.exponentialDist(scale=9, length=int(dLength/3), distType=2)
                dSlice3 = self.exponentialDist(scale=3, length=int(dLength/3), distType=2)
                distribution = dSlice1 + dSlice2 + dSlice3
            case (2, "NORMAL"): # Discrete, variable, normal
                dSlice1 = self.normalDist(mean=6, dev=2, length=int(dLength/3), distType=3)
                dSlice2 = self.normalDist(mean=9, dev=2, length=int(dLength/3), distType=3)
                dSlice3 = self.normalDist(mean=6, dev=2, length=int(dLength/3), distType=3)
                distribution = dSlice1 + dSlice2 + dSlice3
            case (2, "EXPONENTIAL"): # Discrete, variable, exponential
                dSlice1 = self.exponentialDist(scale=3, length=int(dLength/3), distType=3)
                dSlice2 = self.exponentialDist(scale=9, length=int(dLength/3), distType=3)
                dSlice3 = self.exponentialDist(scale=3, length=int(dLength/3), distType=3)
                distribution = dSlice1 + dSlice2 + dSlice3
            case (3, "UNIFORM"): # Continuous, fixed, uniform
                distribution = self.uniformDist(cnst.NUM_OF_CARS, cnst.NUM_OF_CARS*2, length=dLength)
            case (3, "NORMAL"): # Continuous, fixed, normal
                distribution = self.normalDist(mean=dMean, dev=dDev, length=dLength, distType=2)
            case (3, "EXPONENTIAL"): # Continuous, fixed, exponential
                distribution = self.exponentialDist(scale=dScale, length=dLength, distType=2)
            case (4, "UNIFORM"): # Continuous, variable, uniform
                distribution = self.uniformDist(random.randint(cnst.NUM_OF_CARS / 2, cnst.NUM_OF_CARS)
                                                , random.randint(cnst.NUM_OF_CARS, cnst.NUM_OF_CARS * 2), length=dLength)
            case (4, "NORMAL"): # Continuous, variable, normal
                distribution = self.normalDist(mean=dMean, dev=dDev, length=dLength, distType=3)
            case (4, "EXPONENTIAL"): # Continuous, variable, exponential
                distribution = self.exponentialDist(scale=dScale, length=dLength, distType=3)
            case (_, _): # Default
                distribution = [1] * dLength

        match distType:
            case "UNIFORM":
                print(f"Distribution: Uniform Distribution\nArrangement: {distribution}")
            case "NORMAL":
                print(f"Distribution: Normal Distribution\nArrangement: {distribution}")
            case "EXPONENTIAL":
                print(f"Distribution: Exponential Distribution\nArrangement: {distribution}")
            case _:
                print(f"Distribution: _ Distribution\nArrangement: {distribution}")

        return distribution
    
    def createStandartPlots(self, plot_type):
        gap = []
        cars = []
        people = []

        with open('SPS/Datas/SimData.txt', 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                if not line.startswith('-'):
                    if line.startswith('g:'):
                        gap = [int(num) for num in line.split()[1:] if num.isdigit()]
                    elif line.startswith('c:'):
                        cars = [int(num) for num in line.split()[1:] if num.isdigit()]
                    elif line.startswith('p:'):
                        people = [int(num) for num in line.split()[1:] if num.isdigit()]
                else:
                    fig, ax1 = plt.subplots()

                    if plot_type == 't_g':
                        x = self.xAxises['hours']
                        y1 = gap
                        y2 = cars

                        x_label = 'Hours'
                        y1_label = 'Gap'
                        y2_label = 'Cars'

                    elif plot_type == "t_p":
                        x = self.xAxises['hours']
                        y1 = people
                        y2 = cars

                        x_label = 'Hours'
                        y1_label = 'People'
                        y2_label = 'Cars'

                    line1, = ax1.plot(x, y1, marker='o', linestyle='-', color='blue', label=y1_label)
                    ax1.set_ylabel(y1_label, color='blue')

                    ax2 = ax1.twinx()

                    line2, = ax2.plot(x, y2, marker='o', linestyle='-', color='red', label=y2_label)
                    ax2.set_ylabel(y2_label, color='red')

                    plt.xticks(self.xAxisTicks['halfHours'])
                    ax1.set_xlabel(x_label)

                    lines = [line1, line2]
                    labels = [line.get_label() for line in lines]

                    plt.legend(lines, labels, loc='upper left')
                    ax1.grid()
                    ax2.grid()
                        
                    plt.show()
    
    def createBarPlots(self, plot_type):
        gap = []
        cars = []
        people = []

        bar_width = 0.2

        with open('SPS/Datas/SimData.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith('g:'):
                    gap.append(max([int(num) for num in line.split()[1:] if num.isdigit()]))
                elif line.startswith('c:'):
                    cars.append(max([int(num) for num in line.split()[1:] if num.isdigit()]))
                elif line.startswith('p:'):
                    people.append(max([int(num) for num in line.split()[1:] if num.isdigit()]))

            if plot_type == 't_g_2':
                x = self.xAxises['pLots']
                y1 = gap
                y2 = cars

                x_label = 'Parking Lots'
                y1_label = 'Gap'
                y2_label = 'Cars'

            elif plot_type == "t_p_2":
                x = self.xAxises['pLots']
                y1 = people
                y2 = cars

                x_label = 'Parking Lots'
                y1_label = 'People'
                y2_label = 'Cars'

            fig, ax1 = plt.subplots()

            ax1.bar(x - bar_width/2, y1, bar_width, color='blue', alpha=0.7, label=y1_label)
            ax1.set_ylabel(y1_label, color='blue')

            ax2 = ax1.twinx()

            ax2.bar(x + bar_width, y2, bar_width, color='red', alpha=0.7, label=y2_label)
            ax2.set_ylabel(y2_label, color='red')

            plt.xticks(self.xAxisTicks['pLots'])
            ax1.set_xlabel(x_label)
                        
            plt.show()
        
    def createAveragePlots(self, plot_type):
        gap = []
        cars = []
        people = []
        gapError = [0] * 24
        peopleError = [0] * 24

        with open('SPS/Datas/SimData.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith('g:'):
                    gap.append([int(num) for num in line.split()[1:] if num.isdigit()])
                elif line.startswith('c:'):
                    cars.append([int(num) for num in line.split()[1:] if num.isdigit()])
                elif line.startswith('p:'):
                    people.append([int(num) for num in line.split()[1:] if num.isdigit()])
                
            transposed_lists = zip(*gap), zip(*cars), zip(*people)

            # gap, cars, people
            averages = [[round(sum(nums) / len(nums)) for nums in group] for group in transposed_lists]
            
            if plot_type == 't_g':
                x = self.xAxises['hours']
                y1 = averages[0]
                y2 = averages[1]
                
                """
                for g in gap:
                    for i, gapNumber in enumerate(g):
                        gapError[i] += abs(gapNumber - averages[0][i])

                averageErrors = [round(x / self.data_num) for x in gapError]
                """
                
                x_label = 'Time (Hours)'
                y1_label = 'Total of Differences (ToD)'
                y2_label = 'Cars'

            elif plot_type == "t_p":
                x = self.xAxises['hours']
                y1 = averages[2]
                y2 = averages[1]

                """
                for p in people:
                    for i, peopleNumber in enumerate(p):
                        peopleError[i] += abs(peopleNumber - averages[1][i])

                averageErrors = [round(x / self.data_num) for x in peopleError]
                """

                x_label = 'Time (Hours)'
                y1_label = 'People'
                y2_label = 'Cars'

            X_Y_Spline1 = make_interp_spline(x, y1)
            X_Y_Spline2 = make_interp_spline(x, y2)

            X_ = np.linspace(min(x), max(x), 481)
            Y1_ = X_Y_Spline1(X_)
            Y2_ = X_Y_Spline2(X_)

            fig, ax1 = plt.subplots(figsize=(6,4), dpi=150)

            line1, = ax1.plot(X_, Y1_, marker='o', markevery=(0,20), color='blue', label=y1_label)
            ax1.set_ylabel(y1_label, color='blue')

            ax2 = ax1.twinx()

            line2, = ax2.plot(X_, Y2_, marker='o', markevery=(0,20), color='red', label=y2_label)
            ax2.set_ylabel(y2_label, color='red')

            plt.xticks(self.xAxisTicks['halfHours'])
            ax1.set_xlabel(x_label)

            # ax1.errorbar(x, y1, yerr=averageErrors, ecolor='black', capsize=2.5, capthick=0.5, linewidth=0.15, linestyle='None')

            lines = [line1, line2]
            labels = [line.get_label() for line in lines]

            plt.legend(lines, labels, loc='upper left', fontsize='8')
            ax1.grid(linewidth=0.25)
                        
            plt.show()
    
    def createNormalDistPlots(self, dataType):
        if dataType == 'mu':
            xLabel = 'σ'
        elif dataType == 'mean':
            xLabel = 'μ'

        with open('SPS/Datas/SimData.txt', 'r') as file:
            data = file.read()
        
        phases = data.strip().split('END\n')
        averages = []
        
        for phase in phases:
            lines = phase.strip().split('\n')
            for line in lines:
                if line.startswith('g:'):
                    g_values = list(map(int, line.split()[1:]))
                    average_g = sum(g_values) / len(g_values)
                    averages.append(average_g)
                    break

        X = range(2, 2 + len(averages))

        X_Y_Spline1 = make_interp_spline(X, averages)

        X_ = np.linspace(min(X), max(X), 751)
        Y_ = X_Y_Spline1(X_)

        num_markers = 15
        markevery = int(len(X_) / (num_markers - 1))
        
        plt.figure(figsize=(6,4), dpi=150)
        plt.plot(X_, Y_, marker='o', markevery=markevery,label='Average ToD')
        plt.xlabel(xLabel)
        plt.xticks(range(2, 2 + len(averages)))
        plt.ylabel('Average ToD')
        plt.grid(linewidth=0.25)
        plt.legend()
        plt.show()
        
    def createTransactionPlots(self, distribution, distType = 2):
        epoch_size = 0
        totalSizes = {'dayTotalSize' : [],
                      'weekTotalSize' : [],
                      'monthTotalSize' : []}
        
        distLists = {'dayDistList': [],
                     'weekDistList' : [],
                     'monthDistList' : []}
        
        xLabels = {'x1Label' : '1 Day',
                   'x2Label' : '1 Week',
                   'x3Label' : '1 Month'}
        
        y_label = 'Ledger Size (MB)'

        if distribution == 'normal':
            for d, dl in zip(self.simDays.values(), distLists.values()):
                for _ in range(d):
                    dl.append(self.normalDist(dev=random.choice( [3.75, 4] ), distType=distType))
        elif distribution == 'expo':
            for d, dl in zip(self.simDays.values(), distLists.values()):
                for _ in range(d):
                    dl.append(self.exponentialDist(start=random.choice( [1, 2, 3] ), end= random.choice( [10, 11] ), distType=distType))

        for dist, size in zip(distLists.values(), totalSizes.values()):
            for req in dist:
                for r in req:
                    epoch_size += r * self.reqSize + self.blockSize
                    size.append(epoch_size)
                
            epoch_size = 0

        plt.figure(figsize=(6,4), dpi=150)

        # Plot for 1 Month
        plt.scatter(self.xAxises['months'], totalSizes['monthTotalSize'], color='green', s=5, label=xLabels['x3Label'])

        # Plot for 1 Week
        plt.scatter(self.xAxises['weeks'], totalSizes['weekTotalSize'], color='red', s=5, label=xLabels['x2Label'])

        # Plot for 1 Day
        plt.scatter(self.xAxises['hours'], totalSizes['dayTotalSize'], color='blue', s=5, label=xLabels['x1Label'])

        plt.xlabel('Time (Hours)')
        plt.ylabel(y_label)

        plt.legend()
        plt.grid(linewidth=0.25)
        plt.show()

    def createComparisonPlots(self, comparisonType='people-near'):
        ToD = [[], []]
        cars = [[], []]
        people = [[], []]
        ToDError = [[0] * 24, [0] * 24]

        with open('SPS/Datas/SimData.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                if line.startswith('g:'):
                    ToD[0].append([int(num) for num in line.split()[1:] if num.isdigit()])
                elif line.startswith('c:'):
                    cars[0].append([int(num) for num in line.split()[1:] if num.isdigit()])
                elif line.startswith('p:'):
                    people[0].append([int(num) for num in line.split()[1:] if num.isdigit()])

        with open('SPS/Datas/SimData2.txt', 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                if line.startswith('g:'):
                    ToD[1].append([int(num) for num in line.split()[1:] if num.isdigit()])
                elif line.startswith('c:'):
                    cars[1].append([int(num) for num in line.split()[1:] if num.isdigit()])
                elif line.startswith('p:'):
                    people[1].append([int(num) for num in line.split()[1:] if num.isdigit()])

        transposed_lists = [[zip(*ToD[0]), zip(*cars[0]), zip(*people[0])],
                            [zip(*ToD[1]), zip(*cars[1]), zip(*people[1])]]

        # ToD, cars, people
        averages = [[[round(sum(nums) / len(nums)) for nums in group] for group in transposed_lists[0]],
                    [[round(sum(nums) / len(nums)) for nums in group] for group in transposed_lists[1]]]
        
        x_label = 'Time (Hours)'
        y_label = 'ToD'

        if comparisonType == 'people-near':
            x = self.xAxises['hours']
            y1 = averages[0][0]
            y2 = averages[1][0]
            y1_label = 'Nearest Lot Model'
            y2_label = 'People Model'
        elif comparisonType == 'car-near':
            x = self.xAxises['hours']
            y1 = averages[0][0]
            y2 = averages[1][0]
            y1_label = 'Nearest Lot Model'
            y2_label = 'Car Model'

        for t in ToD[0]:
            for i, ToDNumber in enumerate(t):
                ToDError[0][i] += abs(ToDNumber - averages[0][0][i])

        for t in ToD[1]:
            for i, ToDNumber in enumerate(t):
                ToDError[1][i] += abs(ToDNumber - averages[1][0][i])

        averageErrors = [[round(x / self.data_num) for x in ToDError[0]],
                            [round(x / self.data_num) for x in ToDError[1]]]
        
        X_Y_Spline1 = make_interp_spline(x, y1)
        X_Y_Spline2 = make_interp_spline(x, y2)

        X_ = np.linspace(min(x), max(x), 481)
        Y1_ = X_Y_Spline1(X_)
        Y2_ = X_Y_Spline2(X_)

        y1 = np.array(y1)
        y2 = np.array(y2)
        
        # Fill Between
        fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
        
        ax.plot(x, y1, color='orange', label=y1_label)
        ax.fill_between(x, y1 - averageErrors[0], y1 + averageErrors[0], color='orange', alpha=0.2)
        ax.plot(x, y2, color='green', label=y2_label)
        ax.fill_between(x, y2 - averageErrors[1], y2 + averageErrors[1], color='green', alpha=0.2)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_xticks(self.xAxisTicks['halfHours'])
        ax.legend(fontsize='6', loc='upper left')
        ax.grid(linewidth=0.25)
        ax.margins(x=0.014, y=0.015)

        inset_size = "27%"
        axins = inset_axes(ax, width=inset_size, height=inset_size, bbox_to_anchor=(0.05, 0.22, 1, 1), bbox_transform=ax.transAxes, loc='lower center') 
        axins.plot(x, y1, color='orange')
        axins.fill_between(x, y1 - averageErrors[0], y1 + averageErrors[0], color='orange', alpha=0.2)
        axins.plot(x, y2, color='green')
        axins.fill_between(x, y2 - averageErrors[1], y2 + averageErrors[1], color='green', alpha=0.2)

        axins.set_xlim(17, 22)
        axins.set_ylim(0, 10)

        mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

        plt.show()

    def createFairnessPlots(self, weight_pairs, lot_capacities):
        data1 = {}
        data2 = {}

        with open('SPS/Datas/SimData.txt', 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith('tac:'):
                tac = list(map(int, line.split(':')[1].split()))
                data1['tac'] = tac
            elif line.startswith('lacn:'):
                lacn_json = line.split(':', 1)[1].strip()
                lacn = json.loads(lacn_json)
                data1['lacn'] = lacn

        with open('SPS/Datas/SimData2.txt', 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith('tac:'):
                tac = list(map(int, line.split(':')[1].split()))
                data2['tac'] = tac
            elif line.startswith('lacn:'):
                lacn_json = line.split(':', 1)[1].strip()
                lacn = json.loads(lacn_json)
                data2['lacn'] = lacn

        fairness_metrics1 = self.calculateFairnessMetric(weight_pairs, lot_capacities, data1)["fairness_metrics"]
        fairness_metrics2 = self.calculateFairnessMetric(weight_pairs, lot_capacities, data2)["fairness_metrics"]

        x_labels = ['0-1', '1-0']
        x = np.linspace(0, len(weight_pairs) - 1, len(weight_pairs))

        plt.figure(figsize=(6, 4), dpi=150)
        plt.plot(x, fairness_metrics1, marker='o', label='BePaS', color='blue', markevery=5)
        plt.plot(x, fairness_metrics2, marker='o', label='Nearest Lot Model', color='red', markevery=10)
        plt.xticks([0, len(weight_pairs) - 1], x_labels, rotation=45)
        
        plt.xlabel('Weight')
        plt.ylabel('Fairness')
        
        plt.grid()
        plt.legend()
        plt.tight_layout()
        
        plt.show()
    
    def createFairnessPlotsForDifMetrics(self, weight_pairs, lot_capacities):
        import numpy as np
        import json
        import matplotlib.pyplot as plt

        data1 = {}
        data2 = {}

        # Load data1
        with open('SPS/Datas/SimData.txt', 'r') as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('tac:'):
                tac = list(map(int, line.split(':')[1].split()))
                data1['tac'] = tac
            elif line.startswith('lacn:'):
                lacn_json = line.split(':', 1)[1].strip()
                lacn = json.loads(lacn_json)
                data1['lacn'] = lacn

        # Load data2
        with open('SPS/Datas/SimData2.txt', 'r') as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('tac:'):
                tac = list(map(int, line.split(':')[1].split()))
                data2['tac'] = tac
            elif line.startswith('lacn:'):
                lacn_json = line.split(':', 1)[1].strip()
                lacn = json.loads(lacn_json)
                data2['lacn'] = lacn

        # Calculate metrics
        results1 = self.calculateFairnessMetric(weight_pairs, lot_capacities, data1)
        results2 = self.calculateFairnessMetric(weight_pairs, lot_capacities, data2)

        fairness_metrics1 = results1["fairness_metrics"]
        phi_j_averages1 = results1["phi_j_averages"]
        psi_j_averages1 = results1["psi_j_averages"]

        fairness_metrics2 = results2["fairness_metrics"]
        phi_j_averages2 = results2["phi_j_averages"]
        psi_j_averages2 = results2["psi_j_averages"]

        x_labels = ['0.0-1.0', '1.0-0.0']
        x = np.linspace(0, len(weight_pairs) - 1, len(weight_pairs))

        # Plot settings
        fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=150)

        # Fairness Metrics
        axes[0].plot(x, fairness_metrics1, label='BePaS', color='#38459C', linestyle='-', marker='o', markevery=5)
        axes[0].plot(x, fairness_metrics2, label='Nearest Lot', color='#A01728', linestyle='-', marker='o', markevery=5)
        axes[0].set_xticks([0, len(weight_pairs) - 1])
        axes[0].set_xticklabels(x_labels)
        axes[0].set_xlabel('Weight')
        axes[0].set_ylabel('Composite Metric')
        axes[0].legend(loc='upper left', frameon=True)
        axes[0].grid(axis='y', linestyle='--', alpha=0.7)

        # Capacity Metrics
        axes[1].plot(x, phi_j_averages1, label='BePaS', color='#E85D04', linestyle='-', marker='o', markevery=5)
        axes[1].plot(x, phi_j_averages2, label='Nearest Lot', color='#D00000', linestyle='-', marker='o', markevery=5)
        axes[1].set_xticks([0, len(weight_pairs) - 1])  # Only show edges
        axes[1].set_xticklabels(x_labels)
        axes[1].set_xlabel('Weight')
        axes[1].set_ylabel('Capacity Metric')
        axes[1].legend(loc='upper left', bbox_to_anchor=(0, 0.9), frameon=True)
        axes[1].grid(axis='y', linestyle='--', alpha=0.7)

        # ToD Metrics
        axes[2].plot(x, psi_j_averages1, label='BePaS', color='#005B96', linestyle='-', marker='o', markevery=5)
        axes[2].plot(x, psi_j_averages2, label='Nearest Lot', color='#288347', linestyle='-', marker='o', markevery=5)
        axes[2].set_xticks([0, len(weight_pairs) - 1])
        axes[2].set_xticklabels(x_labels)
        axes[2].set_xlabel('Weight')
        axes[2].set_ylabel('ToD Metric')
        axes[2].legend(loc='upper left', bbox_to_anchor=(0, 0.9), frameon=True)
        axes[2].grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.show()

    def calculateFairnessMetric(self, weight_pairs, lot_capacities, data):
        tac = data['tac']
        lacn = data['lacn']

        total_p_sums = {f'p{i+1}': 0 for i in range(5)}

        for lots in lacn:
            for i in range(5):
                p_key = f'p{i+1}'
                total_p_sums[p_key] += lots[p_key]

        F_j_values = []
        phi_j_averages = []
        psi_j_averages = []

        for weights in weight_pairs:
            w1, w2 = weights
            phi_j = []
            psi_j = []
            F_j = []

            for i in range(len(lot_capacities)):
                W = tac[i]
                phi_j.append(total_p_sums[f'p{i+1}'] / lot_capacities[i])
                psi_j.append(total_p_sums[f'p{i+1}'] / W)
                F_j.append(w1 * phi_j[-1] + w2 * psi_j[-1])

            F_j_values.append(F_j)
            phi_j_averages.append(np.mean(phi_j))
            psi_j_averages.append(np.mean(psi_j))

        std_devs = [np.std(fj) for fj in F_j_values]
        max_min_differences = [max(fj) - min(fj) for fj in F_j_values]

        fairness_metrics = [1 - (std / dif if dif != 0 else 0) for std, dif in zip(std_devs, max_min_differences)]

        return {
            "fairness_metrics": fairness_metrics,
            "phi_j_averages": phi_j_averages,
            "psi_j_averages": psi_j_averages,
        }

    def __del__(self):
        pass