import google.generativeai as genai
import os

# Configure API Key (Best practice: use Environment Variables)
# os.environ["GOOGLE_API_KEY"] = ""
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def get_chat_response(user_message, context_data=None):
    """
    Sends message to Gemini and gets response.
    context_data: Optional dictionary of current patient data to make answers relevant.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')

        # System Prompt Engineering
        system_context = (
            "You are a helpful medical assistant for an Alzheimer's risk assessment tool. "
            "You provide clear, empathetic explanations of medical terms (like MMSE, BMI). "
            "Do not provide diagnosis. If asked for medical advice, advise consulting a doctor. "
        )

        if context_data:
            system_context += f"Current patient data context: {str(context_data)}. "

        full_prompt = f"{system_context}\nUser: {user_message}"

        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI Assistant: {str(e)}"