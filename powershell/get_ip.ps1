Try
{
    $ip_address = Resolve-DnsName "$args.<domain>" -DnsOnly -NoHostsFile -QuickTimeout -ErrorAction Stop | Select-Object IPAddress -ExpandProperty IPAddress
    $ip_address
}
Catch
{
    Write-Error "Host not found"
}