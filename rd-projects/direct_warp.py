#!/usr/bin/env python3
"""
DIRECT WARP EXECUTION - INSTANT SOLUTION
Just generates email, copies to clipboard, opens browser
NO GUI - DIRECT EXECUTION

Created by: TAQWIN Emergency Response Team
"""

import time
import random
import requests
import pyperclip
import webbrowser
from datetime import datetime

def generate_email():
    """Generate temporary email"""
    try:
        # Try 1secmail API
        response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1', timeout=10)
        if response.status_code == 200:
            emails = response.json()
            if emails:
                email = emails[0]
                pyperclip.copy(email)
                return email
    except:
        pass
    
    # Fallback method
    timestamp = int(time.time())
    random_num = random.randint(10000, 99999)
    domains = ['1secmail.com', 'esiix.com', 'xojxe.com', 'yoggm.com']
    domain = random.choice(domains)
    
    email = f"warp{timestamp}{random_num}@{domain}"
    pyperclip.copy(email)
    return email

def check_verification_email(email):
    """Check for verification email"""
    if not email or '@' not in email:
        return None
        
    try:
        login, domain = email.split('@')
        url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            messages = response.json()
            
            for message in messages:
                subject = message.get('subject', '').lower()
                if 'warp' in subject or 'verify' in subject or 'confirm' in subject:
                    # Get full message
                    msg_id = message.get('id')
                    msg_url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}'
                    
                    msg_response = requests.get(msg_url, timeout=10)
                    if msg_response.status_code == 200:
                        msg_data = msg_response.json()
                        body = msg_data.get('body', '')
                        
                        # Find verification link
                        if 'app.warp.dev' in body:
                            start = body.find('https://app.warp.dev')
                            if start == -1:
                                start = body.find('http://app.warp.dev')
                            
                            if start != -1:
                                end = start
                                while end < len(body) and body[end] not in [' ', '\n', '\t', '"', "'", ')', ']', '<']:
                                    end += 1
                                
                                link = body[start:end].strip()
                                if len(link) > 15:
                                    pyperclip.copy(link)
                                    return link
    except Exception as e:
        print(f"Error checking email: {e}")
    
    return None

def main():
    """Direct execution"""
    print("🚀 DIRECT WARP EXECUTION - INSTANT SOLUTION")
    print("=" * 50)
    
    # Step 1: Generate email
    print("📧 Generating temporary email...")
    email = generate_email()
    
    if email:
        print(f"✅ Generated email: {email}")
        print("📋 Email copied to clipboard!")
        
        # Step 2: Open Warp
        print("🌐 Opening Warp login page...")
        webbrowser.open('https://app.warp.dev/login')
        
        print("\n" + "="*60)
        print("🎯 MANUAL STEP REQUIRED:")
        print(f"📧 Email: {email}")
        print("📋 Email is copied to clipboard")
        print("🌐 Warp login page is opening in browser")
        print("\n📝 NEXT STEPS:")
        print("1. Go to the browser window that just opened")
        print("2. Paste the email (Ctrl+V) into the Warp login form")
        print("3. Click Submit/Continue")
        print("4. Come back here and press Enter to check for verification email")
        print("="*60)
        
        # Wait for user to complete manual step
        input("\n🔄 Press Enter after you've submitted the email in Warp...")
        
        # Step 3: Check for verification email
        print("\n📬 Checking for verification email...")
        
        for attempt in range(1, 11):  # Try 10 times
            print(f"🔍 Attempt {attempt}/10: Checking inbox...")
            
            verification_link = check_verification_email(email)
            
            if verification_link:
                print(f"🎉 SUCCESS! Verification email found!")
                print(f"🔗 Verification link: {verification_link}")
                print("📋 Link copied to clipboard!")
                
                # Open verification link
                print("🌐 Opening verification link...")
                webbrowser.open(verification_link)
                
                print("\n" + "="*60)
                print("🎉 WARP ACCESS COMPLETE!")
                print("✅ Email generated and submitted")
                print("✅ Verification email found")
                print("✅ Verification link opened")
                print("✅ You should now have access to Warp!")
                print("="*60)
                
                return True
            else:
                print(f"📬 No verification email yet (attempt {attempt}/10)")
                if attempt < 10:
                    print("⏳ Waiting 15 seconds before next check...")
                    time.sleep(15)
        
        print("❌ No verification email received after 10 attempts")
        print("💡 Make sure you submitted the email in Warp first")
        
    else:
        print("❌ Failed to generate email")
        return False
    
    return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to exit...")
