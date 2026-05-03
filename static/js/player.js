class RadioPlayer {
    constructor() {
        this.audio = new Audio();       // HTML5 Audio
        this.currentTrack = null;       // текущий трек
        this.playlist = [];             // массив треков для плейлиста
        this.currentIndex = 0;          // индекс текущего трека в плейлисте
        this.isPlaying = false;         // флаг воспроизведения

        this.initElements();            // поиск DOM-элементов
        this.initEventListeners();      // назначения обработчиков
    }

    initElements() {
        this.playBtn = document.querySelector('.play-pause');               // кнопка play/pause
        this.prevBtn = document.querySelector('.prev');                     // предыдущий трек
        this.nextBtn = document.querySelector('.next');                     // следующий трек
        this.trackNameEl = document.querySelector('.player-track-name');    // название трека
        this.trackImageEl = document.querySelector('.player-image');        // обложка
    }

    initEventListeners() {
        this.playBtn.addEventListener('click', () => this.togglePlay());    // при клике на play/pause → вызываем togglePlay
        this.prevBtn.addEventListener('click', () => this.prev());          // при клике на "предыдущий" → вызываем prev
        this.nextBtn.addEventListener('click', () => this.next());          // при клике на "следующий" → вызываем next
        this.audio.addEventListener('ended', () => this.next());            // автопереключение
    }

    loadTrack(track) {
        if (!track) return;                                     // если трека нет — ничего не делаем

        this.currentTrack = track;                              // сохраняем текущий трек
        this.audio.src = `/api/tracks/${track.id}/stream`;      // потоковое аудио
        this.trackNameEl.textContent = track.title;             // обновляем название на экране

        this.updatePlayIcons(track.id);                         // синхронизация иконок

        if (this.isPlaying) {                                   // если плеер был в состоянии воспроизведения — продолжаем играть
            this.audio.play();
        }
    }

    togglePlay() {
        if (!this.currentTrack) return;             // если нет трека

        if (this.isPlaying) {                       // если играет → ставим на паузу
            this.audio.pause();
            this.playBtn.textContent = '▶';         // меняем иконку на "play"
        } else {
            this.audio.play();                      // если на паузе → запускаем
            this.playBtn.textContent = '⏸';         // меняем иконку на "pause"
        }
        this.isPlaying = !this.isPlaying;           // переключаем флаг

        // обновляем иконки
        this.updatePlayIcons(this.currentTrack.id);
    }

    prev() {  // предыдущий трек
        console.log('prev вызван, playlist.length:', this.playlist.length);

        if (!this.playlist.length) return;  // если нет плейлиста

        // Если прошло больше 5 секунд — перемотка в начало текущего трека
        if (this.audio.currentTime > 5) {
            this.audio.currentTime = 0;
            return;
        }

        // Иначе предыдущий трек
        this.currentIndex = (this.currentIndex - 1 + this.playlist.length) % this.playlist.length;
        this.loadTrack(this.playlist[this.currentIndex]);  // загружаем предыдущий трек
        if (!this.isPlaying) this.play();  // если был на паузе — запускаем
    }

    next() {  // следующий трек
        console.log('next вызван, playlist.length:', this.playlist.length);

        if (!this.playlist.length) return;  // если нет трека

        // переключаемся на следующий трек
        this.currentIndex = (this.currentIndex + 1) % this.playlist.length;
        this.loadTrack(this.playlist[this.currentIndex]);
        if (!this.isPlaying) this.play();
    }

    play() {  // запуск воспроизведения
        this.audio.play();
        this.isPlaying = true;
        this.playBtn.textContent = '⏸';

        if (this.currentTrack) {
            this.updatePlayIcons(this.currentTrack.id);
        }
    }

    stop() {  // остановка воспроизведения
        this.isPlaying = false;
        this.playBtn.textContent = '▶';
        this.updatePlayIcons(null);  // null — убираем подсветку всех треугольников
    }

    setPlaylist(tracks, startIndex = 0) {  // устанавливает плейлист (последовательное воспроизведение)
        console.log('setPlaylist вызван, треков:', tracks.length);
        this.playlist = tracks;                     // сохраняем массив треков
        this.currentIndex = startIndex;             // с какого трека начать
        if (tracks.length) {
            this.loadTrack(tracks[startIndex]);     // загружаем первый/выбранный трек
        }
    }

    playSingleTrack(track) {  // воспроизводит один трек (без плейлиста)
        this.currentTrack = track;
        this.audio.src = `/api/tracks/${track.id}/stream`;
        this.trackNameEl.textContent = track.title;
        this.play();                        // запускаем
        this.updatePlayIcons(track.id);     // синхронизируем иконки
    }

    updatePlayIcons(activeTrackId) {  // синхронизация треугольничков в плашке трека
        // находим все кнопки с классом .track-play
        document.querySelectorAll('.track-play').forEach(btn => {
            const trackId = btn.getAttribute('data-id');            // id трека для этой кнопки
            const triangle = btn.querySelector('.play-triangle');   // сам треугольник

            if (!triangle) return;

            // если передан activeTrackId, он совпадает с trackId и музыка играет — скрываем треугольник
            if (activeTrackId && trackId == activeTrackId && this.isPlaying) {
                triangle.style.opacity = '0';   // невидимый треугольник
            } else {
                triangle.style.opacity = '1';   // видимый треугольник
            }
        });
    }
}

const player = new RadioPlayer();  // глобальный экземпляр плеера
