#!/usr/bin/env python3
"""
STRUCTURED ETHEREAL GLOW AI VIDEO GENERATION SYSTEM
Properly organized data structure with configuration management
RTX 3050 Ti optimized with multiple quality levels
"""

import torch
import gc
import os
import json
import psutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_video

class StructuredVideoGenerator:
    """Structured video generator with proper data organization"""
    
    def __init__(self, config_path: str = "video_generation_config.json"):
        """Initialize with configuration file"""
        self.config_path = config_path
        self.config = self.load_configuration()
        self.pipe = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.setup_directories()
        
    def load_configuration(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Configuration loaded from {self.config_path}")
            return config["ethereal_glow_video_generation"]
        except FileNotFoundError:
            print(f"❌ Configuration file {self.config_path} not found!")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in configuration file: {e}")
            return {}
    
    def setup_directories(self) -> None:
        """Create organized directory structure"""
        if not self.config:
            return
            
        base_dir = Path(self.config["output_structure"]["base_directory"])
        subdirs = self.config["output_structure"]["subdirectories"]
        
        # Create base directory
        base_dir.mkdir(exist_ok=True)
        
        # Create all subdirectories
        for subdir_name, subdir_path in subdirs.items():
            full_path = base_dir / subdir_path
            full_path.mkdir(parents=True, exist_ok=True)
            
        print(f"📁 Directory structure created: {base_dir}")
        self.base_output_dir = base_dir
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        info = {}
        
        if torch.cuda.is_available():
            gpu_props = torch.cuda.get_device_properties(0)
            info["gpu"] = {
                "name": gpu_props.name,
                "memory_gb": gpu_props.total_memory / 1024**3,
                "memory_free_gb": (gpu_props.total_memory - torch.cuda.memory_allocated(0)) / 1024**3
            }
        
        ram = psutil.virtual_memory()
        info["system"] = {
            "ram_total_gb": ram.total / 1024**3,
            "ram_available_gb": ram.available / 1024**3,
            "cpu_count": psutil.cpu_count()
        }
        
        return info
    
    def nuclear_memory_cleanup(self) -> None:
        """Comprehensive memory cleanup"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            torch.cuda.ipc_collect()
        
        for _ in range(3):
            gc.collect()
    
    def load_pipeline(self, quality_level: str = "conservative") -> bool:
        """Load pipeline with specified quality level"""
        if not self.config:
            print("❌ No configuration loaded!")
            return False
            
        try:
            self.nuclear_memory_cleanup()
            
            # Get pipeline configuration
            pipeline_config = self.config["pipeline_config"]
            
            # Set environment variables
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = pipeline_config["cuda_alloc_conf"]
            
            print(f"📥 Loading Motion Adapter: {pipeline_config['motion_adapter']}")
            adapter = MotionAdapter.from_pretrained(
                pipeline_config["motion_adapter"],
                torch_dtype=torch.float16
            )
            
            print(f"📥 Loading Main Pipeline: {pipeline_config['model']}")
            self.pipe = AnimateDiffPipeline.from_pretrained(
                pipeline_config["model"],
                motion_adapter=adapter,
                torch_dtype=torch.float16,
                use_safetensors=True
            )
            
            # Apply optimizations
            print("⚙️ Applying optimizations...")
            optimizations = pipeline_config["enable_optimizations"]
            
            if "attention_slicing" in optimizations:
                self.pipe.enable_attention_slicing(1)
            if "sequential_cpu_offload" in optimizations:
                self.pipe.enable_sequential_cpu_offload()
            if "vae_slicing" in optimizations:
                self.pipe.enable_vae_slicing()
            if "vae_tiling" in optimizations:
                self.pipe.enable_vae_tiling()
            
            # GPU settings
            if torch.cuda.is_available():
                if "flash_sdp" in optimizations:
                    torch.backends.cuda.enable_flash_sdp(True)
                torch.cuda.set_per_process_memory_fraction(pipeline_config["memory_fraction"])
            
            self.nuclear_memory_cleanup()
            print(f"✅ Pipeline loaded successfully with {quality_level} settings!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading pipeline: {e}")
            return False
    
    def get_video_settings(self, quality_level: str) -> Dict[str, Any]:
        """Get video settings for specified quality level"""
        if quality_level not in self.config["video_settings"]:
            print(f"⚠️ Quality level '{quality_level}' not found, using 'conservative'")
            quality_level = "conservative"
        
        return self.config["video_settings"][quality_level]
    
    def generate_video_from_template(self, template_name: str, quality_level: str = "conservative") -> Optional[Path]:
        """Generate video from template configuration"""
        if not self.config or not self.pipe:
            print("❌ Configuration or pipeline not loaded!")
            return None
            
        # Get template
        if template_name not in self.config["video_templates"]:
            print(f"❌ Template '{template_name}' not found!")
            return None
            
        template = self.config["video_templates"][template_name]
        settings = self.get_video_settings(quality_level)
        
        try:
            self.nuclear_memory_cleanup()
            
            # Parse resolution
            resolution = settings["resolution"].split("x")
            width, height = int(resolution[0]), int(resolution[1])
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            naming_convention = self.config["output_structure"]["naming_convention"]
            filename = naming_convention.format(
                category=template["category"],
                name=template_name,
                timestamp=timestamp,
                quality_level=quality_level
            )
            
            # Set seed
            generator = torch.manual_seed(template["seed"])
            
            print(f"\n🎬 GENERATING VIDEO FROM TEMPLATE")
            print(f"{'='*50}")
            print(f"📝 Template: {template['name']}")
            print(f"📊 Quality Level: {quality_level}")
            print(f"📏 Resolution: {width}x{height}")
            print(f"🎞️ Frames: {settings['frames']}")
            print(f"⏱️ Duration: {settings['duration_seconds']} seconds")
            print(f"🎯 FPS: {settings['fps']}")
            print(f"📄 Filename: {filename}")
            
            start_time = datetime.now()
            print(f"\n🚀 Starting generation... ({start_time.strftime('%H:%M:%S')})")
            
            # Generate video
            video_frames = self.pipe(
                prompt=template["prompt"],
                negative_prompt=template["negative_prompt"],
                height=height,
                width=width,
                num_frames=settings["frames"],
                guidance_scale=settings["guidance_scale"],
                num_inference_steps=settings["inference_steps"],
                generator=generator
            ).frames[0]
            
            end_time = datetime.now()
            generation_time = (end_time - start_time).total_seconds()
            print(f"✅ Generation completed in {generation_time:.1f} seconds!")
            
            self.nuclear_memory_cleanup()
            
            # Save video
            output_path = self.base_output_dir / "segments" / "raw" / filename
            export_to_video(video_frames, str(output_path), fps=settings["fps"])
            
            # Get file info
            file_size_mb = output_path.stat().st_size / 1024 / 1024
            
            print(f"💾 Video saved: {output_path}")
            print(f"📊 File size: {file_size_mb:.1f} MB")
            
            # Save generation metadata
            self.save_generation_metadata(output_path, template, settings, generation_time, file_size_mb)
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating video: {e}")
            self.nuclear_memory_cleanup()
            return None
    
    def save_generation_metadata(self, video_path: Path, template: Dict, settings: Dict, 
                                generation_time: float, file_size_mb: float) -> None:
        """Save metadata about the generated video"""
        metadata = {
            "video_path": str(video_path),
            "generation_timestamp": datetime.now().isoformat(),
            "template": template,
            "settings": settings,
            "generation_time_seconds": generation_time,
            "file_size_mb": file_size_mb,
            "system_info": self.get_system_info()
        }
        
        metadata_path = video_path.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def list_available_templates(self) -> None:
        """Display available video templates"""
        if not self.config:
            print("❌ No configuration loaded!")
            return
            
        templates = self.config["video_templates"]
        print(f"\n🎬 AVAILABLE VIDEO TEMPLATES ({len(templates)}):")
        print("="*60)
        
        for i, (key, template) in enumerate(templates.items(), 1):
            print(f"{i}. {key}")
            print(f"   📝 Name: {template['name']}")
            print(f"   ⏱️ Duration: {template['duration']} seconds")
            print(f"   🏷️ Category: {template['category']}")
            print(f"   📄 Prompt: {template['prompt'][:80]}...")
            print()
    
    def list_quality_levels(self) -> None:
        """Display available quality levels"""
        if not self.config:
            print("❌ No configuration loaded!")
            return
            
        quality_levels = self.config["quality_levels"]
        print(f"\n🌟 AVAILABLE QUALITY LEVELS ({len(quality_levels)}):")
        print("="*50)
        
        for level, info in quality_levels.items():
            settings = self.config["video_settings"][info["settings"]]
            print(f"📊 {level.upper()}")
            print(f"   📝 Description: {info['description']}")
            print(f"   📏 Resolution: {settings['resolution']}")
            print(f"   🎞️ Frames: {settings['frames']}")
            print(f"   ⚙️ Inference Steps: {settings['inference_steps']}")
            print()

def main():
    """Main execution function"""
    print("🧠 STRUCTURED ETHEREAL GLOW AI VIDEO GENERATION SYSTEM")
    print("="*65)
    print("🎯 Focus: Organized, scalable video generation")
    print("📊 Configuration: JSON-based settings management")
    print("🗂️ Structure: Proper data organization")
    
    # Initialize generator
    generator = StructuredVideoGenerator()
    
    if not generator.config:
        print("❌ Failed to load configuration. Please check config file.")
        return
    
    # Display system info
    print(f"\n📊 SYSTEM ANALYSIS:")
    system_info = generator.get_system_info()
    if "gpu" in system_info:
        gpu = system_info["gpu"]
        print(f"🔧 GPU: {gpu['name']}")
        print(f"💾 GPU Memory: {gpu['memory_gb']:.1f} GB total, {gpu['memory_free_gb']:.1f} GB free")
    
    system = system_info["system"]
    print(f"🖥️ System RAM: {system['ram_total_gb']:.1f} GB total, {system['ram_available_gb']:.1f} GB available")
    
    # Load pipeline
    print(f"\n🚀 PIPELINE LOADING:")
    if not generator.load_pipeline():
        print("❌ Failed to load pipeline.")
        return
    
    # Show available options
    generator.list_quality_levels()
    generator.list_available_templates()
    
    # Get user input
    template_choice = input("Select template (enter key name): ").strip()
    quality_choice = input("Select quality level (conservative/balanced/aggressive): ").strip()
    
    if not quality_choice:
        quality_choice = "conservative"
    
    # Generate video
    print(f"\n🎬 Generating video with template '{template_choice}' at '{quality_choice}' quality...")
    
    result_path = generator.generate_video_from_template(template_choice, quality_choice)
    
    if result_path:
        print(f"\n🎉 SUCCESS! Video generated successfully!")
        print(f"📁 Location: {result_path}")
        print(f"📄 Metadata: {result_path.with_suffix('.json')}")
        print(f"\n💡 Next Steps:")
        print("   1. Review the generated video")
        print("   2. Generate additional segments if needed")
        print("   3. Use video editing software to combine segments")
        print("   4. Add text overlays, music, and effects")
        print("   5. Export for social media platforms")
    else:
        print("❌ Video generation failed.")

if __name__ == "__main__":
    main()
