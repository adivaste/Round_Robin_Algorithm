from queue import Queue
import time

no_of_processes = 0
process_object = {}
copy_of_process_object = {}
sorted_project_object_array = []
grantt_chart = []
ready_queue = Queue()
quantum_time = 2
processes_inserted_to_grantt_chart = 0

def take_input():
    try:
        p = int(input("\nEnter the number of processes : "))
        global no_of_processes
        no_of_processes = p
    except:
        print("\n [ Insert Numbers Only ! ]")
        exit()

    for number in range(no_of_processes):
        try:
            po_id = input(f"\n* Enter the ID of process No. {number+1} : ")
            po_arrival_time = int(input("\t- Arrival Time : "))
            po_burst_time = int(input("\t- Burst Time   : "))

            process_object[po_id] = {
                'id' : po_id,
                'arrival_time' : po_arrival_time,
                'burst_time' : po_burst_time
            }
            copy_of_process_object[po_id] = {
                'id' : po_id,
                'arrival_time' : po_arrival_time,
                'burst_time' : po_burst_time
            }
        except:
            print("\n [ Process ID should be String/Number also Arrival time and Burst time must be in numbers ! ]")
            exit()
    global quantum_time
    quantum_time = int(input("\n* Quantum Time Should be : "))


def initialize_queue():
    temp_array = []
    for p in sorted(process_object.items(), key=lambda k_v: k_v[1]['arrival_time']):
        temp_array.append(p)

    global sorted_project_object_array
    sorted_project_object_array = temp_array    # M
    min_at_process = temp_array[0][1]['arrival_time']
    for tp in temp_array:
        if tp[1]['arrival_time'] != min_at_process:
            break
        ready_queue.put( tp[1]['id'])

    first_process_at = sorted_project_object_array[0][1]["arrival_time"]
    if(first_process_at != 0):
        for i in range(first_process_at):
            grantt_chart.append(" #")


def algorithm():

    is_totally_completed = None
    startIndex = 0
    endIndex = 0
    while( not ready_queue.empty() ):

        # Adding process into ready queue
        top = ready_queue.queue[0]

        if ( process_object[top]['burst_time'] <= quantum_time ):
            for i in range(process_object[top]['burst_time']):
                grantt_chart.append(process_object[top]['id'])

            processes_inserted_to_grantt_chart = process_object[top]['burst_time']
            is_totally_completed = True
            process_object[top]['burst_time'] = 0
        else:

            for i in range(quantum_time):
                grantt_chart.append(process_object[top]['id'])

            processes_inserted_to_grantt_chart = quantum_time
            is_totally_completed = False
            process_object[top]['burst_time'] = process_object[top]['burst_time'] - quantum_time

        # Searching for the in-between processes
        startIndex = len(grantt_chart) - processes_inserted_to_grantt_chart
        endIndex = len(grantt_chart) - 1

        for i in range(startIndex+1,endIndex+2):
            for key in process_object:
                if process_object[key]['arrival_time'] == i :
                    ready_queue.put(process_object[key]['id'])

        if (is_totally_completed == False ):
            ready_queue.put(top)
        ready_queue.get(0)

        is_totally_completed = None  # M 

        # Extra Condition for checking 'ideal' is present or not
        if (ready_queue.empty()):
            r_index = None

            burst_time_array = [ p['burst_time'] for p in copy_of_process_object.values() ]
            sum_of_burst_time = sum(burst_time_array)
            temp_grantt_chart = [ x for x in grantt_chart if x!=' #' ]

            if ( sum_of_burst_time == len(temp_grantt_chart) ):
                return;
            for count,process_tuple in enumerate(sorted_project_object_array):
                if top in process_tuple:
                    r_index = count
            print(r_index)
            if (r_index != None):
                no_of_ideal_processes = sorted_project_object_array[r_index+1][1]['arrival_time'] - sorted_project_object_array[r_index][1]['arrival_time'] - processes_inserted_to_grantt_chart
                for i in range(no_of_ideal_processes):
                    grantt_chart.append(" #")
                ready_queue.put(sorted_project_object_array[r_index+1][0])

def rindex(mylist, myvalue):
    return len(mylist) - mylist[::-1].index(myvalue) - 1

def printTable():

    for key in copy_of_process_object:
        copy_of_process_object[key]['completion_time'] = rindex(grantt_chart,key) + 1
        copy_of_process_object[key]['turn_around_time'] = copy_of_process_object[key]['completion_time'] - copy_of_process_object[key]['arrival_time']
        copy_of_process_object[key]['waiting_time'] = copy_of_process_object[key]['turn_around_time'] - copy_of_process_object[key]['burst_time']

    # Process Table 
    print("\n# Table :\n")
    print(f"+{'-'*125}+")
    print(f"|{'Process No':^20}|{'Arrival Time':^20}|{'Burst Time':^20}|{'Completion Time':^20}|{'Turn Around Time':^20}|{'Waiting Time':^20}|")
    print(f"+{'-'*125}+")

    for value in copy_of_process_object.values():
        print(f"|{value['id']:^20}|{value['arrival_time']:^20}|{value['burst_time']:^20}|{value['completion_time']:^20}|{value['turn_around_time']:^20}|{value['waiting_time']:^20}|")
        print(f"|{'':^20}|{'':^20}|{'':^20}|{'':^20}|{'':^20}|{'':^20}|")
    print(f"+{'-'*125}+")

    # Gantt Chart 
    print("\n# Gantt Chart : \n")
    print(f"+{'-'*len(grantt_chart)*5}+")
    print("| ",end="")
    for p in grantt_chart:
        print(p.upper(),end=" | ")
    print()
    print(f"+{'-'*len(grantt_chart)*5}+")
    for i in range(0,len(grantt_chart)+1):
        if (i<10):
            print(i,end=f"{' '*4}")
        else:
            print(i,end=f"{' '*3}")

    # Average time
    print("\n\n# Average Time : \n")

    sum_tat = []
    sum_wt = []

    for value in copy_of_process_object.values():
        sum_tat.append(value["turn_around_time"])
        sum_wt.append(value["waiting_time"])

    avg_tat = sum(sum_tat)/no_of_processes
    avg_wt = sum(sum_wt)/no_of_processes

    print(":: Average TAT = ",end=" ")
    for count,num in enumerate(sum_tat):
        if count == 0: print(f"{num}",end=" ")
        else : print(f"+ {num}",end=" ")
    print(f"  = {sum(sum_tat)}/{no_of_processes}  = {avg_tat}",end="\n\n")

    print(":: Average WT = ",end=" ")
    for count,num in enumerate(sum_wt):
        if count == 0: print(f"{num}",end=" ")
        else : print(f"+ {num}",end=" ")
    print(f"  = {sum(sum_wt)}/{no_of_processes}  = {avg_wt}")

# Driver Code 
take_input()
initialize_queue()
algorithm()
printTable()
