"""
Script de automatización para generar y actualizar títulos de manera inteligente
Uso: python scripts/auto_update_titles.py
"""

import random
from pathlib import Path
from datetime import datetime

# Plantillas de títulos con variables
TITLE_TEMPLATES = [
    "{emotion} {type} {style} Beat - \"{name}\" | {bpm} BPM | {year}",
    "{style} {type} Beat \"{name}\" ({bpm}BPM) {emotion}",
    "\"{name}\" - {emotion} {style} {type} | {bpm}BPM",
    "[FREE] {emotion} {type} Beat - \"{name}\" ({bpm})",
    "{style} {type} \"{name}\" | {emotion} Beat {bpm}BPM | {year}",
]

# Variables para las plantillas
EMOTIONS = [
    "Emotional", "Dark", "Hard", "Sad", "Aggressive", "Chill", 
    "Melodic", "Heavy", "Atmospheric", "Energetic"
]

TYPES = [
    "Trap", "Drill", "Hip Hop", "Boom Bap", "LoFi", 
    "RnB", "Afrobeat", "Dancehall", "Reggaeton"
]

STYLES = [
    "Type", "Style", "Instrumental", "Sample", 
    "Modern", "Classic", "Underground", "Mainstream"
]

def generate_title(beat_name=None, bpm=None):
    """Genera un título usando plantillas y variables aleatorias"""
    if beat_name is None:
        beat_name = f"Beat_{random.randint(1, 999)}"
    
    if bpm is None:
        bpm = random.choice([120, 130, 140, 145, 150, 160, 170, 180])
    
    template = random.choice(TITLE_TEMPLATES)
    
    title = template.format(
        emotion=random.choice(EMOTIONS),
        type=random.choice(TYPES),
        style=random.choice(STYLES),
        name=beat_name,
        bpm=bpm,
        year=datetime.now().year
    )
    
    return title

def analyze_existing_titles():
    """Analiza títulos existentes para extraer patrones"""
    titles_file = Path("data/titles.txt")
    
    if not titles_file.exists():
        print("⚠️  Archivo titles.txt no encontrado")
        return []
    
    with open(titles_file, 'r', encoding='utf-8') as f:
        titles = [line.strip() for line in f if line.strip()]
    
    print(f"\n📊 Análisis de {len(titles)} títulos existentes:")
    
    # Análisis de palabras clave
    keywords = {}
    for title in titles:
        words = title.lower().split()
        for word in words:
            keywords[word] = keywords.get(word, 0) + 1
    
    # Top 10 palabras más usadas
    top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n🔑 Palabras más usadas:")
    for word, count in top_keywords:
        print(f"  {word}: {count}")
    
    return titles

def generate_batch_titles(count=50, output_file=None):
    """Genera un lote de títulos"""
    print(f"\n✨ Generando {count} títulos...")
    
    titles = []
    for i in range(count):
        title = generate_title()
        titles.append(title)
        print(f"  {i+1}. {title}")
    
    if output_file:
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(titles))
        print(f"\n✅ Títulos guardados en: {output_file}")
    
    return titles

def append_titles_to_file(new_titles, file_path="data/titles.txt"):
    """Añade nuevos títulos al archivo existente"""
    file = Path(file_path)
    
    # Leer títulos existentes
    existing_titles = set()
    if file.exists():
        with open(file, 'r', encoding='utf-8') as f:
            existing_titles = set(line.strip() for line in f if line.strip())
    
    # Filtrar duplicados
    unique_new_titles = [t for t in new_titles if t not in existing_titles]
    
    if unique_new_titles:
        with open(file, 'a', encoding='utf-8') as f:
            f.write('\n' + '\n'.join(unique_new_titles))
        print(f"\n✅ Añadidos {len(unique_new_titles)} títulos nuevos a {file_path}")
    else:
        print(f"\n⚠️  No hay títulos nuevos únicos para añadir")

def clean_duplicate_titles(file_path="data/titles.txt"):
    """Elimina títulos duplicados del archivo"""
    file = Path(file_path)
    
    if not file.exists():
        print(f"⚠️  Archivo no encontrado: {file_path}")
        return
    
    with open(file, 'r', encoding='utf-8') as f:
        titles = [line.strip() for line in f if line.strip()]
    
    original_count = len(titles)
    unique_titles = list(dict.fromkeys(titles))  # Preserva orden
    duplicates_count = original_count - len(unique_titles)
    
    if duplicates_count > 0:
        # Hacer backup
        backup_path = file.with_suffix('.txt.bak')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(titles))
        
        # Guardar títulos únicos
        with open(file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_titles))
        
        print(f"\n✅ Eliminados {duplicates_count} títulos duplicados")
        print(f"   Backup creado: {backup_path.name}")
    else:
        print(f"\n✓ No hay títulos duplicados")

def main():
    """Función principal"""
    import sys
    
    print("=" * 60)
    print("ECB TOOL - Auto Title Generator")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "generate":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            output = sys.argv[3] if len(sys.argv) > 3 else "generated_titles.txt"
            generate_batch_titles(count, output)
        
        elif command == "analyze":
            analyze_existing_titles()
        
        elif command == "append":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 20
            new_titles = [generate_title() for _ in range(count)]
            append_titles_to_file(new_titles)
        
        elif command == "clean":
            clean_duplicate_titles()
        
        else:
            print(f"❌ Comando desconocido: {command}")
            print("\nComandos disponibles:")
            print("  generate [count] [output] - Generar títulos nuevos")
            print("  analyze                   - Analizar títulos existentes")
            print("  append [count]            - Añadir títulos a titles.txt")
            print("  clean                     - Eliminar duplicados")
    else:
        # Por defecto: analizar y generar 10 títulos de ejemplo
        analyze_existing_titles()
        print("\n" + "=" * 60)
        generate_batch_titles(10)

if __name__ == "__main__":
    main()
