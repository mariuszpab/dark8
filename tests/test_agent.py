"""Integration tests for Agent"""

import pytest
import asyncio
from dark8_core.agent import Agent, Task


class TestAgent:
    
    @pytest.mark.asyncio
    async def test_process_command(self):
        agent = Agent()
        
        nlp_result = {
            'intent': 'SEARCH',
            'confidence': 0.9,
            'entities': {},
            'tokens': ['szukaj', 'python']
        }
        
        response = await agent.process_command("szukaj python", nlp_result)
        assert response is not None
        assert isinstance(response, str)
    
    def test_task_creation(self):
        task = Task(
            id="test_1",
            description="Test task",
            intent="SEARCH",
            entities={}
        )
        
        assert task.id == "test_1"
        assert task.status == "pending"
