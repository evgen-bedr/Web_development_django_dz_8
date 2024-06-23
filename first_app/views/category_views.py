from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from ..models import Category
from first_app.serializers.category_serializer import CategoryCreateSerializer, CategorySerializer
from django.shortcuts import get_object_or_404


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 2
        categories = Category.objects.all().order_by('id')

        result_page = paginator.paginate_queryset(categories, request)

        data = [
            {
                'category_id': category.id,
                'category_name': category.name,
                'task_count': category.tasks.count()
            }
            for category in result_page
        ]

        return paginator.get_paginated_response(data)


class CategoryCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryUpdateView(APIView):
    def put(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategoryCreateSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
