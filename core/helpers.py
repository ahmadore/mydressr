import os
import traceback
from pathlib import Path
from django.conf import settings
from django.core.files.storage import default_storage


def _run_inference(job_id, avatar_path, garment_path, category, _jobs):
    """Background worker: calls HuggingFace Space via gradio_client."""
    _jobs[job_id]['status'] = 'running'
    try:
        from gradio_client import Client, handle_file

        result_path = _call_idmvton(avatar_path, garment_path, category)
        # Copy result to media/results/
        result_dir = Path(settings.MEDIA_ROOT) / 'results'
        result_dir.mkdir(parents=True, exist_ok=True)
        result_filename = f"{job_id}_result.png"
        result_dest = result_dir / result_filename

        import shutil
        shutil.copy(result_path, result_dest)

        _jobs[job_id]['status'] = 'done'
        _jobs[job_id]['result_url'] = f"{settings.MEDIA_URL}results/{result_filename}"

    except Exception as e:
        print("Error from response")
        error_string = traceback.format_exc()
        print(error_string)
        _jobs[job_id]['status'] = 'error'
        _jobs[job_id]['error'] = str(e)


def _call_catvton(avatar_path, garment_path, category):
    """
    Call CatVTON HuggingFace Space.
    Space: https://huggingface.co/spaces/zhengchong/CatVTON
    API: /predict  fn_index=0
    Inputs: person_image, cloth_image, cloth_type
    """
    from gradio_client import Client, handle_file

    client = Client("zhengchong/CatVTON")
    result = client.predict(
        person_image=handle_file(avatar_path),
        cloth_image=handle_file(garment_path),
        cloth_type=category,          # 'upper' | 'lower' | 'overall'
        num_inference_steps=50,
        guidance_scale=2.5,
        seed=42,
        show_type="result only",
        api_name="/submit_function"
    )
    # result is a file path or dict; gradio_client downloads it locally
    if isinstance(result, (list, tuple)):
        return result[0]
    return result


def _call_idmvton(avatar_path, garment_path, category):
    """
    Call IDM-VTON HuggingFace Space.
    Space: https://huggingface.co/spaces/yisol/IDM-VTON
    """
    from gradio_client import Client, handle_file

    client = Client("yisol/IDM-VTON")
    result = client.predict(
        dict={"background": handle_file(avatar_path), "layers": [], "composite": None},
        garm_img=handle_file(garment_path),
        garment_des=_category_to_description(category),
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=30,
        seed=42,
        api_name="/tryon"
    )
    if isinstance(result, (list, tuple)):
        return result[0]
    return result


def _category_to_description(category):
    mapping = {
        'upper': 'upper body clothing item',
        'lower': 'lower body clothing item',
        'dresses': 'dress or full outfit',
    }
    return mapping.get(category, 'clothing item')
