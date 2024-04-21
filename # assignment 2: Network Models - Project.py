# assignment 2: Network Models - Project Management

'''
Assumptions that will be made: 
- all workers charge the same rate
- the rates should be hourly, maybe $60/hr
- work should be kept track in hours
- this is likely a minimization problem
- Do not address resource constraints in developing the project plan for this assignment. Stick to a straightforward critical path analysis. 
- workers = supply???
- tasks = demand???
- per stackoverflow: Completion time of job A <= Start time of job B
- we can have more than 1 of each role
- 

'''
from pulp import *

# -------------Best Case Hours--------------- 

# Creating a dictionary of tasks with best case durations
tasks = {'DescribeProduct':4, 'DevelopMarketingStrategy':15, 'DesignBrochure':8, 'RequirementsAnalysis':8, 'SoftwareDesign':30,
 'SystemDesign':30, 'Coding':40, 'WriteDocumentation':15, 'UnitTesting':25, 'SystemTesting':25, 'PackageDeliverables':6, 'SurveyPotentialMarket':25,
 'DevelopPricingPlan':6, 'DevelopImplementationPlan':15, 'WriteClientProposal':10}

# Creating a list of the tasks
tasks_list = list(tasks.keys())

# Creating a dictionary of task precedences
precedences = {
    'DescribeProduct': [], 
    'DevelopMarketingStrategy': [], 
    'DesignBrochure': ['DescribeProduct'], 
    'RequirementsAnalysis': ['DescribeProduct'], 
    'SoftwareDesign': ['RequirementsAnalysis'], 
    'SystemDesign': ['RequirementsAnalysis'], 
    'Coding': ['SoftwareDesign','SystemDesign'],
    'WriteDocumentation': ['Coding'], 
    'UnitTesting': ['Coding'], 
    'SystemTesting': ['UnitTesting'], 
    'PackageDeliverables': ['WriteDocumentation', 'SystemTesting'], 
    'SurveyPotentialMarket': ['DevelopMarketingStrategy', 'DesignBrochure'], 
    'DevelopPricingPlan': ['PackageDeliverables', 'SurveyPotentialMarket'], 
    'DevelopImplementationPlan': ['DescribeProduct', 'PackageDeliverables'], 
    'WriteClientProposal': ['DevelopPricingPlan', 'DevelopImplementationPlan']
    }


# Creating the LP problem
prob = LpProblem("Critical Path Analysis", LpMinimize)

# Creating dictionaries of task start/end/slack times for use as LP variables
start_times = {task: LpVariable(f"start_{task}", 0, None) for task in tasks_list}
end_times = {task: LpVariable(f"end_{task}", 0, None) for task in tasks_list}

# Looping thru the tasks, and adding the end times of each tasks predecessor for the constraints
for task in tasks_list:
    prob += end_times[task] == start_times[task] + tasks[task], f"{task}_duration"
    for predecessor in precedences[task]:
        prob += start_times[task] >= end_times[predecessor], f"{task}_predecessor_{predecessor}"


# Creating the objective function
prob += lpSum([end_times[task] for task in tasks_list]), "minimize_end_times"

# Solving the LP problem
status = prob.solve()

# Printing the results
print('------BEST CASE HOURS------')
print("Critical Path time:")
for task in tasks_list:
    if value(start_times[task]) == 0:
        print(f"{task} starts at time 0")
    if value(end_times[task]) == max([value(end_times[task]) for task in tasks_list]):
        print(f"{task} ends at {value(end_times[task])} hours in duration")

# Creating a dictionary so I can put the solution variables in time order
start_end_times = {}

# Adding all the start and end times to the dictionary
for var in prob.variables():
    start_end_times[var.name] = var.varValue

# Sorting the dictionary into time order, for easier solution reading
ordered_times = {start_end_times: v for start_end_times, v in sorted(start_end_times.items(), key=lambda item: item[1])}

# Printing the solution variables
print("\nSolution variable values in time order:")
for key in ordered_times:
    print(key, '=', ordered_times[key])

print('\n------END BEST CASE HOURS------\n')



# --------------Expected Hours-----------------


expected_tasks = {'DescribeProduct':8, 'DevelopMarketingStrategy':25, 'DesignBrochure':15, 'RequirementsAnalysis':12, 'SoftwareDesign':45,
 'SystemDesign':45, 'Coding':55, 'WriteDocumentation':20, 'UnitTesting':35, 'SystemTesting':35, 'PackageDeliverables':10, 'SurveyPotentialMarket':30,
 'DevelopPricingPlan':8, 'DevelopImplementationPlan':20, 'WriteClientProposal':13}

