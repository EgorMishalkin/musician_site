const player = document.getElementById("player");
const playerToggle = document.getElementById("player-toggle");
const playerTitle = document.getElementById("player-title");
const playerProgress = document.getElementById("player-progress");
const playerCurrent = document.getElementById("player-current");
const playerDuration = document.getElementById("player-duration");
const trackDownload = document.getElementById("track-download");

const audio = new Audio();
audio.preload = "metadata";

let currentElement = null;
let isSeeking = false;


function formatTime(seconds) {
    if (!Number.isFinite(seconds)) {
        return "0:00";
    }

    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);

    return `${minutes}:${String(remainingSeconds).padStart(2, "0")}`;
}


function clearActiveTrack() {
    document.querySelectorAll(
        ".playable-track.active"
    ).forEach((element) => {
        element.classList.remove("active");
    });
}


function updateActiveTrack() {
    clearActiveTrack();

    if (currentElement) {
        currentElement.classList.add("active");
    }
}


function playElement(element) {
    if (currentElement === element) {
        if (audio.paused) {
            audio.play().catch((error) => {
                if (error.name !== "AbortError") {
                    console.error(error);
                }
            });
        } else {
            audio.pause();
        }

        return;
    }

    currentElement = element;

    player.hidden = false;
    playerTitle.textContent = element.dataset.title || "";
    playerCurrent.textContent = "0:00";
    playerDuration.textContent =
        element.dataset.duration || "0:00";
    playerProgress.value = 0;

    trackDownload.href = element.dataset.downloadUrl;

    audio.src = element.dataset.audioUrl;
    audio.load();

    audio.play().catch((error) => {
        if (error.name === "AbortError") {
            return;
        }

        console.error(error);
    });

    updateActiveTrack();
}


document.querySelectorAll(".playable-track").forEach((element) => {
    element.addEventListener("click", () => {
        playElement(element);
    });
});


document.querySelectorAll(".single-toggle").forEach((button) => {
    button.addEventListener("click", () => {
        const item = button.closest(".single-item");
        const tracks = item.querySelector(".single-tracks");

        if (!tracks) {
            return;
        }

        tracks.hidden = !tracks.hidden;
        item.classList.toggle("open", !tracks.hidden);
    });
});


playerToggle.addEventListener("click", () => {
    if (!audio.src) {
        return;
    }

    if (audio.paused) {
        audio.play().catch((error) => {
            if (error.name !== "AbortError") {
                console.error(error);
            }
        });
    } else {
        audio.pause();
    }
});


audio.addEventListener("play", () => {
    playerToggle.textContent = "❚❚";
});


audio.addEventListener("pause", () => {
    playerToggle.textContent = "▶";
});


audio.addEventListener("loadedmetadata", () => {
    playerDuration.textContent = formatTime(audio.duration);
    playerProgress.value = 0;
});


audio.addEventListener("timeupdate", () => {
    if (
        isSeeking ||
        !Number.isFinite(audio.duration) ||
        audio.duration <= 0
    ) {
        return;
    }

    playerProgress.value =
        (audio.currentTime / audio.duration) * 100;

    playerCurrent.textContent =
        formatTime(audio.currentTime);
});


playerProgress.addEventListener("pointerdown", () => {
    isSeeking = true;
});


playerProgress.addEventListener("input", () => {
    if (
        !Number.isFinite(audio.duration) ||
        audio.duration <= 0
    ) {
        return;
    }

    const previewTime =
        (Number(playerProgress.value) / 100) *
        audio.duration;

    playerCurrent.textContent =
        formatTime(previewTime);
});


function applySeek() {
    if (
        !Number.isFinite(audio.duration) ||
        audio.duration <= 0
    ) {
        isSeeking = false;
        return;
    }

    audio.currentTime =
        (Number(playerProgress.value) / 100) *
        audio.duration;

    isSeeking = false;
}


playerProgress.addEventListener("change", applySeek);
playerProgress.addEventListener("pointerup", applySeek);


audio.addEventListener("ended", () => {
    playerToggle.textContent = "▶";
    playerProgress.value = 0;
    playerCurrent.textContent = "0:00";
});


audio.addEventListener("error", () => {
    if (!currentElement) {
        return;
    }

    playerToggle.textContent = "▶";
    playerTitle.textContent =
        `${currentElement.dataset.title || "трек"} - файл не найден`;

    clearActiveTrack();
});
