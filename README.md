<p align="center">
  <img src="https://img.shields.io/badge/Status-Patched-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Language-Python-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PoC-Educational%20Use%20Only-orange?style=for-the-badge" />
  <br />
  <a href="https://x.com/Swezy_1337/status/1973420745364742645"><img src="https://img.shields.io/badge/X Post-Click here to view-white?style=for-the-badge" /></a>
</p>

<h1 align="center">⚡ Whitepages.com Vulnerability Exploit (Patched) ⚡</h1>

<p align="center">
  <strong>⚠️ Exploit by <a href="https://t.me/Swezy">@Swezy</a></strong><br>
  <em>13. September 2025</em>
</p>

---

## 🧠 Overview

This repository contains a **Proof of Concept (PoC)** for a **patched vulnerability** on [whitepages.com](https://www.whitepages.com).  
The exploit demonstrates how an attacker **could have reset user passwords** via a vulnerable endpoint, extracting detailed account data.

> ⚠️ **This exploit no longer works.**  
> It is provided **for educational and research purposes only** to study how such flaws can occur and how to prevent them.

---

## ✨ Features

- 🧰 Automates **password reset exploit flow**
- 🌐 Uses `undetected_chromedriver` and `cloudscraper` to bypass protections
- 🔐 Secure password input handling
- 📅 Beautifully formatted timestamps and account info
- 💻 Includes **GUI** and **CLI** versions
- 🧠 Detailed output with PII (personally identifiable information)

---

## ⚙️ Requirements

- Python **3.9+**
- Google Chrome installed (for `undetected_chromedriver`)

### 🧩 Python Modules
```bash
pip install undetected-chromedriver cloudscraper python-dateutil colorama secure-input customtkinter Pillow
````

---

## 🚀 Usage

### ▶️ Command-line User Interface (CUI) Version

```bash
python main.py
```

### 🖥️ Graphical User Interface (GUI) Version

```bash
python main.py
```

You'll be prompted for the target's email address and a new password.
The script will attempt the old reset flow and display all captured PII (personally identifiable information).

---

## 🧪 Example Output

```bash
Whitepages.com Vulnerability | Telegram @Swezy

[?] Enter E-Mail ➔ example@example.com
[?] Enter new Password ➔ ***********

[*] Preparing Exploit Payload...

[*] Sending Exploit Payload...
[+] Exploit Sent Successfully [202]

[✓] Reset Password URL: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

[*] Preparing Password Reset Exploit...

[*] Sending Password Reset Exploit...

[*] Account Details Found

[✓] Primary Email: example@example.com
[✓] Associated Emails:
    [-] Email: example@example.com
    [-] ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx
    [-] User ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx
    [-] Created At: 13-03-1337T13-03-37 (1337 days ago)
[✓] Password: Example
[✓] Name: Example
[✓] Full Name: Example Example Example
[✓] Associated Phone Numbers:
    [-] Phone Number: +13 37 1337 1337
    [-] ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx
    [-] User ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx
    [-] Created At: 13-03-1337T13-03-37 (1337 days ago)
[✓] Account ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx
[✓] IP Address: xxx.xxx.xxx.xxx
[✓] User Type: expired
[✓] Login Allowed: True
[✓] Membership Type: expired
[✓] Business Features Status: none
[✓] Has Business Features: False
[✓] Has Full Property Features: False
[✓] Premium Subscriber: False
[✓] Account Created at: 13-03-1337T13-03-37 (1337 days ago)
[✓] Password Changed at: 13-03-1337T13-03-37 (1337 days ago)
[✓] Subscription Ended at: 13-03-1337T13-03-37 (1337 days ago)
[✓] Payment Edited at: 13-03-1337T13-03-37 (1337 days ago)
[✓] Premium ToS Accepted at: 13-03-1337T13-03-37 (1337 days ago)
[✓] Landlord ToS Accepted at: 13-03-1337T13-03-37 (1337 days ago)
[✓] Suspended: False
[✓] Disabled: False
[✓] Mobile: False
[✓] Industry: None
[✓] Legacy Modal: False
[✓] Auto Monitor Disabled: False
[✓] PNP Beta Opt in: False

[+] Password Reset Successfully [200]
[✓] New Password: ***********

[$] Total Time Taken: 13.37s
```

---

## ⚠️ Disclaimer

> This tool is a **Proof of Concept** created **for educational and research purposes only**.
> Do **not** use this against any live systems without **explicit authorization**.
> The author is **not responsible** for any misuse or damages caused.

---

## 🧠 Educational Purpose

This repository aims to help **security researchers** and **developers** understand:

* How insecure password reset flows can be exploited
* Why proper token validation and rate limiting are critical
* How to build secure recovery systems

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 💬 Contact

- 📞 Telegram: [@Swezy](https://t.me/Swezy)
- 🐈‍⬛ GitHub: [@SwezyDev](https://github.com/SwezyDev)
- ✖️ X: [@Swezy_1337](https://x.com/Swezy_1337)

---

<p align="center">
  <em>🧠 Knowledge is power. Use it ethically. 🧠</em><br>
  <strong>© 2025 Swezy</strong>
</p>
