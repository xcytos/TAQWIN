#!/usr/bin/env python3
"""
ETHEREAL GLOW STORYTELLING REEL GENERATOR
Complete Script with Cinematic Segments
Theme: "From Ancient Wisdom to Modern Radiance"
"""

import torch
import gc
import os
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_video
import numpy as np
from pathlib import Path
import time

class EtherealGlowStorytellingReel:
    def __init__(self):
        """Initialize the storytelling reel generator"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self.setup_directories()
        
    def setup_directories(self):
        """Create output directories for storytelling reel"""
        self.output_dir = Path("ethereal_glow_storytelling_reel")
        self.segments_dir = self.output_dir / "segments"
        self.final_reel_dir = self.output_dir / "final_reel"
        
        self.output_dir.mkdir(exist_ok=True)
        self.segments_dir.mkdir(exist_ok=True)
        self.final_reel_dir.mkdir(exist_ok=True)
        
    def load_optimized_pipeline(self):
        """Load AnimateDiff with RTX 3050 Ti optimizations"""
        print("🚀 Loading Storytelling Pipeline with RTX 3050 Ti optimizations...")
        
        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            adapter = MotionAdapter.from_pretrained(
                "guoyww/animatediff-motion-adapter-v1-5-2", 
                torch_dtype=torch.float16
            )
            
            self.pipe = AnimateDiffPipeline.from_pretrained(
                "emilianJR/epiCRealism",
                motion_adapter=adapter,
                torch_dtype=torch.float16,
                use_safetensors=True
            )
            
            self.pipe.scheduler = EulerDiscreteScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # Apply all memory optimizations
            self.pipe.enable_attention_slicing(1)
            self.pipe.enable_sequential_cpu_offload()
            self.pipe.enable_vae_slicing()
            self.pipe.enable_vae_tiling()
            
            if torch.cuda.is_available():
                torch.backends.cuda.enable_flash_sdp(True)
                torch.cuda.set_per_process_memory_fraction(0.9)
            
            print("✅ Storytelling Pipeline loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading pipeline: {e}")
            return False
    
    def generate_segment(self, prompt, negative_prompt, duration_seconds=3, seed=None):
        """Generate a single story segment"""
        if self.pipe is None:
            print("❌ Pipeline not loaded.")
            return None
            
        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            num_frames = max(16, min(48, duration_seconds * 16))
            generator = torch.manual_seed(seed if seed else int(time.time()))
            
            print(f"🎬 Generating {duration_seconds}s segment...")
            print(f"   📝 Prompt: {prompt[:60]}...")
            
            video_frames = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                height=512,
                width=512,
                num_frames=num_frames,
                guidance_scale=7.5,
                num_inference_steps=25,
                generator=generator
            ).frames[0]
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            
            print("✅ Segment generated successfully!")
            return video_frames
            
        except Exception as e:
            print(f"❌ Error generating segment: {e}")
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                gc.collect()
            return None
    
    def save_segment(self, video_frames, filename, fps=16):
        """Save video segment to file"""
        try:
            filepath = self.segments_dir / f"{filename}.mp4"
            export_to_video(video_frames, str(filepath), fps=fps)
            print(f"💾 Segment saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error saving segment: {e}")
            return None

    def create_storytelling_reel(self):
        """Create complete storytelling reel with all segments"""
        
        # STORYTELLING SCRIPT: "From Ancient Wisdom to Modern Radiance"
        story_segments = [
            {
                "name": "01_opening_hook",
                "duration": 2,
                "script": "What if ancient beauty secrets could transform your skin today?",
                "prompt": "Ancient Indian woman applying natural clay mask, soft golden lighting, traditional setting, serene expression, cinematic close-up, warm tones",
                "negative_prompt": "modern clothing, synthetic products, harsh lighting, blurry, distorted, ugly",
                "seed": 100
            },
            {
                "name": "02_problem_introduction", 
                "duration": 3,
                "script": "Tired of harsh chemicals that promise everything but deliver nothing?",
                "prompt": "Frustrated young woman looking in mirror, concerned expression, bathroom setting, realistic skin concerns, soft dramatic lighting, emotional portrait",
                "negative_prompt": "perfect skin, happy expression, artificial lighting, blurry, distorted",
                "seed": 200
            },
            {
                "name": "03_ancient_wisdom",
                "duration": 3,
                "script": "For centuries, Indian women have trusted nature's purest ingredients",
                "prompt": "Traditional Indian spices and clay ingredients, turmeric, multani mitti, neem leaves, wooden bowls, natural textures, warm sunlight, aesthetic arrangement",
                "negative_prompt": "synthetic products, plastic containers, artificial colors, modern packaging",
                "seed": 300
            },
            {
                "name": "04_ethereal_glow_introduction",
                "duration": 2,
                "script": "Introducing Ethereal Glow - Where tradition meets transformation",
                "prompt": "Ethereal Glow product jar, elegant glass container, golden cap, premium packaging, soft studio lighting, luxury beauty product photography",
                "negative_prompt": "cheap packaging, plastic, harsh lighting, blurry, distorted",
                "seed": 400
            },
            {
                "name": "05_transformation_process",
                "duration": 4,
                "script": "Watch as ancient wisdom transforms your skin naturally",
                "prompt": "Gentle application of natural face mask, smooth cream texture, hands applying product to face, peaceful spa-like setting, soft movements, natural skin tones",
                "negative_prompt": "harsh application, artificial products, synthetic textures, aggressive movements",
                "seed": 500
            },
            {
                "name": "06_results_reveal",
                "duration": 3,
                "script": "Experience the radiance that comes from within",
                "prompt": "Beautiful woman with glowing healthy skin, confident smile, natural makeup, soft natural lighting, radiant complexion, peaceful expression",
                "negative_prompt": "heavy makeup, artificial skin, plastic appearance, harsh lighting, fake smile",
                "seed": 600
            },
            {
                "name": "07_product_showcase",
                "duration": 2,
                "script": "Pure. Natural. Effective.",
                "prompt": "Three Ethereal Glow products arranged beautifully, The Raw multani mitti, Vitamin Orange, Neem Ubtan, natural lighting, premium display",
                "negative_prompt": "cluttered arrangement, poor lighting, cheap appearance, plastic packaging",
                "seed": 700
            },
            {
                "name": "08_call_to_action",
                "duration": 2,
                "script": "Your journey to radiant skin starts now",
                "prompt": "Confident young woman holding Ethereal Glow product, genuine smile, natural background, inspiring pose, warm lighting, authentic expression",
                "negative_prompt": "fake smile, artificial pose, harsh lighting, plastic appearance",
                "seed": 800
            },
            {
                "name": "09_brand_closing",
                "duration": 2,
                "script": "Ethereal Glow - Radiate Your Truth",
                "prompt": "Ethereal Glow logo animation, elegant typography, soft gradient background, premium brand presentation, golden accents, fade to elegant finish",
                "negative_prompt": "harsh fonts, cheap design, bright colors, cluttered layout",
                "seed": 900
            }
        ]
        
        print("🎯 Creating Complete Storytelling Reel...")
        print("📖 Story: 'From Ancient Wisdom to Modern Radiance'")
        print(f"📹 Total Segments: {len(story_segments)}")
        print(f"⏱️ Total Duration: {sum(seg['duration'] for seg in story_segments)} seconds")
        
        generated_segments = []
        
        for i, segment in enumerate(story_segments, 1):
            print(f"\n{'='*60}")
            print(f"📹 SEGMENT {i}/{len(story_segments)}: {segment['name']}")
            print(f"📝 Script: \"{segment['script']}\"")
            print(f"⏱️ Duration: {segment['duration']} seconds")
            print(f"🎨 Visual: {segment['prompt'][:80]}...")
            
            # Generate segment
            frames = self.generate_segment(
                prompt=segment['prompt'],
                negative_prompt=segment['negative_prompt'],
                duration_seconds=segment['duration'],
                seed=segment['seed']
            )
            
            if frames:
                # Save segment
                filepath = self.save_segment(frames, segment['name'])
                if filepath:
                    generated_segments.append({
                        'name': segment['name'],
                        'file': filepath,
                        'duration': segment['duration'],
                        'script': segment['script']
                    })
                    print(f"✅ Segment {i} completed successfully!")
                else:
                    print(f"❌ Failed to save segment {i}")
            else:
                print(f"❌ Failed to generate segment {i}")
                
            # Cooling pause between generations
            time.sleep(3)
        
        return generated_segments
    
    def create_script_document(self):
        """Create detailed script document"""
        script_content = """
