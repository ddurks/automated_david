from __future__ import unicode_literals
import youtube_dl

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://v.redd.it/wjybzuj3yy441/DASH_480?source=fallback'])