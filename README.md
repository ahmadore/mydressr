# MyDressr — Virtual Try-On Demo

Django app that calls free HuggingFace Spaces (CatVTON / IDM-VTON) to
composite a garment onto a user photo.

## Quick start

```bash
pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000

## How it works

1. User uploads avatar + garment photo
2. Django saves files, kicks off a background thread
3. Thread calls the HuggingFace Gradio Space via `gradio_client`
4. Frontend polls `/result/<job_id>/` every 3 s
5. When done, result image is displayed + available to download

## Models

| Choice   | Space              | Notes                         |
| -------- | ------------------ | ----------------------------- |
| CatVTON  | zhengchong/CatVTON | Faster, lightweight (default) |
| IDM-VTON | yisol/IDM-VTON     | Higher quality, slower        |

## Notes

- Free HF Spaces go to sleep after inactivity — first request may take
  60–120 s to cold-start. Subsequent requests are faster.
- For production: replace the thread-based job store with Celery + Redis,
  and use a paid HF Inference Endpoint or Replicate for guaranteed uptime.
- Media files are stored in `media/` and not cleaned up automatically in
  this demo. Add a cleanup task for production.

---

title: MyDressr Virtual Try-On
emoji: 👗
colorFrom: rose
colorTo: pink
sdk: docker
pinned: false
app_port: 8000

---
