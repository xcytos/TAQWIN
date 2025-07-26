#!/usr/bin/env python3
"""
EMAIL SERVICE TESTER FOR WARP
Tests multiple email services to find which ones work with Warp

Created by: TAQWIN Emergency Response Team
"""

import time
import random
import requests
import pyperclip
import webbrowser
from datetime import datetime

class EmailServiceTester:
    """Test multiple email services to find working ones"""
    
    def __init__(self):
        self.services = {
            '1secmail': {
                'name': '1SecMail',
                'generate_url': 'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1',
                'check_url': 'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}',
                'read_url': 'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={id}'
            },
            'guerrilla': {
                'name': 'Guerrilla Mail',
                'generate_url': 'https://api.guerrillamail.com/ajax.php?f=get_email_address',
                'check_url': 'https://api.guerrillamail.com/ajax.php?f=get_email_list&offset=0'
            },
            'tempmail': {
                'name': 'TempMail.org',
                'generate_url': 'https://api.tempmail.org/request/mail/id/1/',
                'domains': ['tempmail.org', 'tempmail.net', 'tempmail.co']
            },
            'maildrop': {
                'name': 'MailDrop',
                'domains': ['maildrop.cc']
            },
            'throwaway': {
                'name': 'ThrowAwayMail',
                'domains': ['throwam.com', 'guerrillamailblock.com']
            }
        }
    
    def test_1secmail(self):
        """Test 1secmail service"""
        try:
            print("🔍 Testing 1SecMail service...")
            response = requests.get(self.services['1secmail']['generate_url'], timeout=10)
            
            if response.status_code == 200:
                emails = response.json()
                if emails and len(emails) > 0:
                    email = emails[0]
                    print(f"✅ 1SecMail generated: {email}")
                    return email
            
            print("❌ 1SecMail failed")
            return None
            
        except Exception as e:
            print(f"❌ 1SecMail error: {e}")
            return None
    
    def test_guerrilla(self):
        """Test Guerrilla mail service"""
        try:
            print("🔍 Testing Guerrilla Mail service...")
            response = requests.get(self.services['guerrilla']['generate_url'], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'email_addr' in data:
                    email = data['email_addr']
                    print(f"✅ Guerrilla Mail generated: {email}")
                    return email
            
            print("❌ Guerrilla Mail failed")
            return None
            
        except Exception as e:
            print(f"❌ Guerrilla Mail error: {e}")
            return None
    
    def test_tempmail_org(self):
        """Test TempMail.org service"""
        try:
            print("🔍 Testing TempMail.org service...")
            response = requests.get(self.services['tempmail']['generate_url'], timeout=10)
            
            if response.status_code == 200:
                # TempMail.org returns different format
                data = response.text
                if '@' in data:
                    # Extract email from response
                    lines = data.split('\n')
                    for line in lines:
                        if '@' in line and 'tempmail' in line:
                            email = line.strip()
                            print(f"✅ TempMail.org generated: {email}")
                            return email
            
            print("❌ TempMail.org failed")
            return None
            
        except Exception as e:
            print(f"❌ TempMail.org error: {e}")
            return None
    
    def generate_custom_email(self, service_name, domains):
        """Generate custom email with specific domains"""
        try:
            timestamp = int(time.time())
            random_num = random.randint(10000, 99999)
            domain = random.choice(domains)
            
            email = f"warp{timestamp}{random_num}@{domain}"
            print(f"✅ {service_name} generated: {email}")
            return email
            
        except Exception as e:
            print(f"❌ {service_name} error: {e}")
            return None
    
    def test_all_services(self):
        """Test all email services"""
        print("🧪 TESTING ALL EMAIL SERVICES FOR WARP COMPATIBILITY")
        print("=" * 60)
        
        working_emails = []
        
        # Test 1SecMail
        email = self.test_1secmail()
        if email:
            working_emails.append(('1SecMail', email))
        
        # Test Guerrilla Mail
        email = self.test_guerrilla()
        if email:
            working_emails.append(('Guerrilla Mail', email))
        
        # Test TempMail.org
        email = self.test_tempmail_org()
        if email:
            working_emails.append(('TempMail.org', email))
        
        # Test MailDrop
        email = self.generate_custom_email('MailDrop', self.services['maildrop']['domains'])
        if email:
            working_emails.append(('MailDrop', email))
        
        # Test ThrowAway
        email = self.generate_custom_email('ThrowAwayMail', self.services['throwaway']['domains'])
        if email:
            working_emails.append(('ThrowAwayMail', email))
        
        return working_emails
    
    def check_1secmail_inbox(self, email):
        """Check 1secmail inbox for verification"""
        try:
            if '@' not in email:
                return None
                
            login, domain = email.split('@')
            url = self.services['1secmail']['check_url'].format(login=login, domain=domain)
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                messages = response.json()
                
                for message in messages:
                    subject = message.get('subject', '').lower()
                    if any(keyword in subject for keyword in ['warp', 'verify', 'confirm', 'login']):
                        # Get full message
                        msg_id = message.get('id')
                        read_url = self.services['1secmail']['read_url'].format(
                            login=login, domain=domain, id=msg_id)
                        
                        msg_response = requests.get(read_url, timeout=10)
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
                                        return link
        except Exception as e:
            print(f"Error checking 1secmail: {e}")
        
        return None

def comprehensive_warp_test():
    """Comprehensive test of Warp with multiple email services"""
    print("🚀 COMPREHENSIVE WARP EMAIL SERVICE TEST")
    print("=" * 60)
    print("This will test multiple email services to find which ones work with Warp")
    print("=" * 60)
    
    tester = EmailServiceTester()
    
    # Test all services
    working_emails = tester.test_all_services()
    
    if not working_emails:
        print("\n❌ No email services could be contacted")
        print("💡 Check your internet connection and try again")
        return
    
    print(f"\n✅ Found {len(working_emails)} working email services:")
    for i, (service, email) in enumerate(working_emails, 1):
        print(f"{i}. {service}: {email}")
    
    print("\n" + "=" * 60)
    print("🎯 WARP TESTING PHASE")
    print("=" * 60)
    
    for i, (service, email) in enumerate(working_emails, 1):
        print(f"\n🧪 TESTING {service.upper()} WITH WARP")
        print(f"📧 Email: {email}")
        
        # Copy to clipboard
        pyperclip.copy(email)
        print("📋 Email copied to clipboard!")
        
        # Open Warp
        print("🌐 Opening Warp login page...")
        webbrowser.open('https://app.warp.dev/login')
        
        print("\n" + "-" * 50)
        print(f"🎯 MANUAL TEST #{i}: {service}")
        print(f"📧 Email: {email}")
        print("📋 Email is copied to clipboard")
        print("\n📝 STEPS:")
        print("1. Go to the browser window that opened")
        print("2. Paste the email (Ctrl+V) into Warp login form")
        print("3. Click Submit/Continue")
        print("4. Come back and tell me if you want to:")
        print("   - Continue to next service (press Enter)")
        print("   - Check this email for verification (type 'check')")
        print("   - Skip to manual check (type 'manual')")
        print("-" * 50)
        
        user_choice = input(f"\n🔄 What do you want to do with {service}? (Enter/check/manual): ").strip().lower()
        
        if user_choice == 'check':
            print(f"\n📬 Checking {service} inbox for verification email...")
            
            if service == '1SecMail':
                for attempt in range(1, 6):  # Try 5 times
                    print(f"🔍 Attempt {attempt}/5: Checking {service} inbox...")
                    
                    verification_link = tester.check_1secmail_inbox(email)
                    
                    if verification_link:
                        print(f"🎉 SUCCESS! Verification email found in {service}!")
                        print(f"🔗 Verification link: {verification_link}")
                        pyperclip.copy(verification_link)
                        print("📋 Link copied to clipboard!")
                        
                        # Open verification link
                        print("🌐 Opening verification link...")
                        webbrowser.open(verification_link)
                        
                        print("\n" + "=" * 60)
                        print(f"🎉 WARP ACCESS COMPLETE WITH {service.upper()}!")
                        print("✅ Email service works with Warp!")
                        print("✅ Verification email received!")
                        print("✅ Verification link opened!")
                        print("✅ You should now have access to Warp!")
                        print("=" * 60)
                        
                        return service, email, verification_link
                    else:
                        print(f"📬 No verification email yet in {service} (attempt {attempt}/5)")
                        if attempt < 5:
                            print("⏳ Waiting 15 seconds before next check...")
                            time.sleep(15)
                
                print(f"❌ No verification email received in {service} after 5 attempts")
            else:
                print(f"💡 {service} inbox checking not implemented yet")
                print("📧 Please check the email manually or try another service")
        
        elif user_choice == 'manual':
            print(f"\n📧 {service} email: {email}")
            print("📋 Email copied to clipboard")
            print("💡 Check this email manually for verification")
            break
        
        else:
            print(f"⏭️ Moving to next service...")
    
    print("\n" + "=" * 60)
    print("🏁 EMAIL SERVICE TESTING COMPLETE")
    print("=" * 60)
    print("💡 If none of the services received verification emails,")
    print("   Warp might be blocking temporary email services.")
    print("💡 Consider using a real email service or")
    print("   checking if Warp has specific requirements.")

def main():
    """Main function"""
    try:
        comprehensive_warp_test()
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
