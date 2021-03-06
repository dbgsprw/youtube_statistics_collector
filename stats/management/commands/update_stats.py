from django.core.management.base import BaseCommand

from stats.management.commands import _youtube
from stats import helpers
from stats.models import Video, Stats


class Command(BaseCommand):
    help = 'Update video statistics'

    def add_arguments(self, parser):
        parser.add_argument('channel_id', help='youtube channel id')
        parser.add_argument('key', help='Google api key')

    def handle(self, *args, **options):
        self.youtube_api = _youtube.YoutubeAPI(channel_id=options['channel_id'],
                                               key=options['key'])

        for video_id_list in helpers.get_sliced_list(Video.objects.order_by('-published_at').all().iterator()):
            self.save_stat_of_video_list(video_id_list)

    def save_stat_of_video_list(self, video_id_list):
        for video_detail in self.youtube_api.get_videos_by_id_list(video_id_list, part='statistics'):
            self.save_stat(video_detail)

    def save_stat(self, video_detail):
        stats = video_detail['statistics']

        Stats(video_id=helpers.get_video_id(video_detail),
              view_count=stats.get('viewCount', None),
              like_count=stats.get('likeCount', None),
              dislike_count=stats.get('dislikeCount', None),
              favorite_count=stats.get('favoriteCount', None),
              comment_count=stats.get('commentCount', None)).save()
