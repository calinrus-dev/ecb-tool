"""
Sistema de validación para archivos de configuración JSON.
Valida tipos, rangos y valores obligatorios.
"""
import json
import os
from typing import Any, Dict, List, Optional, Union


class ConfigValidationError(Exception):
    """Error de validación de configuración."""
    pass


class ConfigValidator:
    """Validador de configuración JSON con esquemas."""
    
    def __init__(self, schema: Dict[str, Any]):
        """
        Args:
            schema: Esquema de validación con tipos y restricciones
        """
        self.schema = schema
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Valida datos contra el esquema.
        
        Args:
            data: Datos a validar
        
        Returns:
            Diccionario con errores encontrados por clave
        """
        errors = {}
        self._validate_dict(data, self.schema, "", errors)
        return errors
    
    def _validate_dict(self, data: Any, schema: Any, path: str, errors: Dict[str, List[str]]):
        """Valida recursivamente un diccionario."""
        if not isinstance(schema, dict):
            return
        
        for key, value_schema in schema.items():
            current_path = f"{path}.{key}" if path else key
            
            if key not in data:
                # Verificar si es requerido
                if isinstance(value_schema, dict) and value_schema.get("required", False):
                    if current_path not in errors:
                        errors[current_path] = []
                    errors[current_path].append(f"Campo requerido faltante: {current_path}")
                continue
            
            value = data[key]
            self._validate_value(value, value_schema, current_path, errors)
    
    def _validate_value(self, value: Any, schema: Any, path: str, errors: Dict[str, List[str]]):
        """Valida un valor individual."""
        if isinstance(schema, dict):
            # Esquema de validación completo
            expected_type = schema.get("type")
            if expected_type:
                if not self._check_type(value, expected_type):
                    if path not in errors:
                        errors[path] = []
                    errors[path].append(f"Tipo incorrecto en {path}: esperado {expected_type}, recibido {type(value).__name__}")
                    return
            
            # Validar rango numérico
            if "min" in schema and isinstance(value, (int, float)):
                if value < schema["min"]:
                    if path not in errors:
                        errors[path] = []
                    errors[path].append(f"Valor en {path} menor que el mínimo: {value} < {schema['min']}")
            
            if "max" in schema and isinstance(value, (int, float)):
                if value > schema["max"]:
                    if path not in errors:
                        errors[path] = []
                    errors[path].append(f"Valor en {path} mayor que el máximo: {value} > {schema['max']}")
            
            # Validar opciones permitidas
            if "options" in schema:
                if value not in schema["options"]:
                    if path not in errors:
                        errors[path] = []
                    errors[path].append(f"Valor no permitido en {path}: {value} no está en {schema['options']}")
            
            # Validar propiedades anidadas
            if "properties" in schema and isinstance(value, dict):
                self._validate_dict(value, schema["properties"], path, errors)
        
        elif isinstance(value, dict) and isinstance(schema, type):
            # Esquema simple (solo tipo)
            if not isinstance(value, schema):
                if path not in errors:
                    errors[path] = []
                errors[path].append(f"Tipo incorrecto en {path}: esperado {schema.__name__}, recibido {type(value).__name__}")
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Verifica si un valor coincide con el tipo esperado."""
        type_map = {
            "string": str,
            "int": int,
            "float": (int, float),
            "bool": bool,
            "dict": dict,
            "list": list,
            "number": (int, float),
        }
        
        expected = type_map.get(expected_type, str)
        return isinstance(value, expected)


def load_and_validate_json(path: str, schema: Dict[str, Any], defaults: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Carga y valida un archivo JSON.
    
    Args:
        path: Ruta al archivo JSON
        schema: Esquema de validación
        defaults: Valores por defecto si el archivo no existe
    
    Returns:
        Datos validados (o defaults si hay error)
    
    Raises:
        ConfigValidationError: Si hay errores de validación críticos
    """
    if not os.path.exists(path):
        if defaults is not None:
            return defaults.copy()
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {path}")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        if defaults is not None:
            print(f"Warning: JSON inválido en {path}: {e}. Usando defaults.")
            return defaults.copy()
        raise ConfigValidationError(f"JSON inválido en {path}: {e}")
    
    # Validar
    validator = ConfigValidator(schema)
    errors = validator.validate(data)
    
    if errors:
        error_msg = "\n".join([f"{k}: {', '.join(v)}" for k, v in errors.items()])
        print(f"Warning: Errores de validación en {path}:\n{error_msg}")
        
        # Si hay defaults, usarlos; si no, lanzar error
        if defaults is not None:
            # Mezclar defaults con data válido
            result = defaults.copy()
            result.update(data)
            return result
        else:
            raise ConfigValidationError(f"Errores de validación en {path}:\n{error_msg}")
    
    return data


# Esquemas de validación predefinidos

CONVERSION_CONFIG_SCHEMA = {
    "rutas": {
        "type": "dict",
        "properties": {
            "beats_entrada": {"type": "string"},
            "portadas_entrada": {"type": "string"},
            "videos_salida": {"type": "string"},
        }
    },
    "conversion": {
        "type": "dict",
        "properties": {
            "bpv": {"type": "int", "min": 1, "max": 10},
            "lotes": {"type": "int", "min": 1, "max": 10},
            "fps": {"type": "int", "min": 1, "max": 120},
            "resolucion": {"type": "string"},
            "bitrate_video": {"type": "string"},
            "bitrate_audio": {"type": "string"},
            "multiportada": {"type": "bool"},
            "loop_portada": {"type": "bool"},
            "autoborrado_beats": {"type": "bool"},
            "autoborrado_portadas": {"type": "bool"},
        }
    }
}

UPLOAD_CONFIG_SCHEMA = {
    "rutas": {
        "type": "dict",
        "properties": {
            "subidos": {"type": "string"},
            "titulos": {"type": "string"},
            "descripcion": {"type": "string"},
        }
    },
    "subida": {
        "type": "dict",
        "properties": {
            "estado": {"type": "string", "options": ["publico", "privado", "no_listado"]},
            "intervalo": {"type": "int", "min": 0},
            "lotes": {"type": "int", "min": 1, "max": 10},
            "autoborrado_subidos": {"type": "bool"},
        }
    }
}

ORDER_CONFIG_SCHEMA = {
    "modo": {"type": "string", "options": ["convertir", "subir", "alternar", "simultaneo", "convert", "upload", "alternate", "simultaneous"]},
    "ordenes": {"type": "int", "min": 1, "max": 999},
    "auto": {"type": "bool"},
    "proceso": {"type": "bool"},
}


__all__ = [
    "ConfigValidator",
    "ConfigValidationError",
    "load_and_validate_json",
    "CONVERSION_CONFIG_SCHEMA",
    "UPLOAD_CONFIG_SCHEMA",
    "ORDER_CONFIG_SCHEMA",
]
