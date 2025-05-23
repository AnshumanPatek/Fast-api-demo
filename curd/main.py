from fastapi import FastAPI, HTTPException, Path, Query, status
from typing import Dict, List, Optional
from models import MsgPayload, MsgResponse

app = FastAPI(
    title="Message CRUD API",
    description="A simple API for managing messages",
    version="1.0.0"
)

# In-memory database
messages_list: Dict[int, MsgPayload] = {}


@app.get("/", response_model=Dict[str, str])
def root() -> Dict[str, str]:
    """Root endpoint returning a welcome message."""
    return {"message": "Hello"}


@app.get("/about", response_model=Dict[str, str])
def about() -> Dict[str, str]:
    """About page route."""
    return {"message": "This is the about page."}


# CREATE - Create a new message
@app.post("/messages/", response_model=MsgResponse, status_code=status.HTTP_201_CREATED)
def create_message(message: MsgPayload) -> Dict[str, MsgPayload]:
    """
    Create a new message
    
    - **msg_name**: Name of the message (required)
    - **content**: Content of the message (optional)
    - **is_active**: Whether the message is active (defaults to True)
    """
    # Generate an ID for the message
    msg_id = max(messages_list.keys()) + 1 if messages_list else 1
    
    # Create new message with the generated ID
    new_message = MsgPayload(
        msg_id=msg_id, 
        msg_name=message.msg_name,
        content=message.content,
        is_active=message.is_active
    )
    messages_list[msg_id] = new_message
    
    return {
        "success": True,
        "data": new_message.model_dump(),
        "message": "Message created successfully"
    }


# READ - Get all messages
@app.get("/messages/", response_model=MsgResponse)
def get_all_messages(active_only: bool = Query(False, description="Filter for active messages only")) -> Dict:
    """
    Get all messages
    
    - **active_only**: Filter to retrieve only active messages (optional)
    """
    if active_only:
        filtered_messages = {k: v for k, v in messages_list.items() if v.is_active}
        return {
            "success": True,
            "data": filtered_messages,
            "message": "Retrieved active messages successfully"
        }
    
    return {
        "success": True,
        "data": messages_list,
        "message": "Retrieved all messages successfully"
    }


# READ - Get a specific message by ID
@app.get("/messages/{msg_id}", response_model=MsgResponse)
def get_message(
    msg_id: int = Path(..., title="Message ID", description="ID of the message to retrieve", gt=0)
) -> Dict:
    """
    Get a specific message by its ID
    
    - **msg_id**: ID of the message to retrieve
    """
    if msg_id not in messages_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with ID {msg_id} not found"
        )
        
    return {
        "success": True,
        "data": messages_list[msg_id],
        "message": f"Message with ID {msg_id} retrieved successfully"
    }


# UPDATE - Update a message
@app.put("/messages/{msg_id}", response_model=MsgResponse)
def update_message(
    message: MsgPayload,
    msg_id: int = Path(..., title="Message ID", description="ID of the message to update", gt=0)
) -> Dict:
    """
    Update a message
    
    - **msg_id**: ID of the message to update
    - **message**: Updated message data
    """
    if msg_id not in messages_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with ID {msg_id} not found"
        )
        
    # Update message with new data while preserving its ID
    updated_message = MsgPayload(
        msg_id=msg_id,
        msg_name=message.msg_name,
        content=message.content,
        is_active=message.is_active
    )
    messages_list[msg_id] = updated_message
    
    return {
        "success": True,
        "data": updated_message,
        "message": f"Message with ID {msg_id} updated successfully"
    }


# DELETE - Delete a message
@app.delete("/messages/{msg_id}", response_model=MsgResponse)
def delete_message(
    msg_id: int = Path(..., title="Message ID", description="ID of the message to delete", gt=0)
) -> Dict:
    """
    Delete a message
    
    - **msg_id**: ID of the message to delete
    """
    if msg_id not in messages_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with ID {msg_id} not found"
        )
        
    deleted_message = messages_list.pop(msg_id)
    
    return {
        "success": True,
        "data": deleted_message,
        "message": f"Message with ID {msg_id} deleted successfully"
    }
