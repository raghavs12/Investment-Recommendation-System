# import streamlit as st
# import openai

# # Set your OpenAI API key
# openai.api_key = 'your_openai_api_key'

# # Function to generate AI response
# def get_ai_response(prompt):
#     response = openai.Completion.create(
#         engine="text-davinci-003",  # Use a suitable model
#         prompt=prompt,
#         max_tokens=150,             # Adjust the response length
#         temperature=0.7,            # Adjust the creativity level
#         n=1,                        # Number of responses to generate
#         stop=None                   # Stopping sequence
#     )
#     message = response.choices[0].text.strip()
#     return message

# def main():
#     st.title("24/7 Support")
#     st.write("Ask your questions and get instant help!")

#     # Session state to store chat history
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     # Text input for user's message
#     user_input = st.text_input("You:", "")
    
#     if st.button("Send"):
#         if user_input:
#             # Add user message to chat history
#             st.session_state.chat_history.append({"role": "user", "message": user_input})

#             # Get AI response
#             ai_response = get_ai_response(user_input)

#             # Add AI response to chat history
#             st.session_state.chat_history.append({"role": "ai", "message": ai_response})

#     # Display chat history
#     for chat in st.session_state.chat_history:
#         if chat["role"] == "user":
#             st.write(f"**You:** {chat['message']}")
#         else:
#             st.write(f"**Support:** {chat['message']}")

# if __name__ == "__main__":
#     main()
