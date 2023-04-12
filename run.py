from config import ModelNames, prescribe_time_config
from simulation import PrescribeSimulation
from game import PreTime
from graph import Graph

def combine_info(share, private):

    for key, value in share.items():
        for id, agent in private.items():
            agent[key] = value
    
    return private

def get_model(model_id):

    if model_id == ModelNames.prescibe_time:
        config_dict = prescribe_time_config
        game_model = PreTime()
        model = PrescribeSimulation()
        model.set_T(config_dict['global']['Tf'])


    model.set_graph(Graph.load_matrix(config_dict['global']['matrix']))
    model.epochs = config_dict['global']['epochs']
    paramas = combine_info(config_dict['share'], config_dict['private'])
    model.load_game_model(game_model, paramas)

    return model

        

if __name__ == '__main__':
    
    model = get_model(ModelNames.prescibe_time)
    model.run()



