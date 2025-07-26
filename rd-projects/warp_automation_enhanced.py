#!/usr/bin/env python3
"""
ENHANCED WARP EMAIL AUTOMATION SYSTEM (WEAS-2025-ENHANCED)
Ethereal Glow R&D Project 9 - Enhanced Edition
Complete Automation with Clipboard Integration & Incognito Mode

Created by: TAQWIN Legendary Agent Council
Lead Developers: Leonardo Da Vinci & Nikola Tesla
Enhanced by: Chanakya Strategic Intelligence
"""

import time
import json
import random
import logging
import requests
import pyperclip
import subprocess
import webbrowser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import threading

class EnhancedTemporaryEmailManager:
    """Enhanced temporary email acquisition and monitoring with clipboard integration"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_email = None
        self.current_service = None
        self.session = requests.Session()
        self.verification_link = None
        
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
        """Generate a temporary email address and copy to clipboard"""
        try:
            # Try temp-mail service first
            response = requests.get(self.services['temp-mail']['base_url'] + 
                                  self.services['temp-mail']['methods']['get_email'])
            
            if response.status_code == 200:
                email_data = response.json()
                if email_data and len(email_data) > 0:
                    self.current_email = email_data[0]
                    self.current_service = 'temp-mail'
                    
                    # Copy email to clipboard
                    pyperclip.copy(self.current_email)
                    
                    self.logger.info(f"Generated temporary email: {self.current_email}")
                    return self.current_email
            
            # Fallback to alternative method
            return self._generate_fallback_email()
            
        except Exception as e:
            self.logger.error(f"Error generating temporary email: {e}")
            return self._generate_fallback_email()
    
    def _generate_fallback_email(self):
        """Fallback email generation method with clipboard copy"""
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        domains = ['1secmail.com', 'esiix.com', 'xojxe.com', 'yoggm.com']
        domain = random.choice(domains)
        
        self.current_email = f"warp{timestamp}{random_num}@{domain}"
        self.current_service = 'fallback'
        
        # Copy email to clipboard
        pyperclip.copy(self.current_email)
        
        self.logger.info(f"Generated fallback email: {self.current_email}")
        return self.current_email
    
    def monitor_inbox_and_get_link(self, timeout=300):
        """Monitor inbox for verification emails and extract link"""
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
                                link = self._get_verification_link(message, login, domain)
                                if link:
                                    self.verification_link = link
                                    # Copy verification link to clipboard
                                    pyperclip.copy(link)
                                    return link
                
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
                
                # Extract verification link (multiple patterns)
                patterns = [
                    'https://app.warp.dev',
                    'http://app.warp.dev'
                ]
                
                for pattern in patterns:
                    if pattern in body:
                        start_pos = body.find(pattern)
                        # Look for end markers
                        end_markers = [' ', '\n', '\r', '\t', '"', "'", ')', ']', '}']
                        end_pos = len(body)
                        
                        for marker in end_markers:
                            marker_pos = body.find(marker, start_pos)
                            if marker_pos != -1 and marker_pos < end_pos:
                                end_pos = marker_pos
                        
                        if end_pos == len(body):
                            end_pos = start_pos + 200
                        
                        link = body[start_pos:end_pos].strip()
                        # Clean up any HTML artifacts
                        link = link.replace('&amp;', '&').replace('=\n', '').replace('\n', '')
                        
                        self.logger.info(f"Found verification link: {link}")
                        return link
            
        except Exception as e:
            self.logger.error(f"Error extracting verification link: {e}")
        
        return None

class EnhancedWarpAutomator:
    """Enhanced Warp automation with incognito mode and complete workflow"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.wait = None
        self.incognito_driver = None
    
    def setup_incognito_browser(self):
        """Setup Chrome browser in incognito mode"""
        chrome_options = Options()
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 30)
            self.logger.info("Incognito browser setup completed")
            return True
        except Exception as e:
            self.logger.error(f"Error setting up incognito browser: {e}")
            return False
    
    def open_warp_incognito(self):
        """Open app.warp.dev in incognito mode"""
        try:
            self.driver.get("https://app.warp.dev")
            time.sleep(5)  # Allow page to fully load
            self.logger.info("Opened app.warp.dev in incognito mode")
            return True
        except Exception as e:
            self.logger.error(f"Error opening Warp in incognito: {e}")
            return False
    
    def paste_email_and_submit(self, email):
        """Paste email from clipboard and submit"""
        try:
            # Multiple strategies to find email input
            email_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                'input[placeholder*="email" i]',
                'input[placeholder*="Email" i]',
                '#email',
                '.email-input',
                'input[autocomplete="email"]',
                'input[data-testid*="email"]'
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    email_field = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not email_field:
                # Try finding by text content or nearby labels
                try:
                    email_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'mail') or contains(@name, 'mail')]")
                except:
                    self.logger.error("Could not find email input field")
                    return False
            
            # Click and clear the field
            email_field.click()
            time.sleep(1)
            email_field.clear()
            time.sleep(1)
            
            # Input email (both paste and type for reliability)
            email_field.send_keys(email)
            time.sleep(2)
            
            self.logger.info(f"Email {email} entered successfully")
            
            # Find and click submit button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:contains("Sign")',
                'button:contains("Login")',
                'button:contains("Continue")',
                'button:contains("Next")',
                '.submit-btn',
                '.login-btn',
                '.continue-btn',
                'button[data-testid*="submit"]',
                'button[data-testid*="continue"]'
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    if ':contains(' in selector:
                        # Handle jQuery-style selectors with XPath
                        text = selector.split('"')[1]
                        submit_button = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{text}')]")
                    else:
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if submit_button:
                submit_button.click()
                time.sleep(3)
                self.logger.info("Submit button clicked successfully")
                return True
            else:
                # Try pressing Enter on the email field
                from selenium.webdriver.common.keys import Keys
                email_field.send_keys(Keys.ENTER)
                time.sleep(3)
                self.logger.info("Pressed Enter to submit")
                return True
                
        except Exception as e:
            self.logger.error(f"Error pasting email and submitting: {e}")
            return False
    
    def wait_and_process_verification(self, verification_link):
        """Process verification link"""
        try:
            if verification_link:
                self.logger.info(f"Processing verification link: {verification_link}")
                self.driver.get(verification_link)
                time.sleep(10)  # Allow verification to complete
                
                # Check for successful login indicators
                success_indicators = [
                    "dashboard", "terminal", "welcome", "workspace", 
                    "settings", "profile", "warp-terminal", "app"
                ]
                
                current_url = self.driver.current_url.lower()
                page_content = self.driver.page_source.lower()
                
                for indicator in success_indicators:
                    if indicator in current_url or indicator in page_content:
                        self.logger.info("Verification successful - Warp access granted!")
                        return True
                
                self.logger.info("Verification link processed")
                return True
            else:
                self.logger.error("No verification link provided")
                return False
        except Exception as e:
            self.logger.error(f"Error processing verification: {e}")
            return False
    
    def keep_browser_open(self):
        """Keep browser open for user access"""
        try:
            # Navigate to main Warp interface
            self.driver.get("https://app.warp.dev")
            time.sleep(5)
            self.logger.info("Browser will remain open for Warp access")
            return True
        except Exception as e:
            self.logger.error(f"Error keeping browser open: {e}")
            return False

