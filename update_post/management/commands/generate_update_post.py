from django.template.loader import get_template
from django.urls import reverse

from package.templatetags.package_tags import thumb
from settings.base import SITE_URL

try:
    from django.core.management.base import NoArgsCommand
except ImportError:
    from django.core.management import BaseCommand as NoArgsCommand
from package.models import Project


class Command(NoArgsCommand):

    def handle(self, *args, **options):
        last4 = list(Project.objects.all())[-4:]

        items = []
        for project in last4:
            hive_team_members = ", ".join([
                user.display_name
                for user in  project.team_members.hive_users()
            ])
            category_url = "{}{}".format(SITE_URL, reverse("category", kwargs={"slug": project.category.slug}))
            project_image_url = "{}{}".format(SITE_URL, thumb(project.img, 640))

            items.append({
                "project": project,
                "hive_team_members": hive_team_members,
                "category_name": project.category.title_plural,
                "category_url": category_url,
                "project_image_url": project_image_url,
            })

        print(get_template("update_post/update_post.md").render(context={
            "items": items
        }))

