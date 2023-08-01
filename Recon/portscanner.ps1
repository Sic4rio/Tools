# lightweight powershell port scanner written by SICARI0

function Test-Port {
    param (
        [string]$IPAddress,
        [int[]]$Ports
    )

    $openPorts = @()
    $closedPorts = @()
    $totalPorts = $Ports.Count
    $completedPorts = 0

    foreach ($port in $Ports) {
        try {
            $tcpClient = New-Object System.Net.Sockets.TcpClient
            $tcpClient.Connect($IPAddress, $port)
            $tcpClient.Close()
            $openPorts += $port
        } catch {
            $closedPorts += $port
        }

        $completedPorts++
        $progress = ($completedPorts / $totalPorts) * 100
        Write-Progress -Activity "Scanning Ports" -Status "Progress" -PercentComplete $progress
    }

    return @{
        OpenPorts = $openPorts
        ClosedPorts = $closedPorts
    }
}

function Show-Result {
    param (
        [string]$Message,
        [string]$Color
    )

    if ($Color -eq "Green") {
        Write-Host $Message -ForegroundColor Green
    } elseif ($Color -eq "Red") {
        Write-Host $Message -ForegroundColor Red
    }
}

# Common ports to scan
$commonPorts = 80, 443, 22, 21, 25, 53, 445, 3389, 1433, 3306, 110, 1194, 8080, 8888, 8000, 5900, 5901, 5902, 5903, 5904, 5905, 5906, 5907, 5908, 5909, 3389, 5800, 5801, 5802, 5803, 5900, 5901, 5902, 5903, 5904, 5905, 5906, 5907, 5908, 5909, 8000, 8008, 8080, 8443, 8888, 8001, 8889, 9000

$IPAddress = Read-Host "Enter the IP address to scan"

$portResults = Test-Port -IPAddress $IPAddress -Ports $commonPorts

Show-Result "`nScanning IP address: $IPAddress`n" -Color "Green"

if ($portResults.OpenPorts.Count -gt 0) {
    Show-Result "Open ports: $($portResults.OpenPorts -join ', ')" -Color "Green"
} else {
    Show-Result "No open ports found" -Color "Red"
}
#if ($portResults.ClosedPorts.Count -gt 0) {
 #   Show-Result "Closed ports: $($portResults.ClosedPorts -join ', ')" -Color "Red"
#}
#portscanner
