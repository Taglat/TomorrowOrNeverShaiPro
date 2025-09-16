from typing import List, Optional
from pydantic import BaseModel

class ShaiResponse(BaseModel):
    emotion: List[str] = []
    risk_level: str = "NO_RISK"
    escalation_required: bool = False
    response_to_user: str
    
    @classmethod
    def from_api_response(cls, response_data: dict) -> 'ShaiResponse':
        """Create ShaiResponse from API response data"""
        # Check if we have a simple text response
        if isinstance(response_data, str):
            return cls(
                response_to_user=response_data,
                emotion=["neutral"],
                risk_level="NO_RISK",
                escalation_required=False
            )
        
        # If we have structured response
        if isinstance(response_data, dict):
            if 'choices' in response_data and len(response_data['choices']) > 0:
                message = response_data['choices'][0].get('message', {})
                content = message.get('content', '')
                return cls(
                    response_to_user=content,
                    emotion=["neutral"],
                    risk_level="NO_RISK",
                    escalation_required=False
                )
            
            # Direct response format
            return cls(**response_data)
            
        raise ValueError(f"Unexpected response format: {response_data}")

class UserMessage(BaseModel):
    user_id: int
    message_text: str
    
class EscalationEvent(BaseModel):
    user_id: int
    message: str
    risk_level: str
    emotions: List[str]
    timestamp: str