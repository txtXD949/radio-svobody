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
        this.currentTrack = track;
        this.audio.src = `/api/tracks/${track.id}/stream`;
        this.trackNameEl.textContent = track.title;
        this.trackImageEl.style.backgroundImage = `url(${track.cover_url || '/static/images/default-cover.png'})`;

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

    next() {
        // p
    }

    prev() {
        // p
    }

    play() {
        this.audio.play();
        this.isPlaying = true;
        this.playBtn.textContent = '⏸';
    }

    stop() {
        this.isPlaying = false;
        this.playBtn.textContent = '▶';
        this.updatePlayIcons(null);
    }

    setPlaylist(tracks, startIndex = 0) {
        this.playlist = tracks;
        this.currentIndex = startIndex;
        this.loadTrack(this.playlist[startIndex]);
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
