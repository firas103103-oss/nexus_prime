# PlatformIO — إعداد محلي وسحابي

## محلياً (Linux)

### 1. التثبيت

```bash
# عبر pipx (مُفضّل — إصدار حديث)
pipx install platformio
pipx ensurepath   # إضافة ~/.local/bin إلى PATH

# أو عبر apt (قد يكون قديماً)
sudo apt install platformio
```

### 2. التحقق

```bash
pio --version   # PlatformIO Core 6.x
```

### 3. صلاحيات Serial (ESP32 عبر USB)

```bash
sudo usermod -aG dialout $USER
# ثم تسجيل خروج ودخول أو: newgrp dialout
```

### 4. البناء والرفع

```bash
cd xbio-unified/firmware

# OMEGA WiFi (إنتاج)
pio run -e esp32s3_omega_wifi

# First Breath (Signature X)
pio run -e esp32s3_first_breath

# رفع إلى ESP32
pio run -e esp32s3_omega_wifi -t upload
```

---

## سحابياً (GitHub Actions / CI)

استخدم `platformio/action-platformio` أو التثبيت اليدوي:

```yaml
- name: Install PlatformIO
  run: pip install platformio

- name: Build X-BIO firmware
  run: |
    cd xbio-unified/firmware
    pio run -e esp32s3_omega_wifi
    pio run -e esp32s3_first_breath
```

أو عبر الـ action:

```yaml
- uses: platformio/action-platformio@v1
  with:
    platformio_config_path: xbio-unified/firmware/platformio.ini
```

---

## Envs المتاحة

| Env | الوصف |
|-----|-------|
| `esp32s3_omega` | أساسي (USB CDC) |
| `esp32s3_omega_wifi` | OMEGA مع WiFi |
| `esp32s3_first_breath` | First Breath — Signature X |
