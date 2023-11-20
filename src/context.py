from typing import Any
from app_settings import Settings
from backend.models.lcmdiffusion_setting import LCMLora
from models.interface_types import InterfaceType
from backend.lcm_text_to_image import LCMTextToImage
from time import perf_counter
from backend.image_saver import ImageSaver
from pprint import pprint

class Context:
    use_lcm_lora=False
    lcm_lora=LCMLora()
    
    def __init__(
        self,
        interface_type: InterfaceType,
        device="cpu",
    ):
        self.interface_type = interface_type
        self.lcm_text_to_image = LCMTextToImage(device)

    def generate_text_to_image(
        self,
        settings: Settings,
        reshape: bool = False,
        device: str = "cpu",
    ) -> Any:
        tick = perf_counter()
        pprint(settings.lcm_diffusion_setting.model_dump())
        if not settings.lcm_diffusion_setting.lcm_lora:
            return None
        self.lcm_text_to_image.init(
            settings.lcm_diffusion_setting.lcm_model_id,
            settings.lcm_diffusion_setting.use_openvino,
            device,
            settings.lcm_diffusion_setting.use_offline_model,
            settings.lcm_diffusion_setting.use_tiny_auto_encoder,
            settings.lcm_diffusion_setting.use_lcm_lora,
            settings.lcm_diffusion_setting.lcm_lora,
        )
        images = self.lcm_text_to_image.generate(
            settings.lcm_diffusion_setting,
            reshape,
        )
        elapsed = perf_counter() - tick
        ImageSaver.save_images(
            settings.results_path,
            images=images,
            lcm_diffusion_setting=settings.lcm_diffusion_setting,
        )
        print(f"Elapsed time : {elapsed:.2f} seconds")
        return images
