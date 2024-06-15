from rest_framework import serializers
from first_app.models.task_manager import Category
from first_app.controllers.category_controller import CategoryController


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if self.instance:
            if Category.objects.filter(name=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(f"Category with name {value} already exists")
        else:
            if Category.objects.filter(name=value).exists():
                raise serializers.ValidationError(f"Category with name {value} already exists")
        return value

    def create(self, validated_data):
        return CategoryController.create_category(validated_data)

    def update(self, instance, validated_data):
        return CategoryController.update_category(instance, validated_data)
