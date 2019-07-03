import os

from django.core.management.base import CommandError, BaseCommand
from django.apps import apps
from django.core.files.storage import default_storage

from ._utils import file_patt, file_patt_prefixed


# py2/3-agnostic input
# fixed out of Command method, because "input" is global
input = getattr(__builtins__, 'raw_input', input)


class Command(BaseCommand):
    can_import_settings = True

    def _handle_fixture(self, root, fixture, media_root):
        """ Copy media files to MEDIA_ROOT. """

        file_paths = []
        for line in open(fixture).readlines():
            file_paths.extend(self.pattern.findall(line))
        if file_paths:
            for fp in file_paths:
                fixture_path = os.path.join(root, 'media', fp)
                if not os.path.exists(fixture_path):
                    msg = ('File path ({}) found in fixture '
                           'but not on disk in ({}) \n')
                    self.stderr.write(msg.format(fp, fixture_path))
                    continue
                final_dest = os.path.join(media_root, fp)
                dest_dir = os.path.dirname(final_dest)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                msg = 'Copied {} to {}\n'
                self.stdout.write(msg.format(fp, final_dest))
                with open(fixture_path, 'rb') as f:
                    default_storage.save(fp, f)

    def _autodiscover_fixtures(self, fixture_dirs):
        """ Autodiscover fixtures """

        app_module_paths = [app.path for app in apps.get_app_configs()]
        pathl = lambda path: os.path.join(path, 'fixtures')

        app_fixtures = [pathl(path) for path in app_module_paths]
        app_fixtures += list(fixture_dirs) + ['']

        fixtures = []
        for fixture_path in app_fixtures:
            for root, _, files in os.walk(fixture_path):
                for file in files:
                    if file.rsplit('.', 1)[-1] in ('json', 'yaml'):
                        fixtures.append((root, os.path.join(root, file)))
        return fixtures

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help='Do NOT prompt the user for input of any kind.'
        )

    def handle(self, **options):
        """ Handle command invocation """

        from django.conf import settings

        fixtures = self._autodiscover_fixtures(settings.FIXTURE_DIRS)

        if options['interactive']:
            confirm = input('This will overwrite any '
                            'existing files. Proceed? ')
            if not confirm.lower().startswith('y'):
                raise CommandError('Media syncing aborted')

        if getattr(settings, 'FIXTURE_MEDIA_REQUIRE_PREFIX', False):
            self.pattern = file_patt_prefixed
        else:
            self.pattern = file_patt

        for root, fixture in fixtures:
            self._handle_fixture(root, fixture, settings.MEDIA_ROOT)
