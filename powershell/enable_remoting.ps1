PSExec.exe "\\$args" powershell.exe Enable-PSRemoting
Invoke-Command -ComputerName $args -ScriptBlock {
    Set-NetFirewallRule -DisplayName "Windows Remote Management (HTTP-In)" -Action "Allow" -RemoteAddress "<server remote address>"
}
