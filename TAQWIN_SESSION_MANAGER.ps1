# 📝 TAQWIN SESSION BUILDER MANAGEMENT SYSTEM
# Comprehensive Session Recording, Analysis & Archive
# Created: 2025-07-26T18:12:30Z
# Authority: Syed Muzamil - Founder Directive Implementation

param(
    [string]$Action = "LOG",
    [string]$SessionID = "",
    [string]$UserInput = "",
    [string]$SystemResponse = "",
    [string]$Type = "INTERACTION"
)

# Configuration
$SessionBuilderDir = "00_TAQWIN_CORE\session_builder"
$SessionArchiveDir = "00_TAQWIN_CORE\session_archive"
$SessionAnalyticsDir = "00_TAQWIN_CORE\session_analytics"

# Ensure all directories exist
@($SessionBuilderDir, $SessionArchiveDir, $SessionAnalyticsDir) | ForEach-Object {
    if (!(Test-Path $_)) { New-Item -ItemType Directory -Path $_ -Force | Out-Null }
}

# Initialize Session ID if not provided
if ([string]::IsNullOrEmpty($SessionID)) {
    $SessionID = "TAQWIN_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss')_SESSION"
}

$CurrentSessionFile = "$SessionBuilderDir\$SessionID.json"
$SessionMetaFile = "$SessionBuilderDir\$SessionID" + "_meta.json"

# Function to create session metadata
function Initialize-SessionMetadata {
    param([string]$SessionID)
    
    $MetaData = @{
        session_id = $SessionID
        created_timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        founder = "Syed Muzamil"
        brand = "Ethereal Glow"
        session_type = "TAQWIN_ENHANCED_INTERACTIVE"
        status = "ACTIVE"
        interaction_count = 0
        last_activity = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        categories = @()
        tags = @()
        priority_level = "STANDARD"
        system_version = "TAQWIN_HOME_INTERFACE_V1.0"
    }
    
    $MetaData | ConvertTo-Json -Depth 3 | Out-File $SessionMetaFile -Encoding UTF8
    return $MetaData
}

# Function to log session data
function Add-SessionEntry {
    param(
        [string]$SessionID,
        [string]$Type,
        [string]$Content,
        [string]$Source = "TAQWIN_SYSTEM",
        [string]$Category = "GENERAL",
        [hashtable]$AdditionalData = @{}
    )
    
    $Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    
    $SessionEntry = @{
        timestamp = $Timestamp
        session_id = $SessionID
        type = $Type
        content = $Content
        source = $Source
        category = $Category
        additional_data = $AdditionalData
        entry_id = [System.Guid]::NewGuid().ToString()
    }
    
    # Load existing session data or create new
    if (Test-Path $CurrentSessionFile) {
        $ExistingData = Get-Content $CurrentSessionFile -Raw | ConvertFrom-Json
        $SessionData = [System.Collections.ArrayList]@($ExistingData)
    } else {
        $SessionData = [System.Collections.ArrayList]@()
        Initialize-SessionMetadata -SessionID $SessionID | Out-Null
    }
    
    # Add new entry
    $SessionData.Add($SessionEntry) | Out-Null
    
    # Save session data
    $SessionData | ConvertTo-Json -Depth 4 | Out-File $CurrentSessionFile -Encoding UTF8
    
    # Update metadata
    Update-SessionMetadata -SessionID $SessionID -NewInteraction
    
    Write-Host "📝 Session entry logged: $Type" -ForegroundColor Green
}

# Function to update session metadata
function Update-SessionMetadata {
    param(
        [string]$SessionID,
        [switch]$NewInteraction,
        [string]$Status = "",
        [string[]]$NewCategories = @(),
        [string[]]$NewTags = @()
    )
    
    if (Test-Path $SessionMetaFile) {
        $MetaData = Get-Content $SessionMetaFile -Raw | ConvertFrom-Json
        
        if ($NewInteraction) {
            $MetaData.interaction_count++
            $MetaData.last_activity = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        }
        
        if (![string]::IsNullOrEmpty($Status)) {
            $MetaData.status = $Status
        }
        
        if ($NewCategories.Count -gt 0) {
            $MetaData.categories = ($MetaData.categories + $NewCategories) | Select-Object -Unique
        }
        
        if ($NewTags.Count -gt 0) {
            $MetaData.tags = ($MetaData.tags + $NewTags) | Select-Object -Unique
        }
        
        $MetaData | ConvertTo-Json -Depth 3 | Out-File $SessionMetaFile -Encoding UTF8
    }
}

