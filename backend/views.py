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
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "openrouter/free", # Automatically route to available free models
                        "messages": api_messages,
                        "temperature": 0.7,
                        "max_tokens": 2000,
                    },
                    timeout=30
                )
                
                if response.status_code == 429:
                    return JsonResponse({
                        'error': 'The AI service is currently busy (rate limit reached). Please try again in a few moments.',
                        'details': 'Upstream 429: Rate limit exceeded on OpenRouter free tier.'
                    }, status=429)
                    
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"API Request Error: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"API Error Details: {e.response.text}")
                    return JsonResponse({
                        'error': f'API Error: {e.response.status_code}',
                        'details': e.response.text
                    }, status=500)
                return JsonResponse({'error': f'Request failed: {str(e)}'}, status=500)

            ai_response = response.json()
            if 'choices' not in ai_response or not ai_response['choices']:
                print(f"Unexpected API Response: {ai_response}")
                return JsonResponse({
                    'error': 'Invalid API response format',
                    'details': str(ai_response)
                }, status=500)

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
                
        except Exception as e:
            import traceback
            print(f"General Error in send_message: {str(e)}")
            traceback.print_exc()
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