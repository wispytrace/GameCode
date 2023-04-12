import enum

class ModelNames(enum.Enum):

    prescibe_time = 1

    fixed_time = 2


prescribe_time_config = {

    'global': {
        'matrix': [[1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1]],
        'epochs': 1000,
        'Tf' : 1
    },

    'share' : {
        'n' : {'0', '1', '2', '3', '4'},
        'k' : 0.008
    },

    'private' : {
        '0': {}, 
        '1': {}, 
        '2': {}, 
        '3': {}, 
        '4': {},  
    }
}

fixed_time_config = {

    'global': {
        'matrix': [[1,1,1,1],[1, 1, 1,1], [1, 1, 1, 1], [1,1,1,1]],
        'epochs': 5000,
        'time_delta': 5e-4
    },

    'share': {},

    'private':{
        '0': {'delta': 4, 'eta': 1, 'gama': 20, 'epsilon': 1, 'p': 1, 'q': 10.5}, 
        '1': {'delta': 4, 'eta': 2, 'gama': 20, 'epsilon': 2, 'p': 2, 'q': 5.5}, 
        '2': {'delta': 3, 'eta': 1, 'gama': 20,'epsilon': 1, 'p': 1, 'q': 6}, 
        '3': {'delta': 6, 'eta': 3, 'gama': 20, 'epsilon': 3, 'p': 2, 'q': 11}
    }
}
prescribed_time_constrained_model = {
    # v = {'0': 0.091, '1': 0.161, '2': 0.221, '3': 0.1, '4':0.242, '5': 0.385}
    # n = {'0', '1', '2', '3', '4', '5'}
    # paramas = {
        # '0': {'e1': 0.56, 'e2': 0.075, 'v': v, 'n': n, 'alpha': 100}, 
        # '1': {'e1': 1.37, 'e2': 0.15, 'v': v, 'n': n, 'alpha': 100}, 
        # '2': {'e1': 1.75, 'e2': 0.2, 'v': v, 'n': n, 'alpha': 100}, 
        # '3': {'e1': 1, 'e2': 0.1, 'v': v, 'n': n, 'alpha': 100}, 
        # '4': {'e1': 1.5, 'e2': 0.2, 'v': v, 'n': n, 'alpha': 100}, 
        # '5': {'e1': 2, 'e2': 0.3, 'v': v, 'n': n, 'alpha': 100}, 
    # }
}