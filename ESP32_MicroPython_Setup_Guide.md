# ESP32 MicroPython 開發環境建置手冊（VS Code + uv）

本手冊說明如何在電腦端使用 **VS Code** 與 **uv** 建立 ESP32 MicroPython 開發環境，並完成韌體燒錄、語法提示、範例程式與部署流程。

> 適用對象：想用 ESP32 + MicroPython 開發，並希望在 VS Code 裡有較好的補全、檢查與檔案部署流程的人。

---

## 1. 準備工作

### 硬體

- ESP32 開發板
- 支援資料傳輸的 USB 線
- 可用的 USB 轉序列埠驅動程式（部分開發板需要 CP210x 或 CH340 驅動）

### 軟體

- [VS Code](https://code.visualstudio.com/)
- [uv](https://docs.astral.sh/uv/)
- Python 3
- ESP32 對應的 MicroPython 韌體：到 [MicroPython ESP32 download page](https://micropython.org/download/esp32/) 下載適合開發板的 `.bin` 檔

---

## 2. 建立本機開發環境

在你想放專案的位置開啟終端機：

```bash
mkdir my-esp32-project
cd my-esp32-project
uv venv
```

啟動虛擬環境：

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

安裝本機開發工具與 ESP32 型別提示：

```bash
uv pip install esptool mpremote micropython-esp32-stubs
```

這些套件的用途：

- `esptool`：清除與燒錄 ESP32 flash
- `mpremote`：與 MicroPython 裝置互動、執行程式、複製檔案
- `micropython-esp32-stubs`：讓 VS Code / Pylance 能辨識 `machine`、`network`、`esp32` 等模組

---

## 3. 燒錄 MicroPython 韌體

先確認 ESP32 的序列埠名稱：

- Windows 常見格式：`COM3`、`COM4`
- macOS 常見格式：`/dev/cu.usbserial-*` 或 `/dev/cu.usbmodem*`
- Linux 常見格式：`/dev/ttyUSB0` 或 `/dev/ttyACM0`

清除 flash：

```bash
esptool.py --chip esp32 --port <PORT> erase_flash
```

如果你的環境找不到 `esptool.py`，可改用：

```bash
esptool --chip esp32 --port <PORT> erase_flash
```

燒錄韌體：

```bash
esptool.py --chip esp32 --port <PORT> --baud 460800 write_flash -z 0x1000 <FIRMWARE>.bin
```

若燒錄到一半失敗，先把 baud rate 降低再試：

```bash
esptool.py --chip esp32 --port <PORT> --baud 115200 write_flash -z 0x1000 <FIRMWARE>.bin
```

---

## 4. VS Code 設定

### 必裝

- Python（Microsoft）
- Pylance（通常會隨 Python 擴充套件安裝）

### MicroPython 操作方式

VS Code Marketplace 有多個 MicroPython 相關擴充套件，功能和維護狀態會變動。建議選擇仍在維護、且明確支援 ESP32 / `mpremote` / 檔案上傳的擴充套件，例如：

- MicroPython Workbench
- MicroPython Studio
- MPRemote

如果你偏好完全用終端機，也可以只用 `mpremote`，不一定需要額外的 MicroPython VS Code 擴充套件。

### 選取 Python 直譯器

在 VS Code 中按：

```text
Ctrl + Shift + P -> Python: Select Interpreter
```

選擇專案裡的 `.venv`。

### 建議的 `.vscode/settings.json`

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.extraPaths": [
    ".venv/Lib/site-packages"
  ]
}
```

macOS / Linux 可將 `python.defaultInterpreterPath` 改成：

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

---

## 5. 建立範例程式

新增 `main.py`：

```python
import machine
import time


led = machine.Pin(2, machine.Pin.OUT)

while True:
    led.value(not led.value())
    time.sleep(1)
```

> 注意：很多 ESP32 開發板的板載 LED 是 GPIO 2，但不是全部。如果 LED 沒反應，請查你的開發板腳位圖。

---

## 6. 用 mpremote 執行與部署

確認裝置連線：

```bash
mpremote connect <PORT>
```

執行本機檔案，但不寫入 ESP32：

```bash
mpremote connect <PORT> run main.py
```

複製 `main.py` 到 ESP32，讓它開機自動執行：

```bash
mpremote connect <PORT> cp main.py :main.py
```

重新啟動裝置：

```bash
mpremote connect <PORT> reset
```

進入 REPL：

```bash
mpremote connect <PORT> repl
```

---

## 7. 裝置端函式庫管理

電腦端開發工具用 `uv pip install` 管理；真正要放到 ESP32 上執行的 MicroPython 函式庫，通常用 `mip` 或 `mpremote mip` 安裝。

在 ESP32 已連上 Wi-Fi 的情況下，可於裝置端 REPL 執行：

```python
import mip

mip.install("github:micropython/micropython-lib/python-ecosystem/ssd1306")
```

也可從電腦端透過 `mpremote` 安裝：

```bash
mpremote connect <PORT> mip install github:micropython/micropython-lib/python-ecosystem/ssd1306
```

---

## 8. 常見問題

### `import machine` 在 VS Code 顯示紅線

確認已安裝 stubs，且 VS Code 選到專案的 `.venv`：

```bash
uv pip install micropython-esp32-stubs
```

### 找不到 ESP32 序列埠

- 換一條支援資料傳輸的 USB 線
- 安裝開發板需要的 USB 轉序列埠驅動
- Windows 可到「裝置管理員」查看 COM port
- macOS / Linux 可用 `ls /dev/cu.*` 或 `ls /dev/tty*` 查找

### 燒錄失敗

- 按住開發板上的 `BOOT` 鍵再執行燒錄
- 降低 baud rate，例如 `--baud 115200`
- 換 USB 線或 USB 埠
- 確認下載的韌體符合你的 ESP32 型號

### 程式上傳後沒有自動執行

- 檔名必須是 `main.py`
- 可先進 REPL 看錯誤訊息：

```bash
mpremote connect <PORT> repl
```

---

## 9. 參考來源

- MicroPython ESP32 韌體與安裝說明：https://micropython.org/download/esp32/
- esptool 官方文件：https://docs.espressif.com/projects/esptool/
- uv 官方文件：https://docs.astral.sh/uv/
- VS Code Python extension：https://marketplace.visualstudio.com/items?itemName=ms-python.python
