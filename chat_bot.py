import anthropic
from dotenv import load_dotenv

# Import .env 
load_dotenv()

client = anthropic.Client()

message_history: list[dict] = []

def save_history(message):
    '''
    Appends the response of the LLM to create a history for context.
    '''
    
    message_history.append({
        "role":"assistant",
        "content":message
    })
    
    return message_history
    

def main():
    
    # Limit of messages per session
    current_response: int = 0
    max_responses: int = 5
    
    while current_response < max_responses:
        
        # User write a message
        print("-------------------------")
        user_input = input("Ask something or type 'exit' to stop: ")
        
        if user_input == "exit":
            break
        
        # Create the entire message content with memory information
        message_history.append({
            "role":"user",
            "content":user_input
        })
        
        # Create the message for Anthropic LLM
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=100,
            messages = message_history
        )
        
        # Save output of LLM response
        response = message.content[0].text
        
        # Print the LLM response 
        print("-------------------------")
        print("LLM response: ", response)
        
        # Print accumulative cost of input and output tokens
        print("-------------------------")
        print("Input Tokens: ", message.usage.input_tokens)
        print("-------------------------")
        print("Output Tokens: ", message.usage.output_tokens)
        
        # Append response to save context
        save_history(response)
        
        # Closes current cycle
        current_response += 1
        print("Remaining conversation cycles:", max_responses - current_response)
        

if __name__ == "__main__":
    main()