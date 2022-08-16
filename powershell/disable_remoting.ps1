Invoke-Command -ComputerName $args -InDisconnectedSession -ScriptBlock {
    Disable-PSRemoting -Force
    Remove-Item -Path WSMan:\Localhost\listener\Listener_1084132640 -Recurse
    Set-NetFirewallRule -DisplayName 'Windows Remote Management (HTTP-In)' -Enabled False
    Set-Service -Name WinRM -StartupType Disabled
    Stop-Service -Name WinRM
}