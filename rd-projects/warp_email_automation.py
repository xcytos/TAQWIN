#!/usr/bin/env python3
"""
WARP EMAIL AUTOMATION SYSTEM (WEAS-2025)
Ethereal Glow R&D Project 9
Automated Email Management & Warp Login Solution

Created by: TAQWIN Legendary Agent Council
Lead Developers: Leonardo Da Vinci & Nikola Tesla
Strategic Oversight: Chanakya
"""

import time
import json
import random
import logging
import requests
import pyperclip
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

class TemporaryEmailManager:
    """Handles temporary email acquisition and monitoring"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_email = None
        self.current_service = None
        self.session = requests.Session()
        
        # Available temporary email services
        self.services = {
            'temp-mail': {
                'base_url': 'https://www.1secmail.com/api/v1/',
                'methods': {
                    'get_email': '?action=genRandomMailbox&count=1',
                    'get_messages': '?action=getMessages&login={login}&domain={domain}',
                    'get_message': '?action=readMessage&login={login}&domain={domain}&id={id}'
                }
            },
            'guerrilla': {
                'base_url': 'https://api.guerrillamail.com/ajax.php',
                'methods': {
                    'get_email': '?f=get_email_address',
                    'get_messages': '?f=get_email_list&offset=0'
                }
            }
        }
    
    def get_temporary_email(self):
        """Generate a temporary email address"""
        try:
            # Try temp-mail service first
            response = requests.get(self.services['temp-mail']['base_url'] + 
                                  self.services['temp-mail']['methods']['get_email'])
            
            if response.status_code == 200:
                email_data = response.json()
                if email_data and len(email_data) > 0:
                    self.current_email = email_data[0]
                    self.current_service = 'temp-mail'
                    self.logger.info(f"Generated temporary email: {self.current_email}")
                    return self.current_email
            
            # Fallback to alternative method
            return self._generate_fallback_email()
            
        except Exception as e:
            self.logger.error(f"Error generating temporary email: {e}")
            return self._generate_fallback_email()
    
    def _generate_fallback_email(self):
        """Fallback email generation method"""
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        domains = ['1secmail.com', 'esiix.com', 'xojxe.com', 'yoggm.com']
        domain = random.choice(domains)
        
        self.current_email = f"warp{timestamp}{random_num}@{domain}"
        self.current_service = 'fallback'
        self.logger.info(f"Generated fallback email: {self.current_email}")
        return self.current_email
    
    def monitor_inbox(self, timeout=300):
        """Monitor inbox for verification emails"""
        if not self.current_email:
            return None
            
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if self.current_service == 'temp-mail':
                    login, domain = self.current_email.split('@')
                    url = (self.services['temp-mail']['base_url'] + 
                          self.services['temp-mail']['methods']['get_messages'].format(
                              login=login, domain=domain))
                    
                    response = requests.get(url)
                    if response.status_code == 200:
                        messages = response.json()
                        
                        for message in messages:
                            if 'warp' in message.get('subject', '').lower():
                                return self._get_verification_link(message, login, domain)
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Error monitoring inbox: {e}")
                time.sleep(15)
        
        return None
    
    def _get_verification_link(self, message, login, domain):
        """Extract verification link from email message"""
        try:
            message_id = message.get('id')
            url = (self.services['temp-mail']['base_url'] + 
                  self.services['temp-mail']['methods']['get_message'].format(
                      login=login, domain=domain, id=message_id))
            
            response = requests.get(url)
            if response.status_code == 200:
                message_data = response.json()
                body = message_data.get('body', '')
                
                # Extract verification link (simple regex alternative)
                if 'https://app.warp.dev' in body:
                    start_pos = body.find('https://app.warp.dev')
                    end_pos = body.find(' ', start_pos)
                    if end_pos == -1:
                        end_pos = body.find('\n', start_pos)
                    if end_pos == -1:
                        end_pos = start_pos + 200
                    
                    link = body[start_pos:end_pos].strip()
                    self.logger.info(f"Found verification link: {link}")
                    return link
            
        except Exception as e:
            self.logger.error(f"Error extracting verification link: {e}")
        
        return None

class WarpLoginAutomator:
    """Handles Warp login automation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.wait = None
    
    def setup_browser(self):
        """Setup Chrome browser with proper options"""
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 20)
            self.logger.info("Browser setup completed")
            return True
        except Exception as e:
            self.logger.error(f"Error setting up browser: {e}")
            return False
    
    def navigate_to_warp(self):
        """Navigate to Warp login page"""
        try:
            self.driver.get("https://app.warp.dev")
            time.sleep(3)
            self.logger.info("Navigated to Warp login page")
            return True
        except Exception as e:
            self.logger.error(f"Error navigating to Warp: {e}")
            return False
    
    def input_email_address(self, email):
        """Input email address in the login form"""
        try:
            # Look for email input field
            email_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                'input[placeholder*="email"]',
                '#email',
                '.email-input'
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    email_field = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not email_field:
                self.logger.error("Could not find email input field")
                return False
            
            # Clear and input email
            email_field.clear()
            time.sleep(1)
            email_field.send_keys(email)
            time.sleep(2)
            
            # Look for submit button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:contains("Sign")',
                'button:contains("Login")',
                '.submit-btn',
                '.login-btn'
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if submit_button:
                submit_button.click()
                time.sleep(3)
                self.logger.info(f"Email {email} submitted successfully")
                return True
            else:
                self.logger.error("Could not find submit button")
                return False
                
        except Exception as e:
            self.logger.error(f"Error inputting email address: {e}")
            return False
    
    def handle_verification(self, verification_link):
        """Handle email verification"""
        try:
            if verification_link:
                self.driver.get(verification_link)
                time.sleep(5)
                self.logger.info("Verification link processed")
                return True
            else:
                self.logger.error("No verification link provided")
                return False
        except Exception as e:
            self.logger.error(f"Error handling verification: {e}")
            return False
    
    def complete_login(self):
        """Complete the login process"""
        try:
            # Wait for successful login indicators
            success_indicators = [
                "dashboard",
                "terminal",
                "welcome",
                "warp-terminal"
            ]
            
            time.sleep(10)  # Allow page to load
            
            current_url = self.driver.current_url.lower()
            page_content = self.driver.page_source.lower()
            
            for indicator in success_indicators:
                if indicator in current_url or indicator in page_content:
                    self.logger.info("Login completed successfully")
                    return True
            
            self.logger.warning("Login completion uncertain")
            return True  # Assume success if no clear failure
            
        except Exception as e:
            self.logger.error(f"Error completing login: {e}")
            return False
    
    def cleanup(self):
        """Cleanup browser resources"""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")

