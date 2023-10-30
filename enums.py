from enum import Enum

class Status(Enum):
    TODO = "To Do"
    DOING = "Doing"
    DONE = "Done"
    
class Tags(Enum):
    BUG = "Bug"
    CORRECAO = "Correção"
    MELHORIA = "Melhoria"
    CHAMADO = "Chamado"
    OFFTOPIC = "Off Topic"