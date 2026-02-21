import uuid
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage

from app.database import get_db
from app.models.models import Conversation, Message, Memory
from app.agent.agent import Agent

router = APIRouter(prefix="/api", tags=["api"])


class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    created_at: datetime
    
    model_config = {"from_attributes": True}


class ConversationCreate(BaseModel):
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    id: uuid.UUID
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class ConversationDetail(ConversationResponse):
    messages: List[MessageResponse]


@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db)
):
    conversation = Conversation(title=data.title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


@router.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    return db.query(Conversation).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conversation)
    db.commit()
    return {"status": "deleted"}


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
def send_message(
    conversation_id: str,
    data: MessageCreate,
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=data.content
    )
    db.add(user_message)
    db.commit()
    
    previous_messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()
    
    langchain_messages = [
        HumanMessage(content=m.content) if m.role == "user" else AIMessage(content=m.content)
        for m in previous_messages
    ]
    
    agent = Agent(db, conversation_id)
    result = agent.invoke(langchain_messages)
    
    ai_message_content = result["messages"][-1].content
    
    ai_message = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=ai_message_content
    )
    db.add(ai_message)
    
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(ai_message)
    
    return ai_message


@router.get("/memories", response_model=List[dict])
def list_memories(
    memory_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Memory).filter(Memory.is_active == True)
    if memory_type:
        query = query.filter(Memory.memory_type == memory_type)
    return [
        {
            "id": str(m.id),
            "memory_type": m.memory_type,
            "key": m.key,
            "value": m.value,
            "created_at": m.created_at
        }
        for m in query.order_by(Memory.created_at.desc()).all()
    ]
