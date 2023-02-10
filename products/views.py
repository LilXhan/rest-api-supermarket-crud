from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Item
from .serializers import ItemSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_overview(request):
    api_urls = {
        'all_items': '/',
        'Search by Category': '/?category=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_items(request):
    data = ItemSerializer(data=request.data)

    # Validating for already existing data 

    if Item.objects.filter(**request.data).exists():
        raise serializers.ValidationError('The data being posted already exists!')

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_items(request):
    # Checking for the parameters from the URL

    if request.query_params:
        items = Item.objects.filter(**request.query_params.dict())
    else:
        items = Item.objects.all()
    
    if items:
        data = ItemSerializer(items, many=True)
        return Response(data.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_items(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    data = ItemSerializer(instance=item, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_items(request, pk):  
    item = get_object_or_404(Item, pk=pk)

    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