# Function to display session analytics
function Show-SessionAnalytics {
    param([string]$SessionID)
    
    if (!(Test-Path $CurrentSessionFile)) {
        Write-Host "❌ Session file not found: $SessionID" -ForegroundColor Red
        return
    }
    
    $SessionData = Get-Content $CurrentSessionFile -Raw | ConvertFrom-Json
    $MetaData = Get-Content $SessionMetaFile -Raw | ConvertFrom-Json
    
    Clear-Host
    
    Write-Host ""
    Write-Host "📊═══════════════════════════════════════════════════════════════════════════════📊" -ForegroundColor Yellow
    Write-Host "                        SESSION ANALYTICS DASHBOARD                              " -ForegroundColor Cyan
    Write-Host "📊═══════════════════════════════════════════════════════════════════════════════📊" -ForegroundColor Yellow
    Write-Host ""
    
    # Session Overview
    Write-Host "🎯 SESSION OVERVIEW" -ForegroundColor Magenta
    Write-Host "─────────────────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
    Write-Host "🆔 Session ID: $($MetaData.session_id)" -ForegroundColor Green
    Write-Host "⏰ Created: $($MetaData.created_timestamp)" -ForegroundColor White
    Write-Host "📈 Total Interactions: $($MetaData.interaction_count)" -ForegroundColor Cyan
    Write-Host "🔄 Last Activity: $($MetaData.last_activity)" -ForegroundColor Yellow
    Write-Host "📊 Status: $($MetaData.status)" -ForegroundColor Green
    Write-Host ""
    
    # Interaction Breakdown
    $UserInputs = $SessionData | Where-Object { $_.type -eq "USER_INPUT" }
    $SystemResponses = $SessionData | Where-Object { $_.type -eq "SYSTEM_RESPONSE" }
    $Commands = $SessionData | Where-Object { $_.type -eq "COMMAND" }
    
    Write-Host "📊 INTERACTION BREAKDOWN" -ForegroundColor Magenta
    Write-Host "─────────────────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
    Write-Host "👤 User Inputs: $($UserInputs.Count)" -ForegroundColor Cyan
    Write-Host "🤖 System Responses: $($SystemResponses.Count)" -ForegroundColor Yellow
    Write-Host "⚡ Commands Executed: $($Commands.Count)" -ForegroundColor Green
    Write-Host ""
    
    # Recent Activity
    Write-Host "🕒 RECENT ACTIVITY (Last 5 entries)" -ForegroundColor Magenta
    Write-Host "─────────────────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
    $RecentEntries = $SessionData | Select-Object -Last 5
    foreach ($Entry in $RecentEntries) {
        $TimeStamp = ([DateTime]$Entry.timestamp).ToString("HH:mm:ss")
        $TypeColor = switch ($Entry.type) {
            "USER_INPUT" { "Cyan" }
            "SYSTEM_RESPONSE" { "Yellow" }
            "COMMAND" { "Green" }
            default { "White" }
        }
        Write-Host "  [$TimeStamp] $($Entry.type): $($Entry.content.Substring(0, [Math]::Min(60, $Entry.content.Length)))..." -ForegroundColor $TypeColor
    }
    Write-Host ""
}

# Function to archive session
function Save-SessionArchive {
    param([string]$SessionID)
    
    if (!(Test-Path $CurrentSessionFile)) {
        Write-Host "❌ Session file not found for archiving: $SessionID" -ForegroundColor Red
        return
    }
    
    $ArchiveTimestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $ArchiveFile = "$SessionArchiveDir\ARCHIVE_$SessionID" + "_$ArchiveTimestamp.json"
    
    # Create comprehensive archive
    $SessionData = Get-Content $CurrentSessionFile -Raw | ConvertFrom-Json
    $MetaData = Get-Content $SessionMetaFile -Raw | ConvertFrom-Json
    
    $ArchiveData = @{
        archive_timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        session_metadata = $MetaData
        session_data = $SessionData
        archive_statistics = @{
            total_entries = $SessionData.Count
            session_duration = "Calculated based on first and last timestamps"
            data_size_kb = ((Get-Item $CurrentSessionFile).Length / 1024)
        }
    }
    
    $ArchiveData | ConvertTo-Json -Depth 5 | Out-File $ArchiveFile -Encoding UTF8
    
    # Update metadata to archived
    Update-SessionMetadata -SessionID $SessionID -Status "ARCHIVED"
    
    Write-Host "📁 Session archived successfully: $ArchiveFile" -ForegroundColor Green
}

# Main execution logic
switch ($Action.ToUpper()) {
    "LOG" {
        if (![string]::IsNullOrEmpty($UserInput)) {
            Add-SessionEntry -SessionID $SessionID -Type "USER_INPUT" -Content $UserInput -Source "USER" -Category "INPUT"
        }
        if (![string]::IsNullOrEmpty($SystemResponse)) {
            Add-SessionEntry -SessionID $SessionID -Type "SYSTEM_RESPONSE" -Content $SystemResponse -Source "TAQWIN_SYSTEM" -Category "RESPONSE"
        }
    }
    "ANALYTICS" {
        Show-SessionAnalytics -SessionID $SessionID
    }
    "ARCHIVE" {
        Save-SessionArchive -SessionID $SessionID
    }
    "INIT" {
        Initialize-SessionMetadata -SessionID $SessionID
        Write-Host "🚀 Session initialized: $SessionID" -ForegroundColor Green
    }
    default {
        Write-Host "📋 TAQWIN Session Manager" -ForegroundColor Cyan
        Write-Host "Available actions: LOG, ANALYTICS, ARCHIVE, INIT" -ForegroundColor Yellow
    }
# Return session information for integration
return @{
    session_id = $SessionID
    session_file = $CurrentSessionFile
    meta_file = $SessionMetaFile
    status = "OPERATIONAL"
}
