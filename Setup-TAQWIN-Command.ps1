# Setup-TAQWIN-Command.ps1
# This script sets up the TAQWIN command as an alias

Write-Host "Setting up TAQWIN command..." -ForegroundColor Cyan

# Create an alias that points to the TAQWIN.ps1 script
$scriptPath = Join-Path (Get-Location) "TAQWIN.ps1"

# Check if the script exists
if (Test-Path $scriptPath) {
    # Create the alias for the current session
    Set-Alias -Name "taqwin" -Value $scriptPath -Scope Global
    
    Write-Host "TAQWIN command setup completed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now use the following commands:" -ForegroundColor Yellow
    Write-Host "- 'taqwin' (lowercase)"
    Write-Host "- 'TAQWIN' (uppercase)"
    Write-Host "- '.\TAQWIN.ps1' (direct script execution)"
    Write-Host ""
    Write-Host "Testing the alias..." -ForegroundColor Cyan
    
    # Test the alias
    Write-Host "Executing 'taqwin' command:" -ForegroundColor Magenta
    & taqwin

} else {
    Write-Host "Error: TAQWIN.ps1 script not found in current directory" -ForegroundColor Red
    Write-Host "Please ensure you are in the D:\Ethereal Glow directory" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup completed!" -ForegroundColor Green
