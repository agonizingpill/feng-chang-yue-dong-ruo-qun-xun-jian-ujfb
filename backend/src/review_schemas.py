from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,field_validator
class Inputs(BaseModel):
    model_config=ConfigDict(allow_inf_nan=False)
class ReviewInput(Inputs):
    visit_id:int
    reason:str=Field(min_length=5,max_length=400)
    @field_validator('reason')
    @classmethod
    def reason_required(cls,v):
        if len(v.strip())<5:raise ValueError('现场说明至少5字')
        return v.strip()
class DecisionInput(Inputs):
    decision:Literal['upheld','revoked']
    note:str=Field(min_length=2,max_length=400)
    @field_validator('note')
    @classmethod
    def note_required(cls,v):
        if len(v.strip())<2:raise ValueError('裁决说明至少2字')
        return v.strip()
