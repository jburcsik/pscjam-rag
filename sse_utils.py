"""
Utility functions for Server-Sent Events (SSE) in Flask.
"""
import json
from flask import Response
import time

def format_sse_event(event_type, data=None):
    """
    Format a server-sent event.
    
    Args:
        event_type (str): The type of event
        data: The data to send (will be JSON-encoded if not a string)
        
    Returns:
        str: Properly formatted SSE event
    """
    msg = f"event: {event_type}\n"
    
    if data is not None:
        if not isinstance(data, str):
            data = json.dumps(data)
        msg += f"data: {data}\n"
    
    return msg + "\n"  # End with double newline to signify end of event

def create_sse_response(generator_func):
    """
    Create a Flask Response object for SSE using a generator function.
    
    Args:
        generator_func: A function that yields SSE events
        
    Returns:
        Response: A Flask Response configured for SSE
    """
    return Response(
        generator_func(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'  # Important for nginx
        }
    )
