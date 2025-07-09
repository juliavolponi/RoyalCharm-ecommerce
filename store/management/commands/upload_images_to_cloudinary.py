from django.core.management.base import BaseCommand
from store.models import Product  # Troque 'store' pelo nome do seu app se for diferente
from django.conf import settings
import cloudinary.uploader
import os

class Command(BaseCommand):
    help = 'Envia imagens locais dos produtos para o Cloudinary e atualiza o campo image com a nova URL'

    def handle(self, *args, **kwargs):
        base_dir = settings.MEDIA_ROOT

        produtos = Product.objects.exclude(image='').exclude(image=None)

        for produto in produtos:
            local_path = os.path.join(base_dir, str(produto.image))

            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(f"Arquivo não encontrado: {local_path}"))
                continue

            self.stdout.write(f"⬆️ Enviando {produto.image}...")

            try:
                result = cloudinary.uploader.upload(local_path, folder="ecommerce_produtos")

                # Atualiza com a URL do Cloudinary
                produto.image = result['secure_url']
                produto.save()

                self.stdout.write(self.style.SUCCESS(f"✅ {produto.name} atualizado com {produto.image}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Erro ao enviar {produto.name}: {e}"))
