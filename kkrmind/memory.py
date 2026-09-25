"""
KKR Mind Memory - Conversation history management
"""

from typing import List, Dict, Optional
from collections import deque


class Memory:
    """
    Conversation memory management
    
    Features:
        - Automatic conversation history
        - Configurable max history
        - Easy clear and export
        - Multi-turn conversations
    
    Example:
        >>> memory = Memory(max_history=50)
        >>> memory.add_message("user", "Hello!")
        >>> memory.add_message("assistant", "Hi there!")
        >>> messages = memory.get_messages()
    """
    
    def __init__(self, max_history: int = 50):
        """
        Initialize memory
        
        Args:
            max_history: Maximum messages to keep (default: 50)
        """
        self.max_history = max_history
        self._messages = deque(maxlen=max_history)
    
    def add_message(self, role: str, content: str):
        """
        Add message to history
        
        Args:
            role: Message role (user/assistant/system)
            content: Message content
        """
        if role not in ["user", "assistant", "system"]:
            raise ValueError(f"Invalid role: {role}")
        
        self._messages.append({
            "role": role,
            "content": content,
        })
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        Get all messages in history
        
        Returns:
            List of message dictionaries
        """
        return list(self._messages)
    
    def get_last_message(self) -> Optional[Dict[str, str]]:
        """
        Get last message in history
        
        Returns:
            Last message or None if empty
        """
        if self._messages:
            return self._messages[-1]
        return None
    
    def clear(self):
        """Clear all messages"""
        self._messages.clear()
    
    def __len__(self) -> int:
        """Get number of messages"""
        return len(self._messages)
    
    def __repr__(self) -> str:
        return f"Memory({len(self._messages)}/{self.max_history} messages)"
    
    def export(self) -> str:
        """
        Export conversation as formatted text
        
        Returns:
            Formatted conversation string
        """
        lines = []
        for msg in self._messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            lines.append(f"{role}: {content}")
        
        return "\n\n".join(lines)
    
    def import_messages(self, messages: List[Dict[str, str]]):
        """
        Import messages from list
        
        Args:
            messages: List of message dictionaries
        """
        self.clear()
        for msg in messages:
            if "role" in msg and "content" in msg:
                self.add_message(msg["role"], msg["content"])
