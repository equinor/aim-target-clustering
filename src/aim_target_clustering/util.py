import itertools
import numpy as np
from numpy.core.fromnumeric import clip
import welleng as we
from itertools import permutations, combinations, chain

def create_dataset(num_targets=100, *, volume_meters=(10000,10000,250), value_range_millions=(50,500)):
    '''
    Function to create data for the aim target clustering project.

    Parameters:
    -----------
    num_targets: int
    desired number if targets. Default is 100

    volume_meters: Tuple(int, int, int)
    desired volume in which to place num_targets targets. In meters. Default is 10K, 10K, 250

    value_range_millions: Tuple(int, int)
    value range in millions. Default is 50, 500

    Returns:
    --------
    targets: list<dictionary{
        'value': int
        'x': int
        'y': int
        'z': int
    }>
    '''
    targets = []
    for i in range(num_targets):
        target = {}
        target['id'] = i
        target['value'] = np.random.randint(value_range_millions[0], value_range_millions[1])
        target['x'] = np.random.randint(0, volume_meters[0])
        target['y'] = np.random.randint(0, volume_meters[1])
        target['z'] = np.random.randint(0, volume_meters[2])
        targets.append(target)
    return targets

def calculate_distance(t1, t2):
    '''
    Return distance between two three_dimensional points in space.

    Parameters:
    ----------
    t1, t2 : dictionary{
        'value': int
        'x': int
        'y': int
        'z': int
    }
    points in space, given by a dictionary

    Returns: 
    --------
    distance: int
    distance between given points
    '''
    return np.sqrt((t1['x']-t2['x'])**2 +(t1['y']-t2['y'])**2+ (t1['z']-t2['z'])**2 )

def cost_function(target_list, connector, COST_PER_METER=80):
   # print(connector.md)
    #print("cost function called")
    if connector != None:
        return sum(t['value'] for t in target_list) - 200 - connector.md[-1]*COST_PER_METER
    else:
        return sum(t['value'] for t in target_list) - 200 

def calculate_distance_cart(t1, t2):
    return np.sqrt((t1[0] - t2[0])**2+(t1[1] - t2[1])**2+(t1[2] - t2[2])**2)

    
def basic_greedy_clustering(targets,*, MIN_COST_PER_METER_WELL=40):
    clusters = []
    while len(targets) != 0:
        new_cluster = []
        max_node = max(targets, key= lambda t: t['value'])
        new_cluster.append(max_node)
        targets.remove(max_node)
        for t in targets:
            if calculate_distance(max_node,t)*MIN_COST_PER_METER_WELL < t['value']:
                new_cluster.append(t)
                targets.remove(t)
        if new_cluster != [max_node]:
            clusters.append(new_cluster)
    return clusters

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def partitions(lst):
    for indices in powerset(range(1, len(lst))):
        partition = []
        i = 0
        for j in indices:
            partition.append(lst[i:j])
            i = j
        partition.append(lst[i:])

        yield partition

def try_all_target_combinations(cluster):
    best_partition = []
    highest_value = 0
    for partition in partitions(cluster):
        total_value = 0
        for item in partition:
            #print(item)
            if len(item) > 1:
                #print(cost_function(item, get_shortest_connector(item)))
                total_value += cost_function(item, get_shortest_connector(item))
            else:
                #print(cost_function(item, None))
                total_value += cost_function(item, None)
        if total_value > highest_value:
            best_partition = partition
            highest_value = total_value
    return best_partition, highest_value


def cost_function_cpsat(target_vars, targets):
    current_targets = []
    for i in target_vars:
        print(target_vars[i])
        if target_vars[i] == 1:
            current_targets.append(targets[i])
    connector_array = [[t['x'] , t['y'], t['z']] for t in current_targets]
    prev_dist = np.inf
    best_con = None
    for t in current_targets:
        con = we.connector.connect_points(
            connector_array,
            dls_design = 3.5,
            vec_start = t,
            nev = False
        )
        if con.md[-1] < prev_dist:
            best_con = con
    return cost_function(targets,best_con)

def get_shortest_connector(targets):
    connector_array = [[t['x'] , t['y'], t['z']] for t in targets]
    prev_dist = np.inf
    best_con = None
    # if len(connector_array) == 1:
    #     connector_array = [connector_array]
    #print(np.shape(connector_array))
    for t in connector_array:
        #print(np.shape(t))
        con = we.connector.connect_points(
            connector_array,
            dls_design = 3.5,
            vec_start = t,
            nev = False
        )
        if con.md[-1] < prev_dist:
            best_con = con
    return best_con