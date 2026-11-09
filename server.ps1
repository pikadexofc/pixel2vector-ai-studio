$Port = 3020
$Prefix = "http://localhost:$Port/"
$Root = "e:\Antigravity main\Setting up pc\pixel2vector-ai-studio"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($Prefix)
$listener.Start()

Write-Output ">>> Pixel2Vector AI Studio running at $Prefix"

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        $path = $request.Url.AbsolutePath
        if ($path -eq "/" -or $path -eq "/index.html") {
            $htmlPath = Join-Path $Root "index.html"
            $bytes = [System.IO.File]::ReadAllBytes($htmlPath)
            $response.ContentType = "text/html; charset=utf-8"
            $response.ContentLength64 = $bytes.Length
            $response.OutputStream.Write($bytes, 0, $bytes.Length)
        } elseif ($path -eq "/api/health") {
            $json = '{"status":"UP","service":"Pixel2Vector AI Studio","author":"Pickko","version":"1.0.0"}'
            $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
            $response.ContentType = "application/json"
            $response.ContentLength64 = $bytes.Length
            $response.OutputStream.Write($bytes, 0, $bytes.Length)
        } else {
            $localFile = Join-Path $Root $path.TrimStart('/')
            if ([System.IO.File]::Exists($localFile)) {
                $bytes = [System.IO.File]::ReadAllBytes($localFile)
                $response.ContentLength64 = $bytes.Length
                $response.OutputStream.Write($bytes, 0, $bytes.Length)
            } else {
                $response.StatusCode = 404
            }
        }
        $response.Close()
    } catch {}
}
