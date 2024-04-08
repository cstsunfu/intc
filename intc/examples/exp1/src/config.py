from intc import (
    MISSING,
    AnyField,
    Base,
    BoolField,
    DictField,
    FloatField,
    IntField,
    ListField,
    NestField,
    StrField,
    SubModule,
    cregister,
)


@cregister("embedding", "bert")
class BertEmbedding(Base):
    hidden_size = IntField(
        value=MISSING,
        minimum=1,
        help="the input/output/hidden size for bert, must >= 1",
    )
    dropout_rate = FloatField(
        value=0.0, minimum=0.0, maximum=1.0, help="the dropout rate for bert"
    )


@cregister("embedding", "glove")
class GloveEmbedding:
    """the glove embedding"""

    hidden_size = IntField(
        value=MISSING,
        minimum=1,
        help="the glove embedding size, must >= 1",
    )
    vocab_size = IntField(
        value=MISSING,
        minimum=1,
        help="the vocab size for glove, must >= 1",
    )
    dropout_rate = FloatField(
        value=0.0, minimum=0.0, maximum=1.0, help="the dropout rate for bert"
    )


@cregister("model", "simple_cls")
class Model(Base):
    embedding_combine_method = StrField(
        value="concat",
        options=["concat", "concat_linear"],
        help="the combine method, just `concat` or use `linear` on the concated embedding",
    )
    embedding_size = IntField(
        value=MISSING, help="the sum of bert and glove embedding size"
    )
    active = StrField(
        value="relu",
        options=["relu", "tanh", "sigmoid", "none"],
        help="the activation function",
    )
    submodule = SubModule(
        value={},
        suggestions=[
            "embedding",
        ],
        help="submodules for basic model",
    )
