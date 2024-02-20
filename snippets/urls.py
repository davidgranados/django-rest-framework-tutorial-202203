from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework import renderers
from snippets import views

# API endpoints
snippet_list_viewset = views.SnippetViewSetV6.as_view({"get": "list", "post": "create"})
snippet_detail_viewset = views.SnippetViewSetV6.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
snippet_highlight_viewset = views.SnippetViewSetV6.as_view(
    {"get": "highlight"}, renderer_classes=[renderers.StaticHTMLRenderer]
)
user_list_viewset = views.UserViewSetV6.as_view({"get": "list"})
user_detail_viewset = views.UserViewSetV6.as_view({"get": "retrieve"})

# Create a router and register our viewsets with it.
class CustomRouter(DefaultRouter):
    include_root_view = False


viewset_router = CustomRouter()
viewset_router.register(r"snippets", views.SnippetViewSetV7, basename="v7/snippets")
viewset_router.register(r"users", views.UserViewSetV7, basename="v7/users")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", views.api_root),
    path(
        "v1/snippets/<int:pk>/highlight/",
        views.SnippetHighlight.as_view(),
        name="v1/snippet-highlight",
    ),
    # vanilla
    path(
        "v1/snippets/<int:pk>/", views.snippet_detail_vanilla, name="v1/snippets-detail"
    ),
    path("v1/snippets/", views.snippet_list_vanilla, name="v1/snippets-list"),
    path(
        "v2/snippets/<int:pk>/highlight/",
        views.SnippetHighlight.as_view(),
        name="v2/snippet-highlight",
    ),
    # function based api view
    path("v2/snippets/<int:pk>/", views.snippet_detail, name="v2/snippets-detail"),
    path("v2/snippets/", views.snippet_list, name="v2/snippets-list"),
    path(
        "v3/snippets/<int:pk>/highlight/",
        views.SnippetHighlight.as_view(),
        name="v3/snippet-highlight",
    ),
    # class based api view
    path(
        "v3/snippets/<int:pk>/",
        views.SnippetDetailCBSVanilla.as_view(),
        name="v3/snippets-detail",
    ),
    path(
        "v3/snippets/", views.SnippetListCBSVanilla.as_view(), name="v3/snippets-list"
    ),
    path(
        "v4/snippets/<int:pk>/highlight/",
        views.SnippetHighlight.as_view(),
        name="v4/snippet-highlight",
    ),
    # class based api view with mixins
    path(
        "v4/snippets/<int:pk>/",
        views.SnippetDetailMixinsGenericsVanilla.as_view(),
        name="v4/snippets-detail",
    ),
    path(
        "v4/snippets/",
        views.SnippetListMixinsGenericsVanilla.as_view(),
        name="v4/snippets-list",
    ),
    path("v5/users/<int:pk>/", views.UserDetail.as_view(), name="v5/users-detail"),
    path("v5/users/", views.UserList.as_view(), name="v5/users-list"),
    path(
        "v5/snippets/<int:pk>/highlight/",
        views.SnippetHighlight.as_view(),
        name="v5/snippet-highlight",
    ),
    # class based api view with generics
    path(
        "v5/snippets/<int:pk>/",
        views.SnippetDetail.as_view(),
        name="v5/snippets-detail",
    ),
    path("v5/snippets/", views.SnippetList.as_view(), name="v5/snippets-list"),
    path("v6/users/<int:pk>/", user_detail_viewset, name="v6/users-detail"),
    path("v6/users/", user_list_viewset, name="v6/users-list"),
    path(
        "v6/snippets/<int:pk>/highlight/",
        snippet_highlight_viewset,
        name="v6/snippets-highlight",
    ),
    # viewset without router
    path("v6/snippets/<int:pk>/", snippet_detail_viewset, name="v6/snippets-detail"),
    path("v6/snippets/", snippet_list_viewset, name="v6/snippets-list"),
]

urlpatterns = format_suffix_patterns(urlpatterns) + [
    path("v7/", include(viewset_router.urls))
]
