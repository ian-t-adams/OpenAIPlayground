import os
import json
import openai
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

# Create the required variables to access the Azure Question Answering service
# and Azure OpenAI Services
endpoint = "https://question-answering-language-service.cognitiveservices.azure.com/"
credential = AzureKeyCredential(os.getenv("AZURE_KEY_CREDENTIAL"))
knowledge_base_project = "question-answering-bot-demo"
deployment = "production"
openai.api_type = "azure"
openai.api_base = "https://ian-openaiplayground.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = 'ian-openaiplayground'

def get_answer(question):
    # Get the answer from the knowledge base in Azure Cognitive Services
    question_answering_client = QuestionAnsweringClient(endpoint, credential)
    with question_answering_client:
        response = question_answering_client.get_answers(
            project_name=knowledge_base_project,
            deployment_name=deployment,
            question=question,
            top=1
        )
    # Print the question text for reference
    # print("Q: {}".format(question))
    
    # Retrieve the answer from the question answering bot and then print it
    answer = response.answers[0].answer
    # print("A: {}".format(output.answers[0].answer))

    # Retun the answer to the question
    return answer

def qabot_to_aoai(answer):
    # Passes the response from the question answering bot to the AOAI model

    # Format the output from the QA bot to include the signifier for a summarization from AOAI
    bot_answer = answer + '\n\nTl;dr'

    # REVIEW: Print the length of the bot answer for reference - may want to cut off since summarization
    # doesn't work well with short answer.
    print(len(bot_answer))

    # Submit the answer from the QA Bot to the AOAI model for summariation
    response = openai.Completion.create(
      engine="iandavinci003",
      prompt= bot_answer, 
      temperature=0.7,
      max_tokens=60,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None)

    return response

def print_formatted_response(open_ai_response):
        print("\n", "Azure Open AI response: ", open_ai_response['choices'][0]['text'])

def main(question):
    # Main runner for the application to retrieve answers from Azure Cognitive Services Custom Question
    # Answering service in the Language Studio and then pass the answer to the AOAI model to generate a
    # summarized, more humanistic response

    # Call the get_answer() function and pass the question to it to query the QA bot
    qa_bot_response = get_answer(question)
    # Print the answer for reference
    print("QA Bot Response: {}".format(qa_bot_response))#.answers[0].answer))

    # Call the qabot_to_aoai() function and pass the answer to it to query the AOAI model
    # and summarize the response to give a more concise, humanistic response
    response = qabot_to_aoai(qa_bot_response)

    # Print the response from the AOAI model
    print_formatted_response(response)
    

if __name__ == '__main__':
    main(question)
