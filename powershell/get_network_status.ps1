$ping = new-object System.Net.NetworkInformation.Ping

$result1 = $ping.send($args, 100).Status -eq "Success"
$result2 = $ping.send($args, 100).Status -eq 'Success'

if($result1 -or $result2){"ok"}else{Write-Error "cannot ping device"}