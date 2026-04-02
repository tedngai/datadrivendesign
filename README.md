# Data-Driven Design

A public tutorial library for GIS, data science, visualization, and NLP workflows oriented toward design students.

## Scope

This repository publishes the cleaned tutorial collection in `_tutorials/` together with the images and interactive assets needed to render them.

Primary topic areas:

- GIS
- Data science
- Data visualization
- NLP

## Recommended Public Structure

```text
.
├── _tutorials/
├── _layouts/
├── assets/
│   ├── css/
│   ├── images/
│   └── interactive/
├── _config.yml
├── index.md
├── README.md
└── PUBLISHING.md
```

The following working directories are intentionally excluded from the public site:

- `old tutorials/`
- `future tutorials/`
- `.obsidian/`
- `.ruff_cache/`
- `video_audio/`
- `video_metadata/`
- `video_transcripts/`
- `.env`

## Local Preview

If you want to preview the site locally with Jekyll:

```bash
bundle exec jekyll serve
```

If you prefer not to run Jekyll locally, you can still review the Markdown directly and let GitHub Pages build the site after push.

## Publishing Target

This repo is set up to work cleanly with GitHub Pages as a project site for:

`https://tedngai.github.io/datadrivendesign/`

If you later move to a custom domain, update `url` and `baseurl` in `_config.yml`.
