from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins, permissions, renderers, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import (
    SnippetSerializer,
    SnippetSerializerV1,
    SnippetSerializerV2,
    SnippetSerializerV3,
    SnippetSerializerV4,
    SnippetSerializerV5,
    SnippetSerializerV6,
    SnippetSerializerV7,
    UserSerializer,
    UserSerializerV5,
    UserSerializerV6,
    UserSerializerV7,
)

User = get_user_model()


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "v1/snippets": reverse("v1/snippets-list", request=request),
            "v2/snippets": reverse("v2/snippets-list", request=request, format=format),
            "v3/snippets": reverse("v3/snippets-list", request=request, format=format),
            "v4/snippets": reverse("v4/snippets-list", request=request, format=format),
            "v5/snippets": reverse("v5/snippets-list", request=request, format=format),
            "v5/users": reverse("v5/users-list", request=request, format=format),
            "v6/snippets": reverse("v6/snippets-list", request=request, format=format),
            "v6/users": reverse("v6/users-list", request=request, format=format),
            "v7/snippets": reverse("v7/snippets-list", request=request, format=format),
            "v7/users": reverse("v7/users-list", request=request, format=format),
        }
    )


@csrf_exempt
def snippet_list_vanilla(request):
    """t
    List all code snippets, or create a new snippet.
    """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetSerializerV1(
            snippets, many=True, context={"request": request}
        )
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = SnippetSerializerV1(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET", "POST"])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetSerializerV2(
            snippets, many=True, context={"request": request}
        )
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = SnippetSerializerV2(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetListCBSVanilla(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializerV3(
            snippets, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializerV3(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetListMixinsGenericsVanilla(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializerV4

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializerV5
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


@csrf_exempt
def snippet_detail_vanilla(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = SnippetSerializerV1(snippet, context={"request": request})
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = SnippetSerializerV1(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        snippet.delete()
        return HttpResponse(status=204)


@api_view(["GET", "PUT", "DELETE"])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SnippetSerializerV2(snippet, context={"request": request})
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = SnippetSerializerV2(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetDetailCBSVanilla(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializerV5(snippet, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializerV5(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetDetailMixinsGenericsVanilla(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializerV4

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializerV5
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides
    `list`, `create`, `retrieve`, `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    queryset = Snippet.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetViewSetV6(SnippetViewSet):
    serializer_class = SnippetSerializerV6


class SnippetViewSetV7(SnippetViewSet):
    serializer_class = SnippetSerializerV7


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerV5


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerV5


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()


class UserViewSetV6(UserViewSet):
    serializer_class = UserSerializerV6


class UserViewSetV7(UserViewSet):
    serializer_class = UserSerializerV7
