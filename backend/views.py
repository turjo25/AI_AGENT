import uuid
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import ChatMessage
import json
import requests
from django.conf import settings

# Create your views here.


def chat_view(request):

    session_id = request.session.get('chat_session_id')

    if not session_id:

        session_id = str(uuid.uuid4())
        request.session['chat_session_id'] = session_id
    messages = ChatMessage.objects.filter(session_id=session_id)

    context = {
        'chat_messages': messages,
        'session_id': session_id,
    }
    return render(request, 'chat.html', context)

@csrf_exempt

def send_message(request):

    if request.method == 'POST':

        try:
            data= json.loads(request.body)
            user_message = data.get('message').strip()
            session_id = data.get('session_id', str(uuid.uuid4()))

            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)
            
            if len(user_message) > 5000:
                user_message = user_message[:5000]

            #Save user message
            ChatMessage.objects.create(
                session_id=session_id,
                role='user',
                message=user_message
            )

            # Get Conversation History
            history = ChatMessage.objects.filter(session_id=session_id).order_by('timestamp')

            # Build messages for API
            api_messages = [
                {
                    "role": "system",
                    "content": """You are a helpful and friendly ecommerce customer service assistant. 
                    You help customers with:
                    - Product inquiries and recommendations
                    - Order tracking and status updates
                    - Returns and refunds
                    - Shipping information
                    - Payment issues
                    - General product questions
                    
                    Be professional, courteous, and helpful. Provide clear and concise answers.
                    If you don't have specific information, offer to connect them with a human agent."""
                }
            ]

            # Add conversation history
            for msg in history:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.message
                })
            # Call OpenRouter API
             # Call OpenRouter API
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "google/gemma-4-26b-a4b-it:free",  # Free open source model
                    "messages": api_messages,
                    "temperature": 0.7,
                    "max_tokens": 2000,  # Increased for better responses
                }
            )

            if response.status_code == 200:
                ai_response = response.json()
                assistant_message = ai_response['choices'][0]['message']['content']

                 # Limit assistant message to 5000 characters
                if len(assistant_message) > 5000:
                    assistant_message = assistant_message[:5000] + "..."
                # Save assistant message

                ChatMessage.objects.create(
                session_id=session_id,
                role='assistant',
                message=assistant_message
                )

                return JsonResponse({
                    'success': True,
                    'message': assistant_message,
                    'session_id': session_id
                })
            else:
                return JsonResponse({
                    'error': f'API Error: {response.status_code}',
                    'details': response.text
                }, status=500)
                
                
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def clear_chat(request):
    """Clear chat history for a session"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            
            if session_id:
                ChatMessage.objects.filter(session_id=session_id).delete()
                return JsonResponse({'success': True})
            
            return JsonResponse({'error': 'No session ID provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405) 