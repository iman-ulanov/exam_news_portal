from django.shortcuts import render
from rest_framework import serializers

from .models import News, Comment, Status, CommentStatus, NewsStatus


class NewsSerializer(serializers.ModelSerializer):
    statuses = serializers.ReadOnlyField(source='get_status')

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['created', 'updated', 'author']


class CommentSerializer(serializers.ModelSerializer):
    statuses = serializers.ReadOnlyField(source='get_status')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['created', 'updated', 'author', 'news']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class NewsStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsStatus
        fields = '__all__'



        # def create(self, validated_data):
        #     try:
        #         NewsStatus.objects.create(
        #             status=validated_data['status'],
        #             author=validated_data['author'],
        #             news=validated_data['news']
        #         )
        #     except Exception as e:
        #         status = NewsStatus.objects.get('status')
        #         if status:
        #             raise serializers.ValidationError(f'You already added status {e}')
        #         else:
        #             return 'Status added'



class CommentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentStatus
        fields = '__all__'
