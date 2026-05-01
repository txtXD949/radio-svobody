class RadioPlayer {
    constructor() {
        this.audio = new Audio();
        this.currentTrack = null;
        this.playlist = [];
        this.currentIndex = 0;
        this.isPlaying = false;

        this.initElements();
        this.initEventListeners();
    }

    initElements() {
        this.playBtn = document.querySelector('.play-pause');
        this.prevBtn = document.querySelector('.prev');
        this.nextBtn = document.querySelector('.next');
        this.trackNameEl = document.querySelector('.player-track-name');
        this.trackImageEl = document.querySelector('.player-image');
    }

    initEventListeners() {
        this.playBtn.addEventListener('click', () => this.togglePlay());
        this.prevBtn.addEventListener('click', () => this.prev());
        this.nextBtn.addEventListener('click', () => this.next());
        this.audio.addEventListener('ended', () => this.next());
    }

    loadTrack(track) {
        if (!track) return;

        this.currentTrack = track;
        this.audio.src = `/api/tracks/${track.id}/stream`;
        this.trackNameEl.textContent = track.title;

        this.updatePlayIcons(track.id);

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

    prev() {
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

    next() {
        console.log('next вызван, playlist.length:', this.playlist.length);

        if (!this.playlist.length) return;

        this.currentIndex = (this.currentIndex + 1) % this.playlist.length;
        this.loadTrack(this.playlist[this.currentIndex]);
        if (!this.isPlaying) this.play();
    }

    play() {
        this.audio.play();
        this.isPlaying = true;
        this.playBtn.textContent = '⏸';

        if (this.currentTrack) {
            this.updatePlayIcons(this.currentTrack.id);
        }
    }

    stop() {
        this.isPlaying = false;
        this.playBtn.textContent = '▶';
        this.updatePlayIcons(null);
    }

    setPlaylist(tracks, startIndex = 0) {
        console.log('setPlaylist вызван, треков:', tracks.length);
        this.playlist = tracks;
        this.currentIndex = startIndex;
        if (tracks.length) {
            this.loadTrack(tracks[startIndex]);
        }
    }

    playSingleTrack(track) {
        this.currentTrack = track;
        this.audio.src = `/api/tracks/${track.id}/stream`;
        this.trackNameEl.textContent = track.title;
        this.play();
        this.updatePlayIcons(track.id);
    }

    updatePlayIcons(activeTrackId) {
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

const player = new RadioPlayer();