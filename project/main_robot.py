from project.llm_interaction.interact_with_memory import *
from project.llm_interaction.memory_robot import *
def main():
    agent = Agent()
    agent.greet_master()
    # agent.clear_memory()
    # agent.add_memories(robot_memory_templates)
    agent.chat()
    
    agent.peek_memory()

if __name__ == "__main__":
    main()
    
    
    
