from flask import Flask, render_template, request, jsonify
import os
import argparse
import signal
from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex
from llama_index import LLMPredictor, PromptHelper, ServiceContext
from llama_index import download_loader

from wikiIndexer import wikiQuery

def get_response(query, index):

      response = index.query(query)

      return response.response

# Open the output file in write mode
output_file = open("chat_history", "w")

def handle_exit(sig, frame):
    print("Caught signal, closing file...")
    output_file.close()  # Close the output file before exiting
    exit(0)

# Register signal handler function for SIGTERM
signal.signal(signal.SIGTERM, handle_exit)

if not os.environ['OPENAI_API_KEY']:
    print("You must set the OPENAI_API_KEY environment variable.")
    raise SystemExit(1)

# https://en.wikipedia.org/wiki/Indictment_of_Donald_Trump

parser = argparse.ArgumentParser()
parser.add_argument('--page', type=str, default='Indictment_of_Donald_Trump', help='wiki pages to use')
args = parser.parse_args()

index_name = args.page + ".json"

key_val = os.environ.get("OPENAI_API_KEY")
bot = wikiQuery(key_val)

if os.path.exists(index_name):

    print("loading index from: " + index_name)
    index = GPTSimpleVectorIndex.load_from_disk(index_name)

else:

    print("load data from wiki page: " + args.page)

    WikipediaReader = download_loader("WikipediaReader")
    loader = WikipediaReader()

    # load data from wikipedia page
    wikidocs = loader.load_data([args.page]) 
    # print(wikidocs[0])

    print("Building LLM index...")

    model = bot.load_llm_model()
    index = bot.build_page_index(wikidocs, model)

    index.save_to_disk(index_name)

user_log = "chat_history"
if os.path.exists(user_log):
    output_file = open(user_log, "a")
    print("appending... user log")
else:
    output_file = open(user_log, "w")
    print("creating...user log")


# techmenu chatbot app
wikibot = Flask(__name__)

@wikibot.route('/')
def home():
    return render_template('home.html')

@wikibot.route('/process_text', methods=['POST'])

def process_text():
    # Get the user's input message
    user_message = request.form['user_message']

    # print(user_message)

    # Process the user's message and generate a response
    bot_message = get_response(user_message, index)

    # print(bot_message)

    # Record user questions to the file
    output_file.write(user_message + "\n")

    # Return the chatbot's response as JSON data
    return jsonify({'bot_message': bot_message})

if __name__ == '__main__':
    wikibot.run(host='0.0.0.0', port=7856)

