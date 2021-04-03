<powershell>

# DSaaS URLs
$MainURLs = "app.deepsecurity.trendmicro.com", "agents.deepsecurity.trendmicro.com", "dsmim.deepsecurity.trendmicro.com", "relay.deepsecurity.trendmicro.com"
$APIURLs = "app.deepsecurity.trendmicro.com/webservice/Manager?WSDL", "app.deepsecurity.trendmicro.com/api", "app.deepsecurity.trendmicro.com/rest"
$SPN = "dsaas1100-en-census.trendmicro.com", "deepsecaas11-en.gfrbridge.trendmicro.com", "dsaas.icrc.trendmicro.com", "dsaas-en-f.trx.trendmicro.com", "dsaas-en-b.trx.trendmicro.com","dsaas.url.trendmicro.com"
$DCURLs = "files.trendmicro.com"
$UpdateURLs = "iaus.activeupdate.trendmicro.com", "iaus.trendmicro.com", "ipv6-iaus.trendmicro.com", "ipv6-iaus.activeupdate.trendmicro.com"

# XDR URLs
$xdrURLs = "ak5ih4ev105f2-ats.iot.us-east-1.amazonaws.com", "azrb5zzyvrkw6-ats.iot.us-east-1.amazonaws.com"

#functions
function Show-RetryMenu
{
    Write-Host "Retry? y/n"
}

function Show-ExportMenu
{
    Write-Host "Export to File? y/n"
}

function Test-Port($ip)
{
    $t = New-Object System.Net.Sockets.TcpClient
    try{
    $t.Connect($ip, 443)
    if ($t.Connected) {
    echo "Successfully connected to $ip via port 443"
        }
    }
    catch {
        echo "Failed to connect to $ip via port 443"
    }
}

function Test-Port80($ip)
{
    $t = New-Object System.Net.Sockets.TcpClient
    try{
    $t.Connect($ip, 80)
    if ($t.Connected) {
    echo "Successfully connected to $ip via port 80"
        }
    }
    catch {
        echo "Failed to connect to $ip via port 80"
    }
}

