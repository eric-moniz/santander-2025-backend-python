from typing import Annotated

from pydantic import Field, PositiveFloat

from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", examples=["Joao"], max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", examples=["12345678900"], max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", examples=[25])]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta em kilos", examples=[65.8])]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta em metros", examples=[1.73])]
    sexo: Annotated[str, Field(description="Sexo do atleta", examples=["M"], max_length=1)]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixin):
    pass
