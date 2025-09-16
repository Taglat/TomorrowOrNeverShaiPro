import httpx
from loguru import logger
from app.core.config import settings
from app.core.schemas import ShaiResponse, UserMessage

class ShaiService:
    def __init__(self):
        self.api_url = settings.SHAI_API_URL
        self.api_key = settings.SHAI_API_KEY
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    async def process_message(self, user_message: UserMessage) -> ShaiResponse:
        """
        Send user message to SHAI.pro API and get response
        """
        try:
            payload = {
                "role": "user",
                "content": user_message.message_text
            }
            logger.debug(f"Sending request to {self.api_url} with payload: {payload}")
            
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                
                response_text = response.text
                logger.debug(f"Received response: {response_text}")
                
                if not response_text:
                    raise ValueError("Empty response received from API")
                    
                response_data = response.json()
                logger.debug(f"Parsed response data: {response_data}")
                
                return ShaiResponse.from_api_response(response_data)
        except Exception as e:
            logger.error(f"Error processing message with SHAI API: {str(e)}")
            raise