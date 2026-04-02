# Publishing Checklist

## Before First Push

1. Confirm `.env` is ignored and not staged.
2. Confirm no personal access token, API key, or credential appears in any tracked file.
3. Confirm `old tutorials/`, `future tutorials/`, caches, and transcript/audio working files are not being published unless intentional.
4. Confirm tutorial image paths render correctly.
5. Confirm homepage links resolve to the generated tutorial pages.

## Content QA

1. Review frontmatter for every tutorial: `title`, `subtitle`, `date`, `category`, `tools`, `difficulty`.
2. Check category consistency: prefer `gis`, `data-science`, and `nlp`.
3. Verify thumbnails and inline image references exist.
4. Spot-check YouTube and external links.
5. Confirm unfinished placeholder tutorials are either hidden or intentionally published.

## GitHub Pages Setup

1. Push the repository to GitHub.
2. Open the repository settings.
3. Go to `Pages`.
4. Under `Build and deployment`, choose `Deploy from a branch`.
5. Select the `main` branch and the `/ (root)` folder.
6. Save and wait for the Pages build to finish.

## Recommended First Publish Flow

```bash
git init
git remote add origin https://github.com/tedngai/datadrivendesign.git
git add .
git status
git commit -m "Initial tutorial library publish"
git branch -M main
git push -u origin main
```

## Security Notes

1. Never commit `.env`.
2. Never paste the PAT into a tracked file.
3. Prefer GitHub CLI or your local credential manager for authentication instead of storing tokens in repository content.
