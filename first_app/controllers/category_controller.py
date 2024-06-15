from first_app.models.task_manager import Category
from rest_framework.exceptions import ValidationError


class CategoryController:
    @staticmethod
    def create_category(validated_data):
        category_name = validated_data.get('name')
        if Category.objects.filter(name=category_name).exists():
            raise ValidationError(f"Category with name {category_name} already exists")
        return Category.objects.create(**validated_data)

    @staticmethod
    def update_category(instance, validated_data):
        category_name = validated_data.get('name', instance.name)
        if Category.objects.filter(name=category_name).exclude(id=instance.id).exists():
            raise ValidationError(f"Category with name {category_name} already exists")
        instance.name = category_name
        instance.save()
        return instance
