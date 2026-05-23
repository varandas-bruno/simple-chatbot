import anthropic

class MessageMemory():
    
    def __init__(self, max_buffer: int = 20):
        
        self.buffer: list[dict] = []
        self.max_buffer: int = max_buffer
        self.summary: str = ""
        self.client: anthropic.Client = anthropic.Client()
        
        
    def add_messages(self, role: str, message: str):
        '''Adds a message to the memory buffer with the specified role and content.'''
        
        self.buffer.append({
            "role":role,
            "content":message
        })
        
    
    def show_messages(self):
        '''Returns the current messages stored in the memory buffer.'''
        return self.buffer
    
    
    def summarize_and_reset_conversation(self):
        '''Summarizes the conversation history and resets the memory buffer.'''
        
        prompt = '''
        Summarize the conversation given to initiate a new context window.
        This needs to include all relevant information for the LLM to know what was previously discussed
        '''

        try:
            # Create new temporary buffer to not contaminate original one
            temp_buffer = self.buffer.copy()
            
            temp_buffer.append({
                "role":"user",
                "content":prompt
            })
            
            # Calls LLM to summarize the entire conversation history
            response = self.client.messages.create(
                model="claude-haiku-4-5",
                messages=temp_buffer,
                max_tokens=200
            )
            
            summary = response.content[0].text
            
            # Save summary
            self.summary = summary
            
            # Reset
            self.buffer = []
        
        except Exception as e:
            print("Error ocurred: ", e)
            
        
        
        
        