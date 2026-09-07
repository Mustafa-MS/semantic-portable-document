$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot

function Assert-True([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}

$schemaDirectory = Join-Path $repo 'schemas'
$resultSchema = Join-Path $repo 'validation\conformance-result-0.1.1.schema.json'
$requiredFixtureNames = @{
    valid = @('minimal-base','multi-spine','arabic','mixed-bidi','table','figure-svg','mathml','annotations','mapped','sealed','semantic-only-sealed','fixed-without-mapping','mapping-with-current-fixed','same-semantic-different-revision-id','semantic-change-new-revision','lineage-scoped-annotation','revision-scoped-annotation','accessible')
    invalid = @('duplicate-node-id','missing-document-id','missing-revision-id','bad-resource-hash','unlisted-normative-resource','javascript','event-handler','external-required-font','external-required-css','external-required-image','path-traversal','duplicate-normalized-path','invalid-xhtml','missing-root-direction','missing-root-language','invalid-table-semantics','visual-order-arabic-source','mapping-wrong-revision','mapping-wrong-rendition','mapping-invalid-page','mapping-invalid-range','mapping-invalid-geometry','stale-fixed-rendition','sealed-after-semantic-modification','mutation-semantic','mutation-css','mutation-asset','mutation-mapping','mutation-fixed','sealed-after-annotation-modification','mapping-with-stale-fixed','unlisted-non-normative-resource','multiple-rootfiles','descriptor-discovery-missing','descriptor-discovery-conflict','capability-status-not-user-controlled','partial-mapping-reason','not-visible-reason')
    edge = @('empty-section','very-long-paragraph','deep-lists','table-spanning-pages','node-not-visible','partial-mapping','unsupported-mapping','emoji-range','combining-character-range','rtl-range','cjk-vertical','css-change-stales-fixed','font-change-stales-fixed')
}

$requirementIds = [System.Collections.Generic.HashSet[string]]::new()
$requiredFixtureNames.invalid += 'cross-spine-duplicate-node-id'

function Remove-VerifiedTestTemp([string]$Target) {
    $resolvedTarget = [System.IO.Path]::GetFullPath($Target)
    $tempRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath()).TrimEnd('\') + '\'
    $leaf = [System.IO.Path]::GetFileName($resolvedTarget)
    Assert-True ($resolvedTarget.StartsWith($tempRoot, [System.StringComparison]::OrdinalIgnoreCase) -and $leaf -match '^spd-(verify|invalid)-[0-9a-f]{32}$') 'Unsafe test temporary directory cleanup target.'
    if (Test-Path -LiteralPath $resolvedTarget) { Remove-Item -LiteralPath $resolvedTarget -Recurse -Force }
}
Get-Content (Join-Path $repo 'spec\requirements.yaml') | ForEach-Object {
    if ($_ -match 'id: (SPD-[A-Z0-9]+-[0-9]{3})') { [void]$requirementIds.Add($Matches[1]) }
}
Assert-True ($requirementIds.Count -eq 118) "Expected 118 registry requirements, got $($requirementIds.Count)."

Get-ChildItem $schemaDirectory -Filter '*.json' | ForEach-Object {
    Get-Content -Raw $_.FullName | ConvertFrom-Json | Out-Null
}

foreach ($category in $requiredFixtureNames.Keys) {
    foreach ($name in $requiredFixtureNames[$category]) {
        $folder = Join-Path $repo "tests\$category\$name"
        Assert-True (Test-Path -LiteralPath $folder -PathType Container) "Missing fixture $category/$name."
        foreach ($file in @('README.md','expected.json','document.epub')) {
            Assert-True (Test-Path -LiteralPath (Join-Path $folder $file) -PathType Leaf) "Missing $category/$name/$file."
        }
        $expectedPath = Join-Path $folder 'expected.json'
        Assert-True (Test-Json -LiteralPath $expectedPath -SchemaFile $resultSchema) "Expected result schema failure: $category/$name."
        $expected = Get-Content -Raw $expectedPath | ConvertFrom-Json
        if ($category -eq 'invalid') { Assert-True ($expected.violations.Count -gt 0) "Invalid fixture must expect at least one violation: $name." }
        else { Assert-True ($expected.base -eq 'PASS') "$category fixture must expect Base PASS: $name." }
        foreach ($violation in $expected.violations) {
            Assert-True ($requirementIds.Contains([string]$violation.requirement)) "Unknown requirement $($violation.requirement) in $category/$name."
        }
    }
}

foreach ($category in @('valid','edge')) {
    Get-ChildItem (Join-Path $repo "tests\$category") -Directory | ForEach-Object {
        $package = Join-Path $_.FullName 'document.epub'
        $archive = [System.IO.Compression.ZipFile]::OpenRead($package)
        try {
            Assert-True ($archive.Entries[0].FullName -eq 'mimetype') "mimetype is not first in $category/$($_.Name)."
            Assert-True ($archive.Entries[0].CompressedLength -eq $archive.Entries[0].Length) "mimetype is compressed in $category/$($_.Name)."
            $archiveNames = @($archive.Entries | ForEach-Object { $_.FullName })
        } finally { $archive.Dispose() }

        $temp = Join-Path ([System.IO.Path]::GetTempPath()) ("spd-verify-" + [guid]::NewGuid().ToString('N'))
        try {
            Expand-Archive -LiteralPath $package -DestinationPath $temp
            $pairs = @(
                @('META-INF\spd\document-state.json','document-state.schema.json'),
                @('META-INF\spd\inventory.json','resource-inventory.schema.json'),
                @('META-INF\spd\state.json','state.schema.json')
            )
            if (Test-Path (Join-Path $temp 'META-INF\spd\mapping.json')) { $pairs += ,@('META-INF\spd\mapping.json','mapping.schema.json') }
            foreach ($pair in $pairs) {
                Assert-True (Test-Json -LiteralPath (Join-Path $temp $pair[0]) -SchemaFile (Join-Path $schemaDirectory $pair[1])) "Schema failure for $category/$($_.Name)/$($pair[0])."
            }
            $inventory = Get-Content -Raw (Join-Path $temp 'META-INF\spd\inventory.json') | ConvertFrom-Json
            $listedNames = @($inventory.resources | ForEach-Object { [string]$_.path })
            $unlisted = @($archiveNames | Where-Object { $_ -notin $listedNames -and $_ -notin @('META-INF/spd/inventory.json','META-INF/spd/state.json') })
            Assert-True ($unlisted.Count -eq 0) "Unlisted package entries in $category/$($_.Name): $($unlisted -join ', ')."
            foreach ($item in $inventory.resources) {
                $file = Join-Path $temp ([string]$item.path -replace '/', '\')
                Assert-True (Test-Path -LiteralPath $file -PathType Leaf) "Inventory path missing in $category/$($_.Name): $($item.path)."
                $length = (Get-Item -LiteralPath $file).Length
                $hash = 'sha256:' + (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant()
                Assert-True ($length -eq $item.byteLength) "Length mismatch in $category/$($_.Name): $($item.path)."
                Assert-True ($hash -eq $item.sha256) "Hash mismatch in $category/$($_.Name): $($item.path)."
            }
            $state = Get-Content -Raw (Join-Path $temp 'META-INF\spd\state.json') | ConvertFrom-Json
            $inventoryHash = 'sha256:' + (Get-FileHash -LiteralPath (Join-Path $temp 'META-INF\spd\inventory.json') -Algorithm SHA256).Hash.ToLowerInvariant()
            Assert-True ($state.inventory.sha256 -eq $inventoryHash) "State inventory binding mismatch in $category/$($_.Name)."
            if (Test-Path (Join-Path $temp 'EPUB\annotations.json')) {
                $selector = (Get-Content -Raw (Join-Path $temp 'EPUB\annotations.json') | ConvertFrom-Json).target.selector
                $selectorJson = $selector | ConvertTo-Json -Depth 20
                Assert-True (Test-Json -Json $selectorJson -SchemaFile (Join-Path $schemaDirectory 'annotation-extension.schema.json')) "Annotation selector schema failure."
            }
        } finally {
            Remove-VerifiedTestTemp $temp
        }
    }
}

# Prove the intentionally schema-malformed identity fixtures fail their schemas.
foreach ($name in @('missing-document-id','missing-revision-id')) {
    $temp = Join-Path ([System.IO.Path]::GetTempPath()) ("spd-invalid-" + [guid]::NewGuid().ToString('N'))
    try {
        Expand-Archive -LiteralPath (Join-Path $repo "tests\invalid\$name\document.epub") -DestinationPath $temp
        $valid = Test-Json -LiteralPath (Join-Path $temp 'META-INF\spd\document-state.json') -SchemaFile (Join-Path $schemaDirectory 'document-state.schema.json') -ErrorAction SilentlyContinue
        Assert-True (-not $valid) "$name unexpectedly passed document-state schema."
    } finally {
        Remove-VerifiedTestTemp $temp
    }
}

$validCount = (Get-ChildItem (Join-Path $repo 'tests\valid') -Directory).Count
$invalidCount = (Get-ChildItem (Join-Path $repo 'tests\invalid') -Directory).Count
$edgeCount = (Get-ChildItem (Join-Path $repo 'tests\edge') -Directory).Count
Write-Output "Conformance model verification passed: $($requirementIds.Count) requirements; $validCount valid, $invalidCount invalid, $edgeCount edge fixtures."