# Expected hours task dictionary
expected_tasks_list = list(expected_tasks.keys())

# Creating the LP problem
prob = LpProblem("Critical Path Analysis", LpMinimize)

# Creating dictionaries of task start/end times for use as LP variables
expected_start_times = {task: LpVariable(f"start_{task}", 0, None) for task in expected_tasks_list}
expected_end_times = {task: LpVariable(f"end_{task}", 0, None) for task in expected_tasks_list}

# Looping thru the tasks, and adding the end times of each tasks predecessor for the constraints
for task in expected_tasks_list:
    prob += expected_end_times[task] == expected_start_times[task] + expected_tasks[task], f"{task}_duration"
    for predecessor in precedences[task]:
        prob += expected_start_times[task] >= expected_end_times[predecessor], f"{task}_predecessor_{predecessor}"

# Creating the objective function
prob += lpSum([expected_end_times[task] for task in expected_tasks_list]), "minimize_end_times"

# Solving the LP problem
status = prob.solve()

# Printing the results
print('\n------EXPECTED HOURS------')
print("Critical Path time:")
for task in expected_tasks_list:
    if value(expected_start_times[task]) == 0:
        print(f"{task} starts at time 0")
    if value(expected_end_times[task]) == max([value(expected_end_times[task]) for task in expected_tasks_list]):
        print(f"{task} ends at {value(expected_end_times[task])} hours in duration")

# Adding all the start and end times to the dictionary
expected_start_end_times = {}

for var in prob.variables():
        expected_start_end_times[var.name] = var.varValue

# Sorting all the solution variables in time order, for easier solution reading
expected_ordered_times = {expected_start_end_times: v for expected_start_end_times, v in sorted(expected_start_end_times.items(), key=lambda item: item[1])}

# Print the solution variables
print("\nSolution variable values in time order:")
for key in expected_ordered_times:
    print(key, '=', expected_ordered_times[key])

print('\n------END EXPECTED HOURS------\n')



# -------------Worst Case hours---------------

worst_tasks = {'DescribeProduct':12, 'DevelopMarketingStrategy':30, 'DesignBrochure':20, 'RequirementsAnalysis':15, 'SoftwareDesign':60,
 'SystemDesign':60, 'Coding':70, 'WriteDocumentation':23, 'UnitTesting':40, 'SystemTesting':40, 'PackageDeliverables':13, 'SurveyPotentialMarket':35,
 'DevelopPricingPlan':10, 'DevelopImplementationPlan':24, 'WriteClientProposal':15}

# Expected hours task dictionary
worst_tasks_list = list(worst_tasks.keys())

# Creating the LP problem
prob = LpProblem("Critical Path Analysis", LpMinimize)

# Creating dictionaries of task start/end times for use as LP variables
worst_start_times = {task: LpVariable(f"start_{task}", 0, None) for task in worst_tasks_list}
worst_end_times = {task: LpVariable(f"end_{task}", 0, None) for task in worst_tasks_list}

# Looping thru the tasks, and adding the end times of each tasks predecessor for the constraints
for task in worst_tasks_list:
    prob += worst_end_times[task] == worst_start_times[task] + worst_tasks[task], f"{task}_duration"
    for predecessor in precedences[task]:
        prob += worst_start_times[task] >= worst_end_times[predecessor], f"{task}_predecessor_{predecessor}"

# Creating the objective function
prob += lpSum([worst_end_times[task] for task in worst_tasks_list]), "minimize_end_times"

# Solving the LP problem
status = prob.solve()

# Printing the results
print('\n------WORST CASE HOURS------')
print("Critical Path time:")
for task in worst_tasks_list:
    if value(worst_start_times[task]) == 0:
        print(f"{task} starts at time 0")
    if value(worst_end_times[task]) == max([value(worst_end_times[task]) for task in worst_tasks_list]):
        print(f"{task} ends at {value(worst_end_times[task])} hours in duration")

# Adding all the start and end times to the dictionary
worst_start_end_times = {}

for var in prob.variables():
    worst_start_end_times[var.name] = var.varValue

# Sorting all the solution variables in time order, for easier solution reading
worst_ordered_times = {worst_start_end_times: v for worst_start_end_times, v in sorted(worst_start_end_times.items(), key=lambda item: item[1])}

# Print the solution variables
print("\nSolution variable values in time order:")
for key in worst_ordered_times:
    print(key, '=', worst_ordered_times[key])

print('\n------END WORST CASE HOURS------\n')