import enum


class ModelNames(enum.Enum):

    PreTimeGameA = 1
    
    PreConsGameAA = 11
    PreConsGameAB = 12
    
    FixTimeGameA = 2
    FixConsGameAA = 21
    
    ConstrainedGameA = 3
    



ptg_a_config = {

    'global': {
        'matrix': [[0, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]],
        'epochs': 1000,
        'Tf': 1,
        'tao': 0.01
    },

    'share': {
        'n': {'0', '1', '2', '3', '4'},
        'k': 0.008
    },

    'private': {
        '0': {'p': 10, 'status':{'0': [-10]}},
        '1': {'p': 15, 'status':{'1': [-8]}},
        '2': {'p': 20, 'status':{'2': [-6]}},
        '3': {'p': 25, 'status':{'3': [-4]}},
        '4': {'p': 30, 'status':{'4': [-2]}},
    }
}

ftg_a_config = {

    'global': {
        'matrix': [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
        'epochs': 5000,
        'time_delta': 5e-4
    },

    'share': {
        'n': {'0', '1', '2', '3', '4'}
    },

    'private': {
        '0': {'delta': 4, 'eta': 1, 'gama': 20, 'epsilon': 1, 'p': 1, 'q': 10.5},
        '1': {'delta': 4, 'eta': 2, 'gama': 20, 'epsilon': 2, 'p': 2, 'q': 5.5},
        '2': {'delta': 3, 'eta': 1, 'gama': 20, 'epsilon': 1, 'p': 1, 'q': 6},
        '3': {'delta': 6, 'eta': 3, 'gama': 20, 'epsilon': 3, 'p': 2, 'q': 11}
    }
}

ftg_aa_config = {

    'global': {
        'matrix': [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
        'epochs': 10000,
        'time_delta': 3e-5
    },

    'share': {
        'c': 180,
        'a': 0.02,
        'b': 2.5,
        'n': ['0', '1', '2', '3', '4'],
        'alpha': 100,
        'l': 0,
        'u': 80,
        'gama': 5000
    },


    'private': {
        '0': {'delta': 4, 'eta': 1, 'epsilon': 3, 'r':50},
        '1': {'delta': 4, 'eta': 2, 'epsilon': 3, 'r': 55},
        '2': {'delta': 3, 'eta': 1, 'epsilon': 3, 'r': 60},
        '3': {'delta': 6, 'eta': 3, 'epsilon': 3, 'r': 65},
        '4': {'delta': 6, 'eta': 3, 'epsilon': 3, 'r': 70},
    }
}

cg_a_config = {


    'global': {
        'matrix': [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
        'epochs': 30000,
        'time_delta': 1e-3
    },

    'share': {
        'v': {'0': 0.091, '1': 0.161, '2': 0.221, '3': 0.1, '4': 0.242, '5': 0.385},
        'n': ['0', '1', '2', '3', '4', '5'],
        'alpha': 50,
        'k': 1,
        'w': 100
    },

    'private': {
        '0': {'e1': 0.56, 'e2': 0.075},
        '1': {'e1': 1.37, 'e2': 0.15},
        '2': {'e1': 1.75, 'e2': 0.2},
        '3': {'e1': 1, 'e2': 0.1},
        '4': {'e1': 1.5, 'e2': 0.2},
        '5': {'e1': 2, 'e2': 0.3},
    }

}

ptcg_aa_config = {


    'global': {
        'matrix': [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
        'epochs': 3000,
        'Tf': 1,
        'tao': 3e-4
    },

    'share': {
        'v': {'0': 0.091, '1': 0.161, '2': 0.221, '3': 0.1, '4': 0.242, '5': 0.385},
        'n': ['0', '1', '2', '3', '4', '5'],
        'alpha': 50,
        'k': 0.008,
        'w': 1
    },

    'private': {
        '0': {'e1': 0.56, 'e2': 0.075},
        '1': {'e1': 1.37, 'e2': 0.15},
        '2': {'e1': 1.75, 'e2': 0.2},
        '3': {'e1': 1, 'e2': 0.1},
        '4': {'e1': 1.5, 'e2': 0.2},
        '5': {'e1': 2, 'e2': 0.3},
    }

}

ptcg_ab_config = {


    'global': {
        'matrix': [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
        'epochs': 100000,
        'Tf': 1,
        'tao': 1e-5
    },

    'share': {
        'c': 180,
        'a': 0.02,
        'b': 2.5,
        'n': ['0', '1', '2', '3', '4'],
        'alpha': 1000,
        'k': 0.0001,
    },

    'private': {
        '0': {'u': 80, 'l': 0, 'r': 50},
        '1': {'u': 80, 'l': 0, 'r': 55},
        '2': {'u': 80, 'l': 0, 'r': 60},
        '3': {'u': 80, 'l': 0, 'r': 65},
        '4': {'u': 80, 'l': 0, 'r': 70},
    }

}

