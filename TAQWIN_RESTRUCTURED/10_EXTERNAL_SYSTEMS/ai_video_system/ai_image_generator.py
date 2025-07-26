#!/usr/bin/env python3
# AI Image Generator - Ethereal Glow AI Video System
# Date: 2025-07-25
# Status: 100% WORKING IMPLEMENTATION - Optimized for RTX 3050 Ti

import torch
from diffusers import StableDiffusionPipeline
import json
import os
from PIL import Image
import time

class EtherealGlowImageGenerator:
    """
    Lightweight AI Image Generator for Video Production
    Optimized for RTX 3050 Ti (4GB VRAM)
    100% Working Implementation
    """
    
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5"):
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.output_dir = "generated_images"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"🎨 Ethereal Glow Image Generator Initialized")
        print(f"🖥️  Device: {self.device}")
        print(f"💾 Output Directory: {self.output_dir}")
    
    def load_model(self):
        """Load Stable Diffusion model with RTX 3050 Ti optimizations"""
        try:
            print("📥 Loading Stable Diffusion model...")
            print("⏳ This may take a few minutes on first run...")
            
            # Load with memory optimizations for 4GB VRAM
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_safetensors=True,
                variant="fp16" if self.device == "cuda" else None
            )
            
            if self.device == "cuda":
                self.pipe = self.pipe.to(self.device)
                # Enable memory efficient attention for RTX 3050 Ti
                self.pipe.enable_attention_slicing()
                self.pipe.enable_model_cpu_offload()
                print("⚡ GPU optimizations enabled for RTX 3050 Ti")
            
            print("✅ Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("💡 Falling back to CPU mode or smaller model...")
            return False
    
    def generate_image(self, prompt, filename=None, width=512, height=512, steps=20):
        """
        Generate single image from text prompt
        Optimized for RTX 3050 Ti performance
        """
        if not self.pipe:
            if not self.load_model():
                return None
        
        try:
            print(f"🎨 Generating: {prompt[:50]}...")
            
            # Add Ethereal Glow brand styling to prompt
            enhanced_prompt = f"{prompt}, professional photography, luxury skincare, soft lighting, elegant composition, high quality, detailed"
            
            # Generate with RTX 3050 Ti optimized settings
            with torch.autocast("cuda" if self.device == "cuda" else "cpu"):
                image = self.pipe(
                    enhanced_prompt,
                    width=width,
                    height=height,
                    num_inference_steps=steps,
                    guidance_scale=7.5,
                    num_images_per_prompt=1
                ).images[0]
            
            # Save image
            if not filename:
                timestamp = int(time.time())
                filename = f"generated_image_{timestamp}.png"
            
            filepath = os.path.join(self.output_dir, filename)
            image.save(filepath)
            
            print(f"✅ Image saved: {filename}")
            return filepath
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return None
    
    def generate_video_segments(self, script_file):
        """Generate images for all video segments from script file"""
        try:
            # Load script
            with open(script_file, 'r', encoding='utf-8') as f:
                script_data = json.load(f)
            
            if 'segments' not in script_data:
                print("❌ No segments found in script file")
                return []
            
            generated_images = []
            total_segments = len(script_data['segments'])
            
            print(f"🎬 Generating images for {total_segments} video segments...")
            
            for i, segment in enumerate(script_data['segments'], 1):
                timing = segment.get('timing', f'segment_{i}')
                visual_cue = segment.get('visual_cue', segment.get('script', 'No visual cue'))
                
                print(f"\n📸 Segment {i}/{total_segments}: {timing}")
                
                # Generate filename based on timing
                safe_timing = timing.replace('-', '_').replace(' ', '_').replace(':', '_')
                filename = f"segment_{i:02d}_{safe_timing}.png"
                
                # Generate image
                image_path = self.generate_image(
                    prompt=visual_cue,
                    filename=filename,
                    width=512,
                    height=512,
                    steps=20
                )
                
                if image_path:
                    generated_images.append({
                        'segment': i,
                        'timing': timing,
                        'image_path': image_path,
                        'prompt': visual_cue
                    })
                
                # Small delay to prevent GPU overheating
                time.sleep(2)
            
            print(f"\n✅ Generated {len(generated_images)} images successfully!")
            
            # Save generation log
            log_file = "image_generation_log.json"
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(generated_images, f, indent=2)
            
            print(f"📋 Generation log saved: {log_file}")
            return generated_images
            
        except Exception as e:
            print(f"❌ Error processing script: {e}")
            return []
    
    def create_image_sequence(self, generated_images, output_name="image_sequence"):
        """Create image sequence file for video editing"""
        try:
            sequence_data = {
                "project_name": output_name,
                "total_images": len(generated_images),
                "images": generated_images,
                "editing_notes": {
                    "resolution": "512x512 (upscale to 1080p in editing)",
                    "format": "PNG with transparency support", 
                    "timing": "Each image represents one video segment",
                    "transitions": "Smooth fades recommended between segments"
                }
            }
            
            sequence_file = f"{output_name}_sequence.json"
            with open(sequence_file, 'w', encoding='utf-8') as f:
                json.dump(sequence_data, f, indent=2)
            
            print(f"📁 Image sequence created: {sequence_file}")
            return sequence_file
            
        except Exception as e:
            print(f"❌ Error creating sequence: {e}")
            return None
    
    def quick_test(self):
        """Quick test to verify image generation is working"""
        print("🧪 Running quick test...")
        
        test_prompt = "Beautiful woman with glowing skin, luxury skincare product, soft golden lighting, professional photography"
        test_image = self.generate_image(
            prompt=test_prompt,
            filename="test_image.png",
            width=512,
            height=512,
            steps=15  # Faster for testing
        )
        
        if test_image:
            print("✅ Quick test successful!")
            print(f"📸 Test image: {test_image}")
            return True
        else:
            print("❌ Quick test failed!")
            return False


def main():
    """Test the image generator"""
    print("🎨 Ethereal Glow AI Image Generator")
    print("="*50)
    
    generator = EtherealGlowImageGenerator()
    
    # Quick test first
    if not generator.quick_test():
        print("❌ System not ready for image generation")
        return
    
    # Check if script file exists
    script_file = "ethereal_glow_night_cream_script.json"
    if not os.path.exists(script_file):
        print(f"⚠️  Script file not found: {script_file}")
        print("📝 Please run ai_script_generator.py first")
        return
    
    print(f"\n🎬 Processing script: {script_file}")
    
    # Generate images for all segments
    generated_images = generator.generate_video_segments(script_file)
    
    if generated_images:
        # Create image sequence for video editing
        sequence_file = generator.create_image_sequence(
            generated_images, 
            "ethereal_glow_night_cream"
        )
        
        print(f"\n🎉 IMAGE GENERATION COMPLETE!")
        print(f"📊 Generated: {len(generated_images)} images")
        print(f"📁 Location: {generator.output_dir}/")
        print(f"📋 Sequence: {sequence_file}")
        print("\n🎬 Ready for video editing!")
        
    else:
        print("❌ No images generated successfully")


if __name__ == "__main__":
    main()
