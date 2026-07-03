# Build and publish the Finnish book to GitHub Pages (gh-pages branch).
# Requires: mdbook, mdbook-trpl, ghp-import (pip install ghp-import)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& (Join-Path $PSScriptRoot "build-fi.ps1")

Copy-Item (Join-Path $Root "tools\preview-robots.txt") (Join-Path $Root "book-fi\robots.txt") -Force

ghp-import -m "rebuild Finnish GitHub Pages from book-fi" book-fi
git push origin gh-pages

Write-Host "Finnish preview published to gh-pages branch."
