# 파워셸 GUI 패턴

## 개요

이 가이드에서는 WinForms, WPF 및 TUI(터미널 사용자 인터페이스)를 포함한 PowerShell용 GUI 개발 패턴을 다룹니다.

## WinForms 패턴

### 기본 양식 구조

```powershell
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function Show-WinFormsDialog {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "PowerShell WinForms"
    $form.Width = 400
    $form.Height = 300
    $form.StartPosition = "CenterScreen"
    
    # Add controls
    $button = New-Object System.Windows.Forms.Button
    $button.Text = "Click Me"
    $button.Location = New-Object System.Drawing.Point(150, 200)
    $button.Size = New-Object System.Drawing.Size(100, 30)
    
    $button.Add_Click({
        [System.Windows.Forms.MessageBox]::Show("Button clicked!")
    })
    
    $form.Controls.Add($button)
    
    $form.ShowDialog()
}
```

### 데이터 바인딩

```powershell
function Show-BoundData {
    # Create data source
    $data = @(
        [PSCustomObject]@{ Name = "Item 1"; Value = 100 },
        [PSCustomObject]@{ Name = "Item 2"; Value = 200 },
        [PSCustomObject]@{ Name = "Item 3"; Value = 300 }
    )
    
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Data Binding Example"
    
    # Create DataGridView
    $dataGridView = New-Object System.Windows.Forms.DataGridView
    $dataGridView.Location = New-Object System.Drawing.Point(20, 20)
    $dataGridView.Size = New-Object System.Drawing.Size(340, 200)
    $dataGridView.AutoGenerateColumns = $true
    $dataGridView.DataSource = $data
    
    $form.Controls.Add($dataGridView)
    $form.ShowDialog()
}
```

### 이벤트 처리

```powershell
function Show-EventHandling {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Event Handling"
    
    $textBox = New-Object System.Windows.Forms.TextBox
    $textBox.Location = New-Object System.Drawing.Point(20, 20)
    $textBox.Size = New-Object System.Drawing.Size(340, 20)
    
    # Text changed event
    $textBox.Add_TextChanged({
        param($sender, $e)
        Write-Host "Text changed: $($sender.Text)"
    })
    
    # Key press event
    $textBox.Add_KeyPress({
        param($sender, $e)
        if ($e.KeyChar -eq [char]13) {
            [System.Windows.Forms.MessageBox]::Show("Enter pressed")
        }
    })
    
    $form.Controls.Add($textBox)
    $form.ShowDialog()
}
```

## WPF 패턴

### XAML 기반 WPF

```powershell
$xaml = @"
<Window x:Class="MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="PowerShell WPF" Height="300" Width="400">
    <Grid>
        <Button Name="btnClick" Content="Click Me" 
                HorizontalAlignment="Center" 
                VerticalAlignment="Center"
                Width="100" Height="30"/>
    </Grid>
</Window>
"@

Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName PresentationCore

$reader = [System.Xml.XmlReader]::Create([System.IO.StringReader]::new($xaml))
$window = [System.Windows.Markup.XamlReader]::Load($reader)

# Add event handler
$btnClick = $window.FindName("btnClick")
$btnClick.Add_Click({
    [System.Windows.MessageBox]::Show("Button clicked!")
})

$window.ShowDialog()
```

### MVVM 패턴

```powershell
# ViewModel
class MyViewModel : System.ComponentModel.INotifyPropertyChanged {
    [string]$_name
    
    [string]$Name {
        get { return $this._name }
        set {
            if ($this._name -ne $value) {
                $this._name = $value
                $this.OnPropertyChanged("Name")
            }
        }
    }
    
    [System.Collections.ObjectModel.ObservableCollection[string]]$Items
    
    MyViewModel() {
        $this.Items = [System.Collections.ObjectModel.ObservableCollection[string]]::new()
        $this.Items.Add("Item 1")
        $this.Items.Add("Item 2")
    }
    
    [void]$OnPropertyChanged($propertyName) {
        if ($this.PropertyChanged -ne $null) {
            $this.PropertyChanged.Invoke($this, [System.ComponentModel.PropertyChangedEventArgs]::new($propertyName))
        }
    }
    
    event PropertyChanged($sender, $e)
    hidden [System.ComponentModel.PropertyChangedEventHandler]$PropertyChanged
}
```

### WPF의 데이터 바인딩

```powershell
$xaml = @"
<Window x:Class="MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <StackPanel>
        <TextBlock Text="Enter Name:"/>
        <TextBox Name="txtName" Height="25"/>
        <TextBlock Name="lblName" Height="25" Text="{Binding Name}"/>
    </StackPanel>
</Window>
"@

$reader = [System.Xml.XmlReader]::Create([System.IO.StringReader]::new($xaml))
$window = [System.Windows.Markup.XamlReader]::Load($reader)

# Create ViewModel
$viewModel = [MyViewModel]::new()
$window.DataContext = $viewModel

# Bind TextBox
$txtName = $window.FindName("txtName")
$txtName.SetBinding([System.Windows.Controls.TextBox]::TextProperty, "Name")

$window.ShowDialog()
```

## TUI(터미널 사용자 인터페이스) 패턴

### 기본 TUI 메뉴

