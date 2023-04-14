from simulation import GameSimulation, PrescribeSimulation
from games import *
from graph import Graph
from utils import *


def get_model(model_id):

    if model_id == ModelNames.prescibe_time:
        config_dict = prescribe_time_config
        game_model = PreTimeGame()
        model = PrescribeSimulation()
        model.set_T(config_dict['global']['Tf'], config_dict['global']['tao'])
    elif model_id == ModelNames.fixed_time:
        config_dict = fixed_time_config
        game_model = FixTimeGame()
        model = GameSimulation()
        model.set_update_time(config_dict['global']['time_delta'])
    elif model_id == ModelNames.constrained:
        config_dict = constrained_config
        game_model = ConstrainedGame()
        model = GameSimulation()
        model.set_update_time(config_dict['global']['time_delta'])
    elif model_id == ModelNames.pre_constrained:
        config_dict = pre_constrained1_config
        game_model = PreConsGame()
        model = PrescribeSimulation()
        model.set_T(config_dict['global']['Tf'], config_dict['global']['tao'])

    model.set_graph(Graph.load_matrix(config_dict['global']['matrix']))
    model.epochs = config_dict['global']['epochs']
    paramas = combine_dict(config_dict['share'], config_dict['private'])
    model.load_game_model(game_model, paramas)

    return model


if __name__ == '__main__':

    model = get_model(ModelNames.pre_constrained)
    model.run()
