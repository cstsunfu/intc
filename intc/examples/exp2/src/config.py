from intc import MISSING, Base, IntField, cregister


@cregister("model", "submodule_exp")
class Model(Base):
    para1 = IntField(1)
    para2 = IntField(MISSING)
    para3 = IntField(MISSING)
    para4 = IntField(500)