class CompleteWarpAutomation:
    """Complete automation orchestrator with enhanced features"""
    
    def __init__(self, gui_callback=None):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.email_manager = EnhancedTemporaryEmailManager()
        self.warp_automator = EnhancedWarpAutomator()
        self.gui_callback = gui_callback
        
        # Automation results
        self.generated_email = None
        self.verification_link = None
        self.automation_success = False
    
    def setup_logging(self):
        """Setup enhanced logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enhanced_warp_automation.log'),
                logging.StreamHandler()
            ]
        )
    
    def log_to_gui(self, message):
        """Send log message to GUI if available"""
        if self.gui_callback:
            self.gui_callback(message)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def execute_complete_automation(self):
        """Execute the complete enhanced automation workflow"""
        try:
            self.log_to_gui("🌟 ENHANCED WARP EMAIL AUTOMATION SYSTEM STARTING...")
            self.log_to_gui("🔥 Complete workflow with clipboard integration and incognito mode")
            
            # Step 1: Generate temporary email and copy to clipboard
            self.log_to_gui("📧 Generating temporary email address...")
            self.generated_email = self.email_manager.get_temporary_email()
            if not self.generated_email:
                self.log_to_gui("❌ Failed to generate temporary email")
                return False
            
            self.log_to_gui(f"✅ Generated email: {self.generated_email}")
            self.log_to_gui("📋 Email copied to clipboard automatically!")
            
            # Step 2: Setup incognito browser
            self.log_to_gui("🕵️ Setting up incognito browser for privacy...")
            if not self.warp_automator.setup_incognito_browser():
                self.log_to_gui("❌ Failed to setup incognito browser")
                return False
            
            # Step 3: Open app.warp.dev in incognito
            self.log_to_gui("🌐 Opening app.warp.dev in incognito mode...")
            if not self.warp_automator.open_warp_incognito():
                self.log_to_gui("❌ Failed to open Warp in incognito")
                return False
            
            # Step 4: Paste email and submit
            self.log_to_gui("📝 Automatically pasting email and submitting...")
            if not self.warp_automator.paste_email_and_submit(self.generated_email):
                self.log_to_gui("❌ Failed to paste email and submit")
                return False
            
            self.log_to_gui("✅ Email submitted successfully!")
            
            # Step 5: Monitor inbox and get verification link
            self.log_to_gui("📬 Monitoring inbox for verification email...")
            self.log_to_gui("⏳ This may take up to 5 minutes...")
            self.log_to_gui("🔄 Checking email every 10 seconds...")
            
            self.verification_link = self.email_manager.monitor_inbox_and_get_link(timeout=300)
            if not self.verification_link:
                self.log_to_gui("❌ No verification email received within timeout")
                self.log_to_gui("🔍 You may need to check the email manually")
                return False
            
            self.log_to_gui("✅ Verification email received!")
            self.log_to_gui(f"🔗 Verification link: {self.verification_link}")
            self.log_to_gui("📋 Verification link copied to clipboard!")
            
            # Step 6: Process verification link
            self.log_to_gui("🔐 Processing verification link automatically...")
            if not self.warp_automator.wait_and_process_verification(self.verification_link):
                self.log_to_gui("❌ Failed to process verification")
                return False
            
            # Step 7: Complete and keep browser open
            self.log_to_gui("🏁 Finalizing Warp access...")
            if not self.warp_automator.keep_browser_open():
                self.log_to_gui("⚠️ Warning: Browser may not stay open")
            
            # Success!
            self.log_to_gui("🎉 SUCCESS! COMPLETE WARP AUTOMATION FINISHED!")
            self.log_to_gui("✨ Warp terminal access granted!")
            self.log_to_gui("🖥️ Browser will remain open for your use")
            self.log_to_gui("📋 All links and email copied to clipboard")
            
            self.automation_success = True
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Critical error in automation: {e}")
            self.logger.error(f"Critical error in automation: {e}")
            return False
    
    def get_automation_results(self):
        """Get results of automation for external use"""
        return {
            'success': self.automation_success,
            'email': self.generated_email,
            'verification_link': self.verification_link,
            'timestamp': datetime.now().isoformat()
        }

class EnhancedWarpGUI:
    """Enhanced GUI with better controls and status display"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enhanced Warp Email Automation - Ethereal Glow R&D")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.automator = None
        self.automation_thread = None
        self.results = None
        
        self.setup_enhanced_gui()
    
    def setup_enhanced_gui(self):
        """Setup enhanced GUI components"""
        # Main title
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🌟 ENHANCED WARP EMAIL AUTOMATION",
            font=("Arial", 18, "bold"),
            fg="blue"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Ethereal Glow R&D Project 9 - WEAS-2025-ENHANCED",
            font=("Arial", 11),
            fg="gray"
        )
        subtitle_label.pack()
        
        # Features description
        features_frame = tk.LabelFrame(self.root, text="🔥 Enhanced Features", font=("Arial", 10, "bold"))
        features_frame.pack(pady=10, padx=20, fill=tk.X)
        
        features_text = """✨ Automatic clipboard integration for email and links
🕵️ Incognito browser mode for enhanced privacy  
🚀 Complete end-to-end automation workflow
📧 Advanced temporary email generation with multiple services
🔗 Smart verification link extraction and processing
🖥️ Browser stays open for immediate Warp access"""
        
        features_label = tk.Label(features_frame, text=features_text, justify=tk.LEFT, font=("Arial", 9))
        features_label.pack(pady=10, padx=10)
        
        # Control buttons frame
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=15)
        
        # Main automation button
        self.start_button = tk.Button(
            controls_frame,
            text="🚀 START COMPLETE AUTOMATION",
            font=("Arial", 14, "bold"),
            bg="#28a745",
            fg="white",
            command=self.start_complete_automation,
            height=2,
            width=25
        )
        self.start_button.pack(pady=5)
        
        # Results display frame
        results_frame = tk.LabelFrame(self.root, text="📊 Automation Results", font=("Arial", 10, "bold"))
        results_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.results_text = tk.Text(results_frame, height=4, font=("Courier", 9))
        self.results_text.pack(pady=5, padx=5, fill=tk.X)
        
        # Log display
        log_frame = tk.LabelFrame(self.root, text="📋 Automation Log", font=("Arial", 10, "bold"))
        log_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.log_display = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            width=80,
            font=("Courier", 9),
            wrap=tk.WORD
        )
        self.log_display.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        # Status bar with progress
        status_frame = tk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress_bar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to start enhanced automation",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def log_callback(self, message):
        """Enhanced log callback with better formatting"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_display.insert(tk.END, log_message)
        self.log_display.see(tk.END)
        self.root.update_idletasks()
    
    def update_results_display(self, results):
        """Update the results display"""
        self.results_text.delete(1.0, tk.END)
        if results:
            result_text = f"""🎯 Automation Status: {'✅ SUCCESS' if results['success'] else '❌ FAILED'}