# ETHEREAL GLOW STORYTELLING REEL SCRIPT
## "From Ancient Wisdom to Modern Radiance"

### REEL OVERVIEW
- **Duration**: 23 seconds
- **Theme**: Traditional Indian beauty wisdom meets modern skincare
- **Target**: Gen Z and Millennials seeking natural skincare
- **Tone**: Inspiring, authentic, transformative

### COMPLETE SCRIPT BREAKDOWN

**SEGMENT 1: Opening Hook (2s)**
📝 *Script*: "What if ancient beauty secrets could transform your skin today?"
🎬 *Visual*: Ancient Indian woman applying natural clay mask, golden lighting
🎵 *Audio*: Mysterious, intriguing music build-up

**SEGMENT 2: Problem Introduction (3s)** 
📝 *Script*: "Tired of harsh chemicals that promise everything but deliver nothing?"
🎬 *Visual*: Frustrated young woman looking in mirror, skin concerns
🎵 *Audio*: Soft, empathetic tone

**SEGMENT 3: Ancient Wisdom (3s)**
📝 *Script*: "For centuries, Indian women have trusted nature's purest ingredients"
🎬 *Visual*: Traditional spices, turmeric, multani mitti, natural arrangement
🎵 *Audio*: Traditional, warm, authentic

**SEGMENT 4: Brand Introduction (2s)**
📝 *Script*: "Introducing Ethereal Glow - Where tradition meets transformation"
🎬 *Visual*: Ethereal Glow product jar, premium presentation
🎵 *Audio*: Brand theme, hopeful and premium