function Powershell4upDSaaS {
                    $Global:ProgressPreference = 'SilentlyContinue'
                    echo "Checking C1WS Main URLs..." >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt

                    ForEach ($DSaaSURL in $MainURLs){
                    $Test1 = Test-NetConnection $DSaaSURL -Port 443 -InformationLevel Quiet -ErrorAction SilentlyContinue -WarningAction SilentlyContinue
                        if($Test1 -eq 'True'){
                            echo "Successfully connected to port 443 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                        else{
                            echo "Failed to connect to port 443 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                    }

                    echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    echo "Checking C1WS Download Center URLs..." >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    ForEach ($DSaaSURL in $DCURLs){
                    $Test1 = Test-NetConnection $DSaaSURL -Port 443 -InformationLevel Quiet -ErrorAction SilentlyContinue -WarningAction SilentlyContinue
                        if($Test1 -eq 'True'){
                            echo "Successfully connected to port 443 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                        else{
                            echo "Failed to connect to port 443 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                    }

                    ForEach ($DSaaSURL in $DCURLs){
                    $Test1 = Test-NetConnection $DSaaSURL -Port 80 -InformationLevel Quiet -ErrorAction SilentlyContinue -WarningAction SilentlyContinue
                        if($Test1 -eq 'True'){
                            echo "Successfully connected to port 80 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                        else{
                            echo "Failed to connect to port 80 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                    }

                    echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    echo "Checking C1WS Active Update URLs..." >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    ForEach ($DSaaSURL in $UpdateURLs){
                    $Test1 = Test-NetConnection $DSaaSURL -Port 443 -InformationLevel Quiet -ErrorAction SilentlyContinue -WarningAction SilentlyContinue
                        if($Test1 -eq 'True'){
                            echo "Successfully connected to port 443 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                        else{
                            echo "Failed to connect to port 443 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                    }

                    ForEach ($DSaaSURL in $UpdateURLs){
                    $Test1 = Test-NetConnection $DSaaSURL -Port 80 -InformationLevel Quiet -ErrorAction SilentlyContinue -WarningAction SilentlyContinue
                        if($Test1 -eq 'True'){
                            echo "Successfully connected to port 80 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                        else{
                            echo "Failed to connect to port 80 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                    }
                        
                    echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    echo "Checking C1WS Smart Protection Network URLs..." >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    ForEach ($DSaaSURL in $SPN){
                    $Test1 = Test-NetConnection $DSaaSURL -Port 443 -InformationLevel Quiet -ErrorAction SilentlyContinue -WarningAction SilentlyContinue
                        if($Test1 -eq 'True'){
                            echo "Successfully connected to port 443 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                        else{
                            echo "Failed to connect to port 443 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                    }

                    ForEach ($DSaaSURL in $SPN){
                    $Test1 = Test-NetConnection $DSaaSURL -Port 80 -InformationLevel Quiet -ErrorAction SilentlyContinue -WarningAction SilentlyContinue
                        if($Test1 -eq 'True'){
                            echo "Successfully connected to port 80 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                        else{
                            echo "Failed to connect to port 80 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                    }

                    echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    echo "Checking C1WS XDR URLs..." >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt

                    ForEach ($DSaaSURL in $xdrURLs){
                    $Test1 = Test-NetConnection $DSaaSURL -Port 443 -InformationLevel Quiet -ErrorAction SilentlyContinue -WarningAction SilentlyContinue
                        if($Test1 -eq 'True'){
                            echo "Successfully connected to port 443 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                        else{
                            echo "Failed to connect to port 443 on $DSaaSURL" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                        }
                    }
}


function Powershell4downDSaaS {
                echo "Checking C1WS Main URLs..." >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                ForEach ($DSaaSURL in $MainURLs){
                    Test-Port($DSaaSURL) >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    }

                echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                echo "Checking C1WS Download Center URLs..." >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                ForEach ($DSaaSURL in $DCURLs){
                    Test-Port($DSaaSURL) >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    }
                ForEach ($DSaaSURL in $DCURLs){
                    Test-Port80($DSaaSURL) >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    }

                echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                echo "Checking C1WS Active Update URLs..." >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                ForEach ($DSaaSURL in $UpdateURLs){
                    Test-Port($DSaaSURL) >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    }
                ForEach ($DSaaSURL in $UpdateURLs){
                    Test-Port80($DSaaSURL) >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    }

                echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                echo "Checking C1WS Smart Protection Network URLs..." >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                ForEach ($DSaaSURL in $SPN){
                    Test-Port($DSaaSURL) >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    }
                ForEach ($DSaaSURL in $SPN){
                    Test-Port80($DSaaSURL) >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    }

                echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                echo "Checking C1WS XDR URLs..." >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                echo "`n" >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                ForEach ($DSaaSURL in $xdrURLs){
                    Test-Port($DSaaSURL) >> $env:USERPROFILE\DSaaS_Pre-check\connection.txt
                    }             
}

#Main Program Execution
do
{
                cls
                Remove-Item -Path "$env:USERPROFILE\DSaaS_Pre-check" –recurse -Erroraction 'silent'
                New-Item -Path "$env:USERPROFILE" -Name "DSaaS_Pre-check" -ItemType "directory" -Force | Out-Null
                Write-Host "Please wait..."
                $versionPS = $PSVersionTable.PSVersion.Major
                if ($versionPS -gt 3){
                    Write-Host "You are using Powershell version 4 and up."                    
                    Write-Host "Checking connection to the URLs of Cloud One Workload Security..."
                    Powershell4upDSaaS
                    Write-Host "Done. Displaying Results..."
                    echo "`n"
                    Start-Sleep 5
                    Type $env:USERPROFILE\DSaaS_Pre-check\connection.txt                        
                    
                    }

                else {
                Write-Host "You are using Powershell version 4 lower"
                Write-Host "Checking connection to the URLs of Cloud One Workload Security..."
                echo "`n"
                Powershell4downDSaaS
                Write-Host "Done. Displaying Results..."
                
                Start-Sleep 5
                Type $env:USERPROFILE\DSaaS_Pre-check\connection.txt  
                }
                echo "`n"
                echo "`n"
                Show-RetryMenu
                $input = Read-Host "Enter Choice"
                if ($input -eq 'n'){
                Show-ExportMenu
                $input = Read-Host "Enter Choice"
                    if($input -eq 'y'){
                    Move-Item $env:USERPROFILE\DSaaS_Pre-check\connection.txt -Destination $env:USERPROFILE\Desktop\
                    Remove-Item -Path "$env:USERPROFILE\DSaaS_Pre-check" –recurse -Erroraction 'silent'
                    Write-Host "Done. Check connection.txt in your Desktop!"
                    echo "`n"
                    Write-Host "Thank you for using the tool!"
                    $exported = 1
                    $input = 'q'
                    }else{
                    Write-Host "Results not Exported!"
                    echo "`n"
                    Write-Host "Thank you for using the tool!"
                    $exported = 0
                    $input = 'q'
                    }
                } 

} until ($input -eq 'q')
$ranscript = 1          
$telemurl = 'http://3.138.183.200/telemetry/'
$web  = Invoke-WebRequest -Uri $telemurl -SessionVariable session

$form = $web.Forms[0]
$web.Forms[0].Fields.'ranscript' = $ranscript
$web.Forms[0].Fields.'exported' = $exported

$web2 = Invoke-WebRequest -Uri ($telemurl + $web.Forms[0].Action) -WebSession $session -Method POST -Body $web.Forms[0].Fields
$web2
</powershell>
