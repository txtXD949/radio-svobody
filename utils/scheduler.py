import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from data import db_session
from data.tracks import Track


def update_intop_count():
    """Увеличивает intop_count для треков в топе (один раз в день)"""
    with db_session.create_session() as db_sess:
        week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        top_tracks = db_sess.query(Track).filter(
            Track.created_at >= week_ago
        ).order_by(Track.likes_count.desc()).limit(10).all()

        today = datetime.datetime.now().date()
        for track in top_tracks:
            # Проверяем, обновляли ли сегодня
            if track.last_intop_update != today:
                track.intop_count = (track.intop_count or 0) + 1
                track.last_intop_update = today

        db_sess.commit()


def start_scheduler():
    scheduler = BackgroundScheduler()
    # Запускаем раз в неделю (в воскресенье)
    scheduler.add_job(func=update_intop_count, trigger='cron', day_of_week='sun', hour=0, minute=0)
    scheduler.start()
