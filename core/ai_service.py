import os
from anthropic import Anthropic

def generate_call_summary(transcript_text):
    """
    Sends call transcript to Claude and asks for a summary.
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return "Error: Anthropic API key is missing."

    client = Anthropic(api_key=api_key)

    prompt = f"""
    You are an AI assistant for a contact center. 
    Please summarize the following call transcript into 3 bullet points.
    Also, extract any actionable follow-up items.
    
    Transcript:
    {transcript_text}
    """

    try:
        message = client.messages.create(
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="claude-haiku-4-5-20251001",
        )
        return message.content[0].text
        
    except Exception as e:
        return f"Error generating summary: {str(e)}"