$job = Invoke-Command -ComputerName $args -ScriptBlock { Write-Output $true } -AsJob
$job | Wait-Job -Timeout 5 | Out-Null
$result = Receive-Job -Job $job

if ($result) {
    $result
}
else {
    Write-Error "powershell remoting not enabled"
}
Stop-Job -Job $job | Out-Null
Remove-Job -Job $job
