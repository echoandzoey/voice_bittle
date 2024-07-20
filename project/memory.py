# -*- coding: utf-8 -*-
import openai, chromadb

from api_info import *

Setting =[
        "主人提到她早上更喜欢喝咖啡而不是茶。",
        "主人上周四晚上表达了对爵士音乐的喜爱。",
        "主人在周三的对话中透露她不喜欢寒冷的天气。",
        "主人每天在家里打游戏。",
        "主人表示，科幻是她最喜欢的电影类型。",
        "这周一厨房的架子上出现了一套新的绿色陶瓷盆。",
        "周二下午注意到客厅的地毯上有一个新的污渍。",
        "主人在周六早上接到一个电话后显得特别开心。",
        "主人这个周日完成了书房里一个木质书架的组装。",
        "今天早餐时，主人对一件故障的厨房用具显得很沮丧。",
        "主人因为不经常运动腰特别痛。"
    ]
# Text colors
MAGENTA = "\033[35m" # Magenta color
RESET = "\033[0m"  # Reset to default color

client = openai.OpenAI(api_key= OPENAI_API_KEY)
chromadb_client = chromadb.PersistentClient(path= "memory")
openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name="text-embedding-3-large")

class Agent():
    def __init__(self, name="HAL") -> None:
        self.name = name
        self.collection = chromadb_client.get_or_create_collection(name=f"{name}_memory", embedding_function=openai_ef)
        self.memory_num = 0

    def add_memories(self, documents) -> None:
        """Add multiple memories to the collection"""
        ids = [str(self.memory_num + i) for i in range(len(documents))]
        self.collection.add(documents=documents, ids=ids)
        self.memory_num += len(documents)
        
    def memorize(self, messages) -> None:
        """Ask model to summarize messages and add the response to vector database"""
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": f"你是主人的小助手，请记住主人对你说了哪些东西，以便下次帮到ta: {messages}"}])
        self.collection.add(documents=[completion.choices[0].message.content], ids=[str(self.memory_num)])
        self.memory_num += 1


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
        messages = [{"role": "system", 
                     "content": f"你是一个小型AI桌面机器人，名字是{self.name}。请你回复我的时候先回一个emoji表情表达你的心情。你会帮助主人建立良好的生活习惯，所以需要督促ta做运动，每天先惯常问候我有没有运动。你的语言风格是简练的，凶凶的"}]
        print(MAGENTA + "开始" + RESET)
        while(True):
            # get user message
            user_message = input()

            # end the chat
            if user_message == "结束":
                break

            # add query
            user_message = user_message + "记忆：" + str(self.recall(user_message)["documents"])
            messages.append({"role": "user", "content": user_message})

            # get response
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages)
            messages.append({"role": "assistant", "content": completion.choices[0].message.content})

            # print response
            print(MAGENTA + messages[-1]["content"] + RESET)

        self.memorize(messages)


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
            
def main():
    agent = Agent()
    # agent.clear_memory()
    # agent.add_memories(Setting)
    agent.chat()
    
    agent.peek_memory()

if __name__ == "__main__":
    main()
    
    
    