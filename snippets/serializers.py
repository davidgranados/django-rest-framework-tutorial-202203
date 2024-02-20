from django.contrib.auth import get_user_model
from rest_framework import serializers

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

User = get_user_model()


class SimpleSnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={"base_template": "textarea.html"})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default="python")
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default="friendly")

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.code = validated_data.get("code", instance.code)
        instance.linenos = validated_data.get("linenos", instance.linenos)
        instance.language = validated_data.get("language", instance.language)
        instance.style = validated_data.get("style", instance.style)
        instance.save()
        return instance


class SnippetModelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "linenos", "language", "style", "owner"]


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Snippet
        fields = [
            "url",
            "id",
            "highlight",
            "owner",
            "title",
            "code",
            "linenos",
            "language",
            "style",
        ]


class SnippetSerializerV1(SnippetSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="v1/snippets-detail")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="v1/snippet-highlight", format="html"
    )


class SnippetSerializerV2(SnippetSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="v2/snippets-detail")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="v2/snippet-highlight", format="html"
    )


class SnippetSerializerV3(SnippetSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="v3/snippets-detail")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="v3/snippet-highlight", format="html"
    )


class SnippetSerializerV4(SnippetSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="v4/snippets-detail")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="v4/snippet-highlight", format="html"
    )


class SnippetSerializerV5(SnippetSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="v5/snippets-detail")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="v5/snippet-highlight", format="html"
    )


class SnippetSerializerV6(SnippetSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="v6/snippets-detail")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="v6/snippets-highlight", format="html"
    )


class SnippetSerializerV7(SnippetSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="v7/snippets-detail")
    highlight = serializers.HyperlinkedIdentityField(
        view_name="v7/snippets-highlight", format="html"
    )


class UserModelSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "snippets"]


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ["url", "id", "username", "snippets"]


class UserSerializerV5(UserSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="v5/users-detail")
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name="v5/snippets-detail", read_only=True
    )


class UserSerializerV6(UserSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="v6/users-detail")
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name="v6/snippets-detail", read_only=True
    )


class UserSerializerV7(UserSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="v7/users-detail")
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name="v7/snippets-detail", read_only=True
    )
