# -*- coding: utf-8 -*-
import openai, chromadb

from project.api_info import *
from project.llm_interaction.prompt_design_robot import*
from project.llm_interaction.memory_robot import *
from project.utils.json_operation import *
from project.utils.print_format import *
from project.dog_class import*
# from project.main_robot import dog
# Text colors
MAGENTA = "\033[35m" # Magenta color
RESET = "\033[0m"  # Reset to default color
base_url="https://xiaoai.plus/v1" #openai转接口base_url配置 如果没有配置转接口可以注释本行

# client = openai.OpenAI(api_key= OPENAI_API_KEY)
client = openai.OpenAI(api_key= OPENAI_API_KEY, base_url=base_url)  #Note: openai转接口base_url配置 如果没有配置转接口需要注释本行，并打开上一行
chromadb_client = chromadb.PersistentClient(path= "memory")
# openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name="text-embedding-3-large")
openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name="text-embedding-3-large", api_base=base_url) #Note: openai转接口base_url配置 如果没有配置转接口需要注释本行，并打开上一行

def print_log(content):
    # print("[log] " + str(content))
    pass

class Agent():
    def __init__(self, name="HAL",master="zozo") -> None:
        self.name = name
        self.master =master
        self.collection = chromadb_client.get_or_create_collection(name=f"{name}_memory", embedding_function=openai_ef)
        self.memory_num = self.collection.count()
        self.short_memory = []
        # self.robot_memory = [template.format(master=self.master) for template in robot_memory_templates]

    def greet_master(self):
        print(f"Hello, {self.master}!")
        
    def add_memories(self, documents) -> None:
        """Add multiple memories to the collection"""
        documents = list(documents)
        ids = [str(self.memory_num + i) for i in range(len(documents))]
        self.collection.add(documents=documents, ids=ids)
        self.memory_num += len(documents)
        
    def memorize(self) -> None:
        """Ask model to summarize messages and add the response to vector database"""
        # print("before sending memory to llm:"+str(self.short_memory))
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"你是{self.master}的小助手{self.name}，请**简要**总结你们的对话，以便下次帮到ta: {self.short_memory}"}])
        # print(completion)
        # print("\n")
        # print(completion.choices[0].message.content)
        # print(completion.choices[0])
        self.collection.add(documents=[completion.choices[0].message.content], ids=[str(self.memory_num)])
        self.memory_num += 1
        print_log("memory ID: " + str(self.memory_num))


    def recall(self, query) -> dict:
        """Query the vector database"""
        results = self.collection.query(query_texts=[query], n_results=3)
        return results

    def peek_memory(self) -> None:
            """Print all documents in the memory collection"""
            documents = self.collection.get()["documents"]
            print("Current memory contents:")
            for doc in documents:
                print(doc)

    def chat(self) -> None:
        """Start a chat with the agent"""
        print(MAGENTA + "开始" + RESET)
        while(True):
            # get user message
            user_message = input()
            
            # end the chat
            if user_message == "结束":
                break

            # add query
            self.short_memory.append({"role": "user", "content": user_message})
            # print("short_memory: "+str(self.short_memory))

            retrieved_memory = str(self.recall(user_message)["documents"])

            messages = construct_messages_with_mem(self.short_memory, retrieved_memory)
            # get response
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages)
            print_log("assistant: "+str(completion.choices[0].message.content))
            
            # print response
            print(MAGENTA + messages[-1]["content"] + RESET)
            data=completion.choices[0].message.content
            print_log("before json load" + str(data))
            data=json.loads(data)
            # colored_output("💭 想法" + data["thoughts"], "blue")
            colored_output("🤖 " + data['action'], "green")
            colored_output("🤖 " + data['chat'], "pink")
            self.short_memory.append({"role": "assistant", "content": data["chat"]})

        self.memorize()
        
    def llmInteraction(self,user_message) :
        # #构建初始请求列表，系统prompt+userinput
        # print("Currentinput"+str(Currentinput))
        # print("construct_prompts_robot")
        # messages.append({"role": "user", "content": Currentinput})
        # print("messages: "+str(messages))
        # #根据输入查询相关记忆，添加到记忆库
        # user_message=Currentinput
        #输入结束的时候开始总结记忆，否则不会把记忆加进去
        if user_message == "结束":
            self.memorize()
            self.peek_memory()
            return "结束"
        else:
            # add query
            self.short_memory.append({"role": "user", "content": user_message})
            # print("short_memory: "+str(self.short_memory))

            retrieved_memory = str(self.recall(user_message)["documents"])

            messages = construct_messages_with_mem(self.short_memory, retrieved_memory)
            # get response
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages)
            # print("assistant: "+str(completion.choices[0].message.content))
            
            # print response
            print(MAGENTA + messages[-1]["content"] + RESET)
            data=completion.choices[0].message.content
            # print("before json load" + str(data))
            data=json.loads(data)
            # colored_output("💭 想法" + data["thoughts"], "blue")
            colored_output("🤖 " + data['action'], "green")
            colored_output("🤖 " + data['chat'], "pink")
            # self.short_memory.append({"role": "assistant", "content": data["chat"]})
            self.short_memory.append({"role": "assistant", "content": completion.choices[0].message.content})
            # print("check short_mem form " + str(self.short_memory))

            # user_message = user_message + "记忆：" + str(self.recall(user_message)["documents"])
            # print("查询到的相关记忆是"+ user_message)
            # messages.append({"role": "user", "content": user_message})
            # print("messages send to llm: "+str(messages))

            # # get response
            # completion = client.chat.completions.create(
            #     model="gpt-4o-mini",
            #     messages=messages)
            # messages.append({"role": "assistant", "content": completion.choices[0].message.content})

            # # print response
            # print(MAGENTA + messages[-1]["content"] + RESET)
            # data=format_json(messages[-1]["content"])
            # data=json.loads(data)
            # colored_output("💭 想法: " + data["thoughts"], "blue")
            # colored_output("🤖 " + data["action"], "green")
            # colored_output("🤖 " + data["chat"], "pink")
    
        return data["action"]
                       
    

    def forget(self, ids) -> None:
        """Delete a document from the vector database"""
        self.collection.delete(ids=ids)
        
    def clear_memory(self) -> None:
        """Clear the entire memory collection"""
        documents = self.collection.get()
        ids = documents["ids"]
        if ids:
            self.collection.delete(ids=ids)
            print("delete the memory")
        else:
            print("NO documents to delete")
            

    
    