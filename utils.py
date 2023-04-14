def combine_dict(share, private):

    for key, value in share.items():
        for id, agent in private.items():
            agent[key] = value

    return private