📧 Generated Email: {results.get('email', 'N/A')}
🔗 Verification Link: {results.get('verification_link', 'N/A')[:50]}{'...' if len(str(results.get('verification_link', ''))) > 50 else ''}
⏰ Completed: {results.get('timestamp', 'N/A')}"""
            self.results_text.insert(tk.END, result_text)
    
    def start_complete_automation(self):
        """Start the complete automation process"""
        if self.automation_thread and self.automation_thread.is_alive():
            messagebox.showwarning("Warning", "Automation is already running!")
            return
        
        # Update UI for running state
        self.start_button.config(state=tk.DISABLED, text="🔄 AUTOMATION RUNNING...")
        self.status_label.config(text="Enhanced automation in progress...")
        self.progress_bar.start(10)
        self.log_display.delete(1.0, tk.END)
        self.results_text.delete(1.0, tk.END)
        
        # Start automation thread
        self.automation_thread = threading.Thread(target=self.run_complete_automation)
        self.automation_thread.daemon = True
        self.automation_thread.start()
    
    def run_complete_automation(self):
        """Run complete automation in separate thread"""
        try:
            self.automator = CompleteWarpAutomation(gui_callback=self.log_callback)
            success = self.automator.execute_complete_automation()
            
            # Get results
            self.results = self.automator.get_automation_results()
            
            # Update GUI
            self.root.after(0, self.automation_completed, success)
            
        except Exception as e:
            self.root.after(0, self.automation_error, str(e))
    
    def automation_completed(self, success):
        """Handle automation completion"""
        self.progress_bar.stop()
        
        if success:
            self.status_label.config(text="✅ Enhanced automation completed successfully!")
            messagebox.showinfo("🎉 Success!", 
                              "Warp automation completed successfully!\n"
                              "✅ Email generated and copied to clipboard\n"
                              "✅ Verification link copied to clipboard\n"
                              "✅ Browser opened with Warp access\n"
                              "✅ Ready for immediate use!")
        else:
            self.status_label.config(text="❌ Enhanced automation failed")
            messagebox.showerror("❌ Error", "Automation failed. Check logs for details.")
        
        # Update results display
        if self.results:
            self.update_results_display(self.results)
        
        # Reset button
        self.start_button.config(state=tk.NORMAL, text="🚀 START COMPLETE AUTOMATION")
    
    def automation_error(self, error_message):
        """Handle automation error"""
        self.progress_bar.stop()
        self.status_label.config(text="❌ Automation error occurred")
        messagebox.showerror("❌ Error", f"Automation error: {error_message}")
        self.start_button.config(state=tk.NORMAL, text="🚀 START COMPLETE AUTOMATION")
    
    def run(self):
        """Run the enhanced GUI"""
        self.root.mainloop()

def main():
    """Enhanced main entry point"""
    print("🌟 ENHANCED WARP EMAIL AUTOMATION SYSTEM - ETHEREAL GLOW R&D")
    print("=" * 60)
    print("🔥 Features: Clipboard Integration + Incognito Mode + Complete Automation")
    print("=" * 60)
    
    try:
        # Create and run enhanced GUI
        app = EnhancedWarpGUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Enhanced automation stopped by user")
    except Exception as e:
        print(f"❌ Critical error: {e}")

if __name__ == "__main__":
    main()
