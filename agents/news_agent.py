from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k

def get_news_agent():
    return Agent(
        name="News Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGo(), Newspaper4k()],
        instructions=["Provide concise news summaries"],
        show_tool_calls=True,
        add_datetime_to_instructions=True,
        markdown=True,
        verbose=True
    ) 