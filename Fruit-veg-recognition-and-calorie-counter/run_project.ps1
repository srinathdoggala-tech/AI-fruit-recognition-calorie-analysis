$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ModelApi = Join-Path $Root "model api\Fruit_Veg_recognition"
$WebApp = Join-Path $Root "Food_calorie_counter"
$ModelManage = Join-Path $ModelApi "manage.py"
$WebManage = Join-Path $WebApp "manage.py"

Start-Process python -WorkingDirectory $Root -WindowStyle Hidden -ArgumentList @(
    "`"$ModelManage`"",
    "runserver",
    "127.0.0.1:8010",
    "--noreload"
)

Start-Process python -WorkingDirectory $Root -WindowStyle Hidden -ArgumentList @(
    "`"$WebManage`"",
    "runserver",
    "127.0.0.1:8011",
    "--noreload"
)

Write-Host "Model API: http://127.0.0.1:8010/predict/"
Write-Host "Web app:   http://127.0.0.1:8011/"
