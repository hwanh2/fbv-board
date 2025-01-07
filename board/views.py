from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Board
from .serializers import BoardSerializer
from drf_yasg.utils import swagger_auto_schema

class IndexView(APIView):
    def get(self, request):
        return Response({'message': 'Index page'}, status=status.HTTP_200_OK)

class BoardListView(APIView):
    @swagger_auto_schema(responses={200: BoardSerializer, 404: 'Board not found'})
    def get(self, request):
        boards = Board.objects.all().order_by('-id')
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BoardReadView(APIView):
    @swagger_auto_schema(responses={200: BoardSerializer, 404: 'Board not found'})
    def get(self, request, id):
        try:
            board = Board.objects.get(pk=id)
            board.incrementReadCount()
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)

class BoardRegistView(APIView):
    @swagger_auto_schema(request_body=BoardSerializer, responses={201: BoardSerializer, 404: 'Board not found'})
    def post(self, request):
        title = request.data.get('title')
        writer = request.data.get('writer')
        content = request.data.get('content')
        if title and writer and content:
            board = Board.objects.create(title=title, writer=writer, content=content)
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class BoardEditView(APIView):
    @swagger_auto_schema(request_body=BoardSerializer, responses={200: BoardSerializer, 404: 'Board not found'})
    def put(self, request, id):
        try:
            board = Board.objects.get(pk=id)
            board.title = request.data.get('title', board.title)
            board.writer = request.data.get('writer', board.writer)
            board.content = request.data.get('content', board.content)
            board.save()
            return Response({'message': 'Board updated successfully'}, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)

class BoardRemoveView(APIView):
    def delete(self, request, id):
        try:
            board = Board.objects.get(pk=id)
            board.delete()
            return Response({'message': 'Board deleted successfully'}, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)
