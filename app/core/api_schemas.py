from typing import List
from pydantic import BaseModel, Field

class MessageRequest(BaseModel):
    message: str = Field(..., description="Text content of the message to analyze")

class MessageAnalysis(BaseModel):
    emotion: List[str] = Field(default_factory=list, description="List of detected emotions")
    risk_level: str = Field("", description="Assessed risk level")
    escalation_required: bool = Field(False, description="Whether situation requires escalation")
    response_to_user: str = Field("", description="Generated response text")

class MessageResponse(BaseModel):
    message_id: str = Field(..., description="Unique identifier of the processed message")
    analysis: MessageAnalysis = Field(..., description="Complete message analysis")