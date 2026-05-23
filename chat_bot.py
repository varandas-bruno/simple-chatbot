import anthropic
from dotenv import load_dotenv
from memory import MessageMemory

# Import .env 
load_dotenv()

# Create instance of our memory class
memory = MessageMemory()

def main():
        
    # Limit of messages per session
    current_response: int = 0
    max_responses: int = 5
    
    # Run the chat until the maximum responses allowed is reached
    while current_response < memory.max_buffer:
        
        system_prompt = "You are a helpful assistant"
        
        # Check if the conversation is too long and resets it with a summary of the context window
        if current_response == max_responses:
            memory.summarize_and_reset_conversation()
            if memory.summary:
                system_prompt += f"The previous conversation summary is the following: {memory.summary}"
            
        
        # User write a message
        print("-------------------------")
        user_input = input("Ask something or type 'exit' to stop: ")
        
        if user_input == "exit":
            break
        
        # Create the entire message content with memory information
        memory.add_messages("user", user_input)
        
        try:
            # Create the message for Anthropic LLM
            message = memory.client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=200,
                system=system_prompt,
                messages = memory.buffer
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
            memory.add_messages("assistant", response)
            
        except Exception as e:
            print("Error occurred: ", e)
        
        
        # Closes current cycle
        current_response += 1
        print("Remaining conversation cycles:", max_responses - memory.max_buffer)
        

if __name__ == "__main__":
    main()