from django.shortcuts import render
from django.views.generic import TemplateView
import yt_dlp
import yt_dlp.YoutubeDL
from django.http import JsonResponse, FileResponse
import os
import time
from django.conf import settings

class Index(TemplateView):
    template_name = 'index.html'

    def post(self, request):
        if request.POST.get('musica'):

            musica = request.POST.get('musica')
            if not musica:
                return JsonResponse({'error': 'No se proporcionó la URL del video.'}, status=400)

            # Configurar el directorio de salida
            output_dir = os.path.join(settings.BASE_DIR, 'media')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            # Configuración de yt_dlp
            ydl_opts = {
                'cookiefile': 'cookies.txt',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Ruta para guardar el archivo
                'format': 'bestaudio/best',  # Descargar el mejor audio disponible
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',  # Extraer audio con FFmpeg
                        'preferredcodec': 'mp3',  # Convertir a MP3
                        'preferredquality': '320',  # Calidad del audio (192 kbps)
                    }
                ],
                'noplaylist': True,  # Descargar solo un elemento
                'socket_timeout': 60,  # Tiempo de espera
                'force_ipv4': True,  # Forzar el uso de IPv4
            }

            try:
                # Descargar y procesar el archivo con yt_dlp
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(musica, download=True)  # Descargar la música
                    filename = ydl.prepare_filename(info_dict)  # Obtener el nombre del archivo generado
                    full_path = os.path.splitext(filename)[0] + '.mp3'  # Asegurar la extensión MP3

                # Verificar si el archivo existe
                if not os.path.exists(full_path):
                    return JsonResponse({'error': 'El archivo no pudo ser generado.'}, status=500)

                # Devolver el archivo como respuesta descargable
                return FileResponse(
                    open(full_path, 'rb'),
                    as_attachment=True,
                    filename=os.path.basename(full_path)
                )

            except yt_dlp.utils.DownloadError as e:
                return JsonResponse({'error': f'Error en la descarga: {str(e)}'}, status=500)
            except Exception as e:
                return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)
            
            
        else:
            
            descarga_video = request.POST.get('video')

            if not descarga_video:
                return JsonResponse({'error': 'No se proporcionó la URL del video.'}, status=400)

            # Configurar el directorio de salida
            output_dir = os.path.join(settings.BASE_DIR, 'media')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            # Configuración de yt_dlp
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'playlist_items': '1',
                'socket_timeout': 60,
                'force_ipv4': True,
            }

            try:
                # Descargar y procesar el archivo con yt_dlp
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(descarga_video, download=True)  # Descargar la música
                    filename = ydl.prepare_filename(info_dict)  # Obtener el nombre del archivo generado
                    full_path = os.path.splitext(filename)[0] + '.mp4'  # Asegurar la extensión MP3


                # Devolver el archivo como respuesta descargable
                return FileResponse(
                    open(full_path, 'rb'),
                    as_attachment=True,
                    filename=os.path.basename(full_path)
                )

            except yt_dlp.utils.DownloadError as e:
                return JsonResponse({'error': f'Error en la descarga: {str(e)}'}, status=500)
            except Exception as e:
                return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)
