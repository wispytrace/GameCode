from copy import deepcopy
import numpy as np

class Agent(object):

    def __init__(self, node):

        self.memory = None
        self.memory_updated = None
        
        self.game = None
        
        self.__node = node

        self.records = []
    
    def set_game(self, game):
        
        self.game = game
        
    def set_memory(self, memory):
        
        self.memory = memory
    
    def update(self, time_delta=1e-4):
        
        
        self.memory_updated = deepcopy(self.memory)
        
        self.memory_updated['status'][self.id] += self.game.status_update_function(self) * time_delta

        esitimate_update = self.game.estimation_update_function(self)
        
        for id, value in esitimate_update.items():
            if id not in self.memory_updated['estimate'].keys():
                self.memory_updated['estimate'][id] = np.zeros(self.game.get_memory_format()['estimate'])
            self.memory_updated['estimate'][id] += value * time_delta


    def flush(self):
        
        self.memory['status'] = self.memory_updated['status']
        self.memory['estimate'] = self.memory_updated['estimate']
    
    
    def record(self, time_delta=0.1):

        current_record = {}
        
        if len(self.records) == 0:
            current_record['time'] = 0
        else:
            current_record['time'] = time_delta + self.records[-1]['time']
            
        current_record['status_vector'] = deepcopy(self.memory['status'])
        current_record['estimate_vector'] = deepcopy(self.memory['estimate'])

        self.records.append(current_record)

    def __getattr__(self, attr): # 当在 Proxy 类中搜索不到对应的属性或方法时（调用 __getattribute__ 方法 便会调用 __getattr__ 方法，此时则利用 getattr() 函数获取代理对象的对应方法再返回即可。
        return getattr(self.__node, attr)

    # def __setattr__(self, attr, val):

    #     if attr == '_Agent__node':      # __x 会变成私有变量，即_x_xx 就可以巧妙避免命名重复
    #         object.__setattr__(self, attr, val)
    #     else:
    #         return setattr(self.__node, attr, val)
