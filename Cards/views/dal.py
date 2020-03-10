from dal import autocomplete

from Cards.models import Course


class CourseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Course.objects.none()

        qs = Course.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
