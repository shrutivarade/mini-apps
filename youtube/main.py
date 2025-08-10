import os
import whisper
import yt_dlp
import openai
from dotenv import load_dotenv
import textwrap


# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def download_audio(youtube_url, output_filename="audio.m4a"):
    if os.path.exists(output_filename):
        print(f"⚠️ Audio file already exists: {output_filename} — skipping download.")
        return output_filename

    print("🔽 Downloading audio...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    print(f"✅ Audio downloaded as: {output_filename}")
    return output_filename


def transcribe_audio(audio_file):
    print("🧠 Transcribing audio with Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    transcript = result["text"]
    print("✅ Transcription complete.")
    return transcript


def extract_ai_tools(transcript):
    print("🤖 Extracting AI tools using OpenAI GPT...")
    system_prompt = "Extract all AI tools, libraries, platforms, and frameworks from this transcript. List only the names."

    # Split transcript into ~3000-character chunks (approx. 1000 tokens)
    chunks = textwrap.wrap(transcript, width=3000)
    all_tools = []

    for i, chunk in enumerate(chunks):
        print(f"\n🧩 Processing chunk {i+1} of {len(chunks)}...")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chunk}
            ]
        )

        result = (response.choices[0].message.content or "").strip()
        all_tools.append(result)

    print("\n🎯 Extracted AI Tools from All Chunks:\n")
    combined = "\n".join(all_tools)
    print(combined)

    # ✅ Save to file for later analysis
    with open("extracted_tools.txt", "w", encoding="utf-8") as f:
        f.write(combined)

    return combined


def main():
    youtube_url = input("🎥 Enter YouTube URL: ").strip()
    audio_file = download_audio(youtube_url)
    transcript = transcribe_audio(audio_file)
    extract_ai_tools(transcript)


if __name__ == "__main__":
    main()
