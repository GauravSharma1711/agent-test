const API_BASE = '/api';
let currentConversationId = null;

const conversationsList = document.getElementById('conversations-list');
const memoriesList = document.getElementById('memories-list');
const chatMessages = document.getElementById('chat-messages');
const chatTitle = document.getElementById('chat-title');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const newChatBtn = document.getElementById('new-chat-btn');
const deleteChatBtn = document.getElementById('delete-chat-btn');

async function fetchConversations() {
    try {
        const response = await fetch(`${API_BASE}/conversations`);
        const conversations = await response.json();
        renderConversations(conversations);
    } catch (error) {
        console.error('Error fetching conversations:', error);
    }
}

async function fetchMemories() {
    try {
        const response = await fetch(`${API_BASE}/memories`);
        const memories = await response.json();
        renderMemories(memories);
    } catch (error) {
        console.error('Error fetching memories:', error);
    }
}

function renderConversations(conversations) {
    conversationsList.innerHTML = '';
    
    if (conversations.length === 0) {
        conversationsList.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-muted);font-size:13px;">No conversations yet</div>';
        return;
    }
    
    conversations.forEach(conv => {
        const item = document.createElement('div');
        item.className = `conversation-item ${conv.id === currentConversationId ? 'active' : ''}`;
        const title = conv.title || `Chat ${conv.id.toString().slice(0, 8)}`;
        item.textContent = title;
        item.addEventListener('click', () => loadConversation(conv.id));
        conversationsList.appendChild(item);
    });
}

function renderMemories(memories) {
    memoriesList.innerHTML = '';
    
    if (memories.length === 0) {
        memoriesList.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-muted);font-size:13px;">No memories yet</div>';
        return;
    }
    
    memories.forEach(memory => {
        const item = document.createElement('div');
        item.className = 'memory-item';
        item.innerHTML = `
            <div class="memory-type">${memory.memory_type}</div>
            <div class="memory-key">${memory.key}</div>
            <div class="memory-value">${memory.value}</div>
        `;
        memoriesList.appendChild(item);
    });
}

async function loadConversation(conversationId) {
    currentConversationId = conversationId;
    deleteChatBtn.style.display = 'block';
    
    try {
        const response = await fetch(`${API_BASE}/conversations/${conversationId}`);
        const conversation = await response.json();
        
        chatTitle.textContent = conversation.title || `Chat ${conversationId.toString().slice(0, 8)}`;
        
        chatMessages.innerHTML = '';
        conversation.messages.forEach(msg => {
            appendMessage(msg.role, msg.content);
        });
        
        fetchConversations();
        fetchMemories();
        scrollToBottom();
    } catch (error) {
        console.error('Error loading conversation:', error);
    }
}

function appendMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.textContent = content;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = '<span></span><span></span><span></span>';
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

function hideTypingIndicator() {
    const typingDiv = document.getElementById('typing-indicator');
    if (typingDiv) {
        typingDiv.remove();
    }
}

function showWelcome() {
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">🤖</div>
            <h2>Welcome to AI Agent</h2>
            <p>Start a new conversation to chat with your AI assistant. I can remember information about you and help with various tasks!</p>
        </div>
    `;
    chatTitle.textContent = 'AI Agent';
    deleteChatBtn.style.display = 'none';
}

async function createConversation() {
    try {
        const response = await fetch(`${API_BASE}/conversations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        const conversation = await response.json();
        currentConversationId = conversation.id;
        deleteChatBtn.style.display = 'block';
        chatMessages.innerHTML = '';
        chatTitle.textContent = 'New Chat';
        
        appendMessage('assistant', "Hello! I'm your AI assistant. How can I help you today? Feel free to tell me about yourself - I'll remember important things!");
        
        fetchConversations();
        fetchMemories();
    } catch (error) {
        console.error('Error creating conversation:', error);
    }
}

async function sendMessage() {
    const content = messageInput.value.trim();
    if (!content || !currentConversationId) return;
    
    appendMessage('user', content);
    messageInput.value = '';
    sendBtn.disabled = true;
    messageInput.disabled = true;
    
    showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE}/conversations/${currentConversationId}/messages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content })
        });
        
        hideTypingIndicator();
        
        const aiMessage = await response.json();
        appendMessage('assistant', aiMessage.content);
        
        fetchMemories();
        fetchConversations();
    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        appendMessage('assistant', 'Sorry, there was an error processing your message. Please make sure your API key is configured correctly.');
    } finally {
        sendBtn.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

async function deleteConversation() {
    if (!currentConversationId) return;
    
    if (!confirm('Are you sure you want to delete this conversation?')) return;
    
    try {
        await fetch(`${API_BASE}/conversations/${currentConversationId}`, {
            method: 'DELETE'
        });
        
        currentConversationId = null;
        showWelcome();
        fetchConversations();
        fetchMemories();
    } catch (error) {
        console.error('Error deleting conversation:', error);
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

newChatBtn.addEventListener('click', createConversation);
deleteChatBtn.addEventListener('click', deleteConversation);
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

fetchConversations();
fetchMemories();
showWelcome();
