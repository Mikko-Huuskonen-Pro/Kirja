# Build the Finnish translation of the Rust book.
# Uses book-fi.toml as the book configuration.

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$BookToml = Join-Path $Root "book.toml"
$BookFiToml = Join-Path $Root "book-fi.toml"
$Backup = Join-Path $Root "book.toml.bak-build-fi"

if (-not (Test-Path $BookFiToml)) {
    Write-Error "book-fi.toml not found"
}

Copy-Item $BookToml $Backup -Force
try {
    Copy-Item $BookFiToml $BookToml -Force
    mdbook build -d book-fi
    Write-Host "Finnish book built to book-fi/"
} finally {
    Move-Item $Backup $BookToml -Force
}
