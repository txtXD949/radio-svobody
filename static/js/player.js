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
        this.playBtn.addEventListener('click', () => this.togglePlay());
        this.prevBtn.addEventListener('click', () => this.prev());
        this.nextBtn.addEventListener('click', () => this.next());
        this.audio.addEventListener('ended', () => this.next());            // автопереключение
    }

    loadTrack(track) {
        if (!track) return;

        this.currentTrack = track;
        this.audio.src = `/api/tracks/${track.id}/stream`;      // потоковое аудио
        this.trackNameEl.textContent = track.title;

        this.updatePlayIcons(track.id);                         // синхронизация иконок

        if (this.isPlaying) {
            this.audio.play();
        }
    }

    togglePlay() {
        if (!this.currentTrack) return;

        if (this.isPlaying) {
            this.audio.pause();
            this.playBtn.textContent = '▶';
        } else {
            this.audio.play();
            this.playBtn.textContent = '⏸';
        }
        this.isPlaying = !this.isPlaying;
        this.updatePlayIcons(this.currentTrack.id);
    }

    prev() {  // предыдущий трек
        console.log('prev вызван, playlist.length:', this.playlist.length);

        if (!this.playlist.length) return;

        // Если прошло больше 5 секунд — перемотка в начало текущего трека
        if (this.audio.currentTime > 5) {
            this.audio.currentTime = 0;
            return;
        }

        // Иначе предыдущий трек
        this.currentIndex = (this.currentIndex - 1 + this.playlist.length) % this.playlist.length;
        this.loadTrack(this.playlist[this.currentIndex]);
        if (!this.isPlaying) this.play();
    }

    next() {  // следующий трек
        console.log('next вызван, playlist.length:', this.playlist.length);

        if (!this.playlist.length) return;

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
        this.updatePlayIcons(null);
    }

    setPlaylist(tracks, startIndex = 0) {  // устанавливает плейлист (последовательное воспроизведение)
        console.log('setPlaylist вызван, треков:', tracks.length);
        this.playlist = tracks;
        this.currentIndex = startIndex;
        if (tracks.length) {
            this.loadTrack(tracks[startIndex]);
        }
    }

    playSingleTrack(track) {  // воспроизводит один трек (без плейлиста)
        this.currentTrack = track;
        this.audio.src = `/api/tracks/${track.id}/stream`;
        this.trackNameEl.textContent = track.title;
        this.play();
        this.updatePlayIcons(track.id);
    }

    updatePlayIcons(activeTrackId) {  // синхронизация треугольничков в плашке трека
        document.querySelectorAll('.track-play').forEach(btn => {
            const trackId = btn.getAttribute('data-id');
            const triangle = btn.querySelector('.play-triangle');

            if (!triangle) return;

            if (activeTrackId && trackId == activeTrackId && this.isPlaying) {
                triangle.style.opacity = '0';
            } else {
                triangle.style.opacity = '1';
            }
        });
    }
}

const player = new RadioPlayer();  // глобальный экземпляр плеера
