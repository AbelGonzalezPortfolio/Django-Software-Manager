Invoke-Command -ComputerName $args -ScriptBlock {
    $UninstallKey=”SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall”

    foreach($architecture in @(512, 256)){
    
        $reg=[microsoft.win32.registrykey]::OpenBaseKey(‘LocalMachine’, $architecture)
    
        $regkey=$reg.OpenSubKey($UninstallKey) 
    
        $subkeys=$regkey.GetSubKeyNames() 
    
        foreach($key in $subkeys){
    
            $thisKey=$UninstallKey+”\\”+$key 
    
            $thisSubKey=$reg.OpenSubKey($thisKey) 
    
            "$($thisSubKey.GetValue(“DisplayName”)):$($thisSubKey.GetValue(“DisplayVersion”))"
    
        } 
    }
}

