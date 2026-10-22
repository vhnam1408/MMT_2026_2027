param(
    [ValidateSet('server','client','test')]
    [string]$Mode = 'server',
    [string]$HostAddress,
    [int]$Port = 50000
)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $bundledPython) { $taskPython = $bundledPython }
elseif (Get-Command py -ErrorAction SilentlyContinue) { $taskPython = 'py' }
else { $taskPython = 'python' }
if ($Mode -eq 'server') {
    if (-not $HostAddress) { $HostAddress = '0.0.0.0' }
    & $taskPython -X utf8 server/server.py --host $HostAddress --port $Port
} else {
    $clientArgs = @('-X', 'utf8', 'client/client.py')
    if ($HostAddress) { $clientArgs += @('--host', $HostAddress, '--port', "$Port") }
    elseif ($Mode -eq 'test') { $clientArgs += @('--host', '127.0.0.1', '--port', "$Port") }
    elseif ($PSBoundParameters.ContainsKey('Port')) { $clientArgs += @('--port', "$Port") }
    if ($Mode -eq 'test') { $clientArgs += '--test' }
    & $taskPython @clientArgs
}
exit $LASTEXITCODE