```powershell
function Show-TuiMenu {
    $menuItems = @(
        @{ Label = "Option 1"; Action = { Write-Host "Selected Option 1" } },
        @{ Label = "Option 2"; Action = { Write-Host "Selected Option 2" } },
        @{ Label = "Option 3"; Action = { Write-Host "Selected Option 3" } }
    )
    
    while ($true) {
        Clear-Host
        Write-Host "=== Main Menu ===" -ForegroundColor Cyan
        Write-Host ""
        
        for ($i = 0; $i -lt $menuItems.Count; $i++) {
            Write-Host "  [$($i + 1)] $($menuItems[$i].Label)" -ForegroundColor White
        }
        
        Write-Host "  [Q] Quit" -ForegroundColor Red
        Write-Host ""
        
        $selection = Read-Host "Select option"
        
        if ($selection -eq 'q' -or $selection -eq 'Q') {
            break
        }
        
        $selectedIndex = 0
        if ([int]::TryParse($selection, [ref]$selectedIndex)) {
            $selectedIndex--
            
            if ($selectedIndex -ge 0 -and $selectedIndex -lt $menuItems.Count) {
                Clear-Host
                & $menuItems[$selectedIndex].Action
                Read-Host "Press Enter to continue"
            }
        }
    }
}
```

### TUI 테이블 표시

```powershell
function Show-TuiTable {
    $data = @(
        @{ Name = "Item 1"; Status = "Active"; Value = 100 },
        @{ Name = "Item 2"; Status = "Inactive"; Value = 200 },
        @{ Name = "Item 3"; Status = "Active"; Value = 300 }
    )
    
    Clear-Host
    Write-Host "=== Data Table ===" -ForegroundColor Cyan
    Write-Host ""
    
    $data | Format-Table -AutoSize
    
    Write-Host ""
    Read-Host "Press Enter to continue"
}
```

### TUI 진행률 표시줄

```powershell
function Show-TuiProgress {
    $totalItems = 100
    
    for ($i = 0; $i -le $totalItems; $i++) {
        $progress = ($i / $totalItems) * 100
        $filled = [Math]::Floor(50 * $progress / 100)
        $empty = 50 - $filled
        
        $bar = "█" * $filled + "░" * $empty
        
        Write-Host "`r[$bar] $progress%" -NoNewline -ForegroundColor Green
        
        Start-Sleep -Milliseconds 50
    }
    
    Write-Host "`nComplete!" -ForegroundColor Green
}
```

## 프레임워크 선택

### WinForms를 사용해야 하는 경우

**장점:**
- 구현이 간단함
- 경량
- 간단한 대화에 적합

**단점:**
- 제한된 스타일링 옵션
- 현대적이지 않음
- 제한된 데이터 바인딩

**사용 사례:**
- 간단한 입력 양식
- 유틸리티 대화상자
- 빠른 프로토타입

### WPF를 사용해야 하는 경우

**장점:**
- 현대적인 외관
- 풍부한 스타일링 옵션
- 고급 데이터 바인딩
- MVVM 패턴 지원

**단점:**
- 가파른 학습 곡선
- 구현이 더 복잡함
- WinForms보다 무겁습니다.

**사용 사례:**
- 복잡한 애플리케이션
- 데이터가 많은 인터페이스
- 전문가 수준의 GUI
- MVVM 패턴이 필요합니다.

### TUI를 사용해야 하는 경우

**장점:**
- 크로스 플랫폼 호환
- 경량
- GUI 종속성 없음
- SSH를 통해 작동

**단점:**
- 제한된 상호 작용 옵션
- 그래픽 없음
- 터미널 기반만 해당

**사용 사례:**
- 서버 관리
- SSH/원격 세션
- 명령줄 도구
- 크로스 플랫폼 호환성이 필요합니다.

## 일반적인 패턴

### 모달 대화 상자

```powershell
function Show-ModalDialog {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Modal Dialog"
    $form.ShowDialog() | Out-Null
}
```

### 비동기 작업

```powershell
function Show-Progress {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Processing..."
    
    $progressBar = New-Object System.Windows.Forms.ProgressBar
    $progressBar.Location = New-Object System.Drawing.Point(20, 50)
    $progressBar.Size = New-Object System.Drawing.Size(340, 20)
    
    $form.Controls.Add($progressBar)
    
    # Start operation in background
    $job = Start-Job -ScriptBlock {
        Start-Sleep -Seconds 5
    }
    
    # Update progress
    while ($job.State -eq 'Running') {
        $progressBar.Value += 10
        $form.Refresh()
        Start-Sleep -Milliseconds 500
    }
    
    Remove-Job $job
    $form.ShowDialog()
}
```

## 모범 사례

1. **프레임워크 선택**: 필요에 맞는 프레임워크를 선택하세요.
2. **이벤트 처리**: 적절한 이벤트 핸들러 구현
3. **오류 처리**: 사용자 상호 작용을 위한 try-catch 블록 추가
4. **응답성**: 작업 중에 UI 응답성을 유지합니다.
5. **접근성**: 접근성 기능을 고려하세요.
6. **교차 플랫폼**: 교차 플랫폼 요구 사항에는 TUI를 사용하세요.
7. **테스트**: GUI 애플리케이션을 철저히 테스트합니다.
8. **성능**: 대규모 데이터세트의 성능을 최적화합니다.

## 자원

- [WinForms 설명서](https://docs.microsoft.com/en-us/dotnet/desktop/winforms/)
- [WPF 설명서](https://docs.microsoft.com/en-us/dotnet/desktop/wpf/)
- [PowerShell GUI 예](https://github.com/pscookiemonster/GUI-Examples)