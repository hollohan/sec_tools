while ($true) {
    cls
    $processes = Get-Process | Sort-Object CPU -Descending | Select-Object -First 20
    $processes | Format-Table -Property Id, ProcessName, CPU, Memory
    Start-Sleep -Seconds 1
}
