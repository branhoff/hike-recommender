import os
from langchain.agents.agent_toolkits import create_retriever_tool, create_conversational_retrieval_agent
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain import hub


os.environ["OPENAI_API_KEY"] = None

import os
# llm = OpenAI()


from langchain.document_loaders import UnstructuredPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents import AgentType

embeddings =OpenAIEmbeddings()



# Load FAISS embeddings (OpenAI based)

wa_trail= FAISS.load_local("vectordb", embeddings)
wa_trail = wa_trail.as_retriever()


tool1 = create_retriever_tool(
    wa_trail,
    "search_trails_nearby",
    "provides information about best recommended trails")


tools_trail = [tool1]

# llm chat model
llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo-0613")
# ChatOpenAI(temperature=0.3)


from langchain.schema import SystemMessage

system_message_step1 = SystemMessage(
    content='''
    YOU ARE AN HIKE SUGGESTION EXPERT:
    BASED ON THE GIVEN DATES, WEATHER, AND ESTIMATED DRIVE TIME, PLEASE SUGGEST SOME BEST HIKES/TRAILS.
    """
    '''
)



agent_executor = create_conversational_retrieval_agent(
    llm=llm, 
    tools=tools_trail,
    system_message=system_message_step1,
    remember_intermediate_steps=True,
    verbose=True,
    max_token_limit=3900
)



from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI


from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, initialize_agent, load_tools






from langchain_openai import OpenAI

from langchain.prompts.prompt import PromptTemplate

def trail_recommendation(date, max_drive_time, start_location, prompt_field, difficulty, min_length, max_length, max_elevation_gain):
    merged_text = 'Date' + str(date) + '. Max drive time is' + str(max_drive_time) + '. Start location:' + str(start_location) + ". Suggestion: " + str(prompt_field) + ". Difficulty: " + str(difficulty) + ' Min length: ' + str(min_length) + ' max_length: ' + str(max_length) + ' max elevation gain: ' + str(max_elevation_gain)
    response = agent_executor(merged_text)
    final_answer = response.get('output', 'Sorry, I am not sure how to respond.')
    return final_answer