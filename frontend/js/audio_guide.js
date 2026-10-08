/**
 * Audio Tour Controller — ElevenLabs / Web Speech fallback
 */
class AudioTourController {
  constructor() {
    this.el       = new Audio();
    this.isPlay   = false;
    this.text     = '';
    this.usingTTS = false;
    this.speed    = 1.0;
    this.utterance = null;

    this._buildWaveform();
    this._bind();
  }

  _buildWaveform() {
    const container = document.getElementById('waveform-bars');
    if (!container) return;
    container.innerHTML = '';
    const BAR_COUNT = 80;
    for (let i = 0; i < BAR_COUNT; i++) {
      const bar = document.createElement('div');
      bar.className = 'wave-bar';
      const h = Math.max(8, Math.round(Math.random() * 48));
      bar.style.height = `${h}px`;
      container.appendChild(bar);
    }
    this._waveBars = container.querySelectorAll('.wave-bar');
  }

  _animateWave() {
    if (!this._waveRaf) {
      const tick = () => {
        if (!this.isPlay) return;
        this._waveBars?.forEach((b, i) => {
          const h = Math.max(4, Math.round(8 + Math.random() * 44 * Math.sin(Date.now() / 250 + i * 0.5) ** 2));
          b.style.height = `${h}px`;
          b.classList.toggle('active', Math.random() > 0.55);
        });
        this._waveRaf = requestAnimationFrame(tick);
      };
      this._waveRaf = requestAnimationFrame(tick);
    }
  }

  _stopWave() {
    if (this._waveRaf) { cancelAnimationFrame(this._waveRaf); this._waveRaf = null; }
    this._waveBars?.forEach(b => { b.style.height = `${Math.max(8, Math.round(Math.random() * 24))}px`; b.classList.remove('active'); });
  }

  _bind() {
    document.getElementById('btn-play-pause')?.addEventListener('click', () => this.toggle());
    document.getElementById('btn-skip-back')?.addEventListener('click', () => this.skip(-15));
    document.getElementById('btn-skip-fwd')?.addEventListener('click',  () => this.skip(15));

    const speedBtn = document.getElementById('btn-speed-toggle');
    if (speedBtn) speedBtn.addEventListener('click', () => {
      this.speed = this.speed >= 1.5 ? 1.0 : this.speed + 0.25;
      speedBtn.textContent = `${this.speed}×`;
      this.el.playbackRate = this.speed;
    });

    this.el.addEventListener('timeupdate', () => this._onTime());
    this.el.addEventListener('ended',      () => this._onEnd());
    this.el.addEventListener('play',       () => this._setState(true));
    this.el.addEventListener('pause',      () => this._setState(false));
  }

  load(briefing) {
    this.text = briefing.script || '';
    const audio = briefing.audio || {};

    const transcript = document.getElementById('audio-transcript');
    if (transcript) transcript.textContent = this.text;

    const provTag = document.getElementById('audio-provider-tag');

    if (audio.audio_url) {
      this.usingTTS = false;
      this.el.src = audio.audio_url;
      this.el.playbackRate = this.speed;
      if (provTag) provTag.textContent = audio.provider || 'ElevenLabs';
    } else {
      this.usingTTS = true;
      if (provTag) provTag.textContent = 'On-device speech';
    }

    this.play();
  }

  play() {
    if (!this.text && !this.el.src) return;
    if (this.usingTTS) {
      window.speechSynthesis?.cancel();
      this.utterance = new SpeechSynthesisUtterance(this.text);
      this.utterance.rate  = this.speed;
      this.utterance.pitch = 0.95;
      const voices = window.speechSynthesis?.getVoices() || [];
      const v = voices.find(v => v.lang.startsWith('en') && /daniel|samantha|natural/i.test(v.name));
      if (v) this.utterance.voice = v;
      this.utterance.onend = () => this._onEnd();
      window.speechSynthesis?.speak(this.utterance);
      this._setState(true);
    } else {
      this.el.play().catch(() => {});
    }
  }

  pause() {
    if (this.usingTTS) { window.speechSynthesis?.pause(); this._setState(false); }
    else this.el.pause();
  }

  toggle() { this.isPlay ? this.pause() : this.play(); }

  skip(sec) {
    if (!this.usingTTS && this.el.duration) {
      this.el.currentTime = Math.max(0, Math.min(this.el.duration, this.el.currentTime + sec));
    }
  }

  _setState(playing) {
    this.isPlay = playing;
    const btn = document.getElementById('btn-play-pause');
    if (btn) btn.classList.toggle('playing', playing);
    const icon = document.getElementById('audio-pulse-icon');
    if (icon) icon.classList.toggle('playing', playing);
    if (playing) this._animateWave(); else this._stopWave();
  }

  _onTime() {
    if (!this.el.duration) return;
    const pct  = (this.el.currentTime / this.el.duration) * 100;
    const fill = document.getElementById('audio-progress');
    if (fill) fill.style.width = `${pct}%`;
    const label = document.getElementById('audio-time-label');
    if (label) {
      const fmt = s => `${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
      label.textContent = `${fmt(this.el.currentTime)} / ${fmt(this.el.duration)}`;
    }
  }

  _onEnd() {
    this._setState(false);
    const fill = document.getElementById('audio-progress');
    if (fill) fill.style.width = '100%';
  }
}

window.audioTour = new AudioTourController();
