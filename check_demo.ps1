# Keep Windows awake (prevent sleep / display off).
# Every 3 minutes: ensure desktop demo.txt exists, open it in Notepad,
# and re-assert the keep-awake state. Loop forever. Press Ctrl+C to stop.

$IntervalSeconds = 180
$DemoFile = Join-Path ([Environment]::GetFolderPath('Desktop')) 'demo.txt'

# --- Keep-awake API: kernel32!SetThreadExecutionState ---
if (-not ("PowerManagement" -as [type])) {
    Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class PowerManagement {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@
}

# ES_CONTINUOUS (0x80000000) | ES_SYSTEM_REQUIRED (0x1) | ES_DISPLAY_REQUIRED (0x2)
# = 2147483651. ES_CONTINUOUS keeps it in effect until the process exits.
$KeepAwakeFlags = [uint32]2147483651

function Write-Log([string]$Message) {
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Write-Host "[$timestamp] $Message"
}

# Assert immediately, then re-assert every cycle for extra safety.
[void][PowerManagement]::SetThreadExecutionState($KeepAwakeFlags)
Write-Log "Keep-awake active (system + display). Opening every $($IntervalSeconds / 60) min. Press Ctrl+C to stop."

while ($true) {
    [void][PowerManagement]::SetThreadExecutionState($KeepAwakeFlags)
    Write-Log "Keep-awake re-asserted."

    if (-not (Test-Path -LiteralPath $DemoFile)) {
        Set-Content -LiteralPath $DemoFile -Value 'demo' -Encoding UTF8
        Write-Log "Not found. Created: $DemoFile"
    }
    else {
        Write-Log "Exists: $DemoFile"
    }

    Start-Process notepad -ArgumentList $DemoFile
    Write-Log "Opened in Notepad: $DemoFile"

    Start-Sleep -Seconds $IntervalSeconds
}