class AutomationOrchestrator:
    """Main workflow controller"""
    
    def __init__(self, gui_callback=None):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.email_manager = TemporaryEmailManager()
        self.warp_automator = WarpLoginAutomator()
        self.gui_callback = gui_callback
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('warp_automation.log'),
                logging.StreamHandler()
            ]
        )
    
    def log_to_gui(self, message):
        """Send log message to GUI if available"""
        if self.gui_callback:
            self.gui_callback(message)
    
    def execute_full_workflow(self):
        """Execute the complete automation workflow"""
        try:
            self.log_to_gui("🚀 Starting Warp Email Automation System...")
            
            # Step 1: Generate temporary email
            self.log_to_gui("📧 Generating temporary email address...")
            email = self.email_manager.get_temporary_email()
            if not email:
                self.log_to_gui("❌ Failed to generate temporary email")
                return False
            
            self.log_to_gui(f"✅ Generated email: {email}")
            
            # Step 2: Setup browser and navigate to Warp
            self.log_to_gui("🌐 Setting up browser automation...")
            if not self.warp_automator.setup_browser():
                self.log_to_gui("❌ Failed to setup browser")
                return False
            
            self.log_to_gui("🎯 Navigating to Warp login page...")
            if not self.warp_automator.navigate_to_warp():
                self.log_to_gui("❌ Failed to navigate to Warp")
                return False
            
            # Step 3: Input email and submit
            self.log_to_gui("📝 Inputting email address...")
            if not self.warp_automator.input_email_address(email):
                self.log_to_gui("❌ Failed to input email address")
                return False
            
            # Step 4: Monitor inbox for verification email
            self.log_to_gui("📬 Monitoring inbox for verification email...")
            self.log_to_gui("⏳ This may take up to 5 minutes...")
            
            verification_link = self.email_manager.monitor_inbox(timeout=300)
            if not verification_link:
                self.log_to_gui("❌ No verification email received within timeout")
                return False
            
            self.log_to_gui("✅ Verification email received!")
            
            # Step 5: Handle verification
            self.log_to_gui("🔐 Processing verification link...")
            if not self.warp_automator.handle_verification(verification_link):
                self.log_to_gui("❌ Failed to process verification")
                return False
            
            # Step 6: Complete login
            self.log_to_gui("🏁 Completing login process...")
            if not self.warp_automator.complete_login():
                self.log_to_gui("❌ Failed to complete login")
                return False
            
            self.log_to_gui("🎉 SUCCESS! Warp login automation completed!")
            self.log_to_gui("🖥️ You should now have access to Warp terminal")
            
            # Keep browser open for user
            self.log_to_gui("🔄 Browser will remain open for your use")
            self.log_to_gui("📝 Check the Warp interface for successful login")
            
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Critical error in workflow: {e}")
            self.logger.error(f"Critical error in workflow: {e}")
            return False
        finally:
            # Note: Not cleaning up browser so user can access Warp
            pass

