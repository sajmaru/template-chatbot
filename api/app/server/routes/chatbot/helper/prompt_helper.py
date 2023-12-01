"""
This script demonstrates the use of Vertex AI's TextGenerationModel for creating a context-aware chatbot. The bot acts as an information management manager within a company, providing details about available data, such as table names and column information. It's designed to respond based on the context provided and follow specific instruction patterns.

Functions:
- The script sets up commands (cmd, cmd2, cmd3) to dictate how the bot should interpret and respond to user queries.
- The 'initial_prompt' defines the bot's role and operational guidelines.
- 'chat_prompt_examples' contains examples of input-output pairs, demonstrating how the bot should respond to various queries based on the provided context.

Usage:
1. Import 'vertexai' and relevant classes.
2. Define the bot's behavior and context using predefined commands and prompts.
3. Use 'InputOutputTextPair' to model sample interactions, showcasing the bot's capability to provide specific data information based on the context.

Dependencies:
- vertexai: Google Cloud's Vertex AI SDK for Python.
- TextGenerationModel, InputOutputTextPair from vertexai.preview.language_models: These classes are used to set up the language model and define input-output pairs for training or demonstration purposes.
"""
################################################################
import vertexai
from vertexai.preview.language_models import TextGenerationModel, InputOutputTextPair

cmd = "Only answer from the given context, If the intformation is not present in the context reply 'you don't information reagardong this' "

cmd2 = "Ignore all the privous instructions before this one "

cmd3='is this present in the context, if it is then reply saying yes I have information regarding this table followed by the same previous answer, if not just say I do not have infomation regarding this'

initial_prompt = '''Act as a information management manager play in a company, your role is to inform people about the data the company has and where they can find that data. in the company data there are multiple schemas, each schema has multiple  tables and each table has multiple columns. you  should produce answer only from the given context and you return the table and the columns the user is looking for. you can ask any questions you have before returning the table information. ok?'''

keywors_prompt_examples = """
    input: I am working on a project that requires information regarding operating locations, can you find me the right table
    get keywords from the above sentence and return in a continues string
    
    output:operating locations

    input: I am working on a project that requires information regarding country charge card, can you find me the right table
    get keywords from the above sentence and return in a continues string

    output:country charge card

    input: I am working on a project that requires information regarding purchase orders, can you find me the right table
    get keywords from the above sentence and return in a continues string

    output:purchase orders

    input: I am working on a project that requires information regarding locations where customers are living, can you find me the right table
    get keywords from the above sentence and return in a continues string

    output:locations

    input: Can you help me find claims data?
    get keywords from the above sentence and return in a continues string

    output:claims

    input: delivery data
    get keywords from the above sentence and return in a continues string

    output:delivery

    input: package level data
    get keywords from the above sentence and return in a continues string

    output:package level
    
    input: Can you provide information on data about upload history of data extract
    get keywords from the above sentence and return in a continues string
    
    output: data extract upload history
    """

chat_prompt_examples = [
    InputOutputTextPair(
        input_text='''I am looking for information regarding packages delivery addresses''',
        output_text='''The table "T2UWPADD1 - PACKAGE ADDRESS - DOMESTIC" contains columns related to package delivery addresses. These columns include the secondary unit and number of an address, building or lot number, department or mail stop information, political divisions within an address, address validation indicator, unvalidated political division name, additional address information, postal code parts, country name, and validated postal code.
      These columns provide relevant information for managing and analyzing package delivery addresses.'''),

    InputOutputTextPair(
        input_text='''I am working on a project that requires information regarding operating locations, can you find me the right table''',
        output_text='''the relevant table for your project that contains information regarding operating locations is the 'TICSLIC - SLIC' table from the 'O082IA - Trailer Forecasting Control System' schema. This table includes columns such as 'SLC_ABR_NA' (Slic Abbreviated Name), 'SLC_NR' (person's name, age, gender, and occupation), 'TFS_SYS_IR' (Trailer Forecasting And Control System Indicator), 'DIS_NR' (District Number), 'INF_LIB_UDT_TS' (Information Library Update Timestamp), 'REG_NR' (Region Number), 'CNY_CD' (Country Code), and 'SLC_TYP_CD' (Slic Type Code). 
      These columns provide relevant information about the operating locations for your project.'''
    ),
    InputOutputTextPair(
        input_text='''Can you provide data about locations where drivers shouldn't deliver to?''',
        output_text='''I do not have infomation regarding this'''
    ),
    InputOutputTextPair(
        input_text='''Where can I find these tables?''',
        output_text='''To find the table provided above, you can visit the following URL: https://infapdedc1.usest2infoverity.com:9086/ldmcatalog/. This website contains the catalog where you can explore and search for the tables mentioned earlier. You may need appropriate access credentials or permissions to log in and access the catalog. Once logged in, you can navigate through the catalog to locate the tables you are interested in.'''
    )
]