import os
import sys
import subprocess
import threading
from ecb_tool.core.shared.paths import ROOT_DIR, ORDER_PATH, PARAR_PATH
from ecb_tool.core.config import ConfigManager

class ProcessController:
    """Controlador de procesos para conversión y subida de videos."""
    
    def __init__(self):
        schema = {
            "modo": "convertir",
            "ordenes": 1,
            "auto": True,
            "proceso": False
        }
        self.order_config = ConfigManager(ORDER_PATH, schema)
        self.process_thread = None

    def is_running(self) -> bool:
        """Verifica si hay un proceso en ejecución."""
        return bool(self.order_config.get('proceso', False))

    def start(self, mode: str, parent_widget=None) -> None:
        """
        Inicia un proceso de conversión o subida.
        
        Args:
            mode: Modo de ejecución (convertir, subir, alternar, simultaneo)
            parent_widget: Widget padre para mostrar diálogos (opcional)
        """
        # Si es modo subida, mostrar diálogo de confirmación
        if mode.lower() in ['subir', 'upload'] and parent_widget is not None:
            from ecb_tool.features.ui.blocks.upload_confirmation_dialog import UploadConfirmationDialog
            
            confirmation_dialog = UploadConfirmationDialog(parent_widget)
            
            # Si solicita modificar, abrir configuración
            def on_modify_requested():
                from ecb_tool.features.ui.blocks.upload_settings_dialog_v2 import UploadSettingsDialogV2
                settings_dialog = UploadSettingsDialogV2(parent_widget)
                settings_dialog.exec()
            
            confirmation_dialog.modify_requested.connect(on_modify_requested)
            
            # Solo iniciar si confirma
            result = confirmation_dialog.exec()
            if result != confirmation_dialog.DialogCode.Accepted:
                return  # Usuario canceló
        
        self.order_config.config.update({
            'modo': mode.lower(),
            'proceso': True
        })
        self.order_config.save()
        
        if os.path.exists(PARAR_PATH):
            os.remove(PARAR_PATH)
        
        # Start conversion in background thread
        if mode.lower() in ['convertir', 'alternar', 'simultaneo']:
            self.process_thread = threading.Thread(
                target=self._run_conversion_process,
                daemon=True
            )
            self.process_thread.start()
        else:
            # TODO: Implementar proceso de upload con threading similar a conversión
            # Por ahora usa el legacy mode
            core_path = os.path.join(ROOT_DIR, 'core', 'core.py')
            subprocess.Popen([sys.executable, core_path], cwd=ROOT_DIR)

    def _run_conversion_process(self):
        """Run conversion process in background."""
        try:
            from ecb_tool.features.conversion import ConversionRunner
            runner = ConversionRunner()
            num_orders = self.order_config.get('ordenes', 1)
            runner.run(num_orders)
        except Exception as e:
            print(f"Error en proceso de conversión: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Mark process as finished
            self.order_config.config.update({'proceso': False})
            self.order_config.save()

    def stop(self) -> None:
        """Detiene el proceso en ejecución."""
        self.order_config.config.update({'proceso': False})
        self.order_config.save()
        
        with open(PARAR_PATH, 'w', encoding='utf-8') as f:
            f.write('STOP')
