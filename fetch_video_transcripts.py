#!/usr/bin/env python3

import json
import os
import re
import subprocess
from pathlib import Path

from openai import OpenAI


BASE_DIR = Path("/home/tngai/data/Tutorials")
TUTORIAL_DIR = BASE_DIR / "_tutorials"
METADATA_DIR = BASE_DIR / "video_metadata"
RAW_DIR = BASE_DIR / "video_transcripts" / "raw"
TEXT_DIR = BASE_DIR / "video_transcripts" / "text"
AUDIO_DIR = BASE_DIR / "video_audio"
MANIFEST_PATH = BASE_DIR / "video_transcripts" / "manifest.json"


def load_env_file() -> None:
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value)


def collect_video_map() -> dict[str, list[str]]:
    video_map: dict[str, list[str]] = {}
    for path in sorted(TUTORIAL_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"youtube_ids:\s*\[([^\]]*)\]", text)
        if not match:
            continue
        for video_id in re.findall(r'"([A-Za-z0-9_-]+)"', match.group(1)):
            video_map.setdefault(video_id, []).append(path.name)
    return video_map


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=True, capture_output=True, text=True)


def fetch_metadata(video_id: str) -> dict:
    out_path = METADATA_DIR / f"{video_id}.json"
    if out_path.exists():
        return json.loads(out_path.read_text(encoding="utf-8"))

    result = run(
        [
            "yt-dlp",
            "--skip-download",
            "--dump-single-json",
            f"https://www.youtube.com/watch?v={video_id}",
        ]
    )
    out_path.write_text(result.stdout, encoding="utf-8")
    return json.loads(result.stdout)


def subtitle_files(video_id: str) -> list[Path]:
    return sorted(
        p
        for p in RAW_DIR.glob(f"{video_id}*.json3")
        if ".live_chat." not in p.name and ".description." not in p.name
    )


def download_subtitles(video_id: str) -> list[Path]:
    existing = subtitle_files(video_id)
    if existing:
        return existing

    subprocess.run(
        [
            "yt-dlp",
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            "en.*,en-US,en,en-orig",
            "--sub-format",
            "json3",
            "-o",
            str(RAW_DIR / "%(id)s.%(ext)s"),
            f"https://www.youtube.com/watch?v={video_id}",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    return subtitle_files(video_id)


def json3_to_text(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    chunks = []
    seen = set()
    for event in data.get("events", []):
        segs = event.get("segs")
        if not segs:
            continue
        text = "".join(seg.get("utf8", "") for seg in segs)
        text = text.replace("\n", " ").strip()
        text = re.sub(r"\s+", " ", text)
        if not text or text in seen:
            continue
        seen.add(text)
        chunks.append(text)
    return "\n".join(chunks).strip() + "\n"


def choose_subtitle_file(files: list[Path]) -> Path | None:
    if not files:
        return None
    ranked = sorted(
        files,
        key=lambda p: (
            "orig" in p.name,
            "auto" in p.name,
            p.name,
        ),
    )
    return ranked[0]


def ensure_audio(video_id: str) -> Path:
    out_base = AUDIO_DIR / f"{video_id}.%(ext)s"
    mp3_path = AUDIO_DIR / f"{video_id}.mp3"
    if mp3_path.exists():
        return mp3_path
    subprocess.run(
        [
            "yt-dlp",
            "-x",
            "--audio-format",
            "mp3",
            "-o",
            str(out_base),
            f"https://www.youtube.com/watch?v={video_id}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return mp3_path


def transcribe_audio(client: OpenAI, audio_path: Path) -> str:
    with audio_path.open("rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
        )
    return transcript.strip() + "\n"


def main() -> None:
    load_env_file()
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None

    video_map = collect_video_map()
    manifest = []

    for video_id, tutorials in sorted(video_map.items()):
        metadata = fetch_metadata(video_id)
        title = metadata.get("title", "")
        channel = metadata.get("channel") or metadata.get("uploader") or ""
        text_path = TEXT_DIR / f"{video_id}.txt"
        source = None

        if not text_path.exists():
            subs = download_subtitles(video_id)
            chosen = choose_subtitle_file(subs)
            if chosen:
                text_path.write_text(json3_to_text(chosen), encoding="utf-8")
                source = f"subtitle:{chosen.name}"
            else:
                if client is None:
                    raise RuntimeError(
                        f"No subtitles for {video_id} and OPENAI_API_KEY unavailable"
                    )
                audio_path = ensure_audio(video_id)
                text_path.write_text(
                    transcribe_audio(client, audio_path), encoding="utf-8"
                )
                source = "whisper"
        else:
            source = "cached"

        manifest.append(
            {
                "id": video_id,
                "title": title,
                "channel": channel,
                "tutorials": tutorials,
                "transcript_source": source,
                "transcript_path": str(text_path.relative_to(BASE_DIR)),
            }
        )
        print(f"{video_id}\t{channel}\t{title}\t{source}")

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