**SEGMENT 5: Transformation Process (4s)**
📝 *Script*: "Watch as ancient wisdom transforms your skin naturally"
🎬 *Visual*: Gentle product application, spa-like setting
🎵 *Audio*: Soothing, transformative

**SEGMENT 6: Results Reveal (3s)**
📝 *Script*: "Experience the radiance that comes from within"
🎬 *Visual*: Beautiful woman with glowing skin, confident smile
🎵 *Audio*: Uplifting, confident

**SEGMENT 7: Product Showcase (2s)**
📝 *Script*: "Pure. Natural. Effective."
🎬 *Visual*: Three product lineup, premium display
🎵 *Audio*: Clean, authoritative

**SEGMENT 8: Call to Action (2s)**
📝 *Script*: "Your journey to radiant skin starts now"
🎬 *Visual*: Confident woman holding product, inspiring
🎵 *Audio*: Motivational, action-oriented

**SEGMENT 9: Brand Closing (2s)**
📝 *Script*: "Ethereal Glow - Radiate Your Truth"
🎬 *Visual*: Logo animation, elegant typography
🎵 *Audio*: Brand signature, memorable finish

### PRODUCTION NOTES
- Each segment optimized for RTX 3050 Ti generation
- Professional quality prompts with negative prompts
- Consistent visual style and brand messaging
- Ready for social media deployment
- Includes text overlay positions and timing
        """
        
        script_file = self.output_dir / "COMPLETE_REEL_SCRIPT.md"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"📄 Complete script saved: {script_file}")
        return script_file

def main():
    """Main execution function"""
    print("🧠 ETHEREAL GLOW STORYTELLING REEL GENERATOR")
    print("=" * 65)
    print("🎬 Story: 'From Ancient Wisdom to Modern Radiance'")
    print("⏱️ Total Duration: 23 seconds (9 segments)")
    print("🎯 Optimized for: RTX 3050 Ti 4GB VRAM")
    
    # Initialize generator
    generator = EtherealGlowStorytellingReel()
    
    # Create script document first
    script_file = generator.create_script_document()
    print(f"\n✅ Complete script created: {script_file}")
    
    # Load pipeline
    if not generator.load_optimized_pipeline():
        print("❌ Failed to load storytelling pipeline.")
        return
    
    # Check GPU memory
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"🔧 GPU Memory Available: {gpu_memory:.1f} GB")
    
    print("\n🎯 Ready to generate complete storytelling reel!")
    print("⚠️  This will take approximately 30-45 minutes to complete all 9 segments")
    
    proceed = input("\nProceed with full reel generation? (y/n): ").strip().lower()
    
    if proceed == 'y':
        # Generate complete storytelling reel
        segments = generator.create_storytelling_reel()
        
        if segments:
            print(f"\n🎉 SUCCESS! Generated {len(segments)} segments!")
            
            print("\n📁 Generated Segments:")
            total_duration = 0
            for segment in segments:
                print(f"   • {segment['name']}: {segment['duration']}s")
                print(f"     Script: \"{segment['script']}\"")
                print(f"     File: {segment['file']}")
                total_duration += segment['duration']
            
            print(f"\n⏱️ Total Reel Duration: {total_duration} seconds")
            print(f"📂 All files saved in: {generator.segments_dir}")
            
            print("\n💡 Next Steps:")
            print("   1. Review all generated segments")
            print("   2. Use video editing software (DaVinci Resolve/CapCut) to combine")
            print("   3. Add text overlays with provided script")
            print("   4. Add background music and sound effects")
            print("   5. Export as final storytelling reel")
            print("   6. Deploy across social media platforms")
            
        else:
            print("❌ No segments were generated successfully.")
    
    else:
        print("👍 Generation cancelled. Script document created for reference.")

if __name__ == "__main__":
    main()
