# Corrige driver SQLite no DBeaver (Windows): DLL + JDBC 3.44.1.0 (mais estável com Java 21+)
$ErrorActionPreference = "Stop"
$tmp = "C:\Users\HOME\DBeaver\sqlite-tmp"
$native344 = "C:\Users\HOME\DBeaver\sqlite-native-344"
$driversDir = "$env:APPDATA\DBeaverData\drivers\maven\maven-central\org.xerial"
$jar344Local = "C:\Users\HOME\DBeaver\drivers\sqlite-jdbc-3.44.1.0.jar"
$jar344Url = "https://repo1.maven.org/maven2/org/xerial/sqlite-jdbc/3.44.1.0/sqlite-jdbc-3.44.1.0.jar"

New-Item -ItemType Directory -Force -Path $tmp, $native344, $driversDir, (Split-Path $jar344Local) | Out-Null

if (-not (Test-Path $jar344Local)) {
    Write-Host "Baixando sqlite-jdbc 3.44.1.0..."
    Invoke-WebRequest -Uri $jar344Url -OutFile $jar344Local -UseBasicParsing
}
Copy-Item $jar344Local (Join-Path $driversDir "sqlite-jdbc-3.44.1.0.jar") -Force

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($jar344Local)
try {
    $entry = $zip.Entries | Where-Object { $_.FullName -eq "org/sqlite/native/Windows/x86_64/sqlitejdbc.dll" }
    if (-not $entry) { throw "DLL nao encontrada no jar" }
    $dest = Join-Path $native344 "org\sqlite\native\Windows\x86_64\sqlitejdbc.dll"
    New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
    [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $dest, $true)
    Unblock-File $dest -ErrorAction SilentlyContinue
} finally { $zip.Dispose() }

Copy-Item (Join-Path $native344 "org\sqlite\native\Windows\x86_64\sqlitejdbc.dll") (Join-Path $tmp "sqlitejdbc.dll") -Force
Unblock-File (Join-Path $tmp "sqlitejdbc.dll") -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "OK. Proximos passos:"
Write-Host "  1. Feche o DBeaver por completo."
Write-Host "  2. Abra de novo e teste SQLite Path:"
Write-Host "     C:\Users\HOME\OneDrive\Desktop\Game_Valte\GameVault\db.sqlite3"
Write-Host "  3. Se pedir driver, use SQLite com biblioteca 3.44.1.0 (ja copiada)."