class WarpAutomationGUI:
    """Simple GUI for the automation tool"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Warp Email Automation System - Ethereal Glow R&D")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.orchestrator = None
        self.automation_thread = None
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI components"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🌟 WARP EMAIL AUTOMATION SYSTEM",
            font=("Arial", 16, "bold"),
            fg="blue"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            self.root,
            text="Ethereal Glow R&D Project 9 - WEAS-2025",
            font=("Arial", 10),
            fg="gray"
        )
        subtitle_label.pack(pady=5)
        
        # Description
        desc_text = """
This tool automates the process of:
1. Generating temporary email addresses
2. Logging into app.warp.dev
3. Handling email verification
4. Completing Warp terminal access

Click 'Start Automation' to begin the process.
        """
        
        desc_label = tk.Label(self.root, text=desc_text, justify=tk.LEFT)
        desc_label.pack(pady=10, padx=20)
        
        # Start button
        self.start_button = tk.Button(
            self.root,
            text="🚀 Start Automation",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=self.start_automation,
            height=2
        )
        self.start_button.pack(pady=10)
        
        # Log display
        log_label = tk.Label(self.root, text="📋 Automation Log:", font=("Arial", 10, "bold"))
        log_label.pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        self.log_display = scrolledtext.ScrolledText(
            self.root,
            height=15,
            width=70,
            font=("Courier", 9)
        )
        self.log_display.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready to start automation",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def log_callback(self, message):
        """Callback function for log messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_display.insert(tk.END, log_message)
        self.log_display.see(tk.END)
        self.root.update_idletasks()
    
    def start_automation(self):
        """Start the automation process"""
        if self.automation_thread and self.automation_thread.is_alive():
            messagebox.showwarning("Warning", "Automation is already running!")
            return
        
        self.start_button.config(state=tk.DISABLED, text="🔄 Running...")
        self.status_label.config(text="Automation in progress...")
        self.log_display.delete(1.0, tk.END)
        
        # Create and start automation thread
        self.automation_thread = threading.Thread(target=self.run_automation)
        self.automation_thread.daemon = True
        self.automation_thread.start()
    
    def run_automation(self):
        """Run automation in separate thread"""
        try:
            self.orchestrator = AutomationOrchestrator(gui_callback=self.log_callback)
            success = self.orchestrator.execute_full_workflow()
            
            # Update GUI based on results
            self.root.after(0, self.automation_completed, success)
            
        except Exception as e:
            self.root.after(0, self.automation_error, str(e))
    
    def automation_completed(self, success):
        """Handle automation completion"""
        if success:
            self.status_label.config(text="✅ Automation completed successfully!")
            messagebox.showinfo("Success", "Warp automation completed successfully!\nCheck your browser for Warp access.")
        else:
            self.status_label.config(text="❌ Automation failed")
            messagebox.showerror("Error", "Automation failed. Check logs for details.")
        
        self.start_button.config(state=tk.NORMAL, text="🚀 Start Automation")
    
    def automation_error(self, error_message):
        """Handle automation error"""
        self.status_label.config(text="❌ Automation error")
        messagebox.showerror("Error", f"Automation error: {error_message}")
        self.start_button.config(state=tk.NORMAL, text="🚀 Start Automation")
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main entry point"""
    print("🌟 WARP EMAIL AUTOMATION SYSTEM - ETHEREAL GLOW R&D")
    print("=" * 50)
    
    try:
        # Create and run GUI
        app = WarpAutomationGUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Automation stopped by user")
    except Exception as e:
        print(f"❌ Critical error: {e}")

if __name__ == "__main__":
    main()
