from simulation import GameSimulation, PrescribeSimulation
from games import *
from graph import Graph
from utils import *
import sys

def get_model(model_id, config_index=0):

    if model_id == ModelNames.PreTimeGameA:
        config_dict = ptg_a_config
        game_model = PreTimeGameA()
        model = PrescribeSimulation()
        model.set_T(config_dict['global']['Tf'], config_dict['global']['tao'])
    elif model_id == ModelNames.FixTimeGameA:
        config_dict = ftg_a_config
        game_model = FixTimeGameA()
        model = GameSimulation()
        model.set_update_time(config_dict['global']['time_delta'])
    elif model_id == ModelNames.ConstrainedGameA:
        config_dict = cg_a_config
        game_model = ConstrainedGameA()
        model = GameSimulation()
        model.set_update_time(config_dict['global']['time_delta'])
    elif model_id == ModelNames.PreConsGameAA:
        config_dict = ptcg_aa_config
        game_model = PreConsGameAA()
        model = PrescribeSimulation()
        model.set_T(config_dict['global']['Tf'], config_dict['global']['tao'])
    elif model_id == ModelNames.PreConsGameAB:
        config_dict = ptcg_ab_config
        game_model = PreConsGameAB()
        model = PrescribeSimulation()
        model.set_T(config_dict['global']['Tf'], config_dict['global']['tao'])
    elif model_id == ModelNames.FixConsGameAA:
        config_dict = ftg_aa_configs[config_index]
        game_model = FixConsGameAA()
        model = GameSimulation()
        model.set_update_time(config_dict['global']['time_delta'])

    model.set_graph(Graph.load_matrix(config_dict['global']['matrix']))
    model.epochs = config_dict['global']['epochs']
    paramas = combine_dict(config_dict['share'], config_dict['private'])
    model.load_game_model(game_model, paramas)

    return model


if __name__ == '__main__':

    config_index = int(sys.argv[1])    
    model = get_model(ModelNames.FixConsGameAA, config_index)
    model.run()
