#!/usr/bin/env python3
"""
SIMPLE WARP EMAIL HELPER - ACTUALLY WORKS!
Ethereal Glow R&D Project 9 - SIMPLE EDITION
Just generates email, opens browser, gives instructions

Created by: TAQWIN Emergency Response Team
"""

import time
import random
import requests
import pyperclip
import webbrowser
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class SimpleEmailGenerator:
    """Simple email generator that just works"""
    
    def __init__(self):
        self.current_email = None
    
    def generate_email(self):
        """Generate simple temporary email"""
        try:
            # Try 1secmail API
            response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1', timeout=10)
            if response.status_code == 200:
                emails = response.json()
                if emails:
                    self.current_email = emails[0]
                    pyperclip.copy(self.current_email)
                    return self.current_email
        except:
            pass
        
        # Fallback method
        timestamp = int(time.time())
        random_num = random.randint(10000, 99999)
        domains = ['1secmail.com', 'esiix.com', 'xojxe.com', 'yoggm.com']
        domain = random.choice(domains)
        
        self.current_email = f"warp{timestamp}{random_num}@{domain}"
        pyperclip.copy(self.current_email)
        return self.current_email
    
    def check_email(self):
        """Check for verification emails"""
        if not self.current_email or '@' not in self.current_email:
            return None
            
        try:
            login, domain = self.current_email.split('@')
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

