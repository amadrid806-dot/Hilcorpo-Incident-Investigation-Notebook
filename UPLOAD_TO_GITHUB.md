# Upload this project to GitHub

Repository: `amadrid806-dot/Hilcorpo-Incident-Investigation-Notebook`

## Easiest method - GitHub web upload
1. Download and unzip the project.
2. Open your GitHub repository.
3. Choose **Add file > Upload files**.
4. Drag the contents of the unzipped project into the upload area.
5. Commit the files to `main`.

## Git command-line method
```bash
git clone https://github.com/amadrid806-dot/Hilcorpo-Incident-Investigation-Notebook.git
cd Hilcorpo-Incident-Investigation-Notebook
# Copy the contents of this ZIP into the cloned folder.
git add .
git commit -m "Initialize incident investigation notebook generator"
git push origin main
```

After upload, GitHub Actions will be able to build the PDF variants automatically on source changes.
