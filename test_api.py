import urllib.request
import time
import sys
import json

# Esperar a que Django esté listo
time.sleep(3)

try:
    # Probar endpoint base
    print("Probando http://localhost:8000/ventas/api/")
    url = "http://localhost:8000/ventas/api/"
    
    try:
        with urllib.request.urlopen(url) as response:
            status = response.status
            content_type = response.headers.get('content-type')
            text = response.read().decode('utf-8')
            
            print(f"✅ Status: {status}")
            print(f"Content-Type: {content_type}")
            
            # Ver si existen los endpoints
            if "caja" in text.lower():
                print("✅ ENDPOINT 'caja' ENCONTRADO en la respuesta")
            else:
                print("❌ ENDPOINT 'caja' NO encontrado")
                
            # Buscar específicamente por las acciones
            if "abrir_caja" in text:
                print("✅ ACCIÓN 'abrir_caja' ENCONTRADA")
            else:
                print("❌ ACCIÓN 'abrir_caja' NO ENCONTRADA")
                
            if "obtener_caja_activa" in text:
                print("✅ ACCIÓN 'obtener_caja_activa' ENCONTRADA")
            else:
                print("❌ ACCIÓN 'obtener_caja_activa' NO ENCONTRADA")
            
            print("\n--- RESPUESTA COMPLETA (primeras 2000 caracteres) ---")
            print(text[:2000])
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code}")
        print(f"Response: {e.read().decode('utf-8')[:500]}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
