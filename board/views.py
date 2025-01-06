from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Board
from .serializers import BoardSerializer
from drf_yasg.utils import swagger_auto_schema


@api_view(['GET'])
def index(request):
    return Response({'message': 'Index page'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def list(request):
    boards = Board.objects.all().order_by('-id')
    board_list = [
        {'id': board.id, 'title': board.title, 'writer': board.writer, 'readcount': board.readcount}
        for board in boards
    ]
    return Response(board_list, status=status.HTTP_200_OK)

@swagger_auto_schema(methods=['get'], responses={200: BoardSerializer, 404: 'Board not found'})
@api_view(['GET'])
def read(request, id):
    try:
        board = Board.objects.get(pk=id)
        board.incrementReadCount()
        # 기존에 사용한 BoardDetailSerializer 대신 BoardSerializer를 사용
        serializer = BoardSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Board.DoesNotExist:
        return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def regist(request):
    title = request.data.get('title')
    writer = request.data.get('writer')
    content = request.data.get('content')
    if title and writer and content:
        board = Board.objects.create(title=title, writer=writer, content=content)
        return Response({'id': board.id, 'message': 'Board created successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit(request, id):
    try:
        board = Board.objects.get(pk=id)
        board.title = request.data.get('title', board.title)
        board.writer = request.data.get('writer', board.writer)
        board.content = request.data.get('content', board.content)
        board.save()
        return Response({'message': 'Board updated successfully'}, status=status.HTTP_200_OK)
    except Board.DoesNotExist:
        return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def remove(request, id):
    try:
        board = Board.objects.get(pk=id)
        board.delete()
        return Response({'message': 'Board deleted successfully'}, status=status.HTTP_200_OK)
    except Board.DoesNotExist:
        return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)
