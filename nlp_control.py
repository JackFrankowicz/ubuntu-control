import openai
import subprocess
import os

# Set up OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def get_code_from_natural_language(natural_language):
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=f"Convert the following natural language into Ubuntu command line code:\n\n{natural_language}",
        max_tokens=150,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def execute_code(code):
    try:
        result = subprocess.run(code, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode(), result.stderr.decode()
    except subprocess.CalledProcessError as e:
        return e.stdout.decode(), e.stderr.decode()

def backup_to_github(commit_message):
    os.system("git add .")
    os.system(f"git commit -m '{commit_message}'")
    os.system("git push origin main")

if __name__ == "__main__":
    natural_language = input("Enter your command: ")
    code = get_code_from_natural_language(natural_language)
    print(f"Executing code: {code}")
    stdout, stderr = execute_code(code)
    if stdout:
        print(f"Output:\n{stdout}")
    if stderr:
        print(f"Error:\n{stderr}")
    
    backup_choice = input("Do you want to backup changes to GitHub? (yes/no): ")
    if backup_choice.lower() == 'yes':
        commit_message = input("Enter commit message: ")
        backup_to_github(commit_message)
