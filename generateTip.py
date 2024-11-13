import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Initialize the Gemini model with your API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Safety settings
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
        ]

        # Generate content with safety settings
        response = model.generate_content(
            prompt,
            safety_settings=safety_settings,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error in get_gemini_response: {e}")
        return "Oops! Couldn't fetch a tip right now. Try again later."

def generate_readme(tip, next_tip_time):
    while True:
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        time_remaining = next_tip_time - datetime.datetime.now()
        hours, remainder = divmod(time_remaining.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        if time_remaining.total_seconds() <= 0:
            hours, minutes, seconds = 0, 0, 0
            next_tip_time = datetime.datetime.now() + datetime.timedelta(hours=1)
        readme_content = f"""
# 🌟 Daily Developer Tips

Welcome to the **Daily Developer Tips** repository! This space is dedicated to providing concise, practical, and often witty insights to make your coding journey smoother and more enjoyable.

---

## 💡 Today's Tip

<table align="center" cellpadding="10" cellspacing="0" style="background-color: #f4f4f4; border-radius: 8px; max-width: 600px; width: 100%;">
  <tr>
    <td>
      <h4 style="color: #2F80ED; margin: 0;">"{tip}"</h4>
    </td>
  </tr>
</table>

---

### 📅 Last Updated: {today}

Keep coding, keep improving, and don't forget to laugh along the way! Want to contribute or suggest tips? Open an issue or pull request!

---

<div align="center">
    The next tip will be available at {next_tip_time}.
</div>

---

<div align="center">
    Made with ❤️ by an automated script powered by <strong>Google Gemini Flash</strong>.
</div>
"""
        with open("README.md", "w") as file:
          file.write(readme_content)
        time.sleep(1)  # Wait for 1 second before updating the timer
        os.system('cls' if os.name == 'nt' else 'clear') 

if __name__ == "__main__":
    system_prompt = (
        "You are a seasoned developer with a knack for humor and teaching. Generate one concise, highly practical, and universally helpful coding tip "
        "that is accessible to developers of all skill levels—from beginners to professionals. Add a touch of wit or humor to make the advice engaging, "
        "but ensure the core message remains clear, actionable, and valuable. Avoid overly technical jargon or lengthy explanations; aim for a balance of insight, fun, and brevity."
    )

    try:
        new_tip = get_gemini_response(system_prompt)
        next_tip_time = datetime.datetime.now() + datetime.timedelta(hours=1)
        generate_readme(new_tip, next_tip_time)
    except Exception as e:
        print(f"Error in generating or updating README: {e}")