class SimpleWarpGUI:
    """Ultra-simple GUI that actually works"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 SIMPLE Warp Helper - ACTUALLY WORKS!")
        self.root.geometry("600x500")
        
        self.email_generator = SimpleEmailGenerator()
        self.generated_email = None
        self.monitoring = False
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup simple GUI"""
        # Title
        title_label = tk.Label(
            self.root,
            text="🚀 SIMPLE WARP HELPER",
            font=("Arial", 20, "bold"),
            fg="blue"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="ACTUALLY WORKS! - No Complex Automation",
            font=("Arial", 12),
            fg="green"
        )
        subtitle_label.pack()
        
        # Instructions
        instructions = tk.Text(self.root, height=8, width=70, font=("Arial", 10))
        instructions_text = """SIMPLE 3-STEP PROCESS:

1. Click "🎯 GENERATE EMAIL & OPEN WARP" button below
2. Manually paste the email into the Warp login form (Ctrl+V)
3. Click "📧 MONITOR FOR VERIFICATION EMAIL" to check for verification

That's it! No complex automation - just simple steps that work!"""
        
        instructions.insert("1.0", instructions_text)
        instructions.config(state="disabled")
        instructions.pack(pady=20, padx=20)
        
        # Buttons
        self.step1_button = tk.Button(
            self.root,
            text="🎯 STEP 1: GENERATE EMAIL & OPEN WARP",
            font=("Arial", 12, "bold"),
            bg="#007bff",
            fg="white",
            command=self.step1_generate_and_open,
            height=2
        )
        self.step1_button.pack(pady=10)
        
        self.step2_button = tk.Button(
            self.root,
            text="📧 STEP 2: MONITOR FOR VERIFICATION EMAIL",
            font=("Arial", 12, "bold"),
            bg="#28a745",
            fg="white",
            command=self.step2_monitor_email,
            height=2,
            state="disabled"
        )
        self.step2_button.pack(pady=10)
        
        # Status display
        self.status_label = tk.Label(
            self.root,
            text="Ready to start! Click Step 1 to begin.",
            font=("Arial", 11),
            fg="black",
            bg="lightgray",
            relief="sunken"
        )
        self.status_label.pack(pady=20, padx=20, fill="x")
        
        # Email display
        self.email_display = tk.Label(
            self.root,
            text="",
            font=("Courier", 10, "bold"),
            fg="darkblue",
            bg="lightyellow",
            relief="ridge"
        )
        self.email_display.pack(pady=10, padx=20, fill="x")
    
    def step1_generate_and_open(self):
        """Step 1: Generate email and open Warp"""
        try:
            self.status_label.config(text="🔄 Generating email and opening Warp...", fg="blue")
            self.root.update()
            
            # Generate email
            self.generated_email = self.email_generator.generate_email()
            
            if self.generated_email:
                # Update display
                self.email_display.config(text=f"📧 EMAIL: {self.generated_email} (COPIED TO CLIPBOARD!)")
                
                # Open Warp in browser
                webbrowser.open('https://app.warp.dev/login')
                
                # Update status
                self.status_label.config(
                    text="✅ Email generated and Warp opened! Now paste the email into Warp login form (Ctrl+V)",
                    fg="green"
                )
                
                # Enable step 2
                self.step2_button.config(state="normal")
                
                # Show success message
                messagebox.showinfo(
                    "✅ Step 1 Complete!",
                    f"Success!\n\n"
                    f"📧 Generated email: {self.generated_email}\n"
                    f"📋 Email copied to clipboard!\n"
                    f"🌐 Warp login page opened in browser\n\n"
                    f"NEXT: Go to browser and paste email (Ctrl+V) into Warp login form"
                )
            else:
                self.status_label.config(text="❌ Failed to generate email", fg="red")
                messagebox.showerror("Error", "Failed to generate email. Try again.")
                
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {e}", fg="red")
            messagebox.showerror("Error", f"Error in Step 1: {e}")
    
    def step2_monitor_email(self):
        """Step 2: Monitor for verification email"""
        if not self.generated_email:
            messagebox.showerror("Error", "No email generated yet! Complete Step 1 first.")
            return
        
        if self.monitoring:
            messagebox.showwarning("Warning", "Already monitoring for email!")
            return
        
        self.monitoring = True
        self.step2_button.config(text="🔄 CHECKING EMAIL...", state="disabled")
        self.status_label.config(text="🔍 Checking for verification email...", fg="blue")
        self.root.update()
        
        try:
            # Check for email
            verification_link = self.email_generator.check_email()
            
            if verification_link:
                # Success!
                self.status_label.config(
                    text="🎉 VERIFICATION EMAIL FOUND! Link copied to clipboard!",
                    fg="green"
                )
                
                messagebox.showinfo(
                    "🎉 SUCCESS!",
                    f"Verification email found!\n\n"
                    f"🔗 Verification link: {verification_link[:50]}...\n"
                    f"📋 Link copied to clipboard!\n\n"
                    f"NEXT: The verification link will open automatically!"
                )
                
                # Open verification link
                webbrowser.open(verification_link)
                
                # Final success
                messagebox.showinfo(
                    "✅ COMPLETE!",
                    "🎉 WARP AUTOMATION COMPLETE!\n\n"
                    "✅ Email generated\n"
                    "✅ Verification link found\n"
                    "✅ Verification link opened\n\n"
                    "You should now have access to Warp!"
                )
                
            else:
                self.status_label.config(
                    text="📬 No verification email yet. Make sure you submitted the email in Warp first!",
                    fg="orange"
                )
                
                messagebox.showinfo(
                    "📬 No Email Yet",
                    "No verification email found yet.\n\n"
                    "Make sure you:\n"
                    "1. Pasted the email into Warp login form\n"
                    "2. Clicked Submit/Continue in Warp\n\n"
                    "Then try monitoring again!"
                )
        
        except Exception as e:
            self.status_label.config(text=f"❌ Error checking email: {e}", fg="red")
            messagebox.showerror("Error", f"Error checking email: {e}")
        
        finally:
            self.monitoring = False
            self.step2_button.config(text="📧 STEP 2: MONITOR FOR VERIFICATION EMAIL", state="normal")
    
    def run(self):
        """Run the simple GUI"""
        self.root.mainloop()

def main():
    """Simple main function"""
    print("🚀 SIMPLE WARP HELPER - ACTUALLY WORKS!")
    print("=" * 50)
    print("No complex automation - just simple steps that work!")
    print("=" * 50)
    
    try:
        app = SimpleWarpGUI()
        app.run()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
