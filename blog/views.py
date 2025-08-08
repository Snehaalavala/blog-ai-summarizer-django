from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from openai import OpenAI
import os
from dotenv import load_dotenv
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

load_dotenv()
# template
# openai = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
# )
openai = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['get', 'post'])
    def summarize(self, request, pk=None):
        post = self.get_object()
        try:
            response = openai.chat.completions.create(
                model="llama3",
                messages=[
                    {"role": "user", "content": f"Summarize this blog content: {post.content}"}
                ]
            )
            summary = response.choices[0].message.content
            return Response({"summary": summary}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
