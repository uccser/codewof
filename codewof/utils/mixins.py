"""Mixins used by Django system."""

from django.shortcuts import redirect


class RedirectToCosmeticURLMixin(object):
    """Mixin for a view that redirects to readable URL.

    The view identifies the object by the primary key but ensures
    URL shows readable version (for example slug of title) for SEO
    and readability.
    """

    def get(self, request, **kwargs):
        """Render view to readable URL.

        Examples using /<pk>/<slug>/ url:
            - /1/correct-slug/ with 200 response.
            - /1/ with 302 response to /1/correct-slug/
            - /1/invalid-slug/ with 302 response to /1/correct-slug/
            - /a/ with 404 response.

        If required, checks could be implemented to ensure this
        mixin is only used:
            - With single model view.
            - Object is retrieved by primary key only.

        Returns:
            - 200 response if request path matches object's get_absolute_url.
            - 302 response if pk is correct by URL is incorrect to 200 page.
            - 404 response if object pk is not found.
        """
        self.object = self.get_object()
        if self.request.path != self.object.get_absolute_url():
            return redirect(self.object)
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
