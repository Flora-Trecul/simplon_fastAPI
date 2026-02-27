from pydantic import BaseModel, ConfigDict

class InscriptionCreate(BaseModel):
    user_id: int
    session_id: int
    
class InscriptionRead(BaseModel):
    user_id: int
    session_id: int
     
    model_config = ConfigDict(from_attributes=True)