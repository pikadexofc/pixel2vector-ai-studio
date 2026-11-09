param (
    [Parameter(Mandatory=$true)][string]$InputFile,
    [Parameter(Mandatory=$false)][string]$OutputFile
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$potrace = Join-Path $scriptDir "bin\potrace.exe"

if (!(Test-Path $InputFile)) {
    Write-Host "[ERROR] Input file not found: $InputFile" -ForegroundColor Red
    exit 1
}

if (-not $OutputFile) {
    $OutputFile = [System.IO.Path]::ChangeExtension($InputFile, ".svg")
}

Write-Host ">>> Vectorizing $InputFile -> $OutputFile..." -ForegroundColor Cyan

Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Bitmap]::FromFile((Resolve-Path $InputFile))
$tmpBmp = [System.IO.Path]::GetTempFileName() + ".bmp"
$img.Save($tmpBmp, [System.Drawing.Imaging.ImageFormat]::Bmp)
$img.Dispose()

& $potrace -s -o $OutputFile $tmpBmp
Remove-Item -Path $tmpBmp -Force -ErrorAction SilentlyContinue

if (Test-Path $OutputFile) {
    $size = (Get-Item $OutputFile).Length
    Write-Host "[SUCCESS] Vector SVG generated! Size: $size bytes" -ForegroundColor Green
    Write-Host "Output: $OutputFile" -ForegroundColor Yellow
} else {
    Write-Host "[ERROR] Vectorization failed." -ForegroundColor Red
}
