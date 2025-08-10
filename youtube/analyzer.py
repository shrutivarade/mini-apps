import os
from dotenv import load_dotenv
import openai

# Load your API key
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_extracted_text(file_path="extracted_tools.txt"):
    if not os.path.exists(file_path):
        print("❌ 'extracted_tools.txt' not found.")
        return ""
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_tools_with_gpt(tools_text):
    print("🤖 Asking ChatGPT to analyze tools...")

    prompt = (
        "Here's a noisy and possibly repetitive list of tools and keywords that came out of a YouTube video about AI tools:\n\n"
        f"{tools_text}\n\n"
        "Your task: From this text, extract only the **actual, real AI tools, libraries, platforms, or services** "
        "that are useful or popular in the current AI market (2024–2025). Clean up duplicates and typos. "
        "Return a **concise list of real tools** worth exploring, and optionally include a short 1-line description of each."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert AI market analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    cleaned_output = (response.choices[0].message.content or "").strip()
    print("\n🎯 Recommended AI Tools by ChatGPT:\n")
    print(cleaned_output)

    # Save to a file
    with open("analyzed_ai_tools.txt", "w", encoding="utf-8") as f:
        f.write(cleaned_output)

    print("\n📁 Saved to: analyzed_ai_tools.txt")

if __name__ == "__main__":
    tools_text = load_extracted_text()
    if tools_text:
        analyze_tools_with_gpt(tools_text)
