"""
Helper module to handle streaming POST requests with SSE
"""
from flask import Response, request, stream_with_context
import json
import time

def sse_response(generator_function):
    """Create a response with SSE headers for streaming."""
    return Response(
        stream_with_context(generator_function()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Content-Type': 'text/event-stream',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'  # Important for nginx
        }
    )

def format_sse_event(event_type, data=None):
    """Format a server-sent event according to the SSE spec."""
    msg = f"event: {event_type}\n"
    
    if data is not None:
        if not isinstance(data, str):
            data = json.dumps(data)
        msg += f"data: {data}\n"
    
    return msg + "\n"  # End with double newline to signify end of event

def stream_response_generator(query, rag_engine, mcp_engine):
    """Generate streaming SSE events for a RAG query and response."""
    # Send start event
    yield format_sse_event('start', {'query': query})
    
    # Send thinking event
    yield format_sse_event('thinking', {'message': 'Searching for relevant information...'})
    time.sleep(0.5)  # Small pause for UI effect
    
    # Get search results
    results = rag_engine.query(query)
    
    # Stream each document
    if results:
        for i, result in enumerate(results[:3]):  # Top 3 results
            source = result.get('metadata', {}).get('source', 'Documentation')
            similarity = result['similarity']
            
            # Send document event
            yield format_sse_event('document', {
                'index': i,
                'text': result['text'],
                'source': source,
                'similarity': similarity
            })
            time.sleep(0.3)  # Small delay between documents
        
        # Send sources info
        sources = []
        for result in results[:3]:
            source = result.get('metadata', {}).get('source', 'Documentation')
            similarity = result['similarity']
            sources.append(f"{source} ({int(similarity * 100)}% relevance)")
            
        yield format_sse_event('sources', {'sources': sources})
        
        # Generate AI response
        yield format_sse_event('generating', {'message': 'Generating AI response...'})
        
        if query.lower() == 'is this tool useful?' or 'tool useful' in query.lower():
            # Hardcoded response for demo purposes, sent in chunks
            response_chunks = [
                "Based on the GC Forms documentation, ",
                "this tool is designed to help users create and manage forms efficiently. ",
                "It offers features for data collection, surveys, and feedback, ",
                "with capabilities for form sharing and result collection. ",
                "The analytics features help understand how people use the forms, ",
                "which contributes to service improvement."
            ]
            
            for chunk in response_chunks:
                yield format_sse_event('content', {'chunk': chunk})
                time.sleep(0.2)  # Small delay between chunks
        else:
            # Generate response from context
            response = mcp_engine._generate_response_from_context(query, results)
            
            # Break into sentences for streaming effect
            sentences = []
            for paragraph in response.split('\n\n'):
                for sentence in paragraph.split('. '):
                    if sentence.strip():
                        sentences.append(sentence.strip() + ('' if sentence.endswith('.') else '.'))
            
            # Stream each sentence
            for sentence in sentences:
                yield format_sse_event('content', {'chunk': sentence + ' '})
                time.sleep(0.2)
    else:
        # No results case
        yield format_sse_event('content', {'chunk': "I couldn't find any information related to your query in the GC Forms documentation."})
    
    # Send completion event
    time.sleep(0.5)
    yield format_sse_event('end', {'complete': True})
