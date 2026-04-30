import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from data import db_session
from data.tracks import Track


def update_intop_count():
    with db_session.create_session() as db_sess:
        # Берём топ-10 по лайкам за последние 7 дней
        week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        top_tracks = db_sess.query(Track).filter(
            Track.created_at >= week_ago
        ).order_by(Track.likes_count.desc()).limit(10).all()

        # Увеличиваем счётчик для каждого трека в топе
        for track in top_tracks:
            track.intop_count = (track.intop_count or 0) + 1

        db_sess.commit()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_intop_count, trigger='interval', hours=1)
    scheduler.start()
