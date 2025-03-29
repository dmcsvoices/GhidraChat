import asyncio
import os
import shutil

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio


async def run(mcp_server: MCPServer):
    agent = Agent(
        name="GhidraAssistant",
        instructions="Use the tools to analyze source code and assist in malware reverse engineering.",
        mcp_servers=[mcp_server],
    )
    # Ask a question that reads then reasons.
    #message = "Can you tell if the malware sample reaches out to the internet?"
    #print(f"\n\nRunning: {message}")
    #result = await Runner.run(starting_agent=agent, input=message)
    #print(result.final_output)
    # Interactive loop
    while True:
        # Get user input
        user_message = input("\nEnter your question: ")
        
        # Check for exit command
        if user_message.lower() in ['exit', 'quit', 'bye']:
            print("Exiting interactive mode.")
            break
        
        # Skip empty inputs
        if not user_message.strip():
            continue
            
        print(f"Running: {user_message}")
        
        # Run the agent with the user's input
        result = await Runner.run(starting_agent=agent, input=user_message)
        
        # Print the result
        print("\nResult:")
        print(result.final_output)

async def main():
    #current_dir = os.path.dirname(os.path.abspath(__file__))
    #samples_dir = os.path.join(current_dir, "sample_files")

    async with MCPServerStdio(
        name="GhidraMCP",
        params={
            "command": "python",
            "args": ["/home/kali/MCP/GhidraMCP-release-1-0/bridge_mcp_ghidra.py"],
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="MCP Ghidra Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/{trace_id}\n")
            await run(server)


if __name__ == "__main__":
    # Let's make sure the user has npx installed
    if not shutil.which("python"):
        raise RuntimeError("python is not installed.")

    asyncio.run(main())
