import uuid
import threading
from pathlib import Path
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import default_storage

from core import helpers

# In-memory job store (use Redis/DB in production)
_jobs = {}

def index(request):
    return render(request, 'tryon/index.html')


@csrf_exempt
def try_on(request):
    """
    Accepts multipart POST with:
      - avatar: person image file
      - garment: garment image file
      - category: 'upper' | 'lower' | 'dresses'
    Kicks off background thread, returns job_id immediately.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    avatar_file = request.FILES.get('avatar')
    garment_file = request.FILES.get('garment')
    category = request.POST.get('category', 'upper')
    
    if not avatar_file or not garment_file:
        return JsonResponse({'error': 'Both avatar and garment images are required.'}, status=400)

    # Save uploads
    upload_dir = Path(settings.MEDIA_ROOT) / 'uploads'
    upload_dir.mkdir(parents=True, exist_ok=True)

    job_id = str(uuid.uuid4())
    avatar_path = upload_dir / f"{job_id}_avatar{Path(avatar_file.name).suffix}"
    garment_path = upload_dir / f"{job_id}_garment{Path(garment_file.name).suffix}"

    with open(avatar_path, 'wb') as f:
        for chunk in avatar_file.chunks():
            f.write(chunk)
    with open(garment_path, 'wb') as f:
        for chunk in garment_file.chunks():
            f.write(chunk)

    _jobs[job_id] = {'status': 'queued', 'result_url': None, 'error': None}

    # Run inference in background thread
    thread = threading.Thread(
        target=helpers._run_inference,
        args=(job_id, str(avatar_path), str(garment_path), category, _jobs),
        daemon=True
    )
    thread.start()

    return JsonResponse({'job_id': job_id})


def result(request, job_id):
    """Poll endpoint — returns job status + result URL when ready."""
    job = _jobs.get(job_id)
    if not job:
        return JsonResponse({'error': 'Job not found'}, status=404)
    return JsonResponse(job)
