from groq import Groq
from pydantic import BaseModel

import json




class MyGame:

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.messages = []
        self.started = False

    def create_context(self, user_prompt):
        print('creating context...')
        completion = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages= [
                {
                    "role": "system",
                    "content": "you are a world creator for a role game, user will give you an input and from it you must create, based on its conditions, the context where all the game will happen, explain a little bit of the history, and the present status, for example the techonolgy, the politics and about the location."
                    "when giving the context give it in natural language without using headers and bulletpoints. "
                    "do not talk yet about the user and its missions, by the moment just explain the context."
                    "by the moment do not extend much and make it enjoyable to read, using simple words"

                },
                {
                    "role": "user",
                    "content": user_prompt
                }

            ],
            max_tokens=1000,
            temperature=1,
            top_p=1,
            stream=False,
            stop=None,

        )
        print("context created")
        self.context = completion.choices[0].message.content
        return self.context

    def create_character (self):
        completion = self.client.chat.completions.create(
        model="llama3-70b-8192",
        messages= [
            {
                "role": "system",
                "content": "you are a character creator for a role game, from a context input, you must create a JSON of 5 caracteristics and the value of each "
                "caracteristic must be a list of options for the user to choice, for example one caracteristic could be 'faction', and the user could choose between the different factions "
                "that appear in the context, other examples could be wealth status, job, skills, weapon, magic power or tool. Caracteristics must make sense with the context."
                "An example of how has to be the JSON file to return can be: {'Political Affiliation': ['Anarchist', 'Socialist', 'Monarchist', 'Neutral'], 'Occupation': ['Factory Worker', 'Street Vendor', 'Artist', 'Journalist'], 'Neighborhood': ['Gothic Quarter', 'El Raval', 'Eixamp], 'Socio-Economic Status': ['Working Class', 'Middle Class', 'Upper Class', 'Impoverished'], 'Skillset': ['Rhetoric', 'Mechanics', 'Artistry', 'Street Smarts']}"
            },
            {
                "role": "user",
                "content": self.context
            }

        ],
        response_format={"type": "json_object"},
        temperature=1,
        top_p=1,
        stream=False,
        stop=None,

    )
        self.caracteristics = json.loads(completion.choices[0].message.content)
        self.character = {}
        for key in self.caracteristics:
            self.character[key] = self.caracteristics[key][0]
        return self.caracteristics

    def run_game(self):
        messages = [
                {
                    "role": "system",
                    "content": "you are a the creator for a role game, you will be given the context from which the role game should be ambiented and the user character information. "
                    "generate a little bit of context in terms of the user character, explain why he is in the preset situation, how he got here and his surroundings. This small context "
                    "must be consistent to user characteristics. From the context that you create the hole game will grow, so do not define much de future. You must captivate the user so "
                    "he really feels like he is his character and speak in second person."

                },
                {
                    "role": "user",
                    "content": "the context: " + self.context
                },
                {
                    "role": "user",
                    "content": "the user information: " + str(self.character)
                }

            ]
        if self.started:
            messages = [
                {
                    "role": "system",
                    "content": "you are a the creator for a role game where you create situations and user decides which actions to take, "
                    "you will be given the context from which the role game should be ambiented and the user character information. "
                    "Considering  last situation and the action that the user has choseen, return how the situation evlolves, introducing new events so other actions are made possible"
                    "must be consistent to user characteristics.  You must captivate the user so he really feels like he is his character and speak in second person. Do not repeat "
                    "information told before by the assistant"

                },
                {
                    "role": "user",
                    "content": "the context: " + self.context
                },
                {
                    "role": "user",
                    "content": "the user information: " + str(self.character)
                }

            ] + self.messages

        print('Generating first message')
        completion = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages= messages,
            max_tokens=1000 if self.started else 500,
            temperature=1,
            top_p=1,
            stream=False,
            stop=None,

        )
        print("context created")
        self.last_situation = completion.choices[0].message.content
        self.messages.append({'role':'assistant', 'content':self.last_situation})
        self.started = True
        return self.last_situation
    

    
    def generate_options(self):
        print('Generating first message')
        completion = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages= [
                {
                    "role": "system",
                    "content": "you are a the creator for a role game, you will be given the context from which the role game should be ambiented and the user character information. "
                    "Also you will be given the lasts chunks of story that you have generated so you can make sure that they are consistant. From the user input parameter names last situation, "
                    "create a JSON file with 4 actions for the user to choose. Make sure there is consisitency with the context and with user character information. Actions must be short and "
                    "different between themself so the user can really enjoy de game, actions must be exciting. Output must be a JSON file."
                    "A JSON structure like the one that you must return: {'actions': [{'action': 'Ask Lily what's in the package'}, {'action': 'Invite Lily to join the group'}, {'action': 'Continue writing your poem'}, {'action': 'Join the protest discussion with your friends'}]}"

                },
                {
                    "role": "user",
                    "content": "the context: " + self.context
                },
                {
                    "role": "user",
                    "content": "the user information: " + str(self.character)
                },
                {
                    "role": "user",
                    "content": "last situation: " + str(self.last_situation)
                }

            ],
            response_format={"type": "json_object"},
            max_tokens=400,
            temperature=1,
            top_p=1,
            stream=False,
            stop=None,

        )
        self.options = json.loads(completion.choices[0].message.content)
        return self.options
    
    def save_actions_choice(self, option):
        self.messages.append({'role':'user', 'content':option})
        print(self.messages)
