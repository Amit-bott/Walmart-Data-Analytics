# from fastapi import FastAPI
# from pydantic import BaseModel
# from google import genai
# from google.genai.errors import APIError
 
# # --- 1. CONFIGURATION ---
# # IMPORTANT: FastAPI runs on port 8000 by default. 
# # You must set your GEMINI_API_KEY environment variable.
# try:
#     # Client will automatically pick up the GEMINI_API_KEY from environment variables
#     client = genai.Client()
# except Exception as e:
#     # Handle case where API key is not set
#     print(f"Error initializing Gemini client: {e}")
#     client = None

# app = FastAPI(title="Walmart Sales Summarizer API")

# # --- 2. INPUT DATA STRUCTURE ---
# # Define the structure of the data the API expects from Streamlit
# class SummaryRequest(BaseModel):
#     store_id: int
#     total_sales: float
#     avg_sales: float
#     avg_temp: float
#     max_sales_date: str

# # --- 3. AI SUMMARIZATION LOGIC ---
# def generate_summary_with_gemini(request_data: SummaryRequest):
#     """Constructs the prompt and calls the Gemini API for summarization."""
    
#     # 1. Construct the detailed prompt from the received data
#     prompt = (
#         f"Analyze the following key performance indicators for Walmart Store {request_data.store_id} "
#         f"across the filtered period: Total Sales: ${request_data.total_sales:,.2f}, "
#         f"Average Weekly Sales: ${request_data.avg_sales:,.2f}, "
#         f"Average Temperature: {request_data.avg_temp:.2f}°F. "
#         f"The peak sales of the period occurred on {request_data.max_sales_date}. "
#         "Provide a concise, professional, 3-sentence summary of the store's performance "
#         "and key environmental factors. The tone should be objective and data-driven."
#     )
    
#     if not client:
#         return "Gemini API key not configured on the server."
    
#     try:
#         # 2. Call the Gemini API
#         response = client.models.generate_content(
#             model='gemini-2.5-flash',
#             contents=prompt,
#             config={"temperature": 0.2} # Keep generation focused on facts
#         )
#         return response.text
    
#     except APIError as e:
#         return f"Gemini API Error: Could not generate summary. {e}"
#     except Exception as e:
#         return f"An unexpected error occurred: {e}"

# # --- 4. API ENDPOINT DEFINITION ---
# @app.post("/summarize")
# def get_summary(request_data: SummaryRequest):
#     """Endpoint to receive sales metrics and return an AI summary."""
    
#     # Generate the summary text
#     summary_text = generate_summary_with_gemini(request_data)
    
#     # Return the result as JSON
#     return {"store_id": request_data.store_id, "summary": summary_text}

# # To run: uvicorn main:app --reload
