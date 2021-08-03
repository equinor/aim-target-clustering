import numpy as np

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