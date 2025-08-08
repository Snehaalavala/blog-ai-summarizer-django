from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
import openai
import os
from dotenv import load_dotenv
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def summarize(self, request, pk=None):
        post = self.get_object()
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"Summarize this blog content: {post.content}"}
                ]
            )
            summary = response['choices'][0]['message']['content']
            return Response({"summary": summary}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
